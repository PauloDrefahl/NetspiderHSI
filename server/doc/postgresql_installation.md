# PostgreSQL Installation

Since commit 307095b22, NetSpider won't work unless you install PostgreSQL 17.
NetSpider requires PostgreSQL to be accessible on `localhost`, port 5432, using
the default `postgres` superuser and a password of `password`.

> [!CAUTION]
> NetSpider is intended to run *locally*, so to save users from frequently
> entering passwords, NetSpider connects to the database using a hardcoded
> password. Do **NOT** expose PostgreSQL or NetSpider to untrusted networks.

You can install PostgreSQL in any way you'd like as long as you meet those
requirements. This documentation only outlines two approaches:

1. You can run [the EnterpriseDB installer](#enterprisedb-installer), which is
   the recommended approach unless you've used Docker before.

2. Or, you can install PostgreSQL through [Docker](#docker).

## EnterpriseDB Installer

Begin by downloading the installer executable for PostgreSQL version 17 from
[EDB](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads).
Make sure to choose the correct installer for your operating system and CPU.

> [!IMPORTANT]
> You *can* install different versions of PostgreSQL, but NetSpider only
> supports version 17, so you may encounter issues. Unless you're willing to
> resolve or work around bugs, stick to version 17.

Next, run the installer. A setup window will appear saying "Welcome to the
PostgreSQL Setup Wizard". Click the "Next" button to proceed when ready.

You can change the installation directory if you want, but the default setting
is fine; it won't affect NetSpider anyway. Click the "Next" button to proceed.

NetSpider only requires the "PostgreSQL Server" and "Command Line Tools", but
you can select more components if you want. Click "Next" to proceed.

You can change the data directory, but it's not necessary. If you change the
data directory, make sure to select the same directory whenever reinstalling
PostgreSQL so that NetSpider can find your data. Click "Next" to proceed.

As mentioned before, you MUST set the password for the default database
superuser (`postgres`) to the word `password`. Click "Next" to proceed.

Again, as mentioned before, you MUST set the port number for the PostgreSQL
database server to the default port number of 5432. Click "Next" to proceed.

Select the default system locale, the C locale, or one of the English locales
such as "English, United Kingdom" or "English, United States". We've only tested
these locales because NetSpider is written in English. Click "Next" to proceed.

Review the pre-installation summary. If the settings are correct, click "Next".
On the "Ready to Install" screen, click "Next" to begin installing PostgreSQL.

Once the database installation has finished, click "Finish". If you installed
Stack Builder, you may launch Stack Builder at exit, but it's not necessary.

## Docker

Eventually, the NetSpider repository will contain a Windows batch file to
automate the Docker-based installation, but for now, follow these general steps.
Be prepared to "fill the gaps" and resolve any issues that come your way:

1. Install Docker. On Windows, you can install Docker Desktop from [the official
   site](https://www.docker.com/products/docker-desktop/) or through `winget`.

2. Install [the official PostgreSQL image](https://hub.docker.com/_/postgres).

3. Run a PostgreSQL container, setting the username to `postgres` and the
   password to `password`. NetSpider runs outside of the container, so publish
   the container port for PostgreSQL, 5432 by default, to host port 5432.
