#!/usr/bin/env python

"""Tests for `ghoclient` package."""

import unittest
from click.testing import CliRunner

import ghoclient
from ghoclient import cli
from ghoclient import Index, GHO
import pandas as pd


class TestGhoclient(unittest.TestCase):
    """Tests for `ghoclient` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        help_result = runner.invoke(cli.main, ["--help"])
        assert help_result.exit_code == 0
        assert "--help  Show this message and exit." in help_result.output


class TestGHO(unittest.TestCase):
    def test_get_countries_as_df(self):
        gho = GHO()
        df = gho.session.get_countries()
        self.assertIsInstance(df, pd.DataFrame)

    def test_get_dimensions_as_df(self):
        gho = GHO()
        df = gho.session.get_dimensions()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreaterEqual(len(df.columns), 2)

    def test_get_data(self):
        gho = GHO()
        df = gho.get_data("WHOSIS_000001", countries=["BRA"])
        self.assertIsInstance(df, pd.DataFrame)

    def test_get_indicators(self):
        gho = GHO()
        indicators = gho.get_indicators()
        self.assertIsInstance(indicators, pd.DataFrame)
        self.assertGreater(len(indicators), 0)

    def test_search_indicators(self):
        gho = GHO()
        results = gho.search_indicators("tuberculosis")
        self.assertIsInstance(results, pd.DataFrame)


class TestIndex(unittest.TestCase):
    def test_build_index(self):
        idx = Index()
        gho = GHO()
        datacodes = gho.session.get_data_codes(format="dataframe")
        datacodes.columns = [c.strip("@") for c in datacodes.columns]
        idx.build_index(datacodes)
        self.assertIsNotNone(idx.ix)

    def test_search(self):
        idx = Index()
        gho = GHO()
        datacodes = gho.session.get_data_codes(format="dataframe")
        datacodes.columns = [c.strip("@") for c in datacodes.columns]
        idx.build_index(datacodes)
        res = idx.search("tuberculosis")
        self.assertIsInstance(res, list)
        if len(res) > 0:
            self.assertIsInstance(res[0], dict)
            self.assertIn("code", res[0])
