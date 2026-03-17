from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class OperationTriggerRequest(BaseModel):
    adversary_id: str = Field(..., description="Caldera adversary UUID")
    group: str = Field("red", description="Agent group")
    planner: str = Field("atomic", description="Planner name")
    source: str = Field("basic", description="Fact source")


class OperationTriggerResponse(BaseModel):
    operation_id: str
    operation_name: str
    state: str


class CorrelationMatch(BaseModel):
    operation_id: str
    operation_name: str
    technique_id: str | None
    source_ip: str | None
    alert_time: datetime
    raw_alert: dict[str, Any]


class CorrelationResult(BaseModel):
    total_alerts: int
    total_matches: int
    matches: list[CorrelationMatch]
