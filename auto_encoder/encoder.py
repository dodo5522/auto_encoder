#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import argparse
import glob
import os
import subprocess
import sys
from auto_encoder.base import ConvertError


def convert(path_source_file, path_dest_file, bitrate_video_mbps, bitrate_audio_kbps, deinterlace):
    """ Convert video file to the specified codecs.

    Args:
        path_source_file (str) : source video file
        path_dest_file (str) : destination video file converted
        bitrate_video_mbps (int) : video bitrate
        bitrate_audio_kbps (int) : audio bitrate
        deinterlace (bool) : enable deinterlace if True

    Returns:
        None
    """
    (base, ext) = os.path.splitext(os.path.basename(path_source_file))

    cmd = ["avconv"]
    cmd.extend(["-i", "{0}".format(path_source_file)])
    cmd.extend(["-c:v", "libx264"])
    cmd.extend(["-b:v", "{0}m".format(bitrate_video_mbps)])
    cmd.extend(["-s", "{0}".format("1280x720")])
    cmd.extend(["-b:a", "{0}k".format(bitrate_audio_kbps)])
    cmd.extend(["-c:a", "libvo_aacenc"])
    cmd.extend(["-ac", "2"])
    cmd.extend(["-aq", "100"])
    cmd.extend(["-threads", "4"])
    if deinterlace:
        cmd.extend(["-vf", "yadif"])
    cmd.append("{0}".format(path_dest_file))

    print("Converting: {0}...".format(" ".join(cmd)))
    subp = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    (stdout_data, stderr_data) = subp.communicate()

    if subp.returncode == 0:
        (base, ext) = os.path.splitext(path_source_file)

        with open(base + ".log", "w") as fplog:
            fplog.write(stderr_data.decode("utf-8"))

        raise ConvertError("Error with command \"{0}\" of {1}.".format(cmd, stderr_data))

def gen_src_dst_path(path_root_source="/symlinks/videos/tv", path_root_dest="/symlinks/videos/tv_converted"):
    """ generator to return source and destination file name tuple.

    Args:
        path_root_source (str) : 
        path_root_dest (str) : 

    Returns:
        None
    """
    found_keywords = [os.path.basename(keyword) for keyword \
            in glob.glob(os.path.join(path_root_dest, "*")) \
            if os.path.isdir(keyword)]

    for keyword in found_keywords:
        source_files = glob.glob(os.path.join(path_root_source, "*{0}*.m2ts".format(keyword)))

        for source_file in source_files:
            (base, ext) = os.path.splitext(os.path.basename(source_file))
            dest_file = os.path.join(path_root_dest, keyword, base + ".mp4")
            yield (source_file, dest_file)
