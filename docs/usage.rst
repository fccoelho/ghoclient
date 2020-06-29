=====
Usage
=====

To use GHOclient in a project::

    import ghoclient
    GC = ghoclient.GHOSession()

from this object a simple API is available to fetch data from the WHO's Global Health Observatory::

    df = GC.fetch_data_from_codes(like='MALARIA')
    df.head()

The code above fetches all indicators containing the case-insensitive substring `malaria` in their name, returning a
pandas DataFrame with data for all countries and years, which can later be filtered locally.

In order to find out what indicator codes are available, you can use the following method::

    codes_table = GC.get_data_codes(format='dataframe')

the get a table with full information on the indicators, or if you want just the codes::

    GC.get_data_codes(format='label')
