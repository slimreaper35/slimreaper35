from dataclasses import dataclass
from typing import Any

import apachelogs
import user_agents
from celery import Task

from celery_app import app
from db import mongo_manager


@dataclass
class TaskResult:
    key: str
    value: str


class UserAgentTask(Task):
    def on_success(self, retval: TaskResult, task_id, args, kwargs):
        if retval.value:
            mongo_manager.insert({retval.key: retval.value})
            return super().on_success(retval, task_id, args, kwargs)


@app.task
def parse_log(log: str) -> dict[str, Any]:
    log_format = '%h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i"'
    parser = apachelogs.LogParser(log_format)

    try:
        log_entry = parser.parse(log)
        ua = user_agents.parse(log_entry.headers_in["User-Agent"])
    except Exception:
        return {}

    return {"browser": ua.get_browser(), "device": ua.get_device(), "os": ua.get_os()}


@app.task(base=UserAgentTask)
def get_browser(ua: dict[str, Any]) -> TaskResult:
    return TaskResult(key="browser", value=ua.get("browser", ""))


@app.task(base=UserAgentTask)
def get_device(ua: dict[str, Any]) -> TaskResult:
    return TaskResult(key="device", value=ua.get("device", ""))


@app.task(base=UserAgentTask)
def get_os(ua: dict[str, Any]) -> TaskResult:
    return TaskResult(key="os", value=ua.get("os", ""))
