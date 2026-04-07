"""
Wave Propagation Foundation  v0.1.0
====================================

파인만 물리학 강의 1권 — 파동과 요동에서 출발:
  L1 일반 파동 방정식
  L2 진동자와 공명
  L3 지진파 추적
  L4 수면파·음파
  L5 중력파

지구의 지진부터 우주의 중력파까지 — 모든 파동을 추적한다.
"""
__version__ = "0.1.0"

from .contracts import (
    WaveType, SeismicPhase, MediumType, GravWaveSource, ReadinessVerdict,
    WaveEquationInput, WaveEquationResult,
    OscillatorInput, OscillatorResult,
    SeismicInput, SeismicResult,
    SurfaceAcousticInput, SurfaceAcousticResult,
    GravWaveInput, GravWaveResult,
    WaveTrackingReport,
)
from .wave_equation import screen_wave_equation
from .oscillator import screen_oscillator
from .seismic import screen_seismic
from .surface_acoustic import screen_surface_acoustic
from .gravitational_wave import screen_gravitational_wave
from .foundation import analyze
from .ecosystem_bridges import (
    analyze_ecosystem_stack,
    try_frequencycore_bridge,
    try_oceanus_bridge,
    try_eurus_bridge,
    try_optics_bridge,
    try_orbitalcore_bridge,
)

__all__ = [
    "analyze",
    "screen_wave_equation", "screen_oscillator", "screen_seismic",
    "screen_surface_acoustic", "screen_gravitational_wave",
    "analyze_ecosystem_stack",
    "try_frequencycore_bridge", "try_oceanus_bridge", "try_eurus_bridge",
    "try_optics_bridge", "try_orbitalcore_bridge",
    "WaveType", "SeismicPhase", "MediumType", "GravWaveSource", "ReadinessVerdict",
    "WaveEquationInput", "WaveEquationResult",
    "OscillatorInput", "OscillatorResult",
    "SeismicInput", "SeismicResult",
    "SurfaceAcousticInput", "SurfaceAcousticResult",
    "GravWaveInput", "GravWaveResult",
    "WaveTrackingReport",
]
