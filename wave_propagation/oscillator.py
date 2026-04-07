"""
Layer 2 — Oscillator & Resonance (진동자와 공명)
==================================================

파인만: "자연의 거의 모든 것은 진동자다."

감쇠 강제 진동자:
  m·ẍ + c·ẋ + k·x = F₀·cos(ωt)

ζ = c/(2√(mk))    감쇠비
ω_n = √(k/m)      고유 진동수
Q = 1/(2ζ)         품질 인수

공명: ω_drive ≈ ω_n 일 때 진폭 극대
  A/A_static = 1/√((1-r²)² + (2ζr)²)    r = ω_drive/ω_n

모든 파동 레이어의 기초:
- 지진파 = 지각의 강제 진동
- 수면파 = 유체 표면의 복원력 진동
- 중력파 = 시공간 격자의 진동
"""
from __future__ import annotations

import math
from typing import List

from .contracts import (
    PI, TWO_PI,
    OscillatorInput,
    OscillatorResult,
)


def screen_oscillator(inp: OscillatorInput) -> OscillatorResult:
    """감쇠·강제 진동 스크리닝."""
    advisories: List[str] = []

    f_n = max(inp.natural_frequency_hz, 1e-12)
    omega_n = TWO_PI * f_n
    zeta = max(inp.damping_ratio, 0.0)

    q_factor = 1.0 / (2 * zeta) if zeta > 0 else float("inf")

    if zeta < 1.0:
        f_r = f_n * math.sqrt(max(1.0 - 2.0 * zeta ** 2, 0.0))
    else:
        f_r = 0.0

    if zeta > 0:
        decay_time = 1.0 / (zeta * omega_n)
    else:
        decay_time = float("inf")

    amp_ratio = 1.0
    is_resonant = False
    if inp.driving_frequency_hz > 0:
        r = inp.driving_frequency_hz / f_n
        denom_sq = (1.0 - r ** 2) ** 2 + (2.0 * zeta * r) ** 2
        if denom_sq > 0:
            amp_ratio = 1.0 / math.sqrt(denom_sq)
        else:
            amp_ratio = float("inf")
        is_resonant = 0.7 < r < 1.3 and amp_ratio > 2.0

    k_spring = inp.mass_kg * omega_n ** 2
    if zeta > 0 and inp.initial_displacement > 0:
        energy_initial = 0.5 * k_spring * inp.initial_displacement ** 2
        energy_remaining = energy_initial * math.exp(-2 * zeta * omega_n * inp.time_s)
        energy_dissipated = energy_initial - energy_remaining
    else:
        energy_dissipated = 0.0

    if zeta == 0:
        advisories.append("Undamped oscillator — energy is conserved indefinitely.")
    elif zeta < 0.05:
        advisories.append(f"Very lightly damped (ζ={zeta:.3f}) — long ring-down, high Q={q_factor:.0f}.")
    elif zeta >= 1.0:
        advisories.append(f"Overdamped (ζ={zeta:.2f}) — no oscillation, exponential return to equilibrium.")
    if is_resonant:
        advisories.append(
            f"Near resonance! Amplitude ratio={amp_ratio:.1f}× — structural stress risk."
        )

    score = 0.0
    if q_factor > 10:
        score += 0.25
    elif q_factor > 2:
        score += 0.15
    if is_resonant:
        score += 0.25
    if decay_time < inp.time_s:
        score += 0.15
    score += 0.20 * min(amp_ratio / 10.0, 1.0)
    score += 0.15 * (1.0 - min(len(advisories) / 3, 1.0))
    score = round(max(0.0, min(1.0, score)), 4)

    return OscillatorResult(
        q_factor=round(q_factor, 2) if q_factor < 1e6 else float("inf"),
        resonance_frequency_hz=round(f_r, 6),
        amplitude_ratio=round(amp_ratio, 4) if amp_ratio < 1e6 else float("inf"),
        decay_time_s=round(decay_time, 4) if decay_time < 1e12 else float("inf"),
        energy_dissipated_j=round(energy_dissipated, 6),
        is_resonant=is_resonant,
        omega_oscillator=score,
        advisories=advisories,
    )
