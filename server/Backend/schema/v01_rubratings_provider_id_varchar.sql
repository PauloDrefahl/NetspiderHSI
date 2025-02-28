-- This version is a work-in-progress and MUST NOT be used in production!

-- We can't change a column's type if it's used by a view.
drop view clean_rub_ratings_view;

-- Remove `NULL` values before adding a `NOT NULL` constraint.
update raw_rub_ratings_posts
set provider_id = coalesce(
    provider_id, cast(trim(split_part(trim(link, '/'), '/', -1)) as integer)
);

-- Treating provider IDs as integers was a mistake. Although provider IDs
-- are numbers, they're not "quantities", making most operations meaningless.
-- Therefore, we shouldn't use a data type that supports those operations.
alter table raw_rub_ratings_posts
alter column provider_id set not null,
alter column provider_id type varchar(8) using '#' || provider_id,
add check (provider_id <> '');

-- Re-create the view.
create view clean_rub_ratings_view as
    select
        link,
        city_or_region,
        specified_location,
        cast(last_activity as timestamp without time zone) as timeline,
        poster_phone_number as contacts,
        provider_id as poster,
        concat_ws(
            ' ||| ',
            coalesce(title, 'N/A'),
            coalesce(description, 'N/A')
        ) as description,
        payment_methods,
        social_media_accounts,
        keywords
    from raw_rub_ratings_posts;
