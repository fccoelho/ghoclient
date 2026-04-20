"""Top-level package for GHOclient."""

__author__ = """Flávio Codeço Coelho"""
__email__ = "fccoelho@gmail.com"
__version__ = "1.0.5"

from .ghoclient import GHOSession, GHO
from .index import Index


def get_gho_client():
    """Get a GHO client instance."""
    return GHO()


GC = None
index = None


def _initialize():
    """Initialize the global client and index."""
    global GC, index
    if GC is None:
        GC = GHOSession()
    return GC


def _initialize_index():
    """Initialize the global index."""
    global index, GC
    if GC is None:
        GC = GHOSession()
    if index is None:
        index = Index()
        datacodes = GC.get_data_codes(format="dataframe")
        datacodes.columns = [c.strip("@") for c in datacodes.columns]
        index.build_index(datacodes)
    return index


index = Index()
