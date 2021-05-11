GHOclient
=========

.. image:: https://github.com/fccoelho/ghoclient/actions/workflows/python-package.yml/badge.svg
.. image:: https://github.com/fccoelho/ghoclient/actions/workflows/python-publish.yml/badge.svg


Introduction
------------

The WHO `Global Health Observatory`_ is a large global health data repository that makes available an enormous collection  of indicators_ which can be downloaded through their API_. GHOclient is a Python client which helps data scientists search and access their data programmatically.





* Free software: MIT license
* Documentation: https://ghoclient.readthedocs.io.


Features
--------

* Search for indicators by keyword
* Browse available datasets
* List region and country codes
* get the data as pandas Dataframes

Example usage
-------------
For example, to search for health data ona certain topic, like smoking

.. code-block:: Python

    import ghoclient
    ghoclient.index.search('smoking')

The above lines will fetch a Dataframe with all indicators containing the word smoking in their description.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Global Health Observatory`: https://www.who.int/data/gho
.. _indicators: https://www.who.int/data/gho/data/indicators/indicators-index
.. _API: https://www.who.int/data/gho/info/gho-odata-api
