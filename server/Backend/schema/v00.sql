-- This version is FROZEN and MUST NOT be modified!

-- If you want to make changes, create a new SQL file that modifies any data
-- types, domains, and relations as you see fit, fixing up data along the way.

--=================================================================
-- Common Data Types and Domains
--=================================================================

do language plpgsql $$
    begin
        create type sex as enum ('Male', 'Female', 'Other');
        create domain url as varchar(512) check (value <> '');
        create domain phone_number as varchar(128) check (value <> '');
        create domain email_address as varchar(256) check (value <> '');
        create domain non_empty_text as text check (value <> '');
        create domain non_empty_texts as text[] check (
            array_position(value, '') is null
            and array_position(value, null) is null
        );
    exception
        when duplicate_object then
            null;
    end;
$$;

--=================================================================
-- Eros
--=================================================================

create table if not exists raw_eros_posts (
    primary key (link, city_or_region),
    link url not null,
    city_or_region non_empty_text not null,
    profile_header varchar(4096) check (profile_header <> ''),
    about_info varchar(4096) check (about_info <> ''),
    info_details varchar(4096) check (info_details <> ''),
    contact_details varchar(4096) check (contact_details <> ''),
    payment_methods non_empty_texts not null,
    social_media_accounts non_empty_texts not null,
    keywords non_empty_texts not null
);

----------------
-- Clean View

create or replace view clean_eros_view as
    select
        link,
        city_or_region,
        'N/A' as specified_location,
        cast(null as timestamp without time zone) as timeline,
        coalesce(contact_details, 'N/A') as contacts,
        coalesce(about_info, 'N/A') as poster,
        concat_ws(
            ' ||| ',
            coalesce(profile_header, 'N/A'),
            coalesce(info_details, 'N/A')
        ) as description,
        payment_methods,
        social_media_accounts,
        keywords
    from raw_eros_posts;

--=================================================================
-- Escort Alligator
--=================================================================

create table if not exists raw_escort_alligator_posts (
    primary key (link, city_or_region),
    link url not null,
    city_or_region non_empty_text not null,
    specified_location varchar(2048) check (specified_location <> ''),
    posted_on timestamp without time zone,
    poster_phone_number phone_number,
    poster_age integer check (poster_age > 0),
    description varchar(4096) check (description <> ''),
    payment_methods non_empty_texts not null,
    social_media_accounts non_empty_texts not null,
    keywords non_empty_texts not null
);

----------------
-- Clean View

create or replace view clean_escort_alligator_view as
    select
        link,
        city_or_region,
        coalesce(specified_location, 'N/A') as specified_location,
        posted_on as timeline,
        coalesce(poster_phone_number, 'N/A') as contacts,
        coalesce(cast(poster_age as text), 'N/A') as poster,
        coalesce(description, 'N/A') as description,
        payment_methods,
        social_media_accounts,
        keywords
    from raw_escort_alligator_posts;

--=================================================================
-- MegaPersonals
--=================================================================

create table if not exists raw_mega_personals_posts (
    primary key (link, city_or_region),
    link url not null,
    city_or_region non_empty_text not null,
    specified_city_or_region varchar(256) check (specified_city_or_region <> ''),
    specified_location varchar(512) check (specified_location <> ''),
    poster_phone_number phone_number,
    poster_name varchar(128) check (poster_name <> ''),
    description varchar(4096) check (description <> ''),
    payment_methods non_empty_texts not null,
    social_media_accounts non_empty_texts not null,
    keywords non_empty_texts not null
);

----------------
-- Clean View

create or replace view clean_mega_personals_view as
    select
        link,
        city_or_region,
        concat_ws(
            ' ||| ',
            coalesce(specified_city_or_region, 'N/A'),
            coalesce(specified_location, 'N/A')
        ) as specified_location,
        cast(null as timestamp without time zone) as timeline,
        coalesce(poster_phone_number, 'N/A') as contacts,
        coalesce(poster_name, 'N/A') as poster,
        coalesce(description, 'N/A') as description,
        payment_methods,
        social_media_accounts,
        keywords
    from raw_mega_personals_posts;

--=================================================================
-- RubRatings
--=================================================================

create table if not exists raw_rub_ratings_posts (
    primary key (link, city_or_region),
    link url not null,
    city_or_region non_empty_text not null,
    specified_location varchar(256) not null check (specified_location <> ''),
    last_activity date not null,
    poster_phone_number phone_number not null,
    -- TODO(Daniel): Add a not-null constraint here once the provider ID locator
    -- is fixed; every page should have a provider ID.
    provider_id integer,
    title varchar(1024) check (title <> ''),
    description varchar(4096) check (description <> ''),
    payment_methods non_empty_texts not null,
    social_media_accounts non_empty_texts not null,
    keywords non_empty_texts not null
);

----------------
-- Clean View

create or replace view clean_rub_ratings_view as
    select
        link,
        city_or_region,
        specified_location,
        cast(last_activity as timestamp without time zone) as timeline,
        poster_phone_number as contacts,
        cast(provider_id as text) as poster,
        concat_ws(
            ' ||| ',
            coalesce(title, 'N/A'),
            coalesce(description, 'N/A')
        ) as description,
        payment_methods,
        social_media_accounts,
        keywords
    from raw_rub_ratings_posts;

--=================================================================
-- SkipTheGames
--=================================================================

create table if not exists raw_skipthegames_posts (
    primary key (link, city_or_region),
    link url not null,
    city_or_region non_empty_text not null,
    poster varchar(1024) check (poster <> ''),
    description varchar(4096) check (description <> ''),
    services varchar(2048) check (services <> ''),
    payment_methods non_empty_texts not null,
    social_media_accounts non_empty_texts not null,
    keywords non_empty_texts not null
);

----------------
-- Clean View

create or replace view clean_skipthegames_view as
    select
        link,
        city_or_region,
        'N/A' as specified_location,
        cast(null as timestamp without time zone) as timeline,
        'N/A' as contacts,
        coalesce(poster, 'N/A') as poster,
        concat_ws(
            ' ||| ',
            coalesce(description, 'N/A'),
            coalesce(services, 'N/A')
        ) as description,
        payment_methods,
        social_media_accounts,
        keywords
    from raw_skipthegames_posts;

--=================================================================
-- YesBackpage
--=================================================================

create table if not exists raw_yesbackpage_posts (
    primary key (link, city_or_region),
    link url not null,
    city_or_region non_empty_text not null,
    specified_location varchar(256) check (specified_location <> ''),
    posted_on timestamp without time zone,
    expires_on timestamp without time zone,
    poster_phone_number phone_number,
    poster_email_address email_address,
    poster_name varchar(128) check (poster_name <> ''),
    poster_sex sex,
    reply_to email_address,
    description varchar(4096) check (description <> ''),
    services varchar(512) check (services <> ''),
    payment_methods non_empty_texts not null,
    social_media_accounts non_empty_texts not null,
    keywords non_empty_texts not null
);

----------------
-- Clean View

create or replace view clean_yesbackpage_view as
    select
        link,
        city_or_region,
        coalesce(specified_location, 'N/A') as specified_location,
        posted_on as timeline,
        concat_ws(
            ' ||| ',
            coalesce(poster_phone_number, 'N/A'),
            coalesce(poster_email_address, 'N/A')
        ) as contacts,
        concat_ws(
            ' ||| ',
            coalesce(poster_name, 'N/A'),
            coalesce(cast(poster_sex as text), 'N/A')
        ) as poster,
        concat_ws(
            ' ||| ',
            coalesce(description, 'N/A'),
            coalesce(services, 'N/A'),
            coalesce(reply_to, 'N/A')
        ) as description,
        payment_methods,
        social_media_accounts,
        keywords
    from raw_yesbackpage_posts;
