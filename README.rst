=================
pytest-mark-count
=================

.. image:: https://img.shields.io/pypi/v/pytest-mark-count.svg
    :target: https://pypi.org/project/pytest-mark-count
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-mark-count.svg
    :target: https://pypi.org/project/pytest-mark-count
    :alt: Python versions

.. image:: https://github.com/anogowski/pytest-mark-count/actions/workflows/publish-to-test-pypi.yml/badge.svg
    :target: https://github.com/anogowski/pytest-mark-count/actions/workflows/publish-to-test-pypi.yml
    :alt: See Build Status on GitHub Actions

Get a count of the number of tests marked, unmarked, and unique tests if tests have multiple markers

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Features
--------

.. list-table:: Get list of Searched Markers
   :widths: 100 250
   :header-rows: 1

   * - Key
     - Description

   * - total_found_items
     - Total number of discovered tests

   * - marked_found_items
     - Total number of discovered tests that are marked

   * - unmarked_found_items
     - Total number of discovered tests that are unmarked

   * - single_marked_found_items
     - Total number of discovered tests that only have 1 mark

   * - multi_marked_found_items
     - Total number of discovered tests that have more than 1 mark

   * - unique_marked_searched_items
     - Total number of tests discovered based on provided mark(s)

   * - single_marked_searched_items
     - Total number of tests discovered based on provided mark(s) that only have 1 mark

   * - multi_marked_searched_items
     - Total number of tests discovered based on provided mark(s) that have more than 1 mark

   * - "mark"
     - Total number of tests discovered based on that provided mark (each mark will have its own line)

Store values in metadata together or seperately

Requirements
------------

* See `requirements.txt`


Installation
------------

You can install "pytest-mark-count" via `pip`_ from `PyPI`_::

    $ pip install pytest-mark-count


Usage
-----

    $ --mark-count="it"

    $ --mark-count="it vt"

    $ --mark-count-sep=True

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------
Dual License:

Distributed under the terms of both the `BSD-3`_ AND `Mozilla Public License 2.0`_ licenses.

"pytest-mark-count" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: https://opensource.org/licenses/MIT
.. _`BSD-3`: https://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: https://www.gnu.org/licenses/gpl-3.0.txt
.. _`Mozilla Public License 2.0`: https://opensource.org/license/mpl-2-0
.. _`Apache Software License 2.0`: https://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/anogowski/pytest-mark-count/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
