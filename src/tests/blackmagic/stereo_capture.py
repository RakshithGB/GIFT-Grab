#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Example demonstrating how stereo video frames can be captured
using a frame grabber card that supports this feature.
"""

import time
import cv2
import numpy as np
from pygiftgrab import (IObserver, VideoSourceFactory,
                        ColourSpace, Device, VideoFrame)


class StereoFrameSaver(IObserver):
    """
    Simple class that demonstrates how mono and stereo frames,
    and their respective parameters can be queried and the actual
    frame data can be saved using the GIFT-Grab stereo API.
    """

    def __init__(self):
        super(StereoFrameSaver, self).__init__()
        self.current = 0

    def update(self, frame):
        self.current += 1

        # 4 is the number of variations of stereo/mono
        # calls to the data method, using it here as well to
        # avoid flooding the user's terminal
        if self.current <= 4:
            # display number of stereo frames, should be 2
            # for this device
            print(
                'Got {} stereo frames'.format(
                    frame.stereo_count()
                )
            )
            # display length of data of each stereo frame,
            # each stereo frame should consist of same number
            # of bytes for this device
            print(
                'Stereo data length (bytes):\n'
                '\tdata_length(): {}\n'
                '\tdata_length(0): {}\n'
                '\tdata_length(1): {}\n'.format(
                    frame.data_length(), frame.data_length(0),
                    frame.data_length(1)
                )
            )

        frame_shape = (frame.rows(), frame.cols(), 4)

        # the slicing below, i.e. [:, :, :3], is due to OpenCV's
        # imwrite expecting BGR data, so we strip out the alpha
        # channel of each frame when saving it

        if self.current == 1:
            # all three calls below save the same frame,
            # that is the first of the two stereo frames
            cv2.imwrite(
                'mono-frame.data.png',
                np.reshape(frame.data(), frame_shape)[:, :, :3]
            )
            cv2.imwrite(
                'mono-frame.data-False.png',
                np.reshape(frame.data(False), frame_shape)[:, :, :3]
            )
            cv2.imwrite(
                'mono-frame.data-False-0.png',
                np.reshape(frame.data(False, 0), frame_shape)[:, :, :3]
            )

        elif self.current == 2:
            # the two calls below save the two stereo frames,
            # however the data needs to be reshaped, as the
            # call to the data method yields a flat NumPy array
            cv2.imwrite(
                'stereo-frame.data-False-0.png',
                np.reshape(frame.data(False, 0), frame_shape)[:, :, :3]
            )
            cv2.imwrite(
                'stereo-frame.data-False-1.png',
                np.reshape(frame.data(False, 1), frame_shape)[:, :, :3]
            )

        elif self.current == 3:
            # the two calls below save the two stereo frames,
            # without the need for reshaping the data, as the
            # call to the data method already yields a
            # structured NumPy array
            cv2.imwrite(
                'mono-frame.data-True.png',
                frame.data(True)[:, :, :3]
            )
            cv2.imwrite(
                'mono-frame.data-True-0.png',
                frame.data(True, 0)[:, :, :3]
            )

        elif self.current == 4:
            # the two calls below save the two stereo frames,
            # without the need for reshaping the data, as the
            # call to the data method already yields a
            # structured NumPy array
            cv2.imwrite(
                'stereo-frame.data-True-0.png',
                frame.data(True, 0)[:, :, :3]
            )
            cv2.imwrite(
                'stereo-frame.data-True-1.png',
                frame.data(True, 1)[:, :, :3]
            )


if __name__ == '__main__':
    sfac = VideoSourceFactory.get_instance()
    source = sfac.get_device(
        Device.DeckLink4KExtreme12G, ColourSpace.BGRA
    )

    saver = StereoFrameSaver()

    source.attach(saver)

    time.sleep(2)  # operate pipeline for 2 sec

    source.detach(saver)
