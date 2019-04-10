``pytest_taptest``
==================

.. image :: https://travis-ci.org/oliver-sanders/pytest_taptest.svg?branch=master
   :target: https://travis-ci.org/oliver-sanders/pytest_taptest

.. _Prove: https://perldoc.perl.org/prove.html
.. _pytest-tap: https://pypi.org/project/pytest-tap/

A simple ``pytest`` plugin for running test scripts which produce TAP output.

It's kinda the opposite of `pytest-tap`_ and was designed to be a
``pytest`` replacement for the Perl `Prove`_ command.


Installation
------------

.. code-block:: console

   $ pip install pytest
   $ git clone 'https://github.com/oliver-sanders/pytest_taptest.git' 'pytest_taptest'
   $ pip install -e 'pytest_taptest'


Usage
-----

.. code-block:: console

   # run all scripts named *.t as TAP tests
   $ pytest --tap-test-scripts '*.t'

   # run only TAP tests
   $ pytest --tap-test-scripts '*.t' -k 'TAP'

   # don't run any TAP tests
   $ pytest --tap-test-scripts '*.t' -k 'not TAP'

   # use the prove parser rather than tappy
   $ pytest --tap-test-scripts '*.t' --tap-parser='prove --exec cat'

   # source an environment file (once) before running tests
   $ echo 'FOO=foo' > env-script
   $ pytest --tap-test-scripts '*.t' --tap-env-script='env-script'


Configuration
-------------

Configure as CLI options as regular ``pytest`` options e.g:

*``pytest.ini``*

.. code-block:: ini

   [pytest]
   addopts =
       --tap-test-scripts='*.t'
