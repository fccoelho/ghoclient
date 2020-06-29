"""Main module."""

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

    def get_data_codes(self):
        url = BASE_URL + 'GHO'
        resp = requests.get(url)
        data = xmltodict.parse(resp.text)
        codes = [d for d in data['GHO']['Metadata']['Dimension']['Code']]

        return codes

if __name__ == "__main__":
    GC = GHOSession()

    # pprint(GC.get_available_datasets())
    # print(len(GC.get_available_datasets()))
    # pprint(GC.get_attributes())
    # pprint(GC.get_dimensions())
    pprint(GC.get_data_codes())
