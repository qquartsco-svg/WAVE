"""
Ecosystem Bridges — 형제 엔진 연결
====================================

FrequencyCore   : 스펙트럼 분석 → 지진파/진동 주파수 분해
Oceanus_Engine  : SWE 수면파 ↔ 수면파 레이어 연동
Eurus_Engine    : 대기 음파/중력파 연결
Optics          : 전자기파 속성 비교
OrbitalCore     : 중력원 파라미터 → 중력파 소스 모델링
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from .contracts import SeismicInput, GravWaveInput, SurfaceAcousticInput


def _staging_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _ensure_importable(path: Path) -> None:
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))


def try_frequencycore_bridge(
    seismic_input: Optional[SeismicInput] = None,
    *,
    sample_rate_hz: float = 100.0,
) -> dict[str, Any] | None:
    """Seismic signal → FrequencyCore spectral decomposition."""
    sibling = _staging_root() / "FrequencyCore_Engine"
    _ensure_importable(sibling)
    try:
        from frequencycore_engine import FrequencyInput, screen_frequency
    except Exception:
        return None

    f_dominant = 1.0 / max(seismic_input.epicentral_distance_km / seismic_input.vp_km_s, 0.1) if seismic_input else 1.0
    try:
        result = screen_frequency(FrequencyInput(
            signal_name="seismic_p_wave",
            sample_rate_hz=sample_rate_hz,
            fundamental_hz=f_dominant,
        ))
        return {
            "bridge": "frequencycore_available",
            "dominant_frequency_hz": round(f_dominant, 4),
            "omega_freq": result.omega_freq,
        }
    except Exception:
        return None


def try_oceanus_bridge(
    surface_input: Optional[SurfaceAcousticInput] = None,
) -> dict[str, Any] | None:
    """Surface wave params → Oceanus SWE proxy."""
    sibling = _staging_root() / "Oceanus_Engine"
    _ensure_importable(sibling)
    try:
        from oceanus_engine import OceanGridModel
    except Exception:
        return None

    try:
        return {
            "bridge": "oceanus_available",
            "water_depth_m": surface_input.water_depth_m if surface_input else None,
            "wave_period_s": surface_input.wave_period_s if surface_input else None,
        }
    except Exception:
        return None


def try_eurus_bridge() -> dict[str, Any] | None:
    """Atmospheric acoustic/gravity wave connection."""
    sibling = _staging_root() / "Eurus_Engine"
    _ensure_importable(sibling)
    try:
        from eurus_engine import EARTH
        return {
            "bridge": "eurus_available",
            "planet": EARTH.name,
        }
    except Exception:
        return None


def try_optics_bridge() -> dict[str, Any] | None:
    """EM wave property comparison."""
    sibling = _staging_root() / "Optics_Foundation"
    _ensure_importable(sibling)
    try:
        from optics_foundation import __version__
        return {
            "bridge": "optics_available",
            "version": __version__,
        }
    except Exception:
        return None


def try_orbitalcore_bridge(
    grav_input: Optional[GravWaveInput] = None,
) -> dict[str, Any] | None:
    """OrbitalCore gravity field → GW source context."""
    sibling = _staging_root() / "OrbitalCore_Engine"
    _ensure_importable(sibling)
    try:
        from orbitalcore_engine import MU_EARTH
        return {
            "bridge": "orbitalcore_available",
            "mu_earth": MU_EARTH,
            "gw_source": grav_input.source.value if grav_input else None,
        }
    except Exception:
        return None


def analyze_ecosystem_stack(
    *,
    seismic_input: Optional[SeismicInput] = None,
    surface_input: Optional[SurfaceAcousticInput] = None,
    grav_input: Optional[GravWaveInput] = None,
) -> dict[str, Any]:
    """전체 에코시스템 브리지 상태 요약."""
    return {
        "frequencycore": try_frequencycore_bridge(seismic_input),
        "oceanus": try_oceanus_bridge(surface_input),
        "eurus": try_eurus_bridge(),
        "optics": try_optics_bridge(),
        "orbitalcore": try_orbitalcore_bridge(grav_input),
    }
