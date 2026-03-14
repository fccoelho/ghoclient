GHOclient
=========

.. image:: https://img.shields.io/pypi/v/ghoclient.svg
   :target: https://pypi.org/project/ghoclient/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/ghoclient.svg
   :target: https://pypi.org/project/ghoclient/
   :alt: Python versions

.. image:: https://img.shields.io/pypi/l/ghoclient.svg
   :target: https://github.com/fccoelho/ghoclient/blob/master/LICENSE
   :alt: License

.. image:: https://github.com/fccoelho/ghoclient/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/fccoelho/ghoclient/actions/workflows/python-package.yml
   :alt: Tests

.. image:: https://github.com/fccoelho/ghoclient/actions/workflows/python-publish.yml/badge.svg
   :target: https://github.com/fccoelho/ghoclient/actions/workflows/python-publish.yml
   :alt: Publish

.. image:: https://readthedocs.org/projects/ghoclient/badge/?version=latest
   :target: https://ghoclient.readthedocs.io/en/latest/
   :alt: Documentation

Introduction
------------

The WHO `Global Health Observatory`_ is a large global health data repository that makes available an enormous collection of indicators_ which can be downloaded through their API_. GHOclient is a Python client which helps data scientists search and access their data programmatically.

* Free software: MIT license
* Documentation: https://ghoclient.readthedocs.io.


Installation
------------

Using pip:

.. code-block:: bash

    pip install ghoclient

Using uv:

.. code-block:: bash

    uv pip install ghoclient

For development:

.. code-block:: bash

    git clone https://github.com/fccoelho/ghoclient.git
    cd ghoclient
    uv sync --extra dev


Features
--------

* Search for indicators by keyword
* Browse available datasets
* List region and country codes
* Get the data as pandas DataFrames

Example usage
-------------

Basic usage with the GHO class:

.. code-block:: python

    from ghoclient import GHO
    
    gho = GHO()
    
    # Get all available indicators
    indicators = gho.get_indicators()
    
    # Search for specific indicators
    malaria_indicators = gho.search_indicators('malaria')
    
    # Get data for a specific indicator
    life_expectancy = gho.get_data('WHOSIS_000001', countries=['BRA', 'USA'])

Legacy usage with index search:

.. code-block:: python

    import ghoclient
    ghoclient.index.search('smoking')

The above lines will fetch a DataFrame with all indicators containing the word smoking in their description.


API Reference
-------------

GHO Class
~~~~~~~~~

.. py:class:: GHO

   Main interface for accessing WHO GHO data.

   .. py:method:: get_indicators()

      Returns a DataFrame with all available indicators.

   .. py:method:: search_indicators(query)

      Search for indicators containing the query string.
      
      :param query: Search term
      :return: DataFrame with matching indicators

   .. py:method:: get_data(code, countries=None, filter_query=None)

      Get data for a specific indicator.
      
      :param code: Indicator code (e.g., 'WHOSIS_000001')
      :param countries: Optional list of country codes to filter by
      :param filter_query: Optional OData filter query string
      :return: DataFrame with the requested data

GHOSession Class
~~~~~~~~~~~~~~~~

.. py:class:: GHOSession

   Low-level session class for direct API access.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Global Health Observatory`: https://www.who.int/data/gho
.. _indicators: https://www.who.int/data/gho/data/indicators/indicators-index
.. _API: https://www.who.int/data/gho/info/gho-odata-api
