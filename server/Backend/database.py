__all__ = ["SchemaError", "open"]

import contextlib
import logging
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from importlib import resources
from importlib.resources.abc import Traversable
from typing import LiteralString, cast

import psycopg
from psycopg import sql

MAIN_DATABASE_NAME = "netspider"
logger = logging.getLogger(__name__)


@dataclass
class SchemaVersion:
    number: int
    resource: Traversable


def open() -> psycopg.Connection:
    logger.debug("Opening the database...")
    connection = _connect()
    try:
        _migrate(connection)
    except:
        connection.close()
        raise
    else:
        return connection


def _connect() -> psycopg.Connection:
    logger.debug("Connecting to the main ('%s') database...", MAIN_DATABASE_NAME)
    try:
        return _connect_to(MAIN_DATABASE_NAME)
    except psycopg.OperationalError:
        # NOTE: An operational error can be caused by many things, but there's
        # no way to determine the specific error except clumsily checking the
        # error message. Fortunately, attempting to create the main database in
        # response to ANY operational error causes no issues.
        message = "The initial connection attempt threw an operational error:"
        logger.debug(message, exc_info=True)
        _create_main_database()
        return _connect_to(MAIN_DATABASE_NAME)


def _create_main_database() -> None:
    logger.debug("Creating the main ('%s') database...", MAIN_DATABASE_NAME)
    with _connect_to("postgres") as connection, connection.cursor() as cursor:
        name = sql.Identifier(MAIN_DATABASE_NAME)
        command = sql.SQL("create database {};").format(name)
        with contextlib.suppress(psycopg.errors.DuplicateDatabase):
            cursor.execute(command)


def _connect_to(database_name: str) -> psycopg.Connection:
    logger.debug("Connecting to the '%s' database...", database_name)
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


def _migrate(connection: psycopg.Connection) -> None:
    logger.debug("Migrating...")
    versions = _get_schema_versions()
    logger.debug("Versions: %s", versions)
    with connection.cursor() as cursor, connection.transaction():
        current_version = _get_current_version(connection, cursor)
        if current_version is None:
            logger.debug("The database hasn't been initialized yet.")
        else:
            logger.debug("The database is at version %s.", current_version)
        next_version = 0 if current_version is None else current_version + 1
        for version in versions[next_version:]:
            _migrate_to(cursor, version)


def _migrate_to(cursor: psycopg.Cursor, version: SchemaVersion) -> None:
    logger.debug("Migrating to version %s...", version.number)
    commands = version.resource.read_text(encoding="utf-8")
    execution_begin_timestamp = datetime.now(UTC)
    # WARNING: This type cast bypasses the SQL injection prevention, but
    # `schema_v00` comes from a trusted source (us!), so it's okay.
    cursor.execute(cast(LiteralString, commands))
    cursor.execute(
        """
        insert into schema_versions (version_number, migrated_on, execution_time)
        values (%s, statement_timestamp(), statement_timestamp() - %s);
        """,
        (version.number, execution_begin_timestamp),
    )


def _get_current_version(
    connection: psycopg.Connection,
    cursor: psycopg.Cursor,
) -> int | None:
    try:
        with connection.transaction():
            cursor.execute("""
                create table schema_versions (
                    primary key (version_number),
                    version_number integer not null,
                    migrated_on timestamptz not null,
                    execution_time interval second not null
                    check (version_number >= 0),
                    check (execution_time >= interval '0' second)
                );
            """)
    except psycopg.errors.DuplicateTable:
        logger.debug("`schema_versions` already exists.")

    cursor.execute("select max(version_number) from schema_versions;")
    record = cursor.fetchone()
    assert record is not None
    if record[0] is None:
        logger.debug("`schema_versions` is empty.")
        return None
    assert isinstance(record[0], int)
    return record[0]


_VERSION_DIGITS: int = 2
_VERSION_REGEX = re.compile(rf"v(?P<number>[0-9]{{{_VERSION_DIGITS}}})\.sql")


class SchemaError(Exception):
    pass


def _get_schema_versions() -> list[SchemaVersion]:
    schema_container = resources.files() / "schema"
    schema = [*schema_container.iterdir()]
    # Parse version numbers and ignore extraneous resources.
    versions: list[SchemaVersion] = []
    for resource in schema:
        logger.debug("Resource: %s", resource)
        match = _VERSION_REGEX.fullmatch(resource.name)
        if not match:
            logger.debug("Resource '%s' is not a schema version.", resource)
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
