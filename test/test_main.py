#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import unittest
from auto_encoder import __main__ as _main


class TestMain(unittest.TestCase):
    """Test case for main function."""

    @classmethod
    def setUpClass(cls):
        """setup class"""
        pass

    @classmethod
    def tearDownClass(cls):
        """teardown class"""
        pass

    def setUp(self):
        """setup"""
        pass

    def tearDown(self):
        """teardown"""
        pass

    def test_get_debug_level_lower(self):
        """test with lower case string argument."""
        self.assertEqual(logging.DEBUG, _main.get_logging_level_from('debug'))
        self.assertEqual(logging.INFO, _main.get_logging_level_from('info'))

    def test_get_debug_level_upper(self):
        """test with upper case string argument."""
        self.assertEqual(logging.DEBUG, _main.get_logging_level_from('DEBUG'))
        self.assertEqual(logging.INFO, _main.get_logging_level_from('INFO'))

    def test_get_debug_level_invalid(self):
        """test with invalid string argument."""
        self.assertEqual(logging.INFO, _main.get_logging_level_from('HOGE'))


if __name__ == "__main__":
    unittest.main(verbosity=2)
