from importlib import resources
from typing import LiteralString, NamedTuple, cast

import psycopg
from psycopg.rows import namedtuple_row

from . import schema


def open() -> psycopg.Connection[NamedTuple]:
    connection = _connect()
    try:
        _prepare(connection)
    except:
        connection.close()
        raise
    else:
        return connection


def _connect() -> psycopg.Connection[NamedTuple]:
    return psycopg.Connection[NamedTuple].connect(
        autocommit=True,
        row_factory=namedtuple_row,
        host="localhost",
        port=5432,
        dbname="netspider",
        user="postgres",
        password="password",
    )


def _prepare(connection: psycopg.Connection[NamedTuple]) -> None:
    with connection.cursor() as cursor:
        schema_v00_resource = resources.files(schema) / "v00.sql"
        schema_v00 = schema_v00_resource.read_text(encoding="utf-8")
        # WARNING: This type cast bypasses the SQL injection prevention, but
        # `schema_v00` comes from a trusted source (us!), so it's okay.
        cursor.execute(cast(LiteralString, schema_v00))
