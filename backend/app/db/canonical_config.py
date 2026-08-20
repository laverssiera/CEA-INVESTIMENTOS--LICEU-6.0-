from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import quote_plus

from sqlalchemy.engine import URL, make_url


@dataclass(frozen=True)
class CanonicalDatabaseConfig:
    url: str
    host: str
    port: int
    database: str
    user: str | None
    schema: str
    source: str


def resolve_canonical_database() -> CanonicalDatabaseConfig:
    configured_url = os.getenv("DATABASE_URL") or os.getenv("CANONICAL_EVENT_STORE_DATABASE_URL")
    schema = os.getenv("EVENT_STORE_SCHEMA", "public")

    if configured_url:
        parsed = make_url(configured_url)
        return CanonicalDatabaseConfig(
            url=configured_url,
            host=parsed.host or "",
            port=parsed.port or 5432,
            database=parsed.database or "",
            user=parsed.username,
            schema=schema,
            source="DATABASE_URL" if os.getenv("DATABASE_URL") else "CANONICAL_EVENT_STORE_DATABASE_URL",
        )

    host = os.getenv("EVENT_STORE_DB_HOST", "db_core_os")
    port = int(os.getenv("EVENT_STORE_DB_PORT", "5432"))
    database = os.getenv("EVENT_STORE_DB_NAME", "liceu_core_os")
    user = os.getenv("EVENT_STORE_DB_USER") or os.getenv("POSTGRES_USER")
    password = os.getenv("EVENT_STORE_DB_PASSWORD") or os.getenv("POSTGRES_PASSWORD")
    auth = ""
    if user:
        auth = quote_plus(user)
        if password:
            auth += f":{quote_plus(password)}"
        auth += "@"

    url = URL.create(
        "postgresql+psycopg2",
        username=None,
        host=host,
        port=port,
        database=database,
    )
    rendered_url = str(url).replace("postgresql+psycopg2://", f"postgresql+psycopg2://{auth}", 1)
    return CanonicalDatabaseConfig(
        url=rendered_url,
        host=host,
        port=port,
        database=database,
        user=user,
        schema=schema,
        source="canonical environment defaults",
    )