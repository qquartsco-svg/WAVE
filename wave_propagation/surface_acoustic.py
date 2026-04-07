"""
Layer 4 — Surface & Acoustic Waves (수면파·음파)
==================================================

수면파 — 중력이 복원력인 표면 중력파:

  분산관계: ω² = gk·tanh(kd)

  심해 (kd >> 1): c = √(g/k) = gT/(2π)   — 장주기가 빠름
  천해 (kd << 1): c = √(gd)              — 수심에만 의존 (쓰나미)

  군속도 vs 위상속도:
    심해: v_g = c/2  (에너지가 파면보다 느림)
    천해: v_g = c    (비분산)

음파 — 공기/물 내 종파:

  c_air = 331.3 + 0.606·T(°C)            m/s
  c_water ≈ 1449 + 4.6T - 0.055T² + ...   Mackenzie (1981)

  음향 임피던스: Z = ρ·c
  반사 계수: R = (Z₂-Z₁)/(Z₂+Z₁)

파인만: "수면에서 깊은 물은 분산적이고, 얕은 물은 비분산적이다."
"""
from __future__ import annotations

import math
from typing import List

from .contracts import (
    PI, TWO_PI, G_EARTH, RHO_WATER, RHO_AIR,
    MediumType,
    SurfaceAcousticInput,
    SurfaceAcousticResult,
)


def _sound_speed_air(T_c: float) -> float:
    return 331.3 + 0.606 * T_c


def _sound_speed_water(T_c: float) -> float:
    return 1449.2 + 4.6 * T_c - 0.055 * T_c ** 2 + 0.00029 * T_c ** 3


def _solve_dispersion(period_s: float, depth_m: float, g: float) -> tuple:
    """Solve ω² = gk·tanh(kd) for k.

    Fixed-point iteration can oscillate for long-period shallow-water waves
    such as tsunamis, so use monotonic bisection on the dispersion residual.
    """
    omega = TWO_PI / max(period_s, 0.01)
    target = omega ** 2

    def residual(k: float) -> float:
        return g * k * math.tanh(max(k * depth_m, 1e-18)) - target

    lo = 0.0
    hi = max(target / max(g, 1e-12), omega / max(math.sqrt(g * max(depth_m, 1e-12)), 1e-12), 1e-12)
    while residual(hi) < 0.0:
        hi *= 2.0
        if hi > 1e6:
            break

    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if residual(mid) >= 0.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi), omega


def screen_surface_acoustic(inp: SurfaceAcousticInput) -> SurfaceAcousticResult:
    """수면파·음파 스크리닝."""
    advisories: List[str] = []
    g = inp.gravity_ms2

    k, omega = _solve_dispersion(inp.wave_period_s, inp.water_depth_m, g)
    wavelength = TWO_PI / k if k > 0 else 0.0
    kd = k * inp.water_depth_m

    phase_vel = omega / k if k > 0 else 0.0

    n = 0.5 * (1.0 + 2.0 * kd / math.sinh(max(2.0 * kd, 1e-12)))
    group_vel = n * phase_vel

    is_deep = kd > PI
    is_shallow = kd < 0.05 * TWO_PI

    rho = RHO_WATER
    wave_energy = 0.125 * rho * g * inp.wave_height_m ** 2

    if inp.medium == MediumType.GAS:
        sound_speed = _sound_speed_air(inp.temperature_c)
        rho_medium = RHO_AIR
    elif inp.medium == MediumType.LIQUID:
        sound_speed = _sound_speed_water(inp.temperature_c)
        rho_medium = RHO_WATER
    elif inp.medium == MediumType.SOLID:
        sound_speed = 5000.0
        rho_medium = 2700.0
    else:
        sound_speed = 0.0
        rho_medium = 0.0

    impedance = rho_medium * sound_speed

    if is_deep:
        advisories.append(f"Deep-water regime (kd={kd:.1f}) — dispersive: long waves travel faster.")
    elif is_shallow:
        advisories.append(
            f"Shallow-water regime (kd={kd:.4f}) — non-dispersive: c=√(gd)={math.sqrt(g*inp.water_depth_m):.1f} m/s."
        )
        if inp.wave_height_m > 0.5 * inp.water_depth_m:
            advisories.append("Wave height comparable to depth — nonlinear effects (breaking).")
    else:
        advisories.append(f"Intermediate depth (kd={kd:.2f}).")

    if inp.wave_height_m > 4.0:
        advisories.append(f"Wave height {inp.wave_height_m:.1f}m — rough/very rough sea state.")

    score = 0.0
    score += 0.20 * min(phase_vel / 20.0, 1.0)
    score += 0.20 * min(wave_energy / 5000.0, 1.0)
    if sound_speed > 0:
        score += 0.20
    score += 0.20 * (1.0 if not is_shallow else 0.5)
    score += 0.20 * (1.0 - min(len(advisories) / 4, 1.0))
    score = round(max(0.0, min(1.0, score)), 4)

    return SurfaceAcousticResult(
        phase_velocity_m_s=round(phase_vel, 4),
        group_velocity_m_s=round(group_vel, 4),
        wavelength_m=round(wavelength, 4),
        is_deep_water=is_deep,
        is_shallow_water=is_shallow,
        wave_energy_j_m2=round(wave_energy, 2),
        sound_speed_m_s=round(sound_speed, 2),
        acoustic_impedance=round(impedance, 2),
        omega_surface=score,
        advisories=advisories,
    )
