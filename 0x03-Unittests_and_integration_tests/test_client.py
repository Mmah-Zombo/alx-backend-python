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
        test_payload = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-19T00:31:37Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "has_issues": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    "id": 8566972,
                    "name": "kratu",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/kratu",
                    "created_at": "2013-03-04T22:52:33Z",
                    "updated_at": "2019-11-15T22:22:16Z",
                    "has_issues": True,
                    "forks": 32,
                    "default_branch": "master",
                },
            ]
        }
        gjson.return_value = test_payload['repos']

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=property) as pru:
            pru.return_value = test_payload['repos_url']
            self.assertEqual(GithubOrgClient('google').public_repos(),
                             ["episodes.dart", "kratu"])
            pru.assert_called_once()
        gjson.assert_called_once()
