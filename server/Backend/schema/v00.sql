-- This schema is a work-in-progress and MUST NOT be used in production!

-- During development, the following lines can be uncommented to DROP (!!!)
-- all data types, domains, and relations every time the scraper is run:

/*
drop type if exists sex cascade;
drop domain if exists url, phone_number, email_address cascade;
*/

do $$
    begin
        create type sex as enum ('Male', 'Female');
        create domain url as varchar(256) check (value <> '');
        create domain phone_number as varchar(64) check (value <> '');
        create domain email_address as varchar(128) check (value <> '');
    exception
        when duplicate_object then
            null;
    end;
$$;
