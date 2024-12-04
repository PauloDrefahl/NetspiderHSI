-- This schema is a work-in-progress and MUST NOT be used in production!

-- During development, the following lines can be uncommented to DROP (!!!)
-- all data types, domains, and relations every time the scraper is run:

/*
drop type if exists sex cascade;
drop domain if exists url, phone_number, email_address cascade;
drop domain if exists non_empty_text, non_empty_texts cascade;
drop table if exists raw_eros_posts cascade;
drop view if exists clean_eros_view cascade;
drop table if exists raw_escort_alligator_posts cascade;
drop view if exists clean_escort_alligator_view cascade;
drop table if exists raw_skipthegames_posts cascade;
drop view if exists clean_skipthegames_view cascade;
drop table if exists raw_yesbackpage_posts cascade;
drop view if exists clean_yesbackpage_view cascade;
*/

--=================================================================
-- Common Data Types and Domains
--=================================================================

do language plpgsql $$
    begin
        create type sex as enum ('Male', 'Female', 'Other');
        create domain url as varchar(256) check (value <> '');
        create domain phone_number as varchar(64) check (value <> '');
        create domain email_address as varchar(128) check (value <> '');
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
    profile_header varchar(2048) check (profile_header <> ''),
    about_info varchar(2048) check (about_info <> ''),
    info_details varchar(2048) check (info_details <> ''),
    contact_details varchar(2048) check (contact_details <> ''),
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
    specified_location varchar(1024) check (specified_location <> ''),
    posted_on timestamp without time zone,
    poster_phone_number phone_number,
    poster_age integer check (poster_age > 0),
    description varchar(2048) check (description <> ''),
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
-- SkipTheGames
--=================================================================

create table if not exists raw_skipthegames_posts (
    primary key (link, city_or_region),
    link url not null,
    city_or_region non_empty_text not null,
    poster varchar(512) check (poster <> ''),
    description varchar(2048) check (description <> ''),
    services varchar(1024) check (services <> ''),
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
    specified_location varchar(128) check (specified_location <> ''),
    posted_on timestamp without time zone not null,
    expires_on timestamp without time zone not null,
    poster_phone_number phone_number,
    poster_email_address email_address,
    poster_name varchar(64) check (poster_name <> ''),
    poster_sex sex,
    reply_to email_address,
    description varchar(2048) check (description <> ''),
    services varchar(256) check (services <> ''),
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
