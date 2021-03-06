def test_detector_atributes(beamline):
    assert not beamline.detector is None, "Detector hardware objects is None (not initialized)"
    current_distance = beamline.detector.get_distance()
    distance_limits = beamline.detector.get_distance_limits()
    exp_time_limits = beamline.detector.get_exposure_time_limits()
    has_shutterless = beamline.detector.has_shutterless()

    assert isinstance(current_distance, float), "Distance value has to be int or float. Now %s" % str(current_distance)
    assert isinstance(distance_limits, (list, tuple)), "Distance limits has to be defined as a tuple or list"
    assert not None in distance_limits, "One or several distance limits is None"
    assert distance_limits[0] < distance_limits[1], "First value of distance limits has to be the low limit"

def test_detector_methods(beamline):
    target = 600
    beamline.detector.set_distance(target)
    assert beamline.detector.get_distance() == target
