# Project: Log Analysis

## Joseph Behrens

### July 29, 2018

---

#### Requirements

1.  What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.
2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.
3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.

#### Design

- All SQL queries are organzied into functions.
- The functions are called in order of the requriements list and the output is assigned to respective variables. This was done to make it easier to manipulate the output when presenting it to the screen.
- The print statements to output the returned info from the queries fromat the strings from the variables into a readable fashion for the end user.
- The time module is imported to allow conversion of the datetime from SQL into a friendly string of Month DayNumber, Year -- example January 1, 2018. Without this the time was formatted as 01-01-2018.

#### Prerequisites

- This application requires psycopg2 to be installed, if not already installed.
    ```
    pip install psycop2
    ```

#### Views

- This application uses two SQL views but it builds them from within the application. There is error handling in place in case the view already exists when the application is started.
- The first view is:
    ```sql
    create view top_articles as
        select articles.title, articles.author, count(log.id)
        from log, articles
        where '/article/' || articles.slug = log.path
        group by articles.title, articles.author
        order by count(log.id) desc;
    ```
- And the second view:
    ```sql
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
        ) all_codes on error_codes.day = all_codes.day;
    ```
