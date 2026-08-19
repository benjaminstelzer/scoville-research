#!/usr/bin/env python3
"""Run frozen SkillOpt Studio fixtures against an isolated Codex target with no Skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

from skillopt_studio.benchmark import load_split, score_rollout
from skillopt_studio.codex import codex_command, isolated_codex_environment, parse_codex_jsonl
from skillopt_studio.config import load_config


def safe_relative(value: str) -> PurePosixPath:
    path = PurePosixPath(value.replace("\\", "/"))
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"unsafe fixture path: {value!r}")
    return path


def materialize(item: dict[str, Any], workspace: Path) -> None:
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True)
    for raw_path, content in item["prediction"]["files"].items():
        target = workspace.joinpath(*safe_relative(str(raw_path)).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(str(content), encoding="utf-8", newline="\n")
    if (workspace / ".agents").exists():
        raise RuntimeError("no-Skill workspace unexpectedly contains .agents")


def request_for(item: dict[str, Any]) -> str:
    prediction = item["prediction"]
    return (
        f"Task:\n{str(prediction['task_text']).strip()}\n\n"
        f"Output contract:\n{str(prediction['output_contract']).strip()}\n\n"
        "Use only the supplied fixture files. Web search and command network access are disabled. "
        "Read only task-required named files, each at most once, using one "
        "Get-Content -Raw -LiteralPath '<relative-path>' operation per file. "
        "Do not list or inspect the workspace. Return only the output required by the contract."
    )


def run_item(item: dict[str, Any], *, output_root: Path, config: Any) -> dict[str, Any]:
    item_id = str(item["id"])
    prediction_dir = output_root / "predictions" / item_id
    prediction_dir.mkdir(parents=True)
    workspace = prediction_dir / "workspace"
    materialize(item, workspace)
    request = request_for(item)
    (prediction_dir / "request.sha256").write_text(
        hashlib.sha256(request.encode("utf-8")).hexdigest().upper() + "\n",
        encoding="ascii",
        newline="\n",
    )
    result: dict[str, Any] = {"id": item_id, "agent_ok": False, "hard": 0, "fail_reason": ""}
    try:
        with tempfile.TemporaryDirectory(prefix="scoville-research-no-skill-") as isolated_home:
            completed = subprocess.run(
                codex_command(
                    executable=config.codex_executable,
                    workspace=workspace,
                    model=config.target.model,
                    reasoning=config.target.reasoning,
                    network_access=False,
                ),
                input=request.encode("utf-8"),
                cwd=workspace,
                env=isolated_codex_environment(Path(isolated_home), auth_home=config.codex_auth_home),
                capture_output=True,
                timeout=config.runtime.timeout_seconds,
                check=False,
            )
        stdout = completed.stdout.decode("utf-8", errors="strict")
        stderr = completed.stderr.decode("utf-8", errors="replace")
        (prediction_dir / "stdout.jsonl").write_text(stdout, encoding="utf-8", newline="\n")
        (prediction_dir / "stderr.log").write_text(stderr, encoding="utf-8", newline="\n")
        if completed.returncode != 0:
            raise RuntimeError(f"codex exec failed with exit code {completed.returncode}: {stderr[:1000]}")
        parsed = parse_codex_jsonl(stdout)
        result.update(score_rollout(item, parsed=parsed, skill_tokens=0, loaded_skill_tokens=0))
        result.update({"response": parsed["final_text"], "agent_ok": True})
    except Exception as exc:  # benchmark evidence preserves exact failures
        result["fail_reason"] = f"{type(exc).__name__}: {exc}"
    (prediction_dir / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--split", choices=("train", "val"), required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args(argv)

    config = load_config(args.config)
    if config.runtime.network_access:
        raise RuntimeError("no-Skill baseline requires network_access=false")
    items = load_split(config.benchmark_path / args.split)
    if args.limit:
        items = items[: args.limit]
    output_root = (config.output_root / args.run_id).resolve()
    if output_root.exists():
        raise FileExistsError(f"run directory already exists: {output_root}")
    output_root.mkdir(parents=True)

    results = [run_item(item, output_root=output_root, config=config) for item in items]
    summary = {
        "schema_version": 1,
        "arm": "no-skill",
        "split": args.split,
        "target": {"model": config.target.model, "reasoning": config.target.reasoning},
        "network_access": False,
        "global_skill_isolation": True,
        "items": len(results),
        "agent_ok": sum(bool(row.get("agent_ok")) for row in results),
        "hard_passes": sum(int(row.get("hard") or 0) for row in results),
        "results": [{"id": row["id"], "agent_ok": row.get("agent_ok"), "hard": row.get("hard"), "fail_reason": row.get("fail_reason", "")} for row in results],
    }
    (output_root / "eval_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({**summary, "run_root": str(output_root)}, ensure_ascii=False, indent=2))
    return 0 if summary["agent_ok"] == summary["items"] else 1


if __name__ == "__main__":
    sys.exit(main())
