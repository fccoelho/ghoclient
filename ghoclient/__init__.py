"""Top-level package for GHOclient."""

__author__ = """Flávio Codeço Coelho"""
__email__ = 'fccoelho@gmail.com'
__version__ = '0.1.0'

from .ghoclient import GHOSession
from ghoclient.index import Index

index = Index()
GC = GHOSession()
datacodes =  GC.get_data_codes(format='dataframe')
datacodes.columns = [c.strip('@') for c in datacodes.columns]
index.build_index(datacodes)



