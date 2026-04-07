"""Wave Propagation Foundation — tests (v0.1.0)."""
from __future__ import annotations

import math

from wave_propagation import (
    WaveEquationInput, MediumType,
    OscillatorInput,
    SeismicInput, SeismicPhase,
    SurfaceAcousticInput,
    GravWaveInput, GravWaveSource,
    screen_wave_equation,
    screen_oscillator,
    screen_seismic,
    screen_surface_acoustic,
    screen_gravitational_wave,
    analyze,
    analyze_ecosystem_stack,
    try_frequencycore_bridge,
    try_oceanus_bridge,
    try_eurus_bridge,
    try_optics_bridge,
    try_orbitalcore_bridge,
)


# ═══════════════════════════════════════════════════════
# 1. Wave Equation
# ═══════════════════════════════════════════════════════

class TestWaveEquation:
    def test_default_sound(self):
        r = screen_wave_equation(WaveEquationInput())
        assert r.wavelength_m > 0
        assert r.period_s > 0
        assert abs(r.phase_velocity_m_s - 343.0) < 0.1
        assert 0 <= r.omega_wave <= 1

    def test_light_in_vacuum(self):
        r = screen_wave_equation(WaveEquationInput(
            wave_speed_m_s=3e8, frequency_hz=5e14, medium=MediumType.VACUUM,
        ))
        assert r.wavelength_m < 1e-6
        assert r.omega_wave > 0

    def test_attenuation(self):
        r = screen_wave_equation(WaveEquationInput(
            attenuation_np_per_m=0.01, propagation_distance_m=500,
        ))
        assert r.amplitude_at_distance < 1.0

    def test_solid_seismic_speed(self):
        r = screen_wave_equation(WaveEquationInput(
            wave_speed_m_s=6000, frequency_hz=1.0, medium=MediumType.SOLID,
        ))
        assert r.wavelength_m == 6000.0

    def test_vacuum_advisory(self):
        r = screen_wave_equation(WaveEquationInput(
            wave_speed_m_s=100, medium=MediumType.VACUUM,
        ))
        assert any("vacuum" in a.lower() for a in r.advisories)


# ═══════════════════════════════════════════════════════
# 2. Oscillator
# ═══════════════════════════════════════════════════════

class TestOscillator:
    def test_undamped(self):
        r = screen_oscillator(OscillatorInput(damping_ratio=0.0))
        assert r.q_factor == float("inf")
        assert r.decay_time_s == float("inf")

    def test_light_damping(self):
        r = screen_oscillator(OscillatorInput(damping_ratio=0.01))
        assert r.q_factor == 50.0
        assert r.decay_time_s > 0

    def test_critical_damping(self):
        r = screen_oscillator(OscillatorInput(damping_ratio=1.0))
        assert r.resonance_frequency_hz == 0.0

    def test_overdamped(self):
        r = screen_oscillator(OscillatorInput(damping_ratio=2.0))
        assert any("Overdamped" in a for a in r.advisories)

    def test_resonance(self):
        r = screen_oscillator(OscillatorInput(
            natural_frequency_hz=10.0, damping_ratio=0.05,
            driving_frequency_hz=10.0, driving_amplitude=1.0,
        ))
        assert r.is_resonant is True
        assert r.amplitude_ratio > 5.0

    def test_off_resonance(self):
        r = screen_oscillator(OscillatorInput(
            natural_frequency_hz=10.0, damping_ratio=0.1,
            driving_frequency_hz=1.0,
        ))
        assert r.is_resonant is False


# ═══════════════════════════════════════════════════════
# 3. Seismic
# ═══════════════════════════════════════════════════════

class TestSeismic:
    def test_moderate_earthquake(self):
        r = screen_seismic(SeismicInput(magnitude=5.0, depth_km=10, epicentral_distance_km=50))
        assert r.p_travel_time_s > 0
        assert r.s_travel_time_s > r.p_travel_time_s
        assert r.sp_delay_s > 0
        assert r.energy_joules > 0
        assert 0 <= r.omega_seismic <= 1

    def test_major_earthquake(self):
        r = screen_seismic(SeismicInput(magnitude=7.5))
        assert any("major" in a.lower() for a in r.advisories)
        assert r.peak_ground_acceleration_g > 0

    def test_shallow_focus(self):
        r = screen_seismic(SeismicInput(depth_km=2.0))
        assert any("Shallow" in a for a in r.advisories)

    def test_deep_focus(self):
        r = screen_seismic(SeismicInput(depth_km=500))
        assert any("Deep" in a for a in r.advisories)

    def test_triangulation(self):
        r = screen_seismic(SeismicInput(station_count=5))
        assert r.triangulation_possible is True

    def test_insufficient_stations(self):
        r = screen_seismic(SeismicInput(station_count=2))
        assert r.triangulation_possible is False

    def test_mmi_intensity(self):
        r = screen_seismic(SeismicInput(magnitude=6.0, epicentral_distance_km=20))
        assert r.intensity_mmi != ""

    def test_rayleigh_love_speeds(self):
        r = screen_seismic(SeismicInput())
        assert r.rayleigh_speed_km_s < r.love_speed_km_s


# ═══════════════════════════════════════════════════════
# 4. Surface & Acoustic
# ═══════════════════════════════════════════════════════

class TestSurfaceAcoustic:
    def test_deep_water(self):
        r = screen_surface_acoustic(SurfaceAcousticInput(water_depth_m=1000, wave_period_s=8))
        assert r.is_deep_water is True
        assert r.group_velocity_m_s < r.phase_velocity_m_s

    def test_shallow_water_tsunami(self):
        r = screen_surface_acoustic(SurfaceAcousticInput(
            water_depth_m=4000, wave_period_s=900, wave_height_m=0.5,
        ))
        assert r.is_shallow_water is True
        expected_c = math.sqrt(9.80665 * 4000)
        assert abs(r.phase_velocity_m_s - expected_c) / expected_c < 0.05

    def test_sound_in_air(self):
        r = screen_surface_acoustic(SurfaceAcousticInput(
            medium=MediumType.GAS, temperature_c=20,
        ))
        assert abs(r.sound_speed_m_s - 343.4) < 1.0

    def test_sound_in_water(self):
        r = screen_surface_acoustic(SurfaceAcousticInput(
            medium=MediumType.LIQUID, temperature_c=15,
        ))
        assert 1400 < r.sound_speed_m_s < 1600

    def test_wave_energy(self):
        r = screen_surface_acoustic(SurfaceAcousticInput(wave_height_m=3.0))
        assert r.wave_energy_j_m2 > 0


# ═══════════════════════════════════════════════════════
# 5. Gravitational Waves
# ═══════════════════════════════════════════════════════

class TestGravitationalWave:
    def test_binary_bh_gw150914(self):
        r = screen_gravitational_wave(GravWaveInput(
            m1_solar=36, m2_solar=29, distance_mpc=410,
            orbital_frequency_hz=35, detector_sensitivity_strain=1e-21,
        ))
        assert r.chirp_mass_solar > 20
        assert r.gw_frequency_hz == 70.0
        assert r.strain_amplitude > 0
        assert 0 <= r.omega_grav <= 1

    def test_binary_ns(self):
        r = screen_gravitational_wave(GravWaveInput(
            source=GravWaveSource.BINARY_NS,
            m1_solar=1.4, m2_solar=1.4, distance_mpc=40,
            orbital_frequency_hz=100,
        ))
        assert r.chirp_mass_solar < 2.0
        assert any("neutron star" in a.lower() for a in r.advisories)

    def test_far_source_undetectable(self):
        r = screen_gravitational_wave(GravWaveInput(
            distance_mpc=5000, m1_solar=10, m2_solar=10,
            orbital_frequency_hz=10,
        ))
        assert r.signal_to_noise < 1.0

    def test_isco_frequency(self):
        r = screen_gravitational_wave(GravWaveInput(m1_solar=30, m2_solar=30))
        assert r.isco_frequency_hz > 0


# ═══════════════════════════════════════════════════════
# 6. Foundation Integration
# ═══════════════════════════════════════════════════════

class TestFoundation:
    def test_seismic_only(self):
        r = analyze(seismic_input=SeismicInput())
        assert r.seismic is not None
        assert r.gravitational is None
        assert r.omega_overall > 0

    def test_grav_only(self):
        r = analyze(grav_input=GravWaveInput())
        assert r.gravitational is not None
        assert r.seismic is None

    def test_all_layers(self):
        r = analyze(
            wave_input=WaveEquationInput(),
            oscillator_input=OscillatorInput(),
            seismic_input=SeismicInput(),
            surface_input=SurfaceAcousticInput(),
            grav_input=GravWaveInput(),
        )
        assert r.wave_equation is not None
        assert r.oscillator is not None
        assert r.seismic is not None
        assert r.surface_acoustic is not None
        assert r.gravitational is not None
        assert len(r.evidence_tags) == 5
        assert 0 < r.omega_overall <= 1

    def test_empty(self):
        r = analyze()
        assert r.omega_overall == 0.0


# ═══════════════════════════════════════════════════════
# 7. Ecosystem Bridges
# ═══════════════════════════════════════════════════════

class TestEcosystemBridges:
    def test_frequencycore(self):
        out = try_frequencycore_bridge(SeismicInput())
        assert out is None or "dominant_frequency_hz" in out

    def test_oceanus(self):
        out = try_oceanus_bridge(SurfaceAcousticInput())
        assert out is None or "water_depth_m" in out

    def test_eurus(self):
        out = try_eurus_bridge()
        assert out is None or "planet" in out

    def test_optics(self):
        out = try_optics_bridge()
        assert out is None or "version" in out

    def test_orbitalcore(self):
        out = try_orbitalcore_bridge(GravWaveInput())
        assert out is None or "mu_earth" in out

    def test_stack_rollup(self):
        out = analyze_ecosystem_stack(
            seismic_input=SeismicInput(),
            surface_input=SurfaceAcousticInput(),
            grav_input=GravWaveInput(),
        )
        assert set(out.keys()) == {
            "frequencycore", "oceanus", "eurus", "optics", "orbitalcore",
        }


# ═══════════════════════════════════════════════════════
# 8. Integrity
# ═══════════════════════════════════════════════════════

class TestIntegrity:
    REQUIRED = [
        "wave_propagation/__init__.py",
        "wave_propagation/contracts.py",
        "wave_propagation/wave_equation.py",
        "wave_propagation/oscillator.py",
        "wave_propagation/seismic.py",
        "wave_propagation/surface_acoustic.py",
        "wave_propagation/gravitational_wave.py",
        "wave_propagation/foundation.py",
        "wave_propagation/ecosystem_bridges.py",
        "VERSION",
        "pyproject.toml",
    ]

    def test_files_exist(self):
        import os
        root = os.path.join(os.path.dirname(__file__), "..")
        for f in self.REQUIRED:
            assert os.path.isfile(os.path.join(root, f)), f"Missing: {f}"
