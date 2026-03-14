"""
Main module.
Provides a class with utility methods for fetching data from the Global Health Observatory.
"""

import requests
import pandas as pd
import io

BASE_URL = "https://ghoapi.azureedge.net/api/"

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


class GHOSession:
    def __init__(self):
        resp = requests.get(BASE_URL, headers=header)
        resp.raise_for_status()
        self.data = resp.json()

    def get_available_datasets(self):
        """
        Check for available datasets

        Returns
        -------
        datasets : list
            list of datasets.

        """
        return self.data.get("value", [])

    def get_dimensions(self, format="dataframe"):
        """
        List dimensions of data

        Parameters
        ----------
        format : str, output format, of `dataframe` (default) or `list`
            DESCRIPTION. The default is 'dataframe'.

        Returns
        -------
        dimensions: dataframe or list
            description of every variable in the datasets and their dimension.

        """
        url = BASE_URL + "DIMENSION"
        data = self._fetch_data(url)
        if format == "dataframe":
            return pd.DataFrame(data.get("value", []))
        return data.get("value", [])

    def get_region_codes(self):
        """
        Returns region codes

        Returns
        -------
        regions : dictionary
            Dictionary with code, description pairs.

        """
        url = BASE_URL + "DIMENSION/REGION/DimensionValues"
        data = self._fetch_data(url)
        regions = {c["Code"]: c["Title"] for c in data.get("value", [])}
        return regions

    def get_countries(self, format="dataframe"):
        """
        Returns a dataframe with country codes and metadata

        Parameters
        ----------
        format : str, optional
            The default is 'dataframe'.

        Returns list if `format` is 'full'
        -------
        data: dataframe by default
            country info.

        """
        url = BASE_URL + "DIMENSION/COUNTRY/DimensionValues"
        data = self._fetch_data(url)
        if format == "dataframe":
            return pd.DataFrame(data.get("value", []))
        elif format == "full":
            return data.get("value", [])
        return data

    def get_data_codes(self, format="dataframe"):
        """
        Get Codes that can be fetched as indicators.
        :param format: either 'full', 'label' or 'dataframe'
        :return: list of dicts when `format` is 'full', a Dataframe when it is 'dataframe' or a list of strings otherwise.
        """
        url = BASE_URL + "Indicator"
        data = self._fetch_data(url)
        indicators = data.get("value", [])

        if format == "full":
            return indicators
        if format == "dataframe":
            df = pd.DataFrame(indicators)
            df = df.rename(
                columns={"IndicatorCode": "Label", "IndicatorName": "Display"}
            )
            df["IndicatorCode"] = df["Label"]
            df["IndicatorName"] = df["Display"]
            return df
        elif format == "label":
            return [d["IndicatorCode"] for d in indicators]

    def fetch_data_from_codes(self, code=None, like=None, filter_query=None):
        """
        Fetches data for a specific indicator code or a list of indicators matching the substring in `like`
        :param code: Indicator code to fetch (for a full list of available codes use `get_data_codes` method.)
        :param like: substring of the codes desired
        :param filter_query: OData filter query string (e.g., "Dim1 eq 'MLE'")
        :return: Dataframe with table.
        """
        if code is None and like is None:
            raise ValueError("Either 'code' or 'like' must be provided")

        if code is None:
            codes = [
                c
                for c in self.get_data_codes(format="label")
                if like.lower() in c.lower()
            ]
        elif isinstance(code, (list, tuple)):
            codes = list(code)
        elif isinstance(code, str):
            codes = [code]
        else:
            raise ValueError("code must be a string or list of strings")

        all_data = []
        for c in codes:
            url = BASE_URL + c
            if filter_query:
                url += f"?$filter={filter_query}"
            response = requests.get(url, headers=header)
            response.raise_for_status()
            data = response.json()
            if "value" in data and data["value"]:
                all_data.extend(data["value"])

        if all_data:
            return pd.DataFrame(all_data)
        return pd.DataFrame()

    def get_data(self, code, countries=None, filter_query=None):
        """
        Get data for a specific indicator code, optionally filtered by countries.
        :param code: Indicator code to fetch
        :param countries: Optional list of country codes to filter by
        :param filter_query: Additional OData filter query string
        :return: DataFrame with the data
        """
        url = BASE_URL + code
        filters = []

        if countries:
            if isinstance(countries, str):
                countries = [countries]
            country_filter = " or ".join([f"SpatialDim eq '{c}'" for c in countries])
            filters.append(f"({country_filter})")

        if filter_query:
            filters.append(filter_query)

        if filters:
            url += "?$filter=" + " and ".join(filters)

        response = requests.get(url, headers=header)
        response.raise_for_status()
        data = response.json()

        if "value" in data and data["value"]:
            return pd.DataFrame(data["value"])
        return pd.DataFrame()

    def get_indicators(self):
        """
        Get all available indicators as a DataFrame.
        :return: DataFrame with indicator codes and names
        """
        return self.get_data_codes(format="dataframe")

    def _fetch_data(self, url):
        """
        Downloads JSON data from the given URL.
        :param url: URL to fetch
        :return: JSON data as dict
        """
        resp = requests.get(url, headers=header)
        resp.raise_for_status()
        return resp.json()


class GHO:
    """
    Simplified interface for WHO GHO data access.
    Provides a more intuitive API for common operations.
    """

    def __init__(self):
        self.session = GHOSession()

    def get_indicators(self):
        """Get all available indicators."""
        return self.session.get_data_codes(format="dataframe")

    def get_data(self, code, countries=None, filter_query=None):
        """
        Get data for a specific indicator.

        Parameters
        ----------
        code : str
            Indicator code (e.g., 'WHOSIS_000001' for life expectancy)
        countries : list or str, optional
            Country code(s) to filter by (e.g., ['BRA', 'USA'] or 'BRA')
        filter_query : str, optional
            Additional OData filter query

        Returns
        -------
        DataFrame
            The requested data
        """
        return self.session.get_data(code, countries, filter_query)

    def search_indicators(self, query):
        """
        Search for indicators containing the query string.

        Parameters
        ----------
        query : str
            Search term

        Returns
        -------
        DataFrame
            Matching indicators
        """
        indicators = self.get_indicators()
        mask = indicators.apply(lambda row: query.lower() in str(row).lower(), axis=1)
        return indicators[mask]


if __name__ == "__main__":
    gho = GHO()
    print("Available indicators:")
    indicators = gho.get_indicators()
    print(indicators.head())
