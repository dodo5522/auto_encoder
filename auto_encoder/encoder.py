#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import glob
import logging
import os
import subprocess
from auto_encoder.base import ConvertError


def encode(src, dst, reso='1280x720', vb_mbps=2, ab_kbps=256, is_deint=False):
    """Encode video file with the specified settings.

    Args:
        src: source video file path
        dst: destination video file path
        reso: resolution like '1280x720'
        vb_mbps: video bitrate as integer
        ab_kbps: audio bitrate as integer
        is_deint: enable deinterlace if True
    Returns:
        None
    Raises:
        ConvertError if avconv command failed
    """
    (base, ext) = os.path.splitext(os.path.basename(src))

    cmd = ['avconv']
    cmd.extend(['-i', src])
    cmd.extend(['-c:v', 'libx264'])
    cmd.extend(['-b:v', '{}m'.format(vb_mbps)])
    cmd.extend(['-s', reso])
    cmd.extend(['-b:a', '{}k'.format(ab_kbps)])
    cmd.extend(['-c:a', 'libvo_aacenc'])
    cmd.extend(['-ac', '2'])
    cmd.extend(['-aq', '100'])
    cmd.extend(['-threads', '4'])
    if is_deint:
        cmd.extend(['-vf', 'yadif'])
    cmd.append(dst)

    logging.info(' '.join(cmd))

    subp = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE)

    (stdout_data, stderr_data) = subp.communicate()

    if subp.returncode:
        with open(os.path.splitext(src)[0] + '.log', 'w') as fp:
            fp.write(stderr_data.decode())

        logging.error('Convert failed with ' + stderr_data.decode())
        raise ConvertError(stderr_data.decode())


def get_keywords(root_dir):
    """Get keywords for media files to be encoded.
       This function tries to find directory names in specified root dir.
       The directory names are the keywords.

    Args:
        root_dir: root path string to find keyword
    Returns:
        list of keywords
    Raises:
        None
    """
    return [os.path.basename(keyword) for keyword in glob.glob(os.path.join(root_dir, "*")) if os.path.isdir(keyword)]


def gen_src_dst(root_src, root_dst, src_ext='m2ts', dst_ext='mp4'):
    """Generator to return source and destination file name tuple.

    Args:
        root_src: root directory of source files, or a source file
        root_dst: root directory of destination having child directories of keyword, or a dest file
        src_ext: source file's extention string like 'm2ts'
        dst_ext: destination file's extention string like 'mp4'
    Returns:
        None
    Raises:
        None
    """
    if os.path.isfile(root_src) or os.path.isfile(root_dst):
        yield (root_src, root_dst)
    else:
        for keyword in get_keywords(root_dst):
            src_files = glob.glob(
                os.path.join(root_src, '*{}*.{}'.format(keyword, src_ext)))

            for src_file in src_files:
                (base, ext) = os.path.splitext(os.path.basename(src_file))
                dst_file = os.path.join(root_dst, keyword, base + '.' + dst_ext)
                yield (src_file, dst_file)
