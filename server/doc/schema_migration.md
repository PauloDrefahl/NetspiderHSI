# Schema Migration

When coding for NetSpider, you may want to *change* the database's schema.
Changes come in many forms, including, but not limited to:

- creating a table,
- renaming a table,
- adding a column to a table, and
- changing a column's type.

You'll encounter an obstacle: what do you do about the databases that *already
exist*? For instance, if you want to change a column's data type, modifying
the original `create table` statement won't work; the modified statement will
immediately throw an error because the table already exists.

Sometimes it's not too difficult to manually take care of both new and existing
databases, but in general, you'll need a *schema migration tool*. According to
[Wikipedia](https://en.wikipedia.org/wiki/Schema_migration):

> In software engineering, a **schema migration** refers to the management of
> version-controlled, incremental and sometimes reversible changes to relational
> database schemas. A schema migration is performed on a database whenever it is
> necessary to update or revert that database's schema . . .
>
> Migrations are performed programmatically by using a *schema migration tool*.
> When invoked . . ., the tool automates the successive application or reversal
> of an appropriate sequence of schema changes . . .

NetSpider implements its own "low-tech" schema migration tool. You can find
the complete implementation in `Backend/database.py`. The initial schema is in
`Backend/schema/v00.sql`. Later versions are stored in sequentially numbered
files: `v01.sql`, `v02.sql`, `v03.sql`, and so on. NetSpider runs each file
exactly once, in order, to change the database's schema.

The `database` module tracks which files it has already run in an auxiliary
table named `schema_versions`. Each row has a few attributes, but the key is
the version number. When NetSpider connects to the database, it determines the
current version by calling the `_get_current_version` function, which queries
the `schema_versions` table for the *maximum* version number.

Then, the `_migrate` function calls `_migrate_to` for each file that NetSpider
hasn't run yet, that is, each file corresponding to a *more recent* version.
`_migrate_to` runs the file and inserts a row into the `schema_versions` table
so that NetSpider doesn't run the same file again.

For example, suppose that the `schema/` directory contains the files `v00.sql`
and `v01.sql`. Then, assuming that the `schema_versions` table looks like:

```
 version_number |          migrated_on          | execution_time
----------------+-------------------------------+----------------
              0 | 2024-12-21 22:09:03.956962-05 | 00:00:00.04697
```

When NetSpider connects to the database, it would run the SQL stored in
`v01.sql`. As a result, the `schema_versions` table would look like:

```
 version_number |          migrated_on          | execution_time
----------------+-------------------------------+-----------------
              0 | 2024-12-21 22:09:03.956962-05 | 00:00:00.04697
              1 | 2024-12-21 23:00:54.135993-05 | 00:00:00.030261
```

The next time NetSpider connects to the database, it'll find that the database
is already at the latest version, so it won't run any schema files.

If the `schema_versions` table didn't exist, NetSpider would know that it hadn't
initialized the database yet, so it would've run `v00.sql` *and* `v01.sql`.

## Schema Files

The `database` module enforces particular requirements on the `schema/`
directory. The requirements, as implemented by `_get_schema_versions`, are:

1. Schema files MUST be named `vNN.sql`, where `NN` represents any two-digit
   number. Leading zeros MUST be included so that there are exactly two digits.
   NetSpider ignores files that aren't named `vNN.sql`.

2. There MUST be at least one schema file.

3. Schema files MUST be sequentially numbered from zero up to the most recent
   version number. Requirements two and three together imply that the schema
   file for version zero MUST exist, and if the latest version is version *N*,
   then there must be a schema file for *every* version from zero through *N*.

4. Directories MUST NOT be named as if they were schema files.
