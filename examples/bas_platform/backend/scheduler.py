from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler


def configure_scheduler(job, minutes: int = 5) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(job, "interval", minutes=minutes, id="correlation-job", replace_existing=True)
    return scheduler
