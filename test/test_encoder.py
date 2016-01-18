#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import unittest
from auto_encoder import encoder
from auto_encoder.base import ConvertError
from minimock import Mock, restore


class TestEncoder(unittest.TestCase):
    """Test case for encoder function."""

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
        restore()

    def test_encode_success(self):
        """encode test with succeeded"""
        encoder.subprocess.Popen = Mock(
            'encoder.subprocess.Popen',
            returns=Mock(
                'proc',
                communicate=Mock(
                    'proc.communicate',
                    returns=(b'', b'')),
                returncode=0))

        encoder.encode('aaa.m2ts', 'bbb.mp4', reso='1280x720', vb_mbps=2, ab_kbps=256, is_deint=False)

    def test_encode_failed_returncode_1(self):
        """encode test with failed"""
        encoder.subprocess.Popen = Mock(
            'encoder.subprocess.Popen',
            returns=Mock(
                'proc',
                communicate=Mock(
                    'proc.communicate',
                    returns=(b'', b'')),
                returncode=1))

        dummy_src_file = 'aaa.m2ts'
        args = (dummy_src_file, 'bbb.mp4')
        kwargs = {'reso': '1280x720', 'vb_mbps': 2, 'ab_kbps': 256, 'is_deint': False}

        self.assertRaises(ConvertError, encoder.encode, *args, **kwargs)
        self.assertTrue(os.path.isfile(os.path.splitext(dummy_src_file)[0] + '.log'))

        os.remove(os.path.splitext(dummy_src_file)[0] + '.log')

    def test_get_keywords_valid(self):
        """get_keywords valid test"""

        encoder.glob.glob = Mock(
            'encoder.glob.glob',
            returns=['/aaa/bbb/ccc', '/aaa/bbb/ddd'])

        encoder.os.path.isdir = Mock(
            'encoder.os.path.isdir',
            returns=True)

        keywords = encoder.get_keywords('/aaa/bbb')

        self.assertEqual(set(('ccc', 'ddd')), set(keywords))

    def test_get_keywords_empty(self):
        """get_keywords empty test"""

        encoder.glob.glob = Mock(
            'encoder.glob.glob',
            returns=[''])

        encoder.os.path.isdir = Mock(
            'encoder.os.path.isdir',
            returns=False)

        keywords = encoder.get_keywords('/aaa/bbb')

        self.assertEqual(0, len(keywords))

    def test_get_src_dst_(self):
        """get_keywords test"""
        #gen_src_dst(root_src, root_dst, src_ext='m2ts', dst_ext='mp4'):
        pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
