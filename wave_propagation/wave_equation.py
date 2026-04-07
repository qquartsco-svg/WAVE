"""
Layer 1 — Wave Equation Core (일반 파동 방정식)
=================================================

모든 파동의 시작점:

  ∂²u/∂t² = c² ∇²u

이 식 하나에서 음파, 지진파, 수면파, 전자기파, 중력파가 모두 나온다.
파인만 물리학 강의 1권: "자연의 모든 파동은 같은 방정식을 공유한다."

핵심 산출:
  λ = c/f                    파장
  k = 2π/λ                   파수
  ω = 2πf                    각진동수
  A(x) = A₀ · exp(-αx)      지수 감쇠
  I = ½ρc·ω²A²              에너지 플럭스 (음파 기준)
"""
from __future__ import annotations

import math
from typing import List

from .contracts import (
    PI, TWO_PI, RHO_AIR,
    WaveEquationInput,
    WaveEquationResult,
    MediumType,
)


_MEDIUM_DENSITY = {
    MediumType.GAS: RHO_AIR,
    MediumType.LIQUID: 1025.0,
    MediumType.SOLID: 2700.0,
    MediumType.PLASMA: 1e-12,
    MediumType.VACUUM: 0.0,
}


def screen_wave_equation(inp: WaveEquationInput) -> WaveEquationResult:
    """일반 파동 방정식 스크리닝."""
    advisories: List[str] = []

    c = max(inp.wave_speed_m_s, 1e-6)
    f = max(inp.frequency_hz, 1e-12)

    wavelength = c / f
    period = 1.0 / f
    omega = TWO_PI * f
    k = TWO_PI / wavelength

    amp_at_dist = inp.amplitude * math.exp(-inp.attenuation_np_per_m * inp.propagation_distance_m)

    rho = _MEDIUM_DENSITY.get(inp.medium, RHO_AIR)
    if rho > 0 and inp.medium != MediumType.VACUUM:
        energy_flux = 0.5 * rho * c * (omega * amp_at_dist) ** 2
    else:
        energy_flux = 0.0

    if inp.attenuation_np_per_m > 0:
        penetration_depth = 1.0 / inp.attenuation_np_per_m
        if inp.propagation_distance_m > 3 * penetration_depth:
            advisories.append(
                f"Distance {inp.propagation_distance_m:.0f}m >> penetration depth {penetration_depth:.0f}m — "
                "signal heavily attenuated."
            )

    if inp.medium == MediumType.VACUUM and inp.wave_speed_m_s < 3e8:
        advisories.append("Mechanical waves cannot propagate in vacuum.")

    ratio = amp_at_dist / inp.amplitude if inp.amplitude > 0 else 0.0

    score = 0.0
    score += 0.25 * min(ratio, 1.0)
    score += 0.20 * min(c / 6000.0, 1.0)
    score += 0.20 * (1.0 if wavelength > 0.01 else 0.5)
    if energy_flux > 0:
        score += 0.20
    score += 0.15 * (1.0 - min(len(advisories) / 3, 1.0))
    score = round(max(0.0, min(1.0, score)), 4)

    return WaveEquationResult(
        wavelength_m=round(wavelength, 12),
        period_s=round(period, 12),
        angular_frequency_rad_s=round(omega, 4),
        wavenumber_rad_m=round(k, 6),
        phase_velocity_m_s=round(c, 4),
        amplitude_at_distance=round(amp_at_dist, 6),
        energy_flux_w_m2=round(energy_flux, 4),
        omega_wave=score,
        advisories=advisories,
    )
