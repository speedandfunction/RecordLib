**********
Developing
**********

The project is still in its development stage, and if you'd like to get involved, getting
set up takes just a few steps.


Quickstart with Docker-Compose
==============================

Prerequisites:

- git
- yarn
- docker
- docker-compose


Clone the repository to your development computer. 

.. code-block:: bash 

    git clone https://github.com/clsphila/RecordLib

Set up environment variables. Copy the example env file and change the secrets. 


Startup docker-compose. Use the `-dev` compose file so that you can update code and see your changes
reflected in the running app.

.. code-block:: bash

    make docker-dev-up

Credentials for the default admin will show up in the compose logs. 

Visit `localhost:3000` to see the site.


Do everything locally 
=======================

This is a little more difficult.

Clone the repository to your development computer. 

.. code-block:: bash 

    git clone https://github.com/clsphila/RecordLib`

Set up environment variables. Copy the example env file and change the secrets. 


.. code-block:: bash

    cp .env.example .env

**Install pdftotext.** The application needs to convert pdfs to text for parsing. It uses "pdftotext" to 
accomplish this. This utility is included in
most Linux distributions.  For other operating systems, find it here: 
http://www.xpdfreader.com/download.html.  Download the command line tools and 
place pdftotext somewhere in your PATH.

.. code-block:: bash

    # for debian
    apt install xpdf

**Setup postgres.** Instructions for this are available `here: <https://www.postgresql.org/download/>`

You also need to set up a database and user for the app, and set the relevant environment variables.

**Setup DocketScraperAPI** RecordLib uses another app, 
_DocketScraperAPI: https://github.com/CLSPhila/DocketScraperAPI/ to search for public criminal records. 
Clone this repository, install its dependencies with `pipenv install`, and run it with `flask run`.

**Install python dependencies** with `pipenv install --dev` (you might need `--pre` as well).

Then **install js dependencies** with `yarn install`

**Migrate the postgres database** with `./manage.py migrate`.


**Setup an admin django account** the usual way, with `./manage.py createsuperuser`.


**Run the app.** There are two ways to do this. 

The first version requires running different processes in a few different terminals. 

First, in one terminal, run the DocketScraper api with `flask run` from that app's project root.

Second, in another terminal, run the django app from RecordLib's root with `./manage.py runserver`.

Finally, in a third terminal, also from RecordLib's root, run `yarn watch` to build the frontend
update on changes.

Alternatively, you can run DocketScraperAPI in one terminal and run the django app and frontend at the
same time with `python dev.py` from RecordLib's root. Using `dev.py` is marginally more convenient, but
logs can be harder to follow and debugging doesn't work well because stdout for both yarn and django are 
mashed together. 


Additional Notes
====================


Statutes contain a lot of section symbols: §. To make this symbol using vim or vim inspired keybindings, use CTL-K SE. That's Control K, then the uppercase letters S and E.


