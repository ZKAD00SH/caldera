from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException

from backend.caldera_client import CalderaClient
from backend.collectors.wazuh import WazuhCollector
from backend.correlation.engine import CorrelationEngine
from backend.models import CorrelationResult, OperationTriggerRequest, OperationTriggerResponse
from backend.scheduler import configure_scheduler

app = FastAPI(title="BAS Wrapper API", version="0.1.0")

caldera_client = CalderaClient(
    base_url=os.getenv("CALDERA_URL", "http://localhost:8888"),
    api_key=os.getenv("CALDERA_API_KEY", ""),
)

wazuh_collector = WazuhCollector(
    base_url=os.getenv("WAZUH_URL", "http://localhost:55000"),
    username=os.getenv("WAZUH_USERNAME", "wazuh-wui"),
    password=os.getenv("WAZUH_PASSWORD", ""),
)

engine = CorrelationEngine()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/operations/trigger", response_model=OperationTriggerResponse)
async def trigger_operation(payload: OperationTriggerRequest) -> OperationTriggerResponse:
    if not caldera_client.headers.get("KEY"):
        raise HTTPException(status_code=400, detail="Missing CALDERA_API_KEY")

    result = await caldera_client.trigger_operation(
        adversary_id=payload.adversary_id,
        group=payload.group,
        planner=payload.planner,
        source=payload.source,
    )
    return OperationTriggerResponse(
        operation_id=result.get("id", "unknown"),
        operation_name=result.get("name", "unknown"),
        state=result.get("state", "running"),
    )


@app.post("/correlation/run-once", response_model=CorrelationResult)
async def run_correlation_once() -> CorrelationResult:
    operations = await caldera_client.list_operations(limit=5)
    alerts = await wazuh_collector.fetch_recent_alerts(minutes=10)
    return engine.correlate(alerts=alerts, operations=operations)


async def scheduled_correlation_job() -> None:
    await run_correlation_once()


@app.on_event("startup")
async def startup_event() -> None:
    schedule_enabled = os.getenv("ENABLE_SCHEDULER", "true").lower() == "true"
    if schedule_enabled:
        scheduler = configure_scheduler(scheduled_correlation_job, minutes=5)
        scheduler.start()
        app.state.scheduler = scheduler


@app.on_event("shutdown")
async def shutdown_event() -> None:
    scheduler = getattr(app.state, "scheduler", None)
    if scheduler:
        scheduler.shutdown(wait=False)
