# Real-Time Fault Diagnosis Related-Work Table Draft

이 표는 `surveys/realtime_fault_diagnosis_survey_protocol.md`의 판정 규칙을 사용하는 원고용 초안이다. 현재 paper card 기준의 예비 판정이며, 원문 재검토 후 `?`와 `△`를 확정해야 한다.

2026-07-21 LINER·Claude 검색에서 수집한 신규 fault-diagnosis 후보 14편은 2026-07-24 full-text 판정을 완료해 아래에 추가했다. 최종 원고에는 직접성이 높은 5~8편만 남기고 나머지는 survey 근거로 유지한다.

## 기호

- O: 원문에서 확인
- △: 부분 충족 또는 간접 근거
- X: 해당 없음 확인
- ?: 확인 필요
- P: 제안 연구의 계획이며 아직 검증되지 않음

## 압축 비교표

| Work | Platform | Execution environment | RTOS | PREEMPT_RT | Deadline | Tail/miss | Sched. analysis | 경량화·배포 기법 | System scheduling | Runtime adapt. | Joint `W/H/M` | `q+S` | RT level |
| --- | --- | --- | :---: | :---: | :---: | :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: |
| Ma et al., Architecture Search FD [1] | Desktop CPU (AMD Ryzen 5 4600H) | OS 미기재; framework·thread 수 미기재 | X | X | △ | X | X | Hardware-aware differentiable NAS (variable-layer; GD-Conv + 다중 kernel; measured op time을 L_time = log(t̄/t_b)로 objective에 포함); 82 K params, 6.08 MFlops; 0.780 ms/sample (820-sample batch ÷ 0.64 s; batch-1 online latency 아님) | X | X | X | X | B |
| Lee and Kim, FRFconv-TDSNet [2] | Raspberry Pi 4B | Linux (OS 미기재); PyTorch Mobile + XNNPACK | X | X | X | X | X | 경량 아키텍처 수동 설계 (FRFconv depthwise separable + TDS late fusion); 9K param, 1.80 MAdds; avg 3.40 ms·max 3.67 ms (100회) | X | X | X | X | B |
| Jalonen et al., Time-Varying Speed FD [3] | MacBook Pro M1 Pro | OS·framework·backend 미기재 | X | X | △ | X | X | 알고리즘 경량화 (speed PSD NUFT 분석 → 10 Hz threshold → T=100 ms → W=2000 고정; angular resampling 없음); C_avg=20.2 ms ± 0.36 ms (10×1000 samples) | X | X | X | X | B |
| Thota et al., TinyML Bearing FD [4] | Espressif ESP-EYE (ESP32 계열); clock·RAM·Flash 사양 미보고 | Edge Impulse firmware; OS·RTOS·runtime 미보고 (ENV-OTHER) | X | X | X | X | X | Compact 3-layer 1D CNN (raw triaxial vibration 직접 입력); 6-class distributed bearing fault; INT8 quantization; Table 2: FP32 99.26%·30 ms·29.3 KB RAM·43.3 KB Flash vs. INT8 99.36%·265 ms·61.2 KB RAM·69.7 KB Flash; 본문은 INT8에 30 ms·29.3 KB를 귀속 — 수치 모순; f_s·H 미보고; energy·cycles 미보고; live motor deployment 미수행 | X | X | X | X | B |
| Choi et al., Low-Cost MCU Shaft FD [5] | STM32 Nucleo-64 / STM32F401RET6 (84 MHz, 96 KiB RAM, 512 KiB Flash) | RTOS 없음; bare-metal 추정; X-CUBE-AI 변환 (ENV-BAREMETAL) | X | X | △ | X | X | FRFconv-TDSNet + X-CUBE-AI 변환; 8-class shaft fault (Healthy/Looseness/Misalignment×3/Unbalance×3); f_s=16 kHz, W=2048, T_W=128 ms, H 미정의; quantization bit-width 미기재; accuracy 99.25%; sensing avg 151 ms (SD 5.2 ms) + inference 555.872 ms (SD 0.028 ms) + output 56.158 ms = E2E ~763 ms ≈ 5.96×T_W; Flash 144.69 KiB, SRAM 73.54 KiB | X | X | X | X | B |
| Zhang et al., Fast Short-Time Root-MUSIC [6] | STM32H743 | FreeRTOS | O | X | X | X | X | 알고리즘 최적화 (DNN 없음, Root-MUSIC 단축 계산) | X | X | X | X | B |
| Yang et al., Stacked AE End-Edge [7] | STM32F407-class + edge | Runtime ? | ? | X | △ | X | X | Cascade AE (space↔time 교환) + End-Edge 오프로딩 | △ | O | X | X | B |
| He et al., Cyclostationary Edge FD [8] | STM32F407IGT6 (168 MHz, 192 KB RAM, 2 MB ext. SRAM) | C + FPU + MCU DSP library; OS·RTOS 미기재 (ENV-OTHER) | X | X | △ | X | X | 비DL 알고리즘 최적화: ICFEE(information-curve 기반 optimal band 자동 선택) + spectral correlation density; sound(PCB377C01 mic) + hall speed 비접촉 취득; f_s=5 kHz, W=5000 samples, T_W=1 s; pipeline 합계 10.294 s (spectral correlation 9.196 s, 89.3%) >> T_W; 논문은 deadline miss로 다루지 않고 future optimization으로 인정; % accuracy 없음, qualitative identification만 | X | X | X | X | B |
| Pubalan et al., Simulated 1D-CNN [9] | PC (CPU·GPU 사양 미보고); 실 embedded target 없음 | MATLAB App Designer; OS 미보고 (ENV-OTHER) | X | X | △ | X | X | Physics-based W 설계: $W=60f_s/\mathrm{RPM}=1602$ samples at 1797 rpm, 48 kHz; $T_W\approx33.4$ ms; H 미정의; 1D CNN 4-block (filter 32→128, GAP, FC-64); per-prediction latency 0.03 s; accuracy 97.37% mean ±0.56 (0 HP, 5-run); param·FLOPs·model size 미보고; CWRU data PC replay (실 hardware 없음) | X | X | X | X | B |
| Arciniegas et al., TinyML Motor Vibration [10] | XIAO ESP32S3 Sense (Xtensa LX7 dual-core) + MPU6050 | OS 미기재; Edge Impulse firmware (ENV-OTHER) | X | X | △ | X | X | INT8 PTQ + matrix factorization pruning + K-means anomaly detection; W=16, H=8, f_s=100 Hz (고정); DNN 3-class (Stopped/Average-speed/High-speed); avg inference 25 ms (SD 3 ms); E2E ~300 ms (collection 80 ms + inference 25 ms + network+alert 195 ms); accuracy 96.5% lab, 98% industrial | X | X | X | X | B |
| Gupta and Shivhare, TinyML ESP32 [11] | ESP32 + ADXL345 | OS·runtime 미기재 (TFLite 여부 불명) | X | X | △ | X | X | INT8 post-training quantization; 1D CNN 13 ms·91.4%·224 KB vs CNN-LSTM 26 ms·93.6%·352 KB (Table 4); W=256, H=128, f_s=1 kHz 고정; "adaptive sampling" 주장이나 구현 확인 불가 | X | X | X | X | B |
| Lima, Edge Impulse Motor FD [12] | Arduino Nano 33 BLE (nRF52840, Cortex-M4, 64 MHz, 256 KB RAM) | Edge Impulse firmware + EON Compiler; OS·TFLite Micro 여부 미보고 (ENV-OTHER) | X | X | △ | X | X | EON Tuner offline grid search: $f_s$ {100,250,500,1000 Hz} × $T_W$ {1,2 s} × $T_H$ {250–2000 ms} × DSP (FFT/Haar/Bior1.3) × ANN depth/width × {FP32, INT8}; 4-bar 최적: $f_s$=250 Hz, $T_W$=1 s, $T_H$=500 ms, 98.6%/27 ms FP32 → 98.1%/1 ms INT8; 1-bar 최적: $f_s$=1000 Hz, $T_W$=1 s, $T_H$=250 ms, 95.8%/39 ms FP32 → 68.3% INT8; RAM 1.4/1.6 KB, Flash 14.5/21.4 KB; 고정 배포 | X | X | X | X | B |
| Alasiry et al., Dual-MCU Monitoring [13] | STM32F103 + ESP32 | Runtime ? | ? | X | X | X | X | 없음 (ML 없음, threshold 기반) | X | X | X | X | B |
| Zhan et al., APTL-net [14] | Jetson Xavier NX | Ubuntu 20.04; JetPack 5.1.2; TensorRT 8.5.1.7 | X | X | X | X | X | Triple-lightweight: recursive inference + FDD weight-sharing multiscale conv + dependency-aware structured pruning (offline training-time, not runtime); 0.96 M params, 10.81 G FLOPs (50% pruned); avg 14.782 ms forward-pass, TensorRT 16.588 ms (SD 9.227 ms) | X | X | X | X | B |
| Garay et al., Multimodal TinyML [15] | Cortex-M4F + gateway | Arduino Mbed OS | O | X | X | △ | X | INT8 PTQ + TFLite Micro + ASIC (NDP120) | X | X | X | X | B |
| Langarica et al., Industrial Internet FD [16] | IIoT edge + server | Linux/server stack | X | X | X | X | X | 없음 (signal processing cascade) | X | △ | X | X | B |
| Shan et al., CS-DKELM [17] | Zynq UltraScale+ MPSoC XCZU9EG | Linux; Python 3.8; PyTorch 1.7.0 (CUDA 기재되나 Zynq에 NVIDIA GPU 없어 환경 불명확) | X | X | △ | X | X | 압축 센싱 (CR=80%, N=4800→M=960) + reconstruction 없는 직접 분류 + DKELM (ELM-AE + RBF kernel); "100 ms industry requirement" 주장하나 physical avg 170 ms로 초과; per-window latency 경계 불명확 | X | X | X | X | B |
| Sayghe, Physics-Aware Transformer [18] | Raspberry Pi 4 | Linux (OS 미기재); ONNX Runtime 1.16 | X | X | X | X | X | 물리 인식 경량 Transformer (overlapping Conv-Stem + physics-guided patch P=⌈f_s/f_min⌉) + ONNX Runtime; 0.52M param; avg 43.6 ms (1000 calls) | X | X | X | X | B |
| Bhaventhan et al., Vibration PdM [19] | Raspberry Pi 4 | Linux (OS 미기재) | X | X | △ | X | X | 없음 (원문 미명시; 표준 CNN 직접 실행 추정) | X | X | X | X | B |
| Asutkar et al., TinyML TL Domain Generalization [20] | ESP32 + Raspberry Pi 4B | TFLite (Arduino IDE) / TF (Pi) | X | X | X | X | X | 통계 특징 10개 (raw→(10×1) 압축) + TFLite + 2498 파라미터 경량 CNN | X | X | X | X | B |
| KCC 2026 system [self-reference 확인 필요] | MCU | Zephyr RTOS | O | X | O | O | △ | 양자화 + Zephyr RTOS 최적화 | O | X | X | X | E |
| Proposed work | Pi Zero 2W | Linux + PREEMPT_RT | X | P | P | P | P | - | P | P | P* | P | Target E; H requires formal analysis |

`P*`: 초기 연구 범위는 joint `W/H`를 코어로 두고 `M`은 고정하거나 제한된 보조 변수로 두는 안을 우선 검토한다.

## Deadline 컬럼 판정 기준

| 판정 | 의미 |
| --- | --- |
| O | Deadline을 명시적으로 정의하고 이를 기준으로 평가함 |
| △ | Period/Window/Acquisition duration은 존재하여 deadline처럼 해석 가능하지만, 논문이 deadline으로 선언하거나 miss를 측정하지 않음 |
| X | Period나 시간 기준 자체를 제시하지 않음 |

## RT Level

- H: explicit deadline과 보수적 execution-time bound에 기반한 schedulability/admission guarantee
- W: bounded deadline miss를 보장하는 weakly-hard 접근
- E: deadline과 tail/miss를 측정하지만 formal guarantee는 없음
- B: average latency, throughput 또는 acquisition interval 대비 처리시간 중심의 best-effort 접근

## Caption Draft

Comparison of real-time support in embedded machine fault-diagnosis studies. Model-level optimization is common in the currently reviewed studies, whereas explicit deadlines, system-level scheduling, and runtime adaptation are limited or absent. The proposed features remain targets pending implementation and schedulability validation.

## 작성 주의

- Proposed work의 `P`는 실험과 분석 완료 전까지 O로 바꾸지 않는다.
- “기존 연구에는 scheduling이 없다”가 아니라 “정의한 검색 범위와 판정 기준에서 확인한 direct RT-FD 문헌에는 제한적이었다”로 쓴다.
- RTOS, average latency 또는 observed max만으로 hard real-time을 주장하지 않는다.
- 최종 원고에는 직접 비교군 5~8편만 남기고, 경량화 대조군과 scheduling bridge를 본문에서 각각 설명한다.
- Platform tag는 우선순위가 아니라 external-validity 정보다. 직접성은 fault-diagnosis domain, runtime variable, trigger, deadline과 guarantee로 판단한다.

## 참고문헌

[1] S. Ma, H. Sun, S. Gao, and G. Zhou, "A Real-Time Mechanical Fault Diagnosis Approach Based on Lightweight Architecture Search Considering Industrial Edge Deployments," *Engineering Applications of Artificial Intelligence*, 2023.

[2] S. Lee and T. Kim, "FRFconv-TDSNet: Lightweight, Noise-Robust Convolutional Neural Network Leveraging Full-Receptive-Field Convolution and Time-Domain Statistics for Intelligent Machine Fault Diagnosis," *IEEE Transactions on Instrumentation and Measurement*, 2024.

[3] T. Jalonen, M. Al-Sa'd, S. Kiranyaz, and M. Gabbouj, "Real-Time Vibration-Based Bearing Fault Diagnosis Under Time-Varying Speed Conditions," *IEEE ICIT*, 2024, doi: 10.1109/ICIT58233.2024.10540813.

[4] Y. R. Thota, M. Afshar, S. Boden, B. Dunlap, B. Akin, and T. Nikoubin, "TinyML Enabled Real-Time Bearing Fault Classification in Motors Using Vibration Signals," *GLSVLSI*, 2025.

[5] S. Choi, S. Kim, and T. Kim, "저비용 마이크로컨트롤러 환경에서의 경량 딥러닝 기반 회전기계 축 결함 진단 시스템," *한국소프트웨어종합학술대회 논문집*, 2025.

[6] H. Zhang, B. Liu, W. Feng, and Z. Li, "A Novel Fast Short-Time Root-MUSIC Method for Vibration Monitoring of High-Speed Spindles," arXiv:2506.17600, 2025.

[7] C. Yang, Z. Lai, Y. Wang, S. Lan, L. Wang, and L. Zhu, "A Novel Bearing Fault Diagnosis Method Based on Stacked Autoencoder and End-Edge Collaboration," *IEEE CSCWD*, 2023, doi: 10.1109/CSCWD57460.2023.10152598.

[8] C. He, P. Han, J. Lu, X. Wang, J. Song, Z. Li, and S. Lu, "Real-Time Fault Diagnosis of Motor Bearing via Improved Cyclostationary Analysis Implemented onto Edge Computing System," *IEEE Transactions on Instrumentation and Measurement*, 2023, doi: 10.1109/TIM.2023.3295476.

[9] B. Pubalan, M. S. R. M. Saufi, M. S. Leong, and A. Jamali, "Real-Time Bearing Fault Detection and Visualization Using 1D CNN: A Simulated Deployment with the CWRU Dataset," *IEEE ICSIMA*, 2025, doi: 10.1109/ICSIMA66552.2025.11233248.

[10] S. Arciniegas, D. Rivero, J. Pinan, E. Diaz, and F. Rivas, "IoT Device for Detecting Abnormal Vibrations in Motors Using TinyML," *Discover Internet of Things*, 2025, doi: 10.1007/s43926-025-00142-4.

[11] S. Gupta and S. N. Shivhare, "Embedded TinyML for Predictive Maintenance: Vibration Analysis on ESP32," *International Journal on Computational Modelling Applications*, 2025, doi: 10.63503/j.ijcma.2025.114.

[12] J. P. B. Lima, "Real-Time Fault Detection in Induction Motors Using TinyML: An Evaluation of the Edge Impulse Platform," *IEEE Latin Conference on IoT*, 2025, doi: 10.1109/LCIoT64881.2025.11118459.

[13] A. H. Alasiry, H. H. Saidya, and N. Tamami, "A Dual-Microcontroller IoT-Based Real-Time Monitoring System for Predictive Maintenance of Induction Motors," *IEEE International Electronics Symposium*, 2025, doi: 10.1109/IES67184.2025.11160991.

[14] Z. Zhan, S. Zhang, J. Xu, and D. Ma, "Edge-Oriented Bearing Fault Diagnosis via Triple-Lightweight Network With Adaptive Pruning," *IEEE Transactions on Instrumentation and Measurement*, 2026, doi: 10.1109/TIM.2026.3699722.

[15] C. E. Garay et al., "A Multimodal TinyML-Based Predictive Maintenance Architecture for Industrial IoT in the 6G Era," *Sensors*, 2026, doi: 10.3390/s26144536.

[16] S. Langarica, C. Ruffelmacher, and F. Nunez, "An Industrial Internet Application for Real-Time Fault Diagnosis in Industrial Motors," *IEEE Transactions on Automation Science and Engineering*, 2020, doi: 10.1109/TASE.2019.2913628.

[17] N. Shan, X. Xu, X. Bao, and S. Qiu, "Fast Fault Diagnosis in Industrial Embedded Systems Based on Compressed Sensing and Deep Kernel Extreme Learning Machines," *Sensors*, 2022, doi: 10.3390/s22113997.

[18] A. Sayghe, "A Physics-Aware Lightweight Transformer Network for Intelligent Bearing Fault Diagnosis Under Variable Operating Conditions," *Artificial Intelligence for Engineering*, 2026, doi: 10.1049/aie2.70014.

[19] R. Bhaventhan, X. D. Stanlyraj, and S. Purushothaman, "Vibration-Based Predictive Maintenance for Motors Using Edge AI," *IEEE RAEEUCCI*, 2026, doi: 10.1109/RAEEUCCI67649.2026.11504862.

[20] S. Asutkar, C. Chalke, K. Shivgan, and S. Tallur, "TinyML-enabled edge implementation of transfer learning framework for domain generalization in machine fault diagnosis," *Expert Systems with Applications*, vol. 213, 2023, doi: 10.1016/j.eswa.2022.119016.

### 참고문헌 주의사항

- KCC 2026 system은 본인 선행연구의 저자, 정식 제목과 publication metadata를 확정한 뒤 번호를 부여한다.
- 표의 `[1]`--`[19]`는 현재 비교 행과 1:1로 대응한다.
