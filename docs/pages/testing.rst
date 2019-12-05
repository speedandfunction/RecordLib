********
Testing
********


Run automated tests of the whole app with ``pytest``.

environment
=============


There are some environment variables you might
want for testing. 

These are env vars so you can test with real names

.. code-block: bash

    # only really test network calls when necessary.
    REAL_NETWORK_TESTS=FALSE # TRUE
    # you can test searches with a real name this way.
    UJS_SEARCH_TEST_FNAME=Joe
    UJS_SEARCH_TEST_LNAME=Normal
    UJS_SEARCH_TEST_DOB=2000-01-01


Grammars
=========

One of the core functions of this project is to parse criminal records dockets. 

We use Context-Free-Grammars for parsing. 

Grammars need to be tested on lots of different source documents. The tests include tests that will try to parse all the dockets in a folder `tests/data/[summaries|dockets]`. If you want those tests to be meaningful, you need to put dockets there.

You could do this manually by downloading dockets and saving them there. You can also use a helper script that randomly generates docket numbers and then uses [natev/DocketScraperAPI](https://hub.docker.com/r/natev/docketscraper_api) to download those dockets. To do this

1. download and run the DocketScraperAPI image with `docker run -p 5000:8800 natev/docketscraper_api`
2. in this project environment, run ``download (summaries | dockets) [-n = 1]``


Frontend
=========
Run just the frontend tests with ``yarn test``. Frontend test coverage is very, very minimal so far.