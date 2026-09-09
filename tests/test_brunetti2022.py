from ots_brunetti2022 import Brunetti2022Model
import numpy as np


def test_brunetti_step_has_delayed_mobile_population():
    response = Brunetti2022Model().simulate_step(2.4, stop_time_s=5e-9)
    assert response.current_a[-1] > response.current_a[0] * 10.0
    assert response.mobile_fraction[-1] > response.mobile_fraction[0]
    assert response.carrier_temperature_k[-1] > response.carrier_temperature_k[0]


def test_triangle_sweep_has_threshold_hysteresis():
    source, response = Brunetti2022Model().simulate_triangle(points=1200)
    midpoint = len(source) // 2
    up_current = response.current_a[:midpoint]
    down_current = response.current_a[midpoint:]
    up_voltage = source[:midpoint]
    down_voltage = source[midpoint:]
    up_slope = np.gradient(np.log10(np.maximum(up_current, 1e-30)), up_voltage)
    down_slope = np.gradient(np.log10(np.maximum(down_current, 1e-30)), down_voltage)
    up_valid = np.flatnonzero(up_current > 1e-6)
    down_valid = np.flatnonzero(down_current > 1e-6)
    vth = up_voltage[up_valid[np.argmax(np.abs(up_slope[up_valid]))]]
    vhold = down_voltage[down_valid[np.argmax(np.abs(down_slope[down_valid]))]]
    assert vth > vhold + 0.5
