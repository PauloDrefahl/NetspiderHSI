-- Load data into keysets
-- Currently broken, keysets are temp. busted
-- Load data into keysets
--COPY keysets (item_name, keywords)
--FROM '/docker-entrypoint-initdb.d/data/keysets.tsv'
--DELIMITER E'\t'
--CSV HEADER;

-- Load data into raw_eros_posts
COPY raw_eros_posts (
    link, city_or_region, profile_header, about_info,
    info_details, contact_details, payment_methods,
    social_media_accounts, keywords
)
FROM '/docker-entrypoint-initdb.d/data/raw_eros_posts.csv'
DELIMITER ','
CSV HEADER;

-- Load data into raw_escort_alligator_posts
COPY raw_escort_alligator_posts
FROM '/docker-entrypoint-initdb.d/data/raw_escort_alligator_posts.csv'
DELIMITER ','
CSV HEADER;

-- Load data into raw_mega_personals_posts
COPY raw_mega_personals_posts
FROM '/docker-entrypoint-initdb.d/data/raw_mega_personals_posts.csv'
DELIMITER ','
CSV HEADER;

-- Load data into raw_rub_ratings_posts
COPY raw_rub_ratings_posts
FROM '/docker-entrypoint-initdb.d/data/raw_rub_ratings_posts.csv'
DELIMITER ','
CSV HEADER;

-- Load data into raw_skipthegames_posts
COPY raw_skipthegames_posts
FROM '/docker-entrypoint-initdb.d/data/raw_skipthegames_posts.csv'
DELIMITER ','
CSV HEADER;

-- Load data into raw_yesbackpage_posts
COPY raw_yesbackpage_posts
FROM '/docker-entrypoint-initdb.d/data/raw_yesbackpage_posts.csv'
DELIMITER ','
CSV HEADER;


-- Load data into keywords
COPY keywords (keyword)
FROM '/docker-entrypoint-initdb.d/data/keywords.txt'
DELIMITER E'\t'
CSV HEADER;
