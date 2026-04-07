"""
Layer 5 — Gravitational Waves (중력파)
=======================================

아인슈타인 일반상대론의 선형화:

  h_μν = (2G/c⁴) · (1/r) · Ï̈_TT

쌍성계 중력파:

  Chirp mass: M_c = (m₁m₂)^(3/5) / (m₁+m₂)^(1/5)

  주파수: f_gw = 2·f_orbital

  Strain: h₀ = (4/c⁴)·(G·M_c)^(5/3)·(π·f_gw)^(2/3) / d

  광도: L_gw = (32/5)·(G⁴/c⁵)·(M_c)^(10/3)·(π·f_gw)^(10/3)

  ISCO 주파수: f_isco = c³/(6^(3/2)·π·G·M_total)

  병합 시간 (Peters, 1964):
    τ ∝ (M_c)^(-5/3) · f_gw^(-8/3)

검출기 감도:
  LIGO:   ~10⁻²³ strain @ 100 Hz
  LISA:   ~10⁻²⁰ strain @ 10⁻³ Hz
  ET:     ~10⁻²⁵ strain @ 10 Hz

우주로 나가면 중력파 = 시공간의 파동.
파인만이 말한 "모든 것은 진동" — 시공간 자체도.
"""
from __future__ import annotations

import math
from typing import List

from .contracts import (
    G_NEWTON, C_LIGHT, M_SUN, PI,
    GravWaveInput,
    GravWaveResult,
    GravWaveSource,
)


def screen_gravitational_wave(inp: GravWaveInput) -> GravWaveResult:
    """중력파 스크리닝."""
    advisories: List[str] = []

    m1 = inp.m1_solar * M_SUN
    m2 = inp.m2_solar * M_SUN
    M_total = m1 + m2

    chirp_kg = (m1 * m2) ** 0.6 / M_total ** 0.2
    chirp_solar = chirp_kg / M_SUN

    f_gw = 2.0 * inp.orbital_frequency_hz
    d_m = inp.distance_mpc * 3.086e22

    G = G_NEWTON
    c = C_LIGHT

    # h₀ = (4/c⁴)·(G·Mc)^(5/3)·(π·f_gw)^(2/3) / d
    if d_m > 0 and f_gw > 0:
        gmc_53 = (G * chirp_kg) ** (5.0 / 3.0)
        pif_23 = (PI * f_gw) ** (2.0 / 3.0)
        strain = (4.0 / c ** 4) * gmc_53 * pif_23 / d_m
    else:
        strain = 0.0

    # L_gw = (32/5)·(G⁴/c⁵)·Mc^(10/3)·(π·f_gw)^(10/3)
    if f_gw > 0:
        luminosity = (32.0 / 5.0) * (G ** 4 / c ** 5) * chirp_kg ** (10.0 / 3.0) * (PI * f_gw) ** (10.0 / 3.0)
    else:
        luminosity = 0.0

    # ISCO frequency
    if M_total > 0:
        f_isco = c ** 3 / (6 ** 1.5 * PI * G * M_total)
    else:
        f_isco = 0.0

    # Merger time (Peters formula simplified)
    if chirp_kg > 0 and f_gw > 0:
        tau = (5.0 / 256.0) * (c ** 5 / (G ** (5.0 / 3.0))) * chirp_kg ** (-5.0 / 3.0) * (PI * f_gw) ** (-8.0 / 3.0)
    else:
        tau = float("inf")

    detectable = strain > inp.detector_sensitivity_strain
    snr = strain / inp.detector_sensitivity_strain if inp.detector_sensitivity_strain > 0 else 0.0

    if detectable:
        advisories.append(f"Detectable! SNR≈{snr:.1f} — strain {strain:.2e} > sensitivity {inp.detector_sensitivity_strain:.2e}.")
    else:
        advisories.append(f"Below detection threshold: strain {strain:.2e} < {inp.detector_sensitivity_strain:.2e}.")

    if inp.source == GravWaveSource.BINARY_BH:
        advisories.append(f"Binary black hole: chirp mass={chirp_solar:.1f} M☉, ISCO at {f_isco:.1f} Hz.")
    elif inp.source == GravWaveSource.BINARY_NS:
        advisories.append(f"Binary neutron star: chirp mass={chirp_solar:.2f} M☉ — EM counterpart expected.")

    if f_gw > f_isco:
        advisories.append("GW frequency exceeds ISCO — system may have already merged.")

    if tau < 1.0:
        advisories.append(f"Merger imminent: τ≈{tau:.3f} s.")
    elif tau < 3.156e7:
        advisories.append(f"Merger in τ≈{tau/3600:.1f} hours.")

    score = 0.0
    if detectable:
        score += 0.35
    score += 0.20 * min(snr / 10.0, 1.0)
    score += 0.15 * min(chirp_solar / 50.0, 1.0)
    if f_gw <= f_isco and f_gw > 0:
        score += 0.15
    score += 0.15 * (1.0 - min(len(advisories) / 4, 1.0))
    score = round(max(0.0, min(1.0, score)), 4)

    return GravWaveResult(
        chirp_mass_solar=round(chirp_solar, 4),
        chirp_mass_kg=round(chirp_kg, 4),
        gw_frequency_hz=round(f_gw, 6),
        strain_amplitude=strain,
        luminosity_w=luminosity,
        detectable=detectable,
        signal_to_noise=round(snr, 2),
        isco_frequency_hz=round(f_isco, 4),
        merger_time_estimate_s=round(tau, 4) if tau < 1e20 else float("inf"),
        omega_grav=score,
        advisories=advisories,
    )
