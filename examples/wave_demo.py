"""
Wave Propagation Foundation — Full Demo
========================================
5개 레이어 + 에코시스템 브리지 실행 예시.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wave_propagation import (
    analyze,
    analyze_ecosystem_stack,
    screen_seismic, screen_gravitational_wave,
    screen_surface_acoustic, screen_oscillator,
    SeismicInput, GravWaveInput, SurfaceAcousticInput,
    OscillatorInput, WaveEquationInput, MediumType, GravWaveSource,
)


def separator(title: str) -> None:
    print(f"\n{'='*55}")
    print(f"  {title}")
    print('='*55)


def main() -> None:
    # ── L2: 지진계 공명 (건물이 흔들리는 이유) ───────────
    separator("L2 Oscillator — 건물 공명 시뮬 (f_n=1Hz, ζ=0.05)")
    r = screen_oscillator(OscillatorInput(
        natural_frequency_hz=1.0, damping_ratio=0.05,
        driving_frequency_hz=1.0, driving_amplitude=1.0,
    ))
    print(f"  Q-factor:      {r.q_factor:.0f}")
    print(f"  Amplitude×:    {r.amplitude_ratio:.1f}  (공명 시 증폭)")
    print(f"  Resonant:      {r.is_resonant}")
    print(f"  Omega:         {r.omega_oscillator:.3f}")
    for a in r.advisories:
        print(f"  ⚠  {a}")

    # ── L3: 지진파 추적 ──────────────────────────────────
    separator("L3 Seismic — M6.3 지진 (진원 15km, 관측소 80km×5개)")
    r = screen_seismic(SeismicInput(
        magnitude=6.3, depth_km=15,
        epicentral_distance_km=80, station_count=5,
    ))
    print(f"  P파 도착:      {r.p_travel_time_s:.1f}s")
    print(f"  S파 도착:      {r.s_travel_time_s:.1f}s")
    print(f"  S-P 시간차:    {r.sp_delay_s:.1f}s → 거리 추적")
    print(f"  Rayleigh:      {r.rayleigh_speed_km_s} km/s")
    print(f"  PGA:           {r.peak_ground_acceleration_g:.4f} g  [proxy]")
    print(f"  진도:          MMI {r.intensity_mmi}")
    print(f"  삼각측량:      {r.triangulation_possible}")
    print(f"  방출 에너지:   {r.energy_joules:.2e} J")
    print(f"  Omega:         {r.omega_seismic:.3f}")

    # ── L4: 쓰나미 (천해 파동) ──────────────────────────
    separator("L4 Surface — 쓰나미 (수심 4000m, 주기 900s)")
    r = screen_surface_acoustic(SurfaceAcousticInput(
        water_depth_m=4000, wave_period_s=900, wave_height_m=0.5,
    ))
    print(f"  위상 속도:     {r.phase_velocity_m_s:.1f} m/s  (√gd≈198 m/s)")
    print(f"  심해 여부:     {r.is_deep_water}")
    print(f"  천해 여부:     {r.is_shallow_water}  ← 쓰나미 = 천해파")
    print(f"  Omega:         {r.omega_surface:.3f}")
    for a in r.advisories:
        print(f"  ℹ  {a}")

    # ── L5: 중력파 (GW150914) ───────────────────────────
    separator("L5 Gravitational Wave — GW150914 재현")
    r = screen_gravitational_wave(GravWaveInput(
        m1_solar=36, m2_solar=29, distance_mpc=410,
        orbital_frequency_hz=35,
        detector_sensitivity_strain=1e-22,
    ))
    print(f"  Chirp mass:    {r.chirp_mass_solar:.1f} M☉")
    print(f"  GW freq:       {r.gw_frequency_hz:.0f} Hz")
    print(f"  Strain h₀:     {r.strain_amplitude:.2e}")
    print(f"  SNR:           {r.signal_to_noise:.1f}")
    print(f"  ISCO:          {r.isco_frequency_hz:.1f} Hz")
    print(f"  탐지 가능:     {r.detectable}")
    print(f"  Omega:         {r.omega_grav:.3f}")

    # ── 통합 분석 ───────────────────────────────────────
    separator("Foundation analyze() — 전 레이어 통합")
    full = analyze(
        wave_input=WaveEquationInput(),
        oscillator_input=OscillatorInput(),
        seismic_input=SeismicInput(magnitude=5.0),
        surface_input=SurfaceAcousticInput(),
        grav_input=GravWaveInput(),
    )
    print(f"  Ω overall:     {full.omega_overall:.3f}  [{full.verdict.value}]")
    print(f"  Evidence tags: {sorted(full.evidence_tags)}")

    # ── 에코시스템 브리지 ────────────────────────────────
    separator("Ecosystem Bridges")
    stack = analyze_ecosystem_stack(
        seismic_input=SeismicInput(),
        surface_input=SurfaceAcousticInput(),
        grav_input=GravWaveInput(),
    )
    for name, payload in stack.items():
        status = "connected ✓" if payload else "not available (standalone mode)"
        print(f"  {name:<16} {status}")


if __name__ == "__main__":
    main()
