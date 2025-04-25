=================================
Contributing to Jupyter NbClassic
=================================

If you're reading this section, you're probably interested in contributing to
Jupyter.  Welcome and thanks for your interest in contributing!

Please take a look at the Contributor documentation, familiarize yourself with
using the Jupyter NbClassic, and introduce yourself on the mailing list and
share what area of the project you are interested in working on.

General Guidelines
------------------

For general documentation about contributing to Jupyter projects, see the
`Project Jupyter Contributor Documentation`__.

__ https://jupyter.readthedocs.io/en/latest/contributing/content-contributor.html


Setting Up a Development Environment
------------------------------------

Installing Node.js and npm
^^^^^^^^^^^^^^^^^^^^^^^^^^

Building the NbClassic from its GitHub source code requires some tools to
create and minify JavaScript components and the CSS,
specifically Node.js and Node's package manager, ``npm``.
It should be node version ≥ 16.0. We also use Yarn (classic) version 1.x.

If you use ``conda``, you can get them with::

    conda install -c conda-forge nodejs=16 yarn=1

If you use `Homebrew <https://brew.sh/>`_ on Mac OS X::

    brew install node yarn

Installation on Linux may vary, but be aware that the `nodejs` or `npm` packages
included in the system package repository may be too old to work properly.

You can also use the installer from the `Node.js website <https://nodejs.org>`_.


Installing the Jupyter NbClassic
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have installed the dependencies mentioned above, use the following
steps::

    pip install --upgrade pip
    git clone https://github.com/jupyter/nbclassic
    cd nbclassic
    pip install -e .

If you are using a system-wide Python installation and you only want to install NbClassic for you,
you can add ``--user`` to the install commands.

Once you have done this, you can launch the main branch of Jupyter NbClassic
from any directory in your system with::

    jupyter nbclassic

Verification
^^^^^^^^^^^^

While running NbClassic, select one of your notebook files (the file will have the extension ``.ipynb``).
In the top tab you will click on "Help" and then click on "About". In the pop window you will see information about the version of Jupyter that you are running. You will see "The version of the notebook server is:".
If you are working in development mode, you will see that your version of Jupyter NbClassic will include the word "dev". If it does not include the word "dev", you are currently not working in development mode and should follow the steps below to uninstall and reinstall Jupyter.

Troubleshooting the Installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you do not see that your Jupyter NbClassic is running on dev mode, it's possible that you are
running other instances of Jupyter NbClassic. You can try the following steps:

1. Uninstall all instances of the NbClassic package. These include any installations you made using
   pip or conda.
2. Run ``python3 -m pip install -e .`` in the NbClassic repository to install NbClassic from there.
3. Run ``npm run build`` to make sure the Javascript and CSS are updated and compiled.
4. Launch with ``python3 -m nbclassic --port 8989``, and check that the browser is pointing to ``localhost:8989``
   (rather than the default 8888). You don't necessarily have to launch with port 8989, as long as you use
   a port that is neither the default nor in use, then it should be fine.
5. Verify the installation with the steps in the previous section.

Code Formatting and Linting
^^^^^^^^^^^^^^^^^^^^^^^^^^^

All source code is linted using `Flake8 <https://github.com/PyCQA/flake8>`_. When
code is modified and committed, staged files are automatically checked for PEP 8
compliance using pre-commit git hooks (with help from `pre-commit
<https://github.com/pre-commit/pre-commit>`_). Using a linter like `flake8` helps
maintain consistent code style and catches potential errors during pull request
reviews, streamlining the review process. Other checks are also run to look for
proper new lines at the end of files and to remove unnecessary whitespace.

To install `pre-commit`, run::

    pip install -e ".[dev]"
    pre-commit install

You can manually trigger the pre-commit hook at any time with::

    pre-commit run

This will check your code against the pre-commit checks and report any style
violations or potential issues.

If you committed files before setting up the pre-commit hook with
`pre-commit install`, you can check all files using
`pre-commit run --all-files`. You will need to fix any reported issues and commit
the changes yourself afterward.

Rebuilding JavaScript and CSS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is a build step for the JavaScript and CSS in the nbclassic.
To make sure that you are working with up-to-date code, you will need to run
this command whenever there are changes to JavaScript or LESS sources::

    npm run build

**IMPORTANT:** Don't forget to run ``npm run build`` after switching branches.
When switching between branches of different versions (e.g. ``4.x`` and
``main``), run ``pip install -e .``. If you have tried the above and still
find that NbClassic is not reflecting the current source code, try cleaning
the repo with ``git clean -xfd`` and reinstalling with ``pip install -e .``.

Development Tip
"""""""""""""""

When doing development, you can use this command to automatically rebuild
JavaScript and LESS sources as they are modified::

    npm run build:watch

Git Hooks
"""""""""

If you want to automatically update dependencies and recompile JavaScript and
CSS after checking out a new commit, you can install post-checkout and
post-merge hooks which will do it for you::

    git-hooks/install-hooks.sh

See ``git-hooks/README.md`` for more details.


Running Tests
-------------

Python Tests
^^^^^^^^^^^^

Install dependencies::

    pip install -e '.[test]'

To run the Python tests, use::

    pytest

For the end to end Pytest-Playwright tests you will need to install the browser binaries using::

    playwright install

Then you can run the end to end tests using::

    pytest -sv nbclassic/tests/end_to_end

If you want coverage statistics as well, you can run::

    py.test --cov nbclassic -v --pyargs nbclassic

JavaScript Tests
^^^^^^^^^^^^^^^^

To run the JavaScript tests, you will need to have PhantomJS and CasperJS
installed::

    npm install -g casperjs phantomjs-prebuilt

Re-build the JavaScript prior to running tests::

    npm run build

Then, to run the JavaScript tests::

    python -m nbclassic.jstest [group]

where ``[group]`` is an optional argument that is a path relative to
``nbclassic/tests/``.
For example, to run all tests in ``nbclassic/tests/notebook``::

    python -m nbclassic.jstest notebook

or to run just ``nbclassic/tests/notebook/deletecell.js``::

    python -m nbclassic.jstest notebook/deletecell.js

.. note::
   If you are getting spawn errors with an ARM Mac on macOS, make sure you
   have Rosetta installed.


Building the Documentation
--------------------------

To build the documentation you'll need `Sphinx <http://www.sphinx-doc.org/>`_,
`pandoc <http://pandoc.org/>`_ and a few other packages.

To install (and activate) a conda environment named ``nbclassic_docs``
containing all the necessary packages (except pandoc), use::

    conda create -n nbclassic_docs pip
    conda activate nbclassic_docs  # Linux and OS X
    activate nbclassic_docs        # Windows
    pip install .[docs]

If you want to install the necessary packages with ``pip``, use the following instead::

    pip install .[docs]

Once you have installed the required packages, you can build the docs with::

    cd docs
    make html

After that, the generated HTML files will be available at
``build/html/index.html``. You may view the docs in your browser.

You can automatically check if all hyperlinks are still valid::

    make linkcheck

Windows users can find ``make.bat`` in the ``docs`` folder.

You should also have a look at the `Project Jupyter Documentation Guide`__.

__ https://jupyter.readthedocs.io/en/latest/contributing/docs-contributions/index.html
