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
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    @patch(
        "client.get_json",
    )
    def test_org(self, orgc: str, output: Dict, gjson: Mock) -> None:
        """Tests the `org` method."""
        gjson.return_value = Mock(return_value=output)
        goc = GithubOrgClient(orgc)
        self.assertEqual(goc.org(), output)
        gjson.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(orgc)
        )

    def test_public_repos_url(self) -> None:
        """test the public_repos_url function"""
        with patch.object(GithubOrgClient, 'org', new_callable=property) as og:
            og.return_value = {
                'repos_url': "https://api.github.com/users/google/repos",
            }

        self.assertEqual(GithubOrgClient._public_repos_url(),
                         "https://api.github.com/users/google/repos",)

    @patch("client.get_json")
    def test_public_repos(self, g_json: Mock) -> None:
        """tests the public_repos function"""
        test_payload = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "has_issues": True,
                },
                {
                    "id": 8566972,
                    "name": "kratu",
                    "private": False,
                    "has_issues": True,
                },
            ]
        }
        g_json.return_value = test_payload["repos"]

        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as pru:
            pru.return_value = test_payload["repos_url"]
            self.assertEqual(GithubOrgClient("google").public_repos(),
                             ["episodes.dart", "kratu"])
            pru.assert_called_once()
        g_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo: Dict, li_key: str,
                         result: bool) -> None:
        """tests if the has_license function"""
        self.assertEqual(
            GithubOrgClient("google").has_license(
                repo, li_key
            ), result
        )


@parameterized_class([
    {"org_payload": TEST_PAYLOAD[0][0],
     "repos_payload": TEST_PAYLOAD[0][1],
     "expected_repos": TEST_PAYLOAD[0][2],
     "apache2_repos": TEST_PAYLOAD[0][3]}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """contains integration test for the public_repo function"""
    @classmethod
    def setUpClass(cls) -> None:
        """setsup the fixtures"""
        cls.get_patcher = patch('requests.get')

        # Mock requests.get to return the org and repos payloads
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = [
            cls.org_payload,  # Mock the org payload
            cls.repos_payload,  # Mock the repos payload
        ]

    def test_public_repos(self) -> None:
        """tests the public_repos function"""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """tests the public_repo_with_license function"""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos)

    @classmethod
    def tearDownClass(cls) -> None:
        """pull down the fixtures"""
        cls.get_patcher_stop()
