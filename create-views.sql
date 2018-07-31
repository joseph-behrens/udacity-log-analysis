create view error_percentages as
    select to_char(error_codes.day,'FMMonth DD, YYYY') as date,
    round((error_codes.count::numeric) / (all_codes.count) * 100, 2)
    as errors
    from
    (
        select time::date as day,
        count(*) from log
        where status != '200 OK' group by day
    ) error_codes
    join
    (
        select time::date as day,
        count(*) from log group by day
    ) all_codes on error_codes.day = all_codes.day;

create view top_articles as
    select articles.title, articles.author, count(log.id)
    from log, articles
    where '/article/' || articles.slug = log.path
    group by articles.title, articles.author
    order by count(log.id) desc;