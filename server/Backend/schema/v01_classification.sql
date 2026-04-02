-- v01: Post classification and bucketing system
-- Adds tables for classifying scraped posts into risk buckets,
-- tracking human review decisions, and linking posts across sites.

--=================================================================
-- Post Classifications
--=================================================================

create table if not exists post_classifications (
    id                  serial primary key,
    source_table        varchar(64) not null,
    post_link           url not null,
    post_city           non_empty_text not null,
    bucket              integer not null check (bucket between 1 and 4),
    risk_score          numeric(5,2) not null check (risk_score between 0 and 100),
    keyword_hits        jsonb not null default '{}',
    payment_flag        boolean not null default false,
    social_flag         boolean not null default false,
    classified_at       timestamp without time zone not null default now(),
    reviewed            boolean not null default false,
    reviewed_by         varchar(128),
    reviewed_at         timestamp without time zone,
    review_notes        text,
    original_bucket     integer check (original_bucket between 1 and 4),
    unique (source_table, post_link, post_city)
);

-- Index for fast review queue lookups
create index if not exists idx_classifications_bucket
    on post_classifications (bucket);

create index if not exists idx_classifications_reviewed
    on post_classifications (reviewed);

create index if not exists idx_classifications_source
    on post_classifications (source_table);

--=================================================================
-- Cross-Site Links (Bucket 4)
--=================================================================

create table if not exists cross_site_links (
    id                  serial primary key,
    cluster_id          uuid not null default gen_random_uuid(),
    classification_id   integer not null references post_classifications(id)
                            on delete cascade,
    match_type          varchar(32) not null,
    match_value         text not null,
    created_at          timestamp without time zone not null default now()
);

create index if not exists idx_cross_site_cluster
    on cross_site_links (cluster_id);

create index if not exists idx_cross_site_match_value
    on cross_site_links (match_value);

--=================================================================
-- Classification Runs (audit log)
--=================================================================

create table if not exists classification_runs (
    id                  serial primary key,
    started_at          timestamp without time zone not null default now(),
    finished_at         timestamp without time zone,
    posts_processed     integer default 0,
    source_filter       varchar(64),
    status              varchar(32) not null default 'running'
);
