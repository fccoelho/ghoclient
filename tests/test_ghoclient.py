#!/usr/bin/env python

"""Tests for `ghoclient` package."""

import unittest
from click.testing import CliRunner

from ghoclient import ghoclient
from ghoclient import cli
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
        # assert 'ghoclient.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output


class TestGHO(unittest.TestCase):
    def test_get_countries_as_df(self):
        GC = ghoclient.GHOSession()
        df = GC.get_countries()
        self.assertIsInstance(df, pd.DataFrame)

    def test_get_dimensions_as_df(self):
        GC = ghoclient.GHOSession()
        df = GC.get_dimensions()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEquals(len(df.columns), 3)
