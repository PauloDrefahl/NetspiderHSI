__all__ = ["SchemaError", "open"]

import re
from contextlib import suppress
from dataclasses import dataclass
from datetime import UTC, datetime
from importlib import resources
from importlib.resources.abc import Traversable
from typing import LiteralString, NamedTuple, cast

import psycopg
from psycopg import sql
from psycopg.rows import namedtuple_row

from . import schema

_DATABASE_NAME = "netspider"


@dataclass
class SchemaVersion:
    number: int
    resource: Traversable


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

    # Migrate the database before returning the connection object.
    try:
        _migrate(connection)
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


def _migrate(connection: psycopg.Connection[NamedTuple]) -> None:
    versions = _get_schema_versions()
    with connection.cursor() as cursor, connection.transaction():
        current_version = _get_current_version(connection, cursor)
        next_version = 0 if current_version is None else current_version + 1
        for version in versions[next_version:]:
            _migrate_to(cursor, version)


def _migrate_to(cursor: psycopg.Cursor[NamedTuple], version: SchemaVersion) -> None:
    commands = version.resource.read_text(encoding="utf-8")
    execution_begin_timestamp = datetime.now(UTC)
    # WARNING: This type cast bypasses the SQL injection prevention, but
    # `commands` comes from a trusted source (us!), so it's okay.
    cursor.execute(cast(LiteralString, commands))
    cursor.execute(
        """
        insert into schema_versions (version_number, migrated_on, execution_time)
        values (%s, statement_timestamp(), statement_timestamp() - %s);
        """,
        (version.number, execution_begin_timestamp),
    )


def _get_current_version(
    connection: psycopg.Connection[NamedTuple],
    cursor: psycopg.Cursor[NamedTuple],
) -> int | None:
    try:
        with connection.transaction():
            cursor.execute("""
                create table schema_versions (
                    primary key (version_number),
                    version_number integer not null,
                    migrated_on timestamptz not null,
                    execution_time interval second not null,
                    check (version_number >= 0),
                    check (execution_time >= interval '0' second)
                );
            """)
    except psycopg.errors.DuplicateTable:
        pass

    cursor.execute("select max(version_number) from schema_versions;")
    record = cursor.fetchone()
    assert record is not None
    if record[0] is None:
        return None
    assert isinstance(record[0], int)
    return record[0]


_VERSION_DIGITS: int = 2
_VERSION_REGEX = re.compile(rf"v(?P<number>[0-9]{{{_VERSION_DIGITS}}})\.sql")


class SchemaError(Exception):
    pass


def _get_schema_versions() -> list[SchemaVersion]:
    schema_container = resources.files(schema)
    # Detect schema version files and parse version numbers.
    versions: list[SchemaVersion] = []
    for resource in schema_container.iterdir():
        match = _VERSION_REGEX.fullmatch(resource.name)
        if not match:
            continue
        number = int(match.group("number"))
        versions.append(SchemaVersion(number, resource))
    # Put versions in ascending order.
    versions.sort(key=lambda version: version.number)
    # Check for missing versions.
    if not versions:
        message = "No versions were found."
        raise SchemaError(message)
    for i, version in enumerate(versions):
        if i != version.number:
            message = f"Version {i} is missing."
            error = SchemaError(message)
            error.add_note(
                f"Version {version.number} was found, "
                + "but version numbers begin at 0 and cannot be skipped.",
            )
            raise error
        if version.resource.is_dir():
            message = f"Resource '{version.resource.name}' is a directory."
            raise SchemaError(message)
    return versions
