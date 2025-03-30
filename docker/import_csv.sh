#!/bin/bash
set -e

DB_USER="postgres"
DB_NAME="netspider"

until pg_isready -U $DB_USER -d $DB_NAME; do
    sleep 2
done

psql -U $DB_USER -d $DB_NAME -f /docker-entrypoint-initdb.d/v00.sql

TABLES=("raw_eros_posts" "raw_escort_alligator_posts" "raw_mega_personals_posts" "raw_rub_ratings_posts" "raw_skipthegames_posts" "raw_yesbackpage_posts" "keywords" "keysets")

table_exists() {
    psql -U $DB_USER -d $DB_NAME -c "SELECT 1 FROM $1 LIMIT 1;" > /dev/null 2>&1
}

for TABLE in "${TABLES[@]}"; do
    until table_exists $TABLE; do
        echo "Waiting for table $TABLE to be created..."
        sleep 2
    done
done

psql -U $DB_USER -d $DB_NAME -c "\COPY raw_eros_posts FROM '/data/raw_eros_posts.csv' CSV HEADER;"
psql -U $DB_USER -d $DB_NAME -c "\COPY raw_escort_alligator_posts FROM '/data/raw_escort_alligator_posts.csv' CSV HEADER;"
psql -U $DB_USER -d $DB_NAME -c "\COPY raw_mega_personals_posts FROM '/data/raw_mega_personals_posts.csv' CSV HEADER;"
psql -U $DB_USER -d $DB_NAME -c "\COPY raw_rub_ratings_posts FROM '/data/raw_rub_ratings_posts.csv' CSV HEADER;"
psql -U $DB_USER -d $DB_NAME -c "\COPY raw_skipthegames_posts FROM '/data/raw_skipthegames_posts.csv' CSV HEADER;"
psql -U $DB_USER -d $DB_NAME -c "\COPY raw_yesbackpage_posts FROM '/data/raw_yesbackpage_posts.csv' CSV HEADER;"
psql -U $DB_USER -d $DB_NAME -c "\COPY keywords(keyword) FROM '/data/keywords.txt' WITH (FORMAT text);"
psql -U $DB_USER -d $DB_NAME -c "\COPY keysets(item_name, keywords) FROM '/data/keysets.tsv' WITH (FORMAT text);"

