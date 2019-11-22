
***********************
Command line interface
***********************


There are several command line utilities for using this project. 

download_docs
=============

``download_docs`` is a cli that can collect summary sheets or dockets for testing purposes. 
It relies on having the DocketScraperAPI application running.

See the script's help information for details.

.. code-block:: bash

    me: download_docs --help
    Usage: download_docs [OPTIONS] COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.

    Commands:
    docket-numbers  Download dockets or summary sheets for the docket numbers...
    names           Download dockets from a list of names.
    random          Download <n> random "summary" documents or "docket"...


analyze
========

``analyze`` is a cli for reviewing a record for expungements and sealings. Currently, you can pass it a single summary sheet. It will build a criminal record out of the summary sheet and then return a json object that reports what expungements and sealings the record may be eligible for.


.. code-block:: bash

    me: analyze --help
    Usage: analyze [OPTIONS]

    Options:
    -ps, --pdf-summary PATH    [required]
    -td, --tempdir PATH
    -rc, --redis-collect TEXT  connection to redis, in the form
                                [host]:[port]:[db number]:[environment name]. For
                                example, 'localhost:6379:0:development'
    --help                     Show this message and exit.



expunge
=========

``expunge`` is a cli for generating petitions. It has subcommands. 

.. code-block:: bash

    me: expunge --help
    Usage: expunge [OPTIONS] COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.

    Commands:
    dir



``expunge dir`` will generate petitions for all the summary and docket pdf files in finds in the target directory. This command only makes sense to run when all the files
in the target directory relate to one person. 


.. code-block:: bash

    me: expunge dir --help
    Usage: expunge dir [OPTIONS]

    Options:
    -d, --directory PATH            [required]
    -a, --archive PATH              [required]
    -et, --expungement-template PATH
                                    [required]
    -st, --sealing-template PATH    [required]
    --atty-name TEXT
    --atty-org TEXT
    --atty-org-addr TEXT
    --atty-org-phone TEXT
    --atty-bar-id TEXT
    -td, --tempdir PATH
    --help                          Show this message and exit.




For example, this command creates an archive of petions generated from processing all the files in the `tests/data/summaries` directory. 

.. code-block:: bash
    expunge dir --directory tests/data/summaries/ --archive expungements.zip -et tests/templates/790ExpungementTemplate_usingpythonvars.docx -st tests/templates/791SealingTemplate.docx


