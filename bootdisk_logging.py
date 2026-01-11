from __future__ import annotations

import json
import logging
import os
import sys
import traceback
from datetime import datetime, timezone
from typing import Any, Mapping


class HumanFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = (
            datetime.fromtimestamp(record.created, tz=timezone.utc)
            .astimezone()
            .strftime("%Y-%m-%d %H:%M:%S")
        )
        level = record.levelname
        message = record.getMessage()

        event: Mapping[str, Any] | None = getattr(record, "event", None)
        if isinstance(event, Mapping) and event:
            extras = " ".join(f"{k}={v!r}" for k, v in sorted(event.items()))
            return f"{timestamp} | {level:<8} | {message} | {extras}"

        return f"{timestamp} | {level:<8} | {message}"


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "source": {
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
            },
        }

        event = getattr(record, "event", None)
        if isinstance(event, Mapping):
            payload["event"] = dict(event)

        if record.exc_info:
            exc_type, exc_value, exc_tb = record.exc_info
            payload["exception"] = {
                "type": getattr(exc_type, "__name__", str(exc_type)),
                "message": str(exc_value),
                "traceback": traceback.format_exception(exc_type, exc_value, exc_tb),
            }

        return json.dumps(payload, ensure_ascii=False)


_configured = False


def configure_logging(*, level: int | None = None) -> None:
    """Configure dual-output logging.

    - Human logs go to stderr.
    - Machine logs (JSON lines) go to stdout.

    Both outputs are derived from the same LogRecord (single-capture).
    """

    global _configured
    if _configured:
        return

    effective_level = level
    if effective_level is None:
        env_level = ("" if "BOOTDISK_LOG_LEVEL" not in os.environ else os.environ["BOOTDISK_LOG_LEVEL"]).upper()
        if env_level in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            effective_level = getattr(logging, env_level)
        else:
            effective_level = logging.INFO

    root = logging.getLogger()
    root.setLevel(effective_level)

    for handler in list(root.handlers):
        root.removeHandler(handler)

    human_handler = logging.StreamHandler(sys.stderr)
    human_handler.setLevel(effective_level)
    human_handler.setFormatter(HumanFormatter())

    json_handler = logging.StreamHandler(sys.stdout)
    json_handler.setLevel(effective_level)
    json_handler.setFormatter(JsonFormatter())

    root.addHandler(human_handler)
    root.addHandler(json_handler)

    _configured = True


def get_logger(name: str = "bootdisk") -> logging.Logger:
    if not _configured:
        configure_logging()
    return logging.getLogger(name)
