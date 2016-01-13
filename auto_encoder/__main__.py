#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from auto_encoder.encoder import convert
from auto_encoder.encoder import gen_src_dst_path
from auto_encoder.encoder import init_args


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
