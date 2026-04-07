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

## Physics Snapshots — Values Derived from Dynamic Flow

> Outputs from `v0.1.0`.  
> These numbers reflect **internal flow consistency within the model** — not empirical ground-truth validation. Real-world comparison requires a separate observational calibration step.

---

### Snap-A · Tsunami — Dispersion Flow Convergence

Difference between the full dispersion relation `ω² = gk·tanh(kd)` and the shallow-water approximation `c = √(gd)` as a function of depth.

| Depth | Dispersion flow | Shallow approx (√gd) | Difference |
|-------|----------------|----------------------|-----------|
| 100 m | 31.31 m/s | 31.32 m/s | 0.008 % |
| 1000 m | 98.95 m/s | 99.03 m/s | 0.083 % |
| 4000 m | 197.40 m/s | 198.06 m/s | 0.331 % |

*Both flows converge to within 0.33 % in shallow-water conditions — internal flow consistency confirmed. Actual seafloor geometry and tidal effects are not included.*

---

### Snap-B · S-P Delay → Distance Inversion Flow

Forward flow `Δt = d·(1/v_S − 1/v_P)`, then inverted — how well does the round-trip close within the model?

| Input distance | S-P delay | Inverted | Round-trip deviation |
|----------------|-----------|----------|---------------------|
| 50 km | 6.07 s | 51.0 km | 0.00 % |
| 100 km | 11.96 s | 100.5 km | 0.03 % |
| 500 km | 59.54 s | 500.1 km | 0.01 % |

*Self-consistency of forward/inverse flow within a 1D homogeneous crust model. Real crust heterogeneity, anisotropy, and velocity gradients will introduce additional deviation.*

---

### Snap-C · Magnitude–Energy Flow — Gutenberg-Richter

Values derived from the empirical flow `E = 10^(1.5M + 4.8)`.

| M | Derived energy | TNT equivalent |
|---|----------------|---------------|
| 3.0 | 2.0 × 10⁹ J | ~0.5 ton |
| 5.0 | 2.0 × 10¹² J | ~477 ton |
| 6.3 | 1.8 × 10¹⁴ J | ~42,500 ton |
| 7.0 | 2.0 × 10¹⁵ J | ~477,000 ton |
| 9.0 | 2.0 × 10¹⁸ J | ~480 million ton |

*Each +1 magnitude = ×31.6 in energy flow (10^1.5). This is an empirical regression relation — actual radiated energy varies by event.*

---

### Snap-D · Oscillator Resonance — Damping vs. Amplitude Flow

Single-DOF harmonic oscillator at driving frequency = natural frequency.

| Damping ζ | Q-factor | Amplitude × | Reference structure |
|-----------|---------|-------------|---------------------|
| 0.01 | 50.0 | ~50× | Low-damping steel frame |
| 0.05 | 10.0 | ~10× | RC building (typical design range) |
| 0.10 | 5.0 | ~5× | High-damping design |
| 1.00 | 0.5 | ~0.5× | Critically damped — no resonance flow |

*Idealized single-DOF linear flow. Real structures are multi-DOF with nonlinear, frequency-dependent damping.*

---

### Snap-E · Gravitational Wave — strain/SNR Distance Flow

`h₀ ∝ 1/d` flow from linearized GR; simplified single-number SNR.  
Parameters: M₁=36 M☉, M₂=29 M☉, f=35 Hz, sensitivity proxy=1e-22.

| Distance | Derived strain | Flow SNR | Note |
|----------|---------------|---------|------|
| 10 Mpc | 5.24 × 10⁻²⁰ | 524 | — |
| 410 Mpc | 1.28 × 10⁻²¹ | 12.8 | GW150914 measured ≈ 24 |
| 1000 Mpc | 5.24 × 10⁻²² | 5.2 | — |
| 5000 Mpc | 1.05 × 10⁻²² | 1.1 | near threshold |

*strain ∝ 1/d is a linearized GR approximation. The SNR gap vs. the real GW150914 detection (~24) is expected: real LIGO uses a frequency-dependent noise curve (ASD), not a single-number proxy.*

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
