#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from auto_encoder.encoder import convert
from auto_encoder.encoder import gen_src_dst_path
from auto_encoder.encoder import init_args


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
        "-s", "--source-file",\
        action="store",\
        default=None,\
        type=str,\
        help="source file path to converting")
    parser.add_argument(
        "-d", "--dest-file",\
        action="store",\
        default=None,\
        type=str,\
        help="destination file path to be converted")
    parser.add_argument(
        "-vb", "--video-bitrate",\
        action="store",\
        default=1,\
        type=int,\
        help="video bitrate as mbps")
    parser.add_argument(
        "-ab", "--audio-bitrate",\
        action="store",\
        default=256,\
        type=int,\
        help="audio bitrate as kbps")
    parser.add_argument(
        "--deinterlace",\
        action="store_true",\
        default=False,\
        help="enable deinterlace")

    return parser.parse_args(args)


def main():
    """ main routine.
    """
    args = init_args()

    if args.source_file and args.dest_file:
        convert(
            args.source_file, args.dest_file,
            args.video_bitrate, args.audio_bitrate,
            args.deinterlace)
    else:
        for (source_file, dest_file) in gen_src_dst_path():
            try:
                convert(
                    source_file, dest_file,
                    args.video_bitrate, args.audio_bitrate,
                    args.deinterlace)
            except Exception:
                if os.path.isfile(dest_file):
                    os.remove(dest_file)
                continue
            else:
                os.remove(args.source_file)


main()
