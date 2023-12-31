#!/usr/bin/env python3
"""this is a test file"""
import unittest
from parameterized import parameterized
from typing import Dict, Tuple, List, Any, Callable
from unittest.mock import patch, Mock
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
    def test_get_json(self,
                      url: str,
                      payload: Dict) -> None:
        """tests if json is gotten"""
        m_obj = Mock()
        m_obj.json.return_value = payload

        with patch("requests.get", return_value=m_obj) as mock_get:
            result = get_json(url)
            mock_get.assert_called_once_with(url)

        self.assertEqual(result, payload)


class TestMemoize(unittest.TestCase):
    """contains tests for the memoize function"""

    def test_memoize(self) -> None:
        """testing memoize"""
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method',
                          return_value=lambda: 42) as a_method:
            tclass = TestClass()
            self.assertEqual(tclass.a_property(), 42)
            self.assertEqual(tclass.a_property(), 42)
            a_method.assert_called_once()
