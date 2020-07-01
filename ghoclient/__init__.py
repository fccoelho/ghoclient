"""Top-level package for GHOclient."""

__author__ = """Flávio Codeço Coelho"""
__email__ = 'fccoelho@gmail.com'
__version__ = '0.1.0'

from .ghoclient import GHOSession
from ghoclient import index


index.build_index()


