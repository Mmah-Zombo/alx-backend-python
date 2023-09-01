#!/usr/bin/env python3
"""this is a test file"""
import unittest
from client import GithubOrgClient
from parameterized import parameterized
from typing import Dict
from unittest.mock import patch, Mock, MagicMock


class TestGithubOrgClient(unittest.TestCase):
    """tests for the GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("get_json")
    def test_org(self, org: str, output: Dict, get_json: MagicMock) -> None:
        """test that GithubOrgClient.org returns the correct value"""
        get_json.return_value = output
        goc = GithubOrgClient(org)
        get_json.assert_called_once_with(f"https://api.github.com/orgs/{org}")

        response = goc.org()
        self.assertEqual(response, output)
