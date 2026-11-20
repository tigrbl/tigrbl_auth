from tba_auth.app import build_application_runtime_plan

plan = build_application_runtime_plan(runner="uvicorn", host="127.0.0.1", port=8000)
assert plan.runner == "uvicorn"
assert plan.port == 8000
