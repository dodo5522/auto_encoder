#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import unittest
from auto_encoder import encoder
from auto_encoder.base import ConvertError
from minimock import mock, Mock, restore


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
        mock('encoder.subprocess.Popen', returns=Mock(
            'proc',
            communicate=Mock(
                'proc.communicate',
                returns=(b'', b'')),
            returncode=0))

        encoder.encode('aaa.m2ts', 'bbb.mp4', reso='1280x720', vb_mbps=2, ab_kbps=256, is_deint=False)

    def test_encode_failed_returncode_1(self):
        """encode test with failed"""
        mock('encoder.subprocess.Popen', returns=Mock(
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

        mock('encoder.glob.glob', returns=['/aaa/bbb/ccc', '/aaa/bbb/ddd'])
        mock('encoder.os.path.isdir', returns=True)

        keywords = encoder.get_keywords('/aaa/bbb')

        self.assertEqual(set(('ccc', 'ddd')), set(keywords))

    def test_get_keywords_empty(self):
        """get_keywords empty test"""

        mock('encoder.glob.glob', returns=[''])
        mock('encoder.os.path.isdir', returns=False)

        keywords = encoder.get_keywords('/aaa/bbb')

        self.assertEqual(0, len(keywords))

    def test_get_src_dst_with_files(self):
        """get_src_dst() test with files directly"""
        mock('encoder.os.path.isfile', returns=True)

        dummy_src_file = 'aaa.m2ts'
        dummy_dst_file = 'aaa.mp4'
        for src, dst in encoder.gen_src_dst(dummy_src_file, dummy_dst_file, src_ext='m2ts', dst_ext='mp4'):
            self.assertEqual(dummy_src_file, src)
            self.assertEqual(dummy_dst_file, dst)

    def test_get_src_dst_with_dirs(self):
        """get_src_dst() test with files read from direcotry"""
        dummy_src_root = '/sym/videos/raw'
        dummy_dst_root = '/sym/videos/converted'

        dummy_src_file = os.path.join(dummy_src_root, '[151210]温泉の旅.m2ts')
        dummy_keyword = '温泉'

        mock('encoder.os.path.isfile', returns=False)
        mock('encoder.get_keywords', returns=(dummy_keyword,))
        mock('encoder.glob.glob', returns=(dummy_src_file,))

        for src, dst in encoder.gen_src_dst(dummy_src_root, dummy_dst_root, src_ext='m2ts', dst_ext='mp4'):
            self.assertEqual(dummy_src_file, src)
            self.assertEqual(
                os.path.join(
                    dummy_dst_root, dummy_keyword,
                    os.path.splitext(os.path.basename(dummy_src_file))[0] + '.mp4'), dst)


if __name__ == "__main__":
    unittest.main(verbosity=2)
