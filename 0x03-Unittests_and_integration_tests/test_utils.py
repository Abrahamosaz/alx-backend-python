#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized
from typing import Dict, Union, Tuple
from utils import access_nested_map, get_json, memoize
"""
Test file for testing utils.py file functions
"""


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class to test the access_nested_map function from
    the utils.py file
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(
        self,
        nested_map: Dict,
        path: Tuple[str], expected: Union[Dict, int]
    ):
        """
        use the self.assertEqual to test if the function is giving the
        expected value
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a"), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Dict,
            path: Tuple[str],
            expected: Exception
    ):
        """"Test for assertionRaise case"""
        with self.assertRaises(expected):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Test class to test the get_json function from the
    utils.py file
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url: str, test_payload: Dict):
        """
        test that the method return the expected result
        """
        attrs = {'json.return_value': test_payload}
        with patch('requests.get', return_value=Mock(**attrs)) as req_get:
            self.assertEqual(get_json(test_url), test_payload)
            req_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):

    def test_memoized(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=10) as mock_a_method:
            test_obj = TestClass()
            self.assertEqual(test_obj.a_property, 10)
            self.assertEqual(test_obj.a_property, 10)
            mock_a_method.assert_called_once()
