"""Set up and connect to the database."""

__all__ = ["connect"]

from importlib import resources
from typing import LiteralString, NamedTuple, cast

import psycopg
from psycopg.rows import namedtuple_row

from . import schema


def connect() -> psycopg.Connection[NamedTuple]:
    """Connect to the database."""
    connection = _open_connection()
    try:
        _set_up(connection)
    except:
        connection.close()
        raise
    else:
        return connection


def _open_connection() -> psycopg.Connection[NamedTuple]:
    """Open a connection to a database using preset parameters."""
    return psycopg.Connection[NamedTuple].connect(
        autocommit=True,
        row_factory=namedtuple_row,
        host="localhost",
        port=5432,
        dbname="netspider",
        user="postgres",
        # WARNING: To save users from frequently entering passwords, we use
        # a hardcoded password. NetSpider is intended to run *locally*, so we
        # don't really need proper authentication or secrets management.
        password="password",  # noqa: S106
    )


def _set_up(connection: psycopg.Connection[NamedTuple]) -> None:
    """Create data types and objects according to the schema."""
    with connection.cursor() as cursor:
        schema_v00_resource = resources.files(schema) / "v00.sql"
        schema_v00 = schema_v00_resource.read_text(encoding="utf-8")
        # WARNING: This type cast bypasses the SQL injection prevention, but
        # `schema_v00` comes from a trusted source (us!), so it's okay.
        cursor.execute(cast(LiteralString, schema_v00))
