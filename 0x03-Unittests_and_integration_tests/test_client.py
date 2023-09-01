#!/usr/bin/env python3
"""this is a test file"""
import unittest
from client import GithubOrgClient
from parameterized import parameterized
from typing import Dict
from unittest.mock import patch, Mock


class TestGithubOrgClient(unittest.TestCase):
    """tests for the GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org: str, output: Dict, get_json: Mock) -> None:
        """test that org returns the correct value"""
        get_json.return_value = output
        goc = GithubOrgClient(org)
        self.assertEqual(goc.org(), output)
        get_json.assert_called_once_with(f"https://api.github.com/orgs/{org}")
