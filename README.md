# Wave Propagation Foundation

> **한국어 (정본).** English: [README_EN.md](README_EN.md)

| 항목 | 내용 |
|------|------|
| 버전 | `v0.1.0` |
| 테스트 | `39 passed` |
| 의존성 | 런타임: **stdlib only** · 테스트: `pytest>=8.0` |
| Python | `>=3.10` |
| 라이선스 | MIT |

---

## 한 줄 정의

**파인만 물리학 강의 1권의 "파동과 요동"에서 출발해, 지구의 지진파부터 우주의 중력파까지 — 모든 파동을 추적·스크리닝하는 foundation.**

---

## 왜 만들었는가

파인만은 말했다: *"자연의 거의 모든 것은 진동이다."*

1. **지구**: 지진파(P/S/Rayleigh/Love)를 추적하고, 진앙을 삼각측량하고, 수면파와 음파의 전파를 분석한다.
2. **우주**: 중력파 — 시공간 자체의 파동 — 를 strain과 chirp mass로 스크리닝한다.
3. **통합**: 하나의 파동 방정식(∂²u/∂t² = c²∇²u)에서 모든 레이어가 출발한다.

기존 엔진 전수 조사 결과:
- **FrequencyCore** = 스펙트럼 분석 도구 (파동 전파 물리 없음)
- **Oceanus** = 수면 SWE + 조석 (지진파 전파 없음)
- **Optics** = 전자기파만 (기계적 파동 없음)
- **OrbitalCore** = 뉴턴 중력 (GR 중력파 없음)

→ **파동 전파·추적을 통합하는 엔진이 없었다.** 이 foundation이 그 갭을 채운다.

---

## 아키텍처

```text
       ∂²u/∂t² = c²∇²u  (일반 파동 방정식)
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───┴───┐   ┌────┴────┐   ┌───┴───┐
│ L1    │   │ L2      │   │ L5    │
│ Wave  │   │ Oscill- │   │ Grav  │
│ Eq.   │   │ ator    │   │ Wave  │
└───┬───┘   └────┬────┘   └───┬───┘
    │             │             │
    │        ┌────┴────┐        │
    │        │ L3      │        │
    │        │ Seismic │        │
    │        └────┬────┘        │
    │             │             │
    │        ┌────┴────┐        │
    │        │ L4 Surf │        │
    │        │ Acoustic│        │
    │        └────┬────┘        │
    │             │             │
    └─────────────┼─────────────┘
                  │
         foundation.analyze()
              Ω · verdict
                  │
    ┌─────────────┼─────────────┐
    │      │      │      │      │
 Freq   Oceanus Eurus  Optics Orbital
 Core   Engine  Engine Found. Core
```

---

## 5개 레이어

### L1: Wave Equation (일반 파동 방정식)

```
λ = c/f     k = 2π/λ     ω = 2πf
A(x) = A₀·exp(-αx)          지수 감쇠
I = ½ρc·ω²A²                에너지 플럭스
```

### L2: Oscillator & Resonance (진동자·공명)

```
m·ẍ + c·ẋ + k·x = F₀·cos(ωt)
Q = 1/(2ζ)                  품질 인수
A/A_static = 1/√((1-r²)²+(2ζr)²)    공명 곡선
```

### L3: Seismic Waves (지진파 추적)

```
v_P ≈ 6 km/s (종파)    v_S ≈ 3.5 km/s (횡파)
Rayleigh ≈ 0.92·v_S     Love ≈ (v_S+v_P)/2
Δt = t_S - t_P → 진앙 거리 삼각측량
M₀ = 10^(1.5M+9.1)      E = 10^(1.5M+4.8)
PGA → MMI 진도 변환
```

### L4: Surface & Acoustic Waves (수면파·음파)

```
ω² = gk·tanh(kd)        수면파 분산관계
심해: c = gT/(2π)        천해: c = √(gd) (쓰나미)
c_air = 331.3 + 0.606·T   c_water ≈ 1449 + 4.6T - 0.055T²
Z = ρ·c                  음향 임피던스
```

### L5: Gravitational Waves (중력파)

```
M_c = (m₁m₂)^(3/5)/(m₁+m₂)^(1/5)    chirp mass
h₀ = (4G^(5/3)/c⁴)·M_c^(5/3)·(πf)^(2/3)/d    strain
f_isco = c³/(6^(3/2)·π·G·M)           최내안정궤도
L_gw = (32/5)·(G⁴/c⁵)·M_c^(10/3)·(πf)^(10/3)
```

---

## Ω 점수 체계

```python
Ω_overall = mean([실행된 레이어만 포함])
```

| Ω 범위 | Verdict | 의미 |
|--------|---------|------|
| ≥ 0.80 | `OPERATIONAL` | 추적 가능 |
| ≥ 0.55 | `FEASIBLE` | 조건부 추적 가능 |
| ≥ 0.30 | `EXPERIMENTAL` | 실험적 |
| < 0.30 | `NOT_FEASIBLE` | 현 조건 불가 |

---

## 사용 가이드

### 지진파 추적

```python
from wave_propagation import screen_seismic, SeismicInput

r = screen_seismic(SeismicInput(
    magnitude=6.3, depth_km=15,
    epicentral_distance_km=80, station_count=5,
))
print(f"P파: {r.p_travel_time_s:.1f}s  S파: {r.s_travel_time_s:.1f}s")
print(f"S-P 시간차: {r.sp_delay_s:.1f}s → 진앙거리 추적")
print(f"PGA: {r.peak_ground_acceleration_g:.4f}g  진도: {r.intensity_mmi}")
print(f"삼각측량: {r.triangulation_possible}")
```

> **PGA 주의**: 현재 PGA는 NGA-West2 함수형을 단순화한 proxy 추정값입니다. 실제 지반 증폭, 지각 구조, 방향성 효과는 반영되지 않으며 v0.2에서 개선 예정입니다.

### 중력파 탐지 (GW150914 재현)

```python
from wave_propagation import screen_gravitational_wave, GravWaveInput

# GW150914: m1=36 M☉, m2=29 M☉, d=410 Mpc
# LIGO Advanced 감도 @ 35 Hz ≈ 1e-22 (설계 감도 근사)
r = screen_gravitational_wave(GravWaveInput(
    m1_solar=36, m2_solar=29, distance_mpc=410,
    orbital_frequency_hz=35,
    detector_sensitivity_strain=1e-22,   # Advanced LIGO 감도 근사
))
print(f"Chirp mass: {r.chirp_mass_solar:.1f} M☉")
print(f"Strain:     {r.strain_amplitude:.2e}")
print(f"SNR:        {r.signal_to_noise:.1f}   (실제 GW150914 ≈ 24)")
print(f"ISCO freq:  {r.isco_frequency_hz:.1f} Hz")
print(f"Detectable: {r.detectable}")
```

> `detector_sensitivity_strain`은 관심 주파수에서의 단순화된 단일 수치입니다. 실제 LIGO는 주파수 의존적 noise curve(ASD)를 사용합니다.

### 통합 분석 (지구+우주 동시)

```python
from wave_propagation import analyze, SeismicInput, GravWaveInput, WaveEquationInput

r = analyze(
    wave_input=WaveEquationInput(),
    seismic_input=SeismicInput(magnitude=5.0),
    grav_input=GravWaveInput(),
)
print(f"Overall Ω={r.omega_overall:.3f} [{r.verdict.value}]")
```

---

## 물리 스냅샷 — 동역학 흐름에서 도출된 함수값

> 아래는 `v0.1.0` 기준 실행 결과다.  
> 각 수치는 **모델 내 동역학 흐름의 자기정합성**을 보는 것이며, 실측 데이터와의 대조는 별도 검증 단계가 필요하다.

---

### Snap-A · 쓰나미 천해파 — 분산관계 흐름 수렴

천해 근사 `c = √(gd)` 와 완전 분산관계 `ω² = gk·tanh(kd)` 사이의 함수값 차이.  
수심이 파장에 비해 충분히 얕을수록 두 흐름이 같은 값으로 수렴하는지 확인.

| 수심 | 분산관계 도출값 | 천해 근사값 (√gd) | 함수값 차이 |
|------|--------------|-----------------|-----------|
| 100 m | 31.31 m/s | 31.32 m/s | 0.008 % |
| 1000 m | 98.95 m/s | 99.03 m/s | 0.083 % |
| 4000 m | 197.40 m/s | 198.06 m/s | 0.331 % |

*천해 조건에서 두 흐름의 함수값 차이는 0.33 % 이하. 모델 내 흐름 정합성 확인. 실제 해저 지형·조석 효과는 반영되지 않음.*

---

### Snap-B · S-P 시간차 → 진앙 거리 역산 흐름

`Δt = d·(1/v_S − 1/v_P)` 에서 출발한 동역학 흐름이 입력 거리를 얼마나 정합적으로 복원하는가.

| 입력 거리 | S-P 시간차 | 역산값 | 흐름 내 편차 |
|----------|-----------|--------|------------|
| 50 km | 6.07 s | 51.0 km | 0.00 % |
| 100 km | 11.96 s | 100.5 km | 0.03 % |
| 500 km | 59.54 s | 500.1 km | 0.01 % |

*1D 균질 지각 모델 내에서 순방향·역방향 흐름의 자기정합성 확인. 실제 지각 구조·이방성·속도 구배를 포함하면 편차가 커진다.*

---

### Snap-C · 규모-에너지 흐름 — Gutenberg-Richter 관계

`E = 10^(1.5M + 4.8)` 흐름에서 도출되는 에너지 함수값.

| 규모 | 도출 에너지 | TNT 환산 |
|------|-----------|---------|
| M3.0 | 2.0 × 10⁹ J | ~0.5 ton |
| M5.0 | 2.0 × 10¹² J | ~477 ton |
| M6.3 | 1.8 × 10¹⁴ J | ~42,500 ton |
| M7.0 | 2.0 × 10¹⁵ J | ~477,000 ton |
| M9.0 | 2.0 × 10¹⁸ J | ~4.8억 ton |

*M 1 증가 → 에너지 흐름 ×31.6 (10^1.5). 이 관계는 경험적 회귀식이며 실제 방출 에너지와 차이가 있을 수 있다.*

---

### Snap-D · 진동자 공명 — 감쇠비 vs 진폭 증폭 흐름

가진 주파수 = 고유 주파수 (완전 공명) 조건에서 감쇠비에 따른 함수값.

| 감쇠비 ζ | Q 인수 | 진폭 증폭 | 구조 예시 (참고) |
|---------|--------|---------|--------------|
| 0.01 | 50.0 | ~50× | 강재 골조 (저감쇠) |
| 0.05 | 10.0 | ~10× | RC 건물 (일반 설계 범위) |
| 0.10 | 5.0 | ~5× | 고감쇠 구조 |
| 1.00 | 0.5 | ~0.5× | 임계감쇠 — 공명 흐름 없음 |

*완전 공명 조건 하의 단자유도 이상 모델 흐름. 실제 구조물은 다자유도·비선형 거동이며 감쇠도 주파수 의존적이다.*

---

### Snap-E · 중력파 — 거리에 따른 strain/SNR 흐름

선형화 GR 흐름에서 `h₀ ∝ 1/d` 로 도출되는 strain 및 단순화 SNR.  
사건 파라미터: M₁=36 M☉, M₂=29 M☉, f=35 Hz, 감도 proxy=1e-22.

| 거리 | 도출 strain | 흐름 SNR | 비고 |
|------|-----------|---------|------|
| 10 Mpc | 5.24 × 10⁻²⁰ | 524 | — |
| 410 Mpc | 1.28 × 10⁻²¹ | 12.8 | GW150914 실측 ≈ 24 |
| 1000 Mpc | 5.24 × 10⁻²² | 5.2 | — |
| 5000 Mpc | 1.05 × 10⁻²² | 1.1 | 임계 근방 |

*strain ∝ 1/d 흐름은 선형 GR 근사에서 도출. GW150914 비교값(~24)과의 차이는 단일 수치 감도 proxy 사용에 기인하며, 실제 LIGO는 주파수 의존 노이즈 곡선(ASD)을 사용한다.*

---

## 에코시스템 엔진 연결

| 엔진 | 브리지 | 연결 |
|------|--------|------|
| **FrequencyCore** | `try_frequencycore_bridge()` | 지진 신호 → 스펙트럼 분해 |
| **Oceanus** | `try_oceanus_bridge()` | 수면파 ↔ SWE 연동 |
| **Eurus** | `try_eurus_bridge()` | 대기 음파/중력파 |
| **Optics** | `try_optics_bridge()` | 전자기파 비교 |
| **OrbitalCore** | `try_orbitalcore_bridge()` | 중력원 → GW 소스 |

모든 브리지는 graceful degradation — 없으면 `None`, 코어는 독립 실행.

---

## 현재 한계 + 확장 로드맵

| 한계 | v0.2 계획 |
|------|-----------|
| 지진파 1D 전파 | 2D/3D ray tracing |
| PGA = proxy | NGA-West2 완전 구현 |
| 분산관계 반복 풀이 | 해석적 근사 + 비선형 보정 |
| 중력파 = inspiral만 | merger + ringdown waveform |
| 단일 검출기 | 다중 검출기 네트워크 |

---

## 테스트

```bash
pip install -e ".[dev]"
python3 -m pytest tests/ -q            # 39 passed
python3 examples/wave_demo.py          # 전 레이어 실행 데모
```

---

## 라이선스

MIT — [LICENSE](LICENSE)
