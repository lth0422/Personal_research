# pi_setup

Pi Zero 2W 환경 설정 기록. 재현 가능하도록 버전·명령어를 그대로 남긴다.

---

## 기록해야 할 항목

아래 항목을 확인 후 `env.md`에 채운다.

### OS

```
Raspberry Pi OS Lite 버전:
커널 버전 (uname -r):
아키텍처: aarch64
```

### TFLite 설치

```bash
# 확인 필요: pip wheel 사용 또는 소스 빌드?
# XNNPACK 활성화 여부 확인
python3 -c "import tflite_runtime; print(tflite_runtime.__version__)"
```

### 모델 파일

- `models/frfconv_tdsnet_int8.tflite` — KCC 2026에서 사용한 모델 변환본
- 변환 명령어 또는 변환 스크립트 경로: 확인 필요

### 데이터

- UOS dataset 위치: 확인 필요
- 사용 클래스: 8-class 축 결함, 1400 RPM, 8kHz
- 전처리 방식: raw 진동 → window size 512 → INT8 정규화

### 패키지 목록

```bash
pip freeze > requirements.txt
dpkg -l | grep -E "stress-ng|cyclictest|rt-tests" > sys_packages.txt
```

---

## 체크리스트

- [ ] OS 버전 기록 완료
- [ ] TFLite 설치 및 버전 확인
- [ ] XNNPACK 백엔드 동작 확인
- [ ] 모델 파일 변환 완료
- [ ] UOS dataset 복사 완료
- [ ] stress-ng 설치 확인
- [ ] rt-tests (cyclictest) 설치 확인
