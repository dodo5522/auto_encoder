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

    def test_init_args_normal(self):
        """test init_args() with normal arguments."""
        args = _main.init_args(['-s', 'dummy.m2ts', '-d', 'dummy.mp4', '--deinterlace'])
        self.assertEqual(args.source, 'dummy.m2ts')
        self.assertEqual(args.dest, 'dummy.mp4')
        self.assertTrue(args.deinterlace)

    def test_init_args_abnormal(self):
        """test init_args() with abnormal arguments."""
        args = _main.init_args([])
        self.assertEqual(args.source, '/symlinks/videos/tv')
        self.assertEqual(args.dest, '/symlinks/videos/tv_converted')
        self.assertFalse(args.deinterlace)

    def test_get_debug_level_lower(self):
        """test get_debug_level() with lower case string argument."""
        self.assertEqual(logging.DEBUG, _main.get_logging_level_from('debug'))
        self.assertEqual(logging.INFO, _main.get_logging_level_from('info'))

    def test_get_debug_level_upper(self):
        """test get_debug_level() with upper case string argument."""
        self.assertEqual(logging.DEBUG, _main.get_logging_level_from('DEBUG'))
        self.assertEqual(logging.INFO, _main.get_logging_level_from('INFO'))

    def test_get_debug_level_invalid(self):
        """test get_debug_level() with invalid string argument."""
        self.assertEqual(logging.INFO, _main.get_logging_level_from('HOGE'))


if __name__ == "__main__":
    unittest.main(verbosity=2)
