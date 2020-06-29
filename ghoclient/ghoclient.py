"""
Main module.
Provides a class with utility methods for fetching data from the Global Health Observatory.
"""

import xmltodict
import pandas as pd
import requests
from pprint import pprint

BASE_URL = 'http://apps.who.int/gho/athena/api/'


class GHOSession:
    def __init__(self):
        resp = requests.get(BASE_URL)
        self.data = xmltodict.parse(resp.text)

    def get_available_datasets(self):
        datasets = []
        for k, v in self.data['GHO']['Metadata'].items():
            if k == 'Dataset':
                datasets.extend([d for d in v])
        return datasets

    def get_attributes(self):
        attributes = []
        for k, v in self.data['GHO']['Metadata'].items():
            if k == 'Attribute':
                attributes.extend([d for d in v])
        return attributes

    def get_dimensions(self):
        dimensions = []
        for k, v in self.data['GHO']['Metadata'].items():
            if k == 'Dimension':
                dimensions.extend([d for d in v])
        return dimensions

    def get_region_codes(self):
        url = BASE_URL + 'REGION'
        data = self._fetch_data_as_dict(url)
        regions = [{c['@Label']: c['Display']} for c in data['GHO']['Metadata']['Dimension']['Code']]
        return regions

    def get_countries(self, format='dataframe'):
        url = BASE_URL + 'COUNTRY'
        data = self._fetch_data_as_dict(url)
        if format == 'dataframe':
            lines = []
            for d in data['GHO']['Metadata']['Dimension']['Code']:
                rec = {k: v for k, v in d.items() if k != 'Attr'}
                for attr in d['Attr']:
                    rec[attr['@Category']] = attr['Value']['Display']
                lines.append(rec)
            return pd.DataFrame(lines)
        elif format == 'full':
            return data['GHO']['Metadata']['Dimension']['Code']
        return data


    def _fetch_data_as_dict(self, url):
        """
        Downloads XML data, parses it and return as dict.
        :param url:
        """
        resp = requests.get(url)
        data = xmltodict.parse(resp.text)
        return data

    def get_data_codes(self, format='full'):
        """
        Get Codes That
        :param format: either 'full', 'label' or 'url'
        :return: list of dicts when format is full or a list of strings otherwise.
        """
        url = BASE_URL + 'GHO'
        data = self._fetch_data_as_dict(url)
        # codes = [d for d in data['GHO']['Metadata']['Dimension']['Code']]
        if format == 'full':
            return [d for d in data['GHO']['Metadata']['Dimension']['Code']]
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
    # pprint(GC.get_data_codes(format='label'))

    # pprint(GC.get_region_codes())
    print(GC.get_countries())
