from contextlib import suppress
from importlib import resources
from typing import LiteralString, NamedTuple, cast

import psycopg
from psycopg import sql
from psycopg.rows import namedtuple_row

from . import schema

_DATABASE_NAME = "netspider"


def open() -> psycopg.Connection[NamedTuple]:
    try:
        # Eagerly attempt to connect to the NetSpider database.
        connection = _connect()
    except psycopg.errors.ConnectionTimeout:
        # `ConnectionTimeout` is a subclass of `OperationalError`, but we can't
        # resolve `ConnectionTimeout` errors, so we re-raise them instead.
        raise
    except psycopg.OperationalError:
        # Psycopg doesn't assign an error code for attempting to connect to a
        # nonexistent database, so we try to create the database and re-connect
        # in response to *any* operational error.
        _create_database()
        connection = _connect()

    # Prepare the database before returning the connection object.
    try:
        _prepare(connection)
    except:
        connection.close()
        raise
    else:
        return connection


def _create_database() -> None:
    # According to PostgreSQL's documentation, we should connect to the
    # `postgres` database to execute the `CREATE DATABASE` command.
    # Source: https://www.postgresql.org/docs/17/manage-ag-createdb.html
    with _connect(dbname="postgres") as connection:
        name = sql.Identifier(_DATABASE_NAME)
        command = sql.SQL("create database {} template template0 encoding 'UTF8';")
        with suppress(psycopg.errors.DuplicateDatabase):
            connection.execute(command.format(name))


def _connect(*, dbname: str = _DATABASE_NAME) -> psycopg.Connection[NamedTuple]:
    return psycopg.Connection[NamedTuple].connect(
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


def _prepare(connection: psycopg.Connection[NamedTuple]) -> None:
    with connection.cursor() as cursor:
        schema_v00_resource = resources.files(schema) / "v00.sql"
        schema_v00 = schema_v00_resource.read_text(encoding="utf-8")
        # WARNING: This type cast bypasses the SQL injection prevention, but
        # `schema_v00` comes from a trusted source (us!), so it's okay.
        cursor.execute(cast(LiteralString, schema_v00))
