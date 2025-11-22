.. _`Development`:

Development
===========
This section is intended for developers that want to create a fix or develop an enhancement to the CMPT221 application.

Code of Conduct
---------------
Coding conventions set by the maintainers are to be followed.

Repository
----------
The repository for CMPT221 is on Github: https://github.com/GregoryTvedt/cmpt221

Development Environment
-----------------------
A `Python virtual environment`_ is recommended. Once the virtual environment is activated, clone the CMPT221 repository and prepare the development environment with 

.. _Python virtual environment: https://virtualenv.pypa.io/en/latest/

.. code-block:: text

    $ git clone https://github.com/GregoryTvedt/cmpt221
    $ cd cmpt221
    $ pip install -r requirements.txt

This will install all local prerequisites needed for ``CMPT221`` to run.

Pytest
-------------------
N/A

Build Documentation
-------------------
The Github pages site is used to publish documentation for the CMPT221 application at https://gregorytvedt.github.io/cmpt221/

To build the documentation, issue:

.. code-block:: text
    
    $ cd docs
    $ make html
    # windows users without make installed use:
    $ make.bat html

The top-level document to open with a web-browser will be  ``docs/_build/html/index.html``.

To publish the page, copy the contents of the directory ``docs/_build/html`` into the branch
``gh-pages``. Then, commit and push to ``gh-pages``.