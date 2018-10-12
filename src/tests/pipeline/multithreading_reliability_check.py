#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os.path
from pygiftgrab import (VideoSourceFactory,
                        ColourSpace,
                        IObservableObserver)

"""
This script provides a multi-threading reliability check.
The background is issue #16. It looks like in applications
where multiple Python threads are involved, occasionally
the acquisition of the Global Interpreter Lock leads to a
deadlocks, which crashes the whole application with a
non-specific segmentation fault.

In this script we run a number of multi-threaded GIFT-Grab
pipelines, which should serve as a validation that this
problem is fixed.
"""


class Dyer(IObservableObserver):

    def __init__(self, channel, value):
        super(Dyer, self).__init__()
        assert 0 <= channel < 3
        assert 0 <= value < 256
        self.channel = channel
        self.value = value

    def update(self, frame):
        data = frame.data(True)
        data[:, :, self.channel] = self.value


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True,
                        metavar='VIDEO_FILE',
                        help='Input video file (HEVC-encoded MP4)')
    args = parser.parse_args()
    in_file = args.input

    filename = os.path.basename(in_file)
    filename, ext = os.path.splitext(filename)
    assert filename
    assert ext == '.mp4'