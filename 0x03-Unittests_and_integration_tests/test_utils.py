#!/usr/bin/env python3
"""this is a test file"""
import unittest
from parameterized import parameterized
from typing import Dict, Tuple, List, Any
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
