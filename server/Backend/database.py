from importlib import resources
from typing import LiteralString, cast

import psycopg


def open() -> psycopg.Connection:
    connection = _connect()
    try:
        _prepare(connection)
        return connection
    except Exception:
        connection.close()
        raise


def _connect() -> psycopg.Connection:
    return psycopg.connect(
        autocommit=True,
        host="localhost",
        port=5432,
        dbname="netspider",
        user="postgres",
        password="password",
    )


def _prepare(connection: psycopg.Connection) -> None:
    with connection.cursor() as cursor:
        schema_v00_resource = resources.files() / "schema" / "v00.sql"
        schema_v00 = schema_v00_resource.read_text(encoding="utf-8")
        # WARNING: This type cast bypasses the SQL injection prevention, but
        # `schema_v00` comes from a trusted source (us!), so it's okay.
        cursor.execute(cast(LiteralString, schema_v00))
