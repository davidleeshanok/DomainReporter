# DomainReporter
My solution to a coding test.

<!-- Instructions -->
Given a table 'mailing':

CREATE TABLE mailing (
    addr VARCHAR(255) NOT NULL
);

The mailing table will initially be empty.  New addresses will be added on a daily basis.  It is expected that the table will store at least 10,000,000 email addresses and 100,000 domains.

Write a Python script that updates another table which holds a daily count of email addresses by their domain name.

Use this table to report the top 50 domains by count sorted by percentage growth of the last 30 days compared to the total.

** NOTE **

- The original mailing table should not be modified.

- All processing must be done in Python (eg. no complex queries or sub-queries)

- Submit a compressed file(tar/zip) with the files required to run your script.