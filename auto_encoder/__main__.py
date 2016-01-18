#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import argparse
import logging
import os
import sys
from auto_encoder.encoder import encode
from auto_encoder.encoder import gen_src_dst


def init_args(args=sys.argv[1:]):
    """Get the parsed argument object.

    Args:
        args: list of arguments
    Returns:
        Parsed argument object.
    Raises:
        None
    """
    parser = argparse.ArgumentParser(
        description="Convert ts files to mp4 files with avconv as default.")

    parser.add_argument(
        "-s", "--source",
        action="store",
        default='/symlinks/videos/tv',
        type=str,
        help="source file or root directory path to converting")
    parser.add_argument(
        "-d", "--dest",
        action="store",
        default='/symlinks/videos/tv_converted',
        type=str,
        help="destination file or directory path to be converted")
    parser.add_argument(
        "-vb", "--video-bitrate",
        action="store",
        default=1,
        type=int,
        help="video bitrate as mbps")
    parser.add_argument(
        "-ab", "--audio-bitrate",
        action="store",
        default=256,
        type=int,
        help="audio bitrate as kbps")
    parser.add_argument(
        "--deinterlace",
        action="store_true",
        default=False,
        help="enable deinterlace")
    parser.add_argument(
        "--level",
        action="store",
        default="info",
        help="debug level")

    return parser.parse_args(args)


def get_logging_level_from(level):
    '''Return debug level according to logging module.

    Args:
        level: level string like 'DEBUG'
    Returns:
        logging.DEBUG, logging.INFO, or something
    '''
    return getattr(logging, level.upper()) if hasattr(logging, level.upper()) else logging.INFO


def main(args):
    """ main routine.
    """
    logging.basicConfig(
        level=get_logging_level_from(args.level),
        format='%(asctime)s-%(levelname)s: %(message)s')

    for (source_file, dest_file) in gen_src_dst(args.source, args.dest):
        try:
            encode(
                source_file, dest_file,
                reso='1280x720', vb_mbps=args.video_bitrate, ab_kbps=args.audio_bitrate,
                is_deint=args.deinterlace)
        except Exception:
            if os.path.isfile(dest_file):
                os.remove(dest_file)
            continue
        else:
            os.remove(source_file)


if __name__ == '__main__':
    main(init_args())
