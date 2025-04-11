
COPY raw_eros_posts (
    link, city_or_region, profile_header, about_info,
    info_details, contact_details, payment_methods,
    social_media_accounts, keywords
)
FROM '/docker-entrypoint-initdb.d/data/raw_eros_posts.csv'
DELIMITER ','
CSV HEADER;

COPY raw_escort_alligator_posts
FROM '/docker-entrypoint-initdb.d/data/raw_escort_alligator_posts.csv'
DELIMITER ','
CSV HEADER;

COPY raw_mega_personals_posts
FROM '/docker-entrypoint-initdb.d/data/raw_mega_personals_posts.csv'
DELIMITER ','
CSV HEADER;

COPY raw_rub_ratings_posts
FROM '/docker-entrypoint-initdb.d/data/raw_rub_ratings_posts.csv'
DELIMITER ','
CSV HEADER;

COPY raw_skipthegames_posts
FROM '/docker-entrypoint-initdb.d/data/raw_skipthegames_posts.csv'
DELIMITER ','
CSV HEADER;

COPY raw_yesbackpage_posts
FROM '/docker-entrypoint-initdb.d/data/raw_yesbackpage_posts.csv'
DELIMITER ','
CSV HEADER;


COPY keywords (keyword)
FROM '/docker-entrypoint-initdb.d/data/keywords.txt'
DELIMITER E'\t'
CSV HEADER;

--must loop JSON rather than copy all :(
DO $$
DECLARE
    raw_json JSON;
    key TEXT;
    value JSON;
BEGIN
    SELECT pg_read_file('/docker-entrypoint-initdb.d/data/keysets.json')::json INTO raw_json;

    FOR key, value IN SELECT * FROM json_each(raw_json)
    LOOP
        INSERT INTO keysets (item_name, keywords) VALUES (key, value::jsonb);
    END LOOP;
END;
$$;
