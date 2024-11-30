-- This schema is a work-in-progress and MUST NOT be used in production!

-- During development, the following lines can be uncommented to DROP (!!!)
-- all data types, domains, and relations every time the scraper is run:

/*
drop type if exists sex cascade;
drop domain if exists url, phone_number, email_address cascade;
drop domain if exists non_empty_text, non_empty_texts cascade;
drop table if exists raw_skipthegames_posts cascade;
drop view if exists clean_skipthegames_view cascade;
*/

--=================================================================
-- Common Data Types and Domains
--=================================================================

do language plpgsql $$
    begin
        create type sex as enum ('Male', 'Female');
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
