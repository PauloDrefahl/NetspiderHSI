# Schema Migration

## Introduction

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

## Changing the Schema

Begin by creating an SQL file in the [`Backend/schema/`](../Backend/schema)
directory. You must name the file `v<number>.sql` where `<number>` is the
*next* two-digit version number. For example, if `schema/` already contains
`v00.sql`, `v01.sql`, and `v02.sql`, the next version number is three, so
your file is `v03.sql`. Optionally, you can append a name by naming the file
`v<number>_<name>.sql`, where `<name>` is a summary of the file.

Your schema file is **not** a *declarative* sequence of statements describing
the state of the database. Instead, the code is an *imperative* sequence of
commands describing *how* to change the database from its current state to its
new state. The [`v01.sql`](../Backend/schema/v01.sql) schema file is a good
example: it contains four commands to change the `provider_id` column's domain.
Notice how it only modifies that column, leaving the rest untouched.

> [!NOTE]
> [`v00.sql`](../Backend/schema/v00.sql) is special because it represents the
> *initial* schema. NetSpider only runs `v00.sql` if:
>
> 1. it just created the database, or
> 2. if a previous version of NetSpider created the database, ran `v00.sql`,
>    but didn't set the database version to zero. This is a historical accident
>    that's only possible because of delays in development.
>
> In case 1, the database is empty, so there's nothing to modify; therefore,
> `v00.sql` creates everything from scratch. In case 2, everything already
> exists, but unfortunately, NetSpider runs `v00.sql` anyway. We work around
> that by catching and/or preventing exceptions in `v00.sql`.

Another example is: suppose that you want to rename the `raw_yesbackpage_posts`
table to `yesbackpage_data`. You can create a schema file containing:

```sql
alter table raw_yesbackpage_posts
rename to yesbackpage_data;
```

This works (even though the `clean_yesbackpage_view` references the
`raw_yesbackpage_posts` table by name!). What if you want to ensure that the
(non-null) strings in the `reply_to` column look like emails? You can try:

```sql
alter table raw_yesbackpage_posts
add check (reply_to like '%@%'); -- '@' surrounded by characters
```

This won't work if some strings already violate the constraint. One way to
resolve the issue is to delete the rows that contain those strings:

```sql
delete from raw_yesbackpage_posts
where reply_to not like '%@%';

alter table raw_yesbackpage_posts
add check (reply_to like '%@%');
```

Another, less destructive strategy is to convert those strings to `NULL`:

```sql
update raw_yesbackpage_posts
set reply_to = null
where reply_to not like '%@%';

alter table raw_yesbackpage_posts
add check (reply_to like '%@%');
```

Notice that you don't need to use clauses like `or replace`, `if exists`, and
`if not exists`. When writing a schema file, you can safely assume that all
previous schema files ran successfully. NetSpider runs the schema files in a
transaction, so PostgreSQL will roll back any changes if an error occurs.

Finally, when writing a schema file, keep in mind that you can't automatically
revert to a previous version of the schema. If your file ran successfully, but
didn't do what you want, you have to manually undo the changes and remove the
corresponding row in the `schema_versions` table. Alternatively, you can drop
the entire database and fix your file before running NetSpider again.

## Implementation Details

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

1. Schema files MUST be named `v<number>.sql` or `v<number>_<name>.sql`, where
   `<number>` is a two-digit number, and `<name>` is an optional name consisting
   of ASCII letters, digits, and underscores. Leading zeros MUST be included
   so that there are exactly two digits. NetSpider silently ignores non-schema
   files in the `schema/` directory.

2. There MUST be at least one schema file.

3. Schema files MUST be sequentially numbered from zero up to the most recent
   version number. Requirements two and three together imply that the schema
   file for version zero MUST exist, and if the latest version is version *N*,
   then there must be a schema file for *every* version from zero through *N*.

4. Directories MUST NOT be named as if they were schema files.
