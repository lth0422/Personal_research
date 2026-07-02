# Work-in-Progress: A Practical Linux Framework for Weakly-Hard Tasks with Constant Bandwidth Server

- **그룹**: 4 idk_weakly_hard
- **출처/연도**: RTSS 2025 Work-in-Progress
- **저자**: Marcus Chen, Pascal Reich, Yidi Wang, Hyunjong Choi

## 두 질문
- **가변 변수**: CBS server parameters `Qk`, `Pk`, `Dk`; weakly-hard constraint `(m, K)`. Task period 자체를 runtime에 조절하는 논문은 아님.
- **트리거**: 없음=constraint-to-server mapping. QoS enhancement는 potential utilization을 늘리는 방향으로 논의되지만, system slack 기반 runtime adaptation은 future work에 가깝다.

## 요점
- 플랫폼: Linux `SCHED_DEADLINE`, user-space API, Raspberry Pi 5 evaluation.
- 도메인: weakly-hard periodic real-time task execution on Linux.
- 핵심 방법: `(m,K)` weakly-hard task를 Constant Bandwidth Server parameter로 변환해 Linux kernel modification 없이 실행한다. `SYS_sched_setattr`을 통해 `dl_runtime = Qk`, `dl_deadline = Dk`, `dl_period = Pk`를 설정한다.
- 정식화/수식: task `tau_i = (C_i, D_i, T_i, (m_i,K_i))`. server budget `Qk = Ci`. server period는 miss threshold `wi`에 기반해 결정한다. feasibility는 constrained-deadline EDF demand bound function으로 검사한다.

## 내 연구 관점
- 한 줄 gap: Linux에서 bounded deadline miss를 다루지만 vibration FD, W/H/M mode selection, machine condition trigger, PREEMPT_RT 비교는 다루지 않는다.
- 내 연구에 쓸 곳: KSC 2026 또는 학위논문에서 deadline miss를 hard zero-miss와 bounded miss로 구분하는 related work.
- 인용할 문장: "without kernel modifications"

## 불확실한 점
- 확인 필요: Raspberry Pi 5 실험은 example task trace와 synthetic taskset schedulability 중심이다. Pi Zero 2W, PREEMPT_RT, TFLite inference pipeline 결과로 일반화하면 안 된다.
- 확인 필요: QoS enhancement는 future work 성격이 있으므로 본 연구의 runtime slack adaptation과 직접 대응시키면 안 된다.
