#!/usr/bin/env python3
"""this is a test file"""
import unittest
from typing import Dict
from unittest.mock import (
    MagicMock,
    Mock,
    PropertyMock,
    patch,
)
from parameterized import parameterized, parameterized_class
from requests import HTTPError

from client import (
    GithubOrgClient
)
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """tests for the GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, orgc: str, output: Dict, gjson: Mock) -> None:
        """tests the org function"""

        gjson.return_value = output
        goc = GithubOrgClient(orgc)
        self.assertEqual(goc.org(), output)
        gjson.assert_called_once_with(f"https://api.github.com/orgs/{orgc}")

    def test_public_repos_url(self) -> None:
        """test the public_repos_url function"""
        with patch.object(GithubOrgClient, 'org', new_callable=property) as og:
            og.return_value = {
                'repos_url': "https://api.github.com/users/google/repos",
            }
        self.assertEqual(GithubOrgClient._public_repos_url(),
                         "https://api.github.com/users/google/repos",)

    @patch("client.get_json")
    def test_public_repos(self, gjson: Mock) -> None:
        """tests the public_repos function"""
        content = [
            {"name": "repo1", "license": {"key": "MIT"}},
            {"name": "repo2", "license": {"key": "Apache"}}
        ]
        gjson.return_value = content
        output = "https://api.github.com/orgs/testorg/repos"

        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=property,
                          return_value=output):
            goc = GithubOrgClient('testorg')
            repos = goc.public_repos(license="MIT")
            gjson.assert_called_once()
            self.assertEqual(repos, ["repo1"])
