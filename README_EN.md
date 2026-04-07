# Wave Propagation Foundation

> **English.** Korean (정본): [README.md](README.md)

| Item | Details |
|------|---------|
| Version | `v0.1.0` |
| Tests | `39 passed` |
| Deps | Runtime: **stdlib only** · Test: `pytest>=8.0` |
| Python | `>=3.10` |
| License | MIT |

---

## One-liner

**From Feynman Lectures Vol. 1 "Waves and Oscillations" — a unified foundation tracking every wave from Earth's seismic pulses to spacetime's gravitational ripples.**

---

## Five Layers

| Layer | Physics | Key Outputs |
|-------|---------|-------------|
| **L1 Wave Equation** | ∂²u/∂t² = c²∇²u | λ, k, ω, attenuation, energy flux |
| **L2 Oscillator** | Damped/forced SHO | Q-factor, resonance curve, decay time |
| **L3 Seismic** | P/S/Rayleigh/Love | Travel times, S-P delay, PGA, MMI, triangulation |
| **L4 Surface & Acoustic** | ω²=gk·tanh(kd), sound speed | Phase/group velocity, deep/shallow regime, impedance |
| **L5 Gravitational Wave** | Linearized GR, chirp mass | h₀ strain, SNR, ISCO freq, merger time, detectability |

---

## Quick Start

```python
from wave_propagation import screen_seismic, SeismicInput

r = screen_seismic(SeismicInput(magnitude=6.3, depth_km=15, station_count=5))
print(f"S-P delay: {r.sp_delay_s:.1f}s  PGA: {r.peak_ground_acceleration_g:.4f}g  MMI: {r.intensity_mmi}")
```

```python
from wave_propagation import screen_gravitational_wave, GravWaveInput

# GW150914 reproduction — use detector_sensitivity_strain=1e-22 (Advanced LIGO approx @ 35 Hz)
r = screen_gravitational_wave(GravWaveInput(
    m1_solar=36, m2_solar=29, distance_mpc=410,
    orbital_frequency_hz=35,
    detector_sensitivity_strain=1e-22,
))
print(f"Chirp mass: {r.chirp_mass_solar:.1f} M☉  Strain: {r.strain_amplitude:.2e}  SNR: {r.signal_to_noise:.1f}")
```

> `detector_sensitivity_strain` is a simplified single-number proxy. Real LIGO uses a frequency-dependent noise curve (ASD).

---

## Ecosystem Bridges

| Engine | Bridge | Role |
|--------|--------|------|
| FrequencyCore | `try_frequencycore_bridge()` | Seismic → spectral decomposition |
| Oceanus | `try_oceanus_bridge()` | Surface wave ↔ SWE |
| Eurus | `try_eurus_bridge()` | Atmospheric acoustic coupling |
| Optics | `try_optics_bridge()` | EM wave comparison |
| OrbitalCore | `try_orbitalcore_bridge()` | Gravity field → GW source |

All bridges degrade gracefully to `None`.

---

## License

MIT — [LICENSE](LICENSE)
