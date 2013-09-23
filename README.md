parse.py
========

Description
-----------

A simple script for parsing an XML file containing job applications and the
schedule I need to adhere to use them.

Usage:

    parse.py [-c] filename

Arguments:

    filename    The XML file containing the company names I wish to apply for

Optional Arguments:

    -c          Optional argument for color output (will highlight different
    companies depending on how close the deadlines are)

Example:

    python parse.py -c test_application.xml

Installation
------------

Installation occurs as with most Python projects, simply by calling virtualenv
on this repository after `git clone`ing it and then running `pip install -r
requirements.txt` within the highest directory level of the repository.

Why make this?
--------------

Because it's jobs and I gotta stay organized :).

What XML tags and options are supported?
----------------------------------------

To view all the possible XML options and tags, please take a look at the example
XML file included in the tests folder.

Tests
-----

Tests are run simply by running `nosetests`.
