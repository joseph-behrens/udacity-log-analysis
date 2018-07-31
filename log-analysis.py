#!/usr/bin/env python


import psycopg2
import time
import datetime


def execute_query(query, dbname):
    """
    Connects to a database defined by DBNAME,
    runs a query defined by QUERY against the
    database and returns the results of the query.
    """
    try:
        db = psycopg2.connect("dbname={}".format(dbname))
        c = db.cursor()
        c.execute(query)
        result = c.fetchall()
        db.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def print_top_articles(num):
    """
    Get the top number of articles by view
    with limiter defined by NUM from the NEWS
    database and print out the list along with
    the number of views for that article by title.
    """
    top_articles = execute_query("select * from top_articles limit {};".format(num),"news")
    print(' ')
    print('TOP THREE ARTICLES')
    print('==================')
    for article in top_articles:
        print('"{}" - {:,} views'.format(article[0], article[2]))
    print(' ')


def print_top_authors():
    """
    Print out a list of authors ordered
    by most views to least views.
    """
    top_authors = execute_query("""\
        select authors.name, sum(top_articles.count) as views
            from top_articles, authors
            where top_articles.author = authors.id
            group by authors.name
            order by views desc;""","news")
    print(' ')
    print('MOST POPULAR AUTHORS')
    print('====================')
    for author in top_authors:
        print('{} - {:,} views'.format(author[0], author[1]))
    print(' ')


def print_top_error_days(percent):
    """
    Print a list of days where the percent
    errors is greater than the provided percenatage
    defined by PERCENT.
    """
    top_errors_days = execute_query(
        "select date, errors from error_percentages where errors > {};".format(percent)
        ,"news")
    print(' ')
    print('DAYS WITH MORE THAN 1% OF REQUESTS AS ERRORS')
    print('============================================')
    for error_day in top_errors_days:
        print('{} - {}% errors'.format(error_day[0], error_day[1]))
    print(' ')


if __name__ == '__main__':
    print_top_articles(3)
    print_top_authors()
    print_top_error_days(1)