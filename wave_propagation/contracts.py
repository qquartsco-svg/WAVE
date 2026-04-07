"""
Wave Propagation Foundation — Data Contracts
==============================================

파동·진동·붕괴를 추적하는 통합 foundation의 타입 계약.

파인만 물리학 강의 1권 — 파동과 요동에서 출발:
  "모든 것은 진동이다. 빛도, 소리도, 지진도, 중력의 주름도."

5개 경로:
  L1  일반 파동 방정식 (∂²u/∂t² = c²∇²u)
  L2  진동자와 공명 (SHO, 감쇠, 강제, 결합)
  L3  지진파 (P/S/Rayleigh/Love, 진앙 추적)
  L4  수면파·음파 (분산, 전파, 감쇠)
  L5  중력파 (GR 선형화, strain, chirp mass)

SI 단위 기본. 모든 dataclass는 frozen.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

# ── Physical Constants ──────────────────────────────────
G_NEWTON: float = 6.674e-11           # m³/(kg·s²)
C_LIGHT: float = 2.998e8              # m/s
G_EARTH: float = 9.80665              # m/s²
RHO_EARTH_AVG: float = 5515.0         # kg/m³
R_EARTH: float = 6.371e6              # m
M_EARTH: float = 5.972e24             # kg
M_SUN: float = 1.989e30               # kg

RHO_AIR: float = 1.225                # kg/m³ @ sea level
RHO_WATER: float = 1025.0             # kg/m³ (seawater)
GAMMA_AIR: float = 1.4                # adiabatic index (air)
P_ATM: float = 101325.0               # Pa

PI: float = math.pi
TWO_PI: float = 2.0 * math.pi


# ── Enums ───────────────────────────────────────────────

class WaveType(Enum):
    LONGITUDINAL = "longitudinal"
    TRANSVERSE = "transverse"
    SURFACE = "surface"
    TORSIONAL = "torsional"

class SeismicPhase(Enum):
    P = "P"
    S = "S"
    RAYLEIGH = "Rayleigh"
    LOVE = "Love"

class MediumType(Enum):
    SOLID = "solid"
    LIQUID = "liquid"
    GAS = "gas"
    VACUUM = "vacuum"
    PLASMA = "plasma"

class GravWaveSource(Enum):
    BINARY_BH = "binary_black_hole"
    BINARY_NS = "binary_neutron_star"
    BH_NS = "black_hole_neutron_star"
    SUPERNOVA = "supernova"
    CONTINUOUS = "continuous"

class ReadinessVerdict(Enum):
    OPERATIONAL = "operational"
    FEASIBLE = "feasible"
    EXPERIMENTAL = "experimental"
    NOT_FEASIBLE = "not_feasible"


# ── Layer 1: Wave Equation ─────────────────────────────

@dataclass(frozen=True)
class WaveEquationInput:
    """일반 파동 방정식 입력."""
    wave_speed_m_s: float = 343.0         # 파동 속도 (공기 중 음속 기본)
    frequency_hz: float = 440.0           # 주파수 (A4 음)
    amplitude: float = 1.0                # 무차원 진폭
    propagation_distance_m: float = 1000.0
    attenuation_np_per_m: float = 0.0     # Neper/m (지수 감쇠)
    medium: MediumType = MediumType.GAS

@dataclass(frozen=True)
class WaveEquationResult:
    wavelength_m: float
    period_s: float
    angular_frequency_rad_s: float
    wavenumber_rad_m: float
    phase_velocity_m_s: float
    amplitude_at_distance: float
    energy_flux_w_m2: float
    omega_wave: float
    advisories: List[str]


# ── Layer 2: Oscillator & Resonance ────────────────────

@dataclass(frozen=True)
class OscillatorInput:
    """감쇠·강제 진동자 입력."""
    natural_frequency_hz: float = 1.0
    damping_ratio: float = 0.1              # ζ (0=무감쇠, 1=임계, >1=과감쇠)
    driving_frequency_hz: float = 0.0       # 0이면 자유 진동
    driving_amplitude: float = 0.0
    mass_kg: float = 1.0
    initial_displacement: float = 1.0
    time_s: float = 10.0

@dataclass(frozen=True)
class OscillatorResult:
    q_factor: float                         # Q = 1/(2ζ)
    resonance_frequency_hz: float           # f_r = f_n√(1-2ζ²)
    amplitude_ratio: float                  # 강제 진동 시 정상 진폭 / 정적 진폭
    decay_time_s: float                     # 1/e 감쇠 시간
    energy_dissipated_j: float
    is_resonant: bool
    omega_oscillator: float
    advisories: List[str]


# ── Layer 3: Seismic Waves ─────────────────────────────

@dataclass(frozen=True)
class SeismicInput:
    """지진파 추적 입력."""
    magnitude: float = 5.0                  # 리히터/모멘트 규모
    depth_km: float = 10.0                  # 진원 깊이
    epicentral_distance_km: float = 100.0   # 관측점까지 거리
    vp_km_s: float = 6.0                    # P파 속도
    vs_km_s: float = 3.5                    # S파 속도
    rock_density_kg_m3: float = 2700.0
    site_amplification: float = 1.0         # 지반 증폭 계수
    station_count: int = 3                  # 관측소 수 (삼각측량)

@dataclass(frozen=True)
class SeismicResult:
    p_travel_time_s: float
    s_travel_time_s: float
    sp_delay_s: float                       # S-P 시간차
    rayleigh_speed_km_s: float
    love_speed_km_s: float
    peak_ground_acceleration_g: float       # PGA (g)
    seismic_moment_nm: float                # M₀
    energy_joules: float                    # 방출 에너지
    triangulation_possible: bool
    intensity_mmi: str                      # Modified Mercalli Intensity
    omega_seismic: float
    advisories: List[str]


# ── Layer 4: Surface & Acoustic Waves ──────────────────

@dataclass(frozen=True)
class SurfaceAcousticInput:
    """수면파·음파 입력."""
    water_depth_m: float = 100.0            # 수심
    wave_period_s: float = 8.0              # 파동 주기
    wave_height_m: float = 2.0              # 파고
    gravity_ms2: float = 9.80665
    temperature_c: float = 20.0             # 매질 온도 (음파 속도에 영향)
    medium: MediumType = MediumType.LIQUID
    propagation_distance_m: float = 1000.0

@dataclass(frozen=True)
class SurfaceAcousticResult:
    phase_velocity_m_s: float
    group_velocity_m_s: float
    wavelength_m: float
    is_deep_water: bool                     # kd >> 1
    is_shallow_water: bool                  # kd << 1
    wave_energy_j_m2: float                 # 단위 면적당 에너지
    sound_speed_m_s: float                  # 매질 내 음속
    acoustic_impedance: float               # ρ·c
    omega_surface: float
    advisories: List[str]


# ── Layer 5: Gravitational Waves ───────────────────────

@dataclass(frozen=True)
class GravWaveInput:
    """중력파 입력."""
    source: GravWaveSource = GravWaveSource.BINARY_BH
    m1_solar: float = 30.0                  # 질량 1 (태양질량)
    m2_solar: float = 30.0                  # 질량 2
    distance_mpc: float = 400.0             # 광원 거리 (Mpc)
    orbital_frequency_hz: float = 30.0      # 궤도 주파수
    detector_sensitivity_strain: float = 1e-23  # LIGO 기준 감도

@dataclass(frozen=True)
class GravWaveResult:
    chirp_mass_solar: float
    chirp_mass_kg: float
    gw_frequency_hz: float                  # f_gw = 2·f_orbital
    strain_amplitude: float                 # h₀
    luminosity_w: float                     # 중력파 광도
    detectable: bool
    signal_to_noise: float
    isco_frequency_hz: float                # 최내안정궤도 주파수
    merger_time_estimate_s: float
    omega_grav: float
    advisories: List[str]


# ── Master Reports ─────────────────────────────────────

@dataclass(frozen=True)
class WaveTrackingReport:
    """Foundation 최종 보고서."""
    wave_equation: Optional[WaveEquationResult] = None
    oscillator: Optional[OscillatorResult] = None
    seismic: Optional[SeismicResult] = None
    surface_acoustic: Optional[SurfaceAcousticResult] = None
    gravitational: Optional[GravWaveResult] = None
    omega_overall: float = 0.0
    verdict: ReadinessVerdict = ReadinessVerdict.NOT_FEASIBLE
    evidence_tags: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
