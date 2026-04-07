"""
Wave Propagation Foundation — Integration
==========================================

5개 레이어 통합:
  L1  Wave Equation (일반 파동)
  L2  Oscillator (진동자·공명)
  L3  Seismic (지진파 추적)
  L4  Surface & Acoustic (수면파·음파)
  L5  Gravitational Wave (중력파)
"""
from __future__ import annotations

from typing import List, Optional

from .contracts import (
    GravWaveInput,
    OscillatorInput,
    ReadinessVerdict,
    SeismicInput,
    SurfaceAcousticInput,
    WaveEquationInput,
    WaveTrackingReport,
)
from .wave_equation import screen_wave_equation
from .oscillator import screen_oscillator
from .seismic import screen_seismic
from .surface_acoustic import screen_surface_acoustic
from .gravitational_wave import screen_gravitational_wave


def _verdict(omega: float) -> ReadinessVerdict:
    if omega >= 0.80:
        return ReadinessVerdict.OPERATIONAL
    if omega >= 0.55:
        return ReadinessVerdict.FEASIBLE
    if omega >= 0.30:
        return ReadinessVerdict.EXPERIMENTAL
    return ReadinessVerdict.NOT_FEASIBLE


def analyze(
    wave_input: Optional[WaveEquationInput] = None,
    oscillator_input: Optional[OscillatorInput] = None,
    seismic_input: Optional[SeismicInput] = None,
    surface_input: Optional[SurfaceAcousticInput] = None,
    grav_input: Optional[GravWaveInput] = None,
) -> WaveTrackingReport:
    """통합 파동 추적 분석. 실행된 경로만 평균하여 Ω를 산출한다."""
    tags: List[str] = []
    warnings: List[str] = []
    scores: List[float] = []

    wave_r = None
    if wave_input:
        wave_r = screen_wave_equation(wave_input)
        tags.append("wave_equation")
        scores.append(wave_r.omega_wave)
        warnings.extend(wave_r.advisories)

    osc_r = None
    if oscillator_input:
        osc_r = screen_oscillator(oscillator_input)
        tags.append("oscillator")
        scores.append(osc_r.omega_oscillator)
        warnings.extend(osc_r.advisories)

    seis_r = None
    if seismic_input:
        seis_r = screen_seismic(seismic_input)
        tags.append("seismic")
        scores.append(seis_r.omega_seismic)
        warnings.extend(seis_r.advisories)

    surf_r = None
    if surface_input:
        surf_r = screen_surface_acoustic(surface_input)
        tags.append("surface_acoustic")
        scores.append(surf_r.omega_surface)
        warnings.extend(surf_r.advisories)

    grav_r = None
    if grav_input:
        grav_r = screen_gravitational_wave(grav_input)
        tags.append("gravitational_wave")
        scores.append(grav_r.omega_grav)
        warnings.extend(grav_r.advisories)

    omega = round(sum(scores) / len(scores), 4) if scores else 0.0

    return WaveTrackingReport(
        wave_equation=wave_r,
        oscillator=osc_r,
        seismic=seis_r,
        surface_acoustic=surf_r,
        gravitational=grav_r,
        omega_overall=omega,
        verdict=_verdict(omega),
        evidence_tags=list(set(tags)),
        warnings=warnings,
    )
