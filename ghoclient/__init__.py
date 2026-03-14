"""Top-level package for GHOclient."""

__author__ = """Flávio Codeço Coelho"""
__email__ = "fccoelho@gmail.com"
__version__ = "0.1.0"

from .ghoclient import GHOSession, GHO


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
