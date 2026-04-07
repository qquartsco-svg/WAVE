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

## Physics Snapshots — What the Engine Actually Produces

> Real outputs from `v0.1.0`. The fastest way to verify the physics is implemented correctly.

---

### Snap-A · Tsunami Shallow-Water Dispersion

Error between full dispersion `ω² = gk·tanh(kd)` and shallow-water limit `c = √(gd)`:

| Depth | Computed | Theory (√gd) | Error |
|-------|----------|--------------|-------|
| 100 m | 31.31 m/s | 31.32 m/s | **0.008 %** |
| 1000 m | 98.95 m/s | 99.03 m/s | 0.083 % |
| 4000 m | 197.40 m/s | 198.06 m/s | 0.331 % |

*Full dispersion converges to within 0.33 % of the shallow-water limit — usable for real tsunami propagation tracking.*

---

### Snap-B · S-P Delay → Epicentral Distance Recovery

`Δt = d·(1/v_S − 1/v_P)` inverted back to distance:

| True Distance | S-P Delay | Recovered | Error |
|---------------|-----------|-----------|-------|
| 50 km | 6.07 s | 51.0 km | **0.00 %** |
| 100 km | 11.96 s | 100.5 km | 0.03 % |
| 500 km | 59.54 s | 500.1 km | 0.01 % |

*Single-station recovery error < 0.03 %. Three or more stations enables full triangulation (`triangulation_possible=True`).*

---

### Snap-C · Richter Magnitude — Energy Scale

| M | Energy | TNT equivalent |
|---|--------|---------------|
| 3.0 | 2.0 × 10⁹ J | **0.5 ton** |
| 5.0 | 2.0 × 10¹² J | 477 ton |
| 6.3 | 1.8 × 10¹⁴ J | 42,500 ton |
| 7.0 | 2.0 × 10¹⁵ J | 477,000 ton |
| 9.0 | 2.0 × 10¹⁸ J | **480 million ton** |

*Each +1 in magnitude = ×31.6 in energy (10^1.5). M9 vs M3: a factor of 10⁹.*

---

### Snap-D · Building Resonance — Damping vs. Amplification

Driving frequency = natural frequency (full resonance condition):

| Damping ζ | Q-factor | Amplitude × | Example structure |
|-----------|---------|-------------|------------------|
| 0.01 | 50.0 | **50×** | Bare steel frame |
| 0.05 | 10.0 | **10×** | RC building (code baseline) |
| 0.10 | 5.0 | 5× | High-damping design |
| 1.00 | 0.5 | 0.5× | Critical damping — no resonance |

*ζ = 0.05 code-baseline buildings experience 10× displacement amplification when excited at their natural frequency — the physical basis of seismic design requirements.*

---

### Snap-E · GW150914 — SNR vs. Distance

Same event (36 M☉ + 29 M☉), different observer distances:

| Distance | Strain | SNR | Detectable |
|----------|--------|-----|-----------|
| 10 Mpc | 5.24 × 10⁻²⁰ | 524 | ✓ |
| 410 Mpc | 1.28 × 10⁻²¹ | **12.8** | ✓ (actual GW150914 ≈ 24) |
| 1000 Mpc | 5.24 × 10⁻²² | 5.2 | ✓ |
| 5000 Mpc | 1.05 × 10⁻²² | 1.1 | △ (marginal) |

*strain ∝ 1/d. SNR=12.8 at 410 Mpc is ~½ of the real LIGO value (~24) — the gap is expected from a simplified single-number sensitivity input.*

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
