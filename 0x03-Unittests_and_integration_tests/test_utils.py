#!/usr/bin/env python3
"""this is a test file"""
import unittest
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """contains unittests for the nestedmap function"""

    @parameterized.expand([
        ({"x": {"y": {"z": "hello"}}}, ["x", "y", "z"], "hello"),
        ({"a": {"b": {"c": "end"}}}, ["a", "b", "c"], "end"),
        ({"a": {"b": {"c": "end"}}}, ["a", "b", "b"], KeyError)])
    def test_access_nested_map(self, dmap, path, result):
        """tests if the access method works"""
        self.assertEqual(access_nested_map(dmap, path), result)
