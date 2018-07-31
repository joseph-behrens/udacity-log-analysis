# Project: Log Analysis

## Joseph Behrens - July 29, 2018

---

### Requirements

1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.
2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.
3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.

These requirements are ran against a fictional news website database with articles by various fictional authors.

The News database contains three tables and is created via a script. The instructions are in the prerequisites section to build the database.

1. #### Articles - Contains the text of the article

    **Columns**:

    |Author|Title|Slug|Lead|Body|ID|
    |------|-----|----|----|----|--|
    |Text|Text|Text|Text|Text|integer|
    |Author name|Title text of the article|Used in URI|Opening paragraph|The main text of the article|primary key|

2. #### Authors - Names of the various authors

    **Columns**:

    |Name|Bio|ID|
    |----|---|--|
    |Text|Text|integer|
    |Author name|Info about the author|primary key|

3. #### Log - Holds statics of page views and status codes

    **Columns**:

    |Path|ip|Method|Status|time|id|
    |----|--|------|------|----|--|
    |Text|inet|text|text|timestamp|integer|
    |Relative path URI|Source IP Address|Get or Post|200 OK or Error code|Date and time of page view|primary key|

---

### Design

- All SQL queries are organzied into functions.
- The functions are called in order of the requriements list and the output is assigned to respective variables. This was done to make it easier to manipulate the output when presenting it to the screen.
- The print statements to output the returned info from the queries fromat the strings from the variables into a readable fashion for the end user.
- The time module is imported to allow conversion of the datetime from SQL into a friendly string of Month DayNumber, Year -- example January 1, 2018. Without this the time was formatted as 01-01-2018.

---

### Prerequisites

- It is recommended to run the application from a preconfigured Vagrant virtual machine that contains Python and PostgreSQL pre-installed.
    1. To install Vagrant you will first need to download and install [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
    2. Download and install [Vagrant](https://www.vagrantup.com/downloads.html)
    3. Clone or download the Vagrant virtual machine from [Github](https://github.com/joseph-behrens/fullstack-nanodegree-vm)
    4. Open a command shell and navigate to the "vagrant" folder in the cloned repo and run `vagrant up` .  This will take a few minutes the first time you run it.
    5. Once the machine is running run `vagrant ssh` from the same directory to log in to the computer.
    6. Download the [News database creation script](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and extract it to the vagrant directory on your computer. This folder is synced with the Vagrant virtual machine you ssh'ed into.
    7. In the Vagrant VM's ssh connection create the database by running `psql -d news -f`

- If you prefer to not use Vagrant, you can download [Python](https://www.python.org/downloads/) and install it onto your own computer.
- [PostgreSQL](https://www.postgresql.org/download/) will also be required if you decided to run without Vagrant.
- This application requires psycopg2 to be installed. This is used to make connections to the database from Python.
    1. First, ensure [pip](https://pip.pypa.io/en/stable/installing/) is installed
    2. Then from your command shell run `pip install psycop2` .

---

### Views

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
---