# Project: Log Analysis

## Joseph Behrens - July 29, 2018

---

### Description

The application has three requirements to solve for:

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

- There is a function used for making queries that takes in the database name and query string. This is to make it easier to add other reports later.
- The printing functions are called in order of the requriements list. Each print function calls the query function and outputs its report.
- There are two views that are used to make the query calls cleaner.

---

### Running the Application

- It is recommended to run the application from a preconfigured Vagrant virtual machine that contains Python and PostgreSQL pre-installed.
    1. To install Vagrant you will first need to download and install [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
    2. Download and install [Vagrant](https://www.vagrantup.com/downloads.html)
    3. Clone or download this repo.
    4. Open a command shell and navigate to the folder where you cloned the repo and run `vagrant up` . This will take a few minutes the first time you run it.
    5. Once the machine is running run `vagrant ssh` from the same directory to log in to the computer.
    6. To run the application from the vagrant ssh session run `python /vagrant/log-analysis.py`

- If you prefer to not use Vagrant.
    1. Download [Python](https://www.python.org/downloads/) and install it onto your own computer.
    2. [PostgreSQL](https://www.postgresql.org/download/) will also be required if you decided to run without Vagrant.
    3. This application requires psycopg2 to be installed. This is used to make connections to the database from Python.
        - First, ensure [pip](https://pip.pypa.io/en/stable/installing/) is installed
        - Then from your command shell run `pip install psycop2-binary` .
    4. Clone or download this repository to your computer.
    5. Open a command shell and navigate to the directory you saved to.
    6. Create the news database by running `psql -d news -f newsdata.sql`
    7. Create the SQL views by running `psql -d news -f create-views.sql`
    8. Run the application using `python log-analysis.py`

---

### Views

This application uses two SQL views that are used by the report printing queries.

1. The first view pulls together a list of all the articles and how many page views each article has:
    ```sql
    create view top_articles as
        select articles.title, articles.author, count(log.id)
        from log, articles
        where '/article/' || articles.slug = log.path
        group by articles.title, articles.author
        order by count(log.id) desc;
    ```
2. The second view sorts page view error codes by day and calculates the percentage of views that resulted in an error for that day:
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
