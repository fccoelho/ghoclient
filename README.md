# GHOclient

[![Sponsored by Kwar-AI](docs/kwar-ai-logo.jpg)](https://kwar-ai.com.br)

*Sponsored by* [Kwar-AI](https://kwar-ai.com.br) *- AI-powered epidemiological intelligence*

---

[![PyPI version](https://img.shields.io/pypi/v/ghoclient.svg)](https://pypi.org/project/ghoclient/)
[![Python versions](https://img.shields.io/pypi/pyversions/ghoclient.svg)](https://pypi.org/project/ghoclient/)
[![License](https://img.shields.io/pypi/l/ghoclient.svg)](https://github.com/fccoelho/ghoclient/blob/master/LICENSE)
[![Tests](https://github.com/fccoelho/ghoclient/actions/workflows/python-package.yml/badge.svg)](https://github.com/fccoelho/ghoclient/actions/workflows/python-package.yml)
[![Publish](https://github.com/fccoelho/ghoclient/actions/workflows/python-publish.yml/badge.svg)](https://github.com/fccoelho/ghoclient/actions/workflows/python-publish.yml)
[![Documentation](https://readthedocs.org/projects/ghoclient/badge/?version=latest)](https://ghoclient.readthedocs.io/en/latest/)

## Introduction

The WHO [Global Health Observatory](https://www.who.int/data/gho) is a large global health data repository that makes available an enormous collection of [indicators](https://www.who.int/data/gho/data/indicators/indicators-index) which can be downloaded through their [API](https://www.who.int/data/gho/info/gho-odata-api). GHOclient is a Python client which helps data scientists search and access their data programmatically.

- Free software: MIT license
- Documentation: https://ghoclient.readthedocs.io.

## Installation

Using pip:

```bash
pip install ghoclient
```

Using uv:

```bash
uv pip install ghoclient
```

For development:

```bash
git clone https://github.com/fccoelho/ghoclient.git
cd ghoclient
uv sync --extra dev
```

## Features

- Search for indicators by keyword
- Browse available datasets
- List region and country codes
- Get the data as pandas DataFrames

## Example usage

Basic usage with the GHO class:

```python
from ghoclient import GHO

gho = GHO()

# Get all available indicators
indicators = gho.get_indicators()

# Search for specific indicators
malaria_indicators = gho.search_indicators('malaria')

# Get data for a specific indicator
life_expectancy = gho.get_data('WHOSIS_000001', countries=['BRA', 'USA'])
```

Legacy usage with index search:

```python
import ghoclient
ghoclient.index.search('smoking')
```

The above lines will fetch a DataFrame with all indicators containing the word smoking in their description.

## API Reference

### GHO Class

Main interface for accessing WHO GHO data.

- **`get_indicators()`**

  Returns a DataFrame with all available indicators.

- **`search_indicators(query)`**

  Search for indicators containing the query string.

  - `query`: Search term
  - Returns: DataFrame with matching indicators

- **`get_data(code, countries=None, filter_query=None)`**

  Get data for a specific indicator.

  - `code`: Indicator code (e.g., `'WHOSIS_000001'`)
  - `countries`: Optional list of country codes to filter by
  - `filter_query`: Optional OData filter query string
  - Returns: DataFrame with the requested data

### GHOSession Class

Low-level session class for direct API access.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
