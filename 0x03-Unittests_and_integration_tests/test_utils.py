#!/usr/bin/env python3
"""this is a test file"""
import unittest
from parameterized import parameterized
from typing import Dict, Tuple, List, Any, Callable
from unittest import mock
from utils import (
    access_nested_map,
    get_json,
    memoize,
)


class TestAccessNestedMap(unittest.TestCase):
    """contains unittests for the nestedmap function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)])
    def test_access_nested_map(self,
                               dmap: Dict,
                               path: Tuple[str],
                               result: Any) -> None:
        """tests if the access method works"""
        self.assertEqual(access_nested_map(dmap, path), result)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(self,
                                         dmap: Dict,
                                         path: Tuple[str],
                                         error: Exception) -> None:
        """tests if the correct exception is raised"""
        with self.assertRaises(error):
            access_nested_map(dmap, path)


class TestGetJson(unittest.TestCase):
    """contains unittests for the get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @mock.patch("requests.get")
    def test_get_json(self,
                      mock_get: Callable, url: str,
                      test_payload: Dict) -> None:
        """tests if json is gotten"""
        mock_obj = mock.Mock()
        mock_obj.json.return_value = test_payload
        mock_get.return_value = mock_obj
        result = get_json(url)
        mock_get.assert_called_once_with(url)
        self.assertEqual(result, test_payload)
