"""
Layer 3 — Seismic Waves (지진파 추적)
======================================

지구 내부를 통과하는 탄성파.

P파 (Primary, 종파):
  v_p = √((K + 4G/3) / ρ)     ~6 km/s in upper crust
  모든 매질(고체, 액체) 통과

S파 (Secondary, 횡파):
  v_s = √(G / ρ)              ~3.5 km/s
  고체만 통과 (외핵에서 소멸 → 지구 내부 구조 증거)

표면파:
  Rayleigh파 ≈ 0.92 × v_s     지표면 타원 운동
  Love파 ≈ v_s ~ v_p 사이       SH 편파 (수평 전단)

진앙 추적 (삼각측량):
  Δt = t_S - t_P = d × (1/v_s - 1/v_p)
  d = Δt / (1/v_s - 1/v_p)

규모-에너지:
  log₁₀(E) = 1.5M + 4.8       (Gutenberg-Richter)
  M₀ = 10^(1.5M + 9.1)        지진 모멘트 (N·m)

PGA (Peak Ground Acceleration):
  Boore-Atkinson 유사 proxy:
  log₁₀(PGA) ≈ a·M - b·log₁₀(R) - c·R + d
"""
from __future__ import annotations

import math
from typing import List

from .contracts import (
    G_EARTH,
    SeismicInput,
    SeismicResult,
)


def _pga_proxy(mag: float, dist_km: float, depth_km: float, site_amp: float) -> float:
    """Simplified PGA proxy (g units) inspired by NGA-West2 functional form."""
    if dist_km <= 0:
        dist_km = 0.1
    r_hypo = math.sqrt(dist_km ** 2 + depth_km ** 2)
    log_pga = 0.55 * mag - 1.2 * math.log10(r_hypo) - 0.003 * r_hypo - 1.5
    pga_g = 10 ** log_pga * site_amp
    return max(pga_g, 0.0)


def _mmi_from_pga(pga_g: float) -> str:
    """PGA (g) → Modified Mercalli Intensity (approximate)."""
    pga_gal = pga_g * 980.665
    if pga_gal < 0.17:
        return "I"
    if pga_gal < 1.4:
        return "II-III"
    if pga_gal < 3.9:
        return "IV"
    if pga_gal < 9.2:
        return "V"
    if pga_gal < 18.0:
        return "VI"
    if pga_gal < 34.0:
        return "VII"
    if pga_gal < 65.0:
        return "VIII"
    if pga_gal < 124.0:
        return "IX"
    return "X+"


def screen_seismic(inp: SeismicInput) -> SeismicResult:
    """지진파 추적 스크리닝."""
    advisories: List[str] = []

    vp = max(inp.vp_km_s, 0.1)
    vs = max(inp.vs_km_s, 0.1)
    dist = max(inp.epicentral_distance_km, 0.01)

    r_hypo = math.sqrt(dist ** 2 + inp.depth_km ** 2)
    t_p = r_hypo / vp
    t_s = r_hypo / vs
    sp_delay = t_s - t_p

    rayleigh_speed = 0.92 * vs
    love_speed = (vs + vp) / 2.0

    pga = _pga_proxy(inp.magnitude, dist, inp.depth_km, inp.site_amplification)
    mmi = _mmi_from_pga(pga)

    seismic_moment = 10 ** (1.5 * inp.magnitude + 9.1)
    energy_j = 10 ** (1.5 * inp.magnitude + 4.8)

    triangulation = inp.station_count >= 3

    if inp.magnitude >= 7.0:
        advisories.append(f"M{inp.magnitude:.1f} — major earthquake. Widespread damage likely.")
    elif inp.magnitude >= 5.0:
        advisories.append(f"M{inp.magnitude:.1f} — moderate earthquake. Damage near epicenter.")
    elif inp.magnitude >= 3.0:
        advisories.append(f"M{inp.magnitude:.1f} — minor earthquake. Felt by people.")

    if inp.depth_km < 5:
        advisories.append(f"Shallow focus ({inp.depth_km:.1f} km) — stronger surface effects.")
    elif inp.depth_km > 300:
        advisories.append(f"Deep focus ({inp.depth_km:.1f} km) — reduced surface shaking.")

    if not triangulation:
        advisories.append(f"Only {inp.station_count} station(s) — triangulation requires ≥3.")

    if pga > 0.1:
        advisories.append(f"PGA={pga:.3f}g — structural damage threshold exceeded.")

    score = 0.0
    score += 0.20 * min(inp.magnitude / 7.0, 1.0)
    if triangulation:
        score += 0.25
    score += 0.20 * (1.0 - min(dist / 500.0, 1.0))
    score += 0.15 * min(sp_delay / 30.0, 1.0)
    score += 0.20 * (1.0 - min(len(advisories) / 4, 1.0))
    score = round(max(0.0, min(1.0, score)), 4)

    return SeismicResult(
        p_travel_time_s=round(t_p, 2),
        s_travel_time_s=round(t_s, 2),
        sp_delay_s=round(sp_delay, 2),
        rayleigh_speed_km_s=round(rayleigh_speed, 3),
        love_speed_km_s=round(love_speed, 3),
        peak_ground_acceleration_g=round(pga, 6),
        seismic_moment_nm=round(seismic_moment, 2),
        energy_joules=round(energy_j, 2),
        triangulation_possible=triangulation,
        intensity_mmi=mmi,
        omega_seismic=score,
        advisories=advisories,
    )
