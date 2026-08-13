from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import text

from app.db.session import SessionLocal

_TABLES_READY = False


def _ensure_tables() -> None:
    global _TABLES_READY
    if _TABLES_READY:
        return

    db = SessionLocal()
    try:
        db.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS automation_job_runs (
                    id VARCHAR(40) PRIMARY KEY,
                    job_name VARCHAR(120) NOT NULL,
                    payload TEXT NOT NULL,
                    executed_at TIMESTAMP WITH TIME ZONE NOT NULL
                )
                """
            )
        )
        db.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS automation_events (
                    id VARCHAR(40) PRIMARY KEY,
                    event_name VARCHAR(120) NOT NULL,
                    payload TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL
                )
                """
            )
        )
        db.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS automation_notifications (
                    id VARCHAR(40) PRIMARY KEY,
                    channel VARCHAR(40) NOT NULL,
                    trigger_name VARCHAR(120) NOT NULL,
                    recipient VARCHAR(180) NOT NULL,
                    message TEXT NOT NULL,
                    status VARCHAR(40) NOT NULL,
                    sent_at TIMESTAMP WITH TIME ZONE NOT NULL
                )
                """
            )
        )
        db.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS automation_documents (
                    id VARCHAR(40) PRIMARY KEY,
                    document_type VARCHAR(80) NOT NULL,
                    context TEXT NOT NULL,
                    status VARCHAR(40) NOT NULL,
                    generated_at TIMESTAMP WITH TIME ZONE NOT NULL
                )
                """
            )
        )
        db.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS automation_event_dispatches (
                    event_id VARCHAR(120) NOT NULL,
                    transport VARCHAR(40) NOT NULL,
                    status VARCHAR(40) NOT NULL,
                    attempts INTEGER NOT NULL DEFAULT 1,
                    last_error TEXT NULL,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
                    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
                    PRIMARY KEY (event_id, transport)
                )
                """
            )
        )
        db.commit()
        _TABLES_READY = True
    except Exception:
        db.rollback()
    finally:
        db.close()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_job_run(job_name: str, payload: dict[str, Any], run_id: str | None = None) -> str:
    _ensure_tables()
    if run_id is None:
        run_id = f"JOB-{int(datetime.now(timezone.utc).timestamp() * 1000)}"

    db = SessionLocal()
    try:
        db.execute(
            text(
                """
                INSERT INTO automation_job_runs (id, job_name, payload, executed_at)
                VALUES (:id, :job_name, :payload, :executed_at)
                """
            ),
            {
                "id": run_id,
                "job_name": job_name,
                "payload": json.dumps(payload),
                "executed_at": _now_iso(),
            },
        )
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

    return run_id


def append_event(event_name: str, payload: dict[str, Any], event_id: str | None = None) -> str:
    _ensure_tables()
    if event_id is None:
        event_id = f"EVT-{int(datetime.now(timezone.utc).timestamp() * 1000)}"

    db = SessionLocal()
    try:
        db.execute(
            text(
                """
                INSERT INTO automation_events (id, event_name, payload, created_at)
                VALUES (:id, :event_name, :payload, :created_at)
                """
            ),
            {
                "id": event_id,
                "event_name": event_name,
                "payload": json.dumps(payload),
                "created_at": _now_iso(),
            },
        )
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

    return event_id


def record_event_dispatch(
    event_id: str,
    transport: str,
    status: str,
    error: str | None = None,
) -> None:
    _ensure_tables()
    db = SessionLocal()
    try:
        now = _now_iso()
        db.execute(
            text(
                """
                INSERT INTO automation_event_dispatches (
                    event_id, transport, status, attempts, last_error, created_at, updated_at
                )
                VALUES (
                    :event_id, :transport, :status, 1, :last_error, :created_at, :updated_at
                )
                ON CONFLICT (event_id, transport)
                DO UPDATE SET
                    status = excluded.status,
                    attempts = automation_event_dispatches.attempts + 1,
                    last_error = excluded.last_error,
                    updated_at = excluded.updated_at
                """
            ),
            {
                "event_id": event_id,
                "transport": transport,
                "status": status,
                "last_error": error,
                "created_at": now,
                "updated_at": now,
            },
        )
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()


def was_event_dispatched(event_id: str, transport: str) -> bool:
    _ensure_tables()
    db = SessionLocal()
    try:
        row = db.execute(
            text(
                """
                SELECT status
                FROM automation_event_dispatches
                WHERE event_id = :event_id AND transport = :transport
                LIMIT 1
                """
            ),
            {"event_id": event_id, "transport": transport},
        ).fetchone()
        return bool(row and row[0] == "success")
    except Exception:
        return False
    finally:
        db.close()


def fetch_event_dispatches(
    limit: int = 200,
    transport: str | None = None,
    status: str | None = None,
) -> list[dict[str, Any]]:
    _ensure_tables()
    db = SessionLocal()
    try:
        stmt = (
            """
            SELECT event_id, transport, status, attempts, last_error, created_at, updated_at
            FROM automation_event_dispatches
            """
        )
        where_parts: list[str] = []
        params: dict[str, Any] = {"limit": limit}

        if transport:
            where_parts.append("transport = :transport")
            params["transport"] = transport
        if status:
            where_parts.append("status = :status")
            params["status"] = status

        if where_parts:
            stmt += " WHERE " + " AND ".join(where_parts)

        stmt += " ORDER BY updated_at DESC LIMIT :limit"

        rows = db.execute(text(stmt), params).mappings()
        return [
            {
                "event_id": row["event_id"],
                "transport": row["transport"],
                "status": row["status"],
                "attempts": int(row["attempts"] or 0),
                "last_error": row["last_error"],
                "created_at": str(row["created_at"]),
                "updated_at": str(row["updated_at"]),
            }
            for row in rows
        ]
    except Exception:
        return []
    finally:
        db.close()


def fetch_event_by_id(event_id: str) -> dict[str, Any] | None:
    _ensure_tables()
    db = SessionLocal()
    try:
        row = db.execute(
            text(
                """
                SELECT id, event_name, payload, created_at
                FROM automation_events
                WHERE id = :event_id
                LIMIT 1
                """
            ),
            {"event_id": event_id},
        ).mappings().first()
        if not row:
            return None
        return {
            "id": row["id"],
            "event": row["event_name"],
            "payload": json.loads(row["payload"]),
            "created_at": str(row["created_at"]),
        }
    except Exception:
        return None
    finally:
        db.close()


def fetch_event_dispatch_status(event_id: str, transport: str) -> dict[str, Any] | None:
    _ensure_tables()
    db = SessionLocal()
    try:
        row = db.execute(
            text(
                """
                SELECT event_id, transport, status, attempts, last_error, created_at, updated_at
                FROM automation_event_dispatches
                WHERE event_id = :event_id AND transport = :transport
                LIMIT 1
                """
            ),
            {"event_id": event_id, "transport": transport},
        ).mappings().first()
        if not row:
            return None
        return {
            "event_id": row["event_id"],
            "transport": row["transport"],
            "status": row["status"],
            "attempts": int(row["attempts"] or 0),
            "last_error": row["last_error"],
            "created_at": str(row["created_at"]),
            "updated_at": str(row["updated_at"]),
        }
    except Exception:
        return None
    finally:
        db.close()


def append_notification(item: dict[str, Any]) -> None:
    _ensure_tables()
    db = SessionLocal()
    try:
        db.execute(
            text(
                """
                INSERT INTO automation_notifications (id, channel, trigger_name, recipient, message, status, sent_at)
                VALUES (:id, :channel, :trigger_name, :recipient, :message, :status, :sent_at)
                """
            ),
            {
                "id": item["id"],
                "channel": item["channel"],
                "trigger_name": item["trigger"],
                "recipient": item["recipient"],
                "message": item["message"],
                "status": item["status"],
                "sent_at": item["sent_at"],
            },
        )
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()


def append_document(item: dict[str, Any]) -> None:
    _ensure_tables()
    db = SessionLocal()
    try:
        db.execute(
            text(
                """
                INSERT INTO automation_documents (id, document_type, context, status, generated_at)
                VALUES (:id, :document_type, :context, :status, :generated_at)
                """
            ),
            {
                "id": item["id"],
                "document_type": item["type"],
                "context": json.dumps(item["context"]),
                "status": item["status"],
                "generated_at": item["generated_at"],
            },
        )
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()


def fetch_job_runs(limit: int = 200) -> list[dict[str, Any]]:
    _ensure_tables()
    db = SessionLocal()
    try:
        rows = db.execute(
            text(
                """
                SELECT id, job_name, payload, executed_at
                FROM automation_job_runs
                ORDER BY executed_at DESC
                LIMIT :limit
                """
            ),
            {"limit": limit},
        ).mappings()
        return [
            {
                "id": row["id"],
                "job": row["job_name"],
                "payload": json.loads(row["payload"]),
                "executed_at": str(row["executed_at"]),
            }
            for row in rows
        ]
    except Exception:
        return []
    finally:
        db.close()


def fetch_events(limit: int = 200) -> list[dict[str, Any]]:
    _ensure_tables()
    db = SessionLocal()
    try:
        rows = db.execute(
            text(
                """
                SELECT id, event_name, payload, created_at
                FROM automation_events
                ORDER BY created_at DESC
                LIMIT :limit
                """
            ),
            {"limit": limit},
        ).mappings()
        return [
            {
                "id": row["id"],
                "event": row["event_name"],
                "payload": json.loads(row["payload"]),
                "created_at": str(row["created_at"]),
            }
            for row in rows
        ]
    except Exception:
        return []
    finally:
        db.close()


def fetch_notifications(limit: int = 200) -> list[dict[str, Any]]:
    _ensure_tables()
    db = SessionLocal()
    try:
        rows = db.execute(
            text(
                """
                SELECT id, channel, trigger_name, recipient, message, status, sent_at
                FROM automation_notifications
                ORDER BY sent_at DESC
                LIMIT :limit
                """
            ),
            {"limit": limit},
        ).mappings()
        return [
            {
                "id": row["id"],
                "channel": row["channel"],
                "trigger": row["trigger_name"],
                "recipient": row["recipient"],
                "message": row["message"],
                "status": row["status"],
                "sent_at": str(row["sent_at"]),
            }
            for row in rows
        ]
    except Exception:
        return []
    finally:
        db.close()


def fetch_documents(limit: int = 200) -> list[dict[str, Any]]:
    _ensure_tables()
    db = SessionLocal()
    try:
        rows = db.execute(
            text(
                """
                SELECT id, document_type, context, status, generated_at
                FROM automation_documents
                ORDER BY generated_at DESC
                LIMIT :limit
                """
            ),
            {"limit": limit},
        ).mappings()
        return [
            {
                "id": row["id"],
                "type": row["document_type"],
                "context": json.loads(row["context"]),
                "status": row["status"],
                "generated_at": str(row["generated_at"]),
            }
            for row in rows
        ]
    except Exception:
        return []
    finally:
        db.close()
