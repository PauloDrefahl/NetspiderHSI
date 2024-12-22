import contextlib
from importlib import resources
from typing import LiteralString, cast

import psycopg
from psycopg import sql

MAIN_DATABASE_NAME = "netspider"


def open() -> psycopg.Connection:
    connection = _connect()
    try:
        _prepare(connection)
        return connection
    except Exception:
        connection.close()
        raise


def _connect() -> psycopg.Connection:
    try:
        return _connect_to(MAIN_DATABASE_NAME)
    except psycopg.OperationalError:
        # NOTE: An operational error can be caused by many things, but there's
        # no way to determine the specific error except clumsily checking the
        # error message. Fortunately, attempting to create the main database in
        # response to ANY operational error causes no issues.
        _create_main_database()
        return _connect_to(MAIN_DATABASE_NAME)


def _create_main_database() -> None:
    with _connect_to("postgres") as connection, connection.cursor() as cursor:
        name = sql.Identifier(MAIN_DATABASE_NAME)
        command = sql.SQL("create database {};").format(name)
        with contextlib.suppress(psycopg.errors.DuplicateDatabase):
            cursor.execute(command)


def _connect_to(database_name: str) -> psycopg.Connection:
    return psycopg.connect(
        autocommit=True,
        host="localhost",
        port=5432,
        dbname=database_name,
        user="postgres",
        # NOTE: NetSpider is intended to be run locally, so we don't need to
        # worry about authentication.
        password="password",  # noqa: S106
        client_encoding="UTF8",
        application_name="NetSpider",
    )


def _prepare(connection: psycopg.Connection) -> None:
    with connection.cursor() as cursor:
        schema_v00_resource = resources.files() / "schema" / "v00.sql"
        schema_v00 = schema_v00_resource.read_text(encoding="utf-8")
        # WARNING: This type cast bypasses the SQL injection prevention, but
        # `schema_v00` comes from a trusted source (us!), so it's okay.
        cursor.execute(cast(LiteralString, schema_v00))
