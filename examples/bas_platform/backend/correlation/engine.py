from __future__ import annotations

from datetime import datetime
from typing import Any

from backend.models import CorrelationMatch, CorrelationResult


class CorrelationEngine:
    """Simple correlation based on ATT&CK technique id + source IP heuristics."""

    @staticmethod
    def _extract_technique(alert: dict[str, Any]) -> str | None:
        rule = alert.get("rule", {})
        groups = rule.get("groups", [])
        for item in groups:
            if isinstance(item, str) and item.startswith("T"):
                return item
        return None

    @staticmethod
    def _extract_source_ip(alert: dict[str, Any]) -> str | None:
        data = alert.get("data", {})
        return data.get("srcip") or data.get("source", {}).get("ip")

    def correlate(
        self,
        alerts: list[dict[str, Any]],
        operations: list[dict[str, Any]],
    ) -> CorrelationResult:
        matches: list[CorrelationMatch] = []
        if not operations:
            return CorrelationResult(total_alerts=len(alerts), total_matches=0, matches=[])

        latest_operation = operations[0]
        operation_id = latest_operation.get("id", "unknown")
        operation_name = latest_operation.get("name", "unknown")

        for alert in alerts:
            technique = self._extract_technique(alert)
            src_ip = self._extract_source_ip(alert)
            if technique or src_ip:
                alert_ts = alert.get("timestamp") or datetime.utcnow().isoformat()
                matches.append(
                    CorrelationMatch(
                        operation_id=operation_id,
                        operation_name=operation_name,
                        technique_id=technique,
                        source_ip=src_ip,
                        alert_time=datetime.fromisoformat(alert_ts.replace("Z", "+00:00")),
                        raw_alert=alert,
                    )
                )

        return CorrelationResult(
            total_alerts=len(alerts),
            total_matches=len(matches),
            matches=matches,
        )
