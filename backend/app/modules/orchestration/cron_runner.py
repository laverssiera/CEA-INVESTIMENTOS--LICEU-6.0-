from __future__ import annotations

import sys

from app.modules.orchestration.orchestrator import build_orchestrator


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python -m app.modules.orchestration.cron_runner <job_name>")
        return 1

    job_name = sys.argv[1]
    orchestrator = build_orchestrator()
    try:
        result = orchestrator.run_job(job_name)
    except KeyError as exc:
        print(str(exc))
        return 2

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
