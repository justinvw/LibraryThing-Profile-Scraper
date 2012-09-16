# LibraryThing.com Profile Scraper #
This is a slightly modified version of the LibraryThing (LT) user profile scraper which I used to collect data for my Master thesis. It uses the Python screen scraping and web crawling framework [Scrapy](http://scrapy.org) to collect basic user profile information and personal libraries of LT members. The scraper eats a seedlist (an initial list of LT profile URLs) and outputs the scraped data in several CSV files.

## Requirements ##
The repo contains a ``requirements.txt`` that can be used to install the necessary requirements, but to give you an idea of the used packages:

* Python 2.5, 2.6 or 2.7
* Scrapy 0.14.4
* python-dateutil 1.5

## Installation ##
First clone the LibraryThing Profile Scraper Git repository:

    $ git clone ...

If you do not have *pip* installed, run:

    $ easy_install pip

Install all required packages that are needed to run the scraper:

    $ cd librarything_profile_scraper/
    $ pip install -r requirements.txt

## Configuration ##
Before running the scraper you first need to change some settings in the ``settings.py`` file found in the ``scraper`` directory.

First set ``PROFILE_SEEDLIST`` variable to the path of a text file containg a list of LT profile URLs that should be used as a starting point for the crawl. This file should be formatted as follows:

    http://www.librarything.com/profile/FemmeSavante
    http://www.librarything.com/profile/hayleyanderton
    http://www.librarything.com/profile/biblionz

Next, set the ``CSV_STORE_LOCATION`` variable to the directory where the crawled data should be stored. The crawler stores four different files in CSV format:

* ``user_profiles.csv``: basic profile information such as profile URL, username and date of registration.
* ``user_connections.csv``: connections from a single user to other LT users; e.g. 'friends' and 'interesting libraries'.
* ``group_memberships.csv``: the LT groups the user is a member of.
* ``user_libraries.csv``: the works a user has added to her library, with the assigned rating and the date when the user added the work.

When the ``FOLLOW_USER_CONNECTIONS`` variable is set to ``False`` the crawler will not follow links to other profiles.

The settings file also contains several options to set the rate at which information should be requested from LibraryThing (specifically the ``DOWNLOAD_DELAY`` and ``CONCURRENT_REQUESTS_PER_DOMAIN``). LT's [robots.txt](http://www.librarything.com/robots.txt) specifies a 'crawl-delay' of two seconds, please don't hit their server too hard. It is in no way my responsibility if you take down or get blocked by LT.

## Running the crawler ##
Enter the following command in the repo's top directory to run the LT profile scraper:

    $ scrapy crawl "Librarything User Profiles"