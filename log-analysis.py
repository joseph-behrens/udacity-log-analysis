#!/usr/bin/python


import psycopg2
import time
import datetime


def create_top_articles_view():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    try:
        c.execute("""\
        create view top_articles as
            select articles.title, articles.author, count(log.id)
            from log, articles
            where '/article/' || articles.slug = log.path
            group by articles.title, articles.author
            order by count(log.id) desc;""")
        db.commit()
    except psycopg2.ProgrammingError:
        c.execute("ROLLBACK;")
        db.commit()
    db.close()


def create_error_percentages_view():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    try:
        c.execute("""\
            create view error_percentages as
                select to_char(error_codes.day,'MM-DD-YYYY') as date,
                trunc((error_codes.count) / (all_codes.count) * 100, 2)
                as errors
                from
                (
                    select date_trunc('day', log.time) as day,
                    cast(count(*) as decimal(7,2)) from log
                    where status != '200 OK' group by day
                ) error_codes
                join
                (
                select date_trunc('day', log.time) as day,
                cast(count(*) as decimal(7,2)) from log group by day
                ) all_codes on error_codes.day = all_codes.day;""")
        db.commit()
    except psycopg2.ProgrammingError:
        c.execute("ROLLBACK;")
        db.commit()
    db.close()


def get_top_articles():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("select * from top_articles limit 3;")
    top_articles = c.fetchall()
    db.close()
    return top_articles


def get_top_authors():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("""\
        select authors.name, sum(top_articles.count) as views
            from top_articles, authors
            where top_articles.author = authors.id
            group by authors.name
            order by views desc;""")
    top_authors = c.fetchall()
    db.close()
    return top_authors


def get_top_errors_days():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("""\
        select date, errors
            from error_percentages
            where errors > 1;""")
    top_errors_day = c.fetchall()
    db.close()
    return top_errors_day


create_top_articles_view()
create_error_percentages_view()
top_articles = get_top_articles()
top_authors = get_top_authors()
top_errors_days = get_top_errors_days()

print(' ')
print('TOP THREE ARTICLES')
print('==================')
for article in top_articles:
    print('"{}" - {:,} views'.format(article[0], article[2]))
print(' ')

print(' ')
print('MOST POPULAR AUTHORS')
print('====================')
for author in top_authors:
    print('{} - {:,} views'.format(author[0], author[1]))
print(' ')

print(' ')
print('DAYS WITH MORE THAN 1% OF REQUESTS AS ERRORS')
print('============================================')
for error_day in top_errors_days:
    converted_date = datetime.datetime.strptime(error_day[0], '%m-%d-%Y')
    print('{} - {}% errors'.format(
        time.strftime("%B %d, %Y", converted_date.timetuple()), error_day[1]))
print(' ')
