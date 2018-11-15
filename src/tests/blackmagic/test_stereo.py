import time
from pytest import mark
from utils import (StereoFrameConsistencyChecker,
                   StereoFrameNumpyCompatibilityChecker,
                   StereoFrameBackwardsCompatibilityChecker)
import pygiftgrab as pgg


@mark.stereo_frames
def test_stereo_frames(device, colour_space):
    factory = pgg.VideoSourceFactory.get_instance()
    source = factory.get_device(device, colour_space)
    consistency_checker = StereoFrameConsistencyChecker()
    numpy_checker = StereoFrameNumpyCompatibilityChecker(colour_space)
    backwards_compatibility_checker = StereoFrameBackwardsCompatibilityChecker()

    source.attach(consistency_checker)
    source.attach(numpy_checker)
    source.attach(backwards_compatibility_checker)

    time.sleep(15)

    source.detach(consistency_checker)
    source.detach(numpy_checker)
    source.detach(backwards_compatibility_checker)

    assert consistency_checker
    assert numpy_checker