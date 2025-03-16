"""Set up and connect to the database."""

__all__ = ["connect"]

import contextlib
from contextlib import suppress
from importlib import resources
from typing import LiteralString, NamedTuple, TypeAlias, cast

import psycopg
from psycopg import sql
from psycopg.rows import namedtuple_row

from . import schema

Connection: TypeAlias = psycopg.Connection[NamedTuple]
Cursor: TypeAlias = psycopg.Cursor[NamedTuple]

_DATABASE_NAME = "netspider"


def connect() -> Connection:
    """Connect to the database."""
    with contextlib.ExitStack() as stack:
        connection = stack.enter_context(_create_and_connect())
        # Set up the database before returning the connection.
        _set_up(connection)
        # Don't close the connection.
        stack.pop_all()
        return connection


def _open_connection(*, dbname: str = _DATABASE_NAME) -> Connection:
    """Open a connection to a database using preset parameters."""
    return Connection.connect(
        autocommit=True,
        row_factory=namedtuple_row,
        host="localhost",
        port=5432,
        dbname=dbname,
        user="postgres",
        # WARNING: To save users from frequently entering passwords, we use
        # a hardcoded password. NetSpider is intended to run *locally*, so we
        # don't really need proper authentication or secrets management.
        password="password",  # noqa: S106
        client_encoding="UTF8",
        application_name="NetSpider",
    )


def _create_and_connect() -> Connection:
    """Connect to the database, creating it if needed."""
    try:
        # Optimistically guess that the database exists.
        return _open_connection()
    except psycopg.errors.ConnectionTimeout:
        # `ConnectionTimeout` is a subclass of `OperationalError`, but creating
        # the database wouldn't resolve any timeouts, so re-raise the error.
        raise
    except psycopg.OperationalError:
        # The `OperationalError` won't indicate if the database exists or not,
        # so we guess that creating the database will resolve the error.
        _create()
        return _open_connection()


def _create() -> None:
    """Create the database if it doesn't already exist."""
    # Connect to the `postgres` database to issue the `CREATE DATABASE` command.
    # Source: https://www.postgresql.org/docs/17/manage-ag-createdb.html
    with _open_connection(dbname="postgres") as connection:
        name = sql.Identifier(_DATABASE_NAME)
        command = sql.SQL("create database {} template template0 encoding 'UTF8';")
        with suppress(psycopg.errors.DuplicateDatabase):
            connection.execute(command.format(name))


def _set_up(connection: Connection) -> None:
    """Create data types and objects according to the schema."""
    with connection.cursor() as cursor:
        schema_v00_resource = resources.files(schema) / "v00.sql"
        schema_v00 = schema_v00_resource.read_text(encoding="utf-8")
        # WARNING: This type cast bypasses the SQL injection prevention, but
        # `schema_v00` comes from a trusted source (us!), so it's okay.
        cursor.execute(cast(LiteralString, schema_v00))
