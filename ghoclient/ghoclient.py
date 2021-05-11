"""
Main module.
Provides a class with utility methods for fetching data from the Global Health Observatory.
"""

import xmltodict
import pandas as pd
import requests
import io
from pprint import pprint

BASE_URL = 'http://apps.who.int/gho/athena/api/'

header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

class GHOSession:
    def __init__(self):
        resp = requests.get(BASE_URL)
        self.data = xmltodict.parse(resp.text)

    def get_available_datasets(self):
        '''
        Check for available datasets

        Returns 
        -------
        datasets : list
            list of datasets.

        '''
        datasets = []
        for k, v in self.data['GHO']['Metadata'].items():
            if k == 'Dataset':
                datasets.extend([d for d in v])
        return datasets

    def get_attributes(self):
        '''
        Lists attributes used on datasets

        Returns
        -------
        attributes : list
            list of attributes represented as dictionaries.

        '''
        attributes = []
        for k, v in self.data['GHO']['Metadata'].items():
            if k == 'Attribute':
                attributes.extend([d for d in v])
        return attributes

    def get_dimensions(self, format='dataframe'):
        '''
        List dimensions of data

        Parameters
        ----------
        format : str, output format, of `dataframe` (default) or `list`
            DESCRIPTION. The default is 'dataframe'.

        Returns
        -------
        dimensions: dataframe or list
            description of every variable in the datasets and their dimension.

        '''
        dimensions = []
        for k, v in self.data['GHO']['Metadata'].items():
            if k == 'Dimension':
                dimensions.extend([d for d in v])
        if format == 'dataframe':
            return pd.DataFrame(dimensions)
        return dimensions

    def get_region_codes(self):
        '''
        Returns region codes

        Returns
        -------
        regions : dictionary
            Dictionary with code, description pairs.

        '''
        url = BASE_URL + 'REGION'
        data = self._fetch_data_as_dict(url)
        regions = {c['@Label']: c['Display'] for c in data['GHO']['Metadata']['Dimension']['Code']}
        return regions

    def get_countries(self, format='dataframe'):
        '''
        Returns a dataframe with country codes and metadata

        Parameters
        ----------
        format : str, optional
            The default is 'dataframe'.

        Returns list if `format` is full
        -------
        data: dataframe by default
            country info.

        '''
        url = BASE_URL + 'COUNTRY'
        data = self._fetch_data_as_dict(url)
        if format == 'dataframe':
            lines = []
            for d in data['GHO']['Metadata']['Dimension']['Code']:
                rec = {k: v for k, v in d.items() if k != 'Attr'}
                if 'Attr' in d:
                    for attr in d['Attr']:
                        rec[attr['@Category']] = attr['Value']['Display']
                lines.append(rec)
            return pd.DataFrame(lines)
        elif format == 'full':
            return data['GHO']['Metadata']['Dimension']['Code']
        return data

    def fetch_data_from_codes(self, code=None, like='MALARIA'):
        """
        Fetches data for a specific indicator code or a list of indicators matching the substring in `like`
        :param code: Indicator code to fetch (for a full list of available codes use `get_data_codes` method.)
        :param like: substring of the codes desired
        :return: Dataframe with table.
        """
        url = BASE_URL + 'GHO/'
        if code is None:
            codes = [c for c in self.get_data_codes(format='label') if like.lower() in c.lower()]
        
        elif isinstance(code, (list, tuple)):
            codes = list(code)
        elif isinstance(code, str):
            codes=[code]
                
        url += ','.join(codes)
        url += '&format=csv' if '?' in url else '?format=csv'
        response = requests.get(url, headers=header)
        file_object = io.StringIO(response.content.decode('utf-8'))
        data = pd.read_csv(file_object)
        
        return data



    def _fetch_data_as_dict(self, url):
        """
        Downloads XML data, parses it and return as dict.
        :param url:
        """
        resp = requests.get(url)
        data = xmltodict.parse(resp.text)
        return data

    def get_data_codes(self, format='dataframe'):
        """
        Get Codes that can be fetched as indicators.
        :param format: either 'full', 'label' or 'url'
        :return: list of dicts when `format` is 'full', a Dataframe when it is 'dataframe' or a list of strings otherwise.
        """
        url = BASE_URL + 'GHO'
        data = self._fetch_data_as_dict(url)
        # codes = [d for d in data['GHO']['Metadata']['Dimension']['Code']]
        if format == 'full':
            return [d for d in data['GHO']['Metadata']['Dimension']['Code']]
        if format == 'dataframe':
            return pd.DataFrame([d for d in data['GHO']['Metadata']['Dimension']['Code']])
        elif format == 'label':
            return [d['@Label'] for d in data['GHO']['Metadata']['Dimension']['Code']]
        elif format == 'url':
            return [d['@URL'] for d in data['GHO']['Metadata']['Dimension']['Code']]

if __name__ == "__main__":
    GC = GHOSession()

    # pprint(GC.get_available_datasets())
    # print(len(GC.get_available_datasets()))
    # pprint(GC.get_attributes())
    # pprint(GC.get_dimensions())
    pprint(GC.get_data_codes(format='dataframe'))

    # pprint(GC.get_region_codes())
    # print(GC.get_countries())
    # pprint(GC.fetch_data_from_codes())
