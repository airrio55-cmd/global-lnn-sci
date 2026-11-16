# STEP2.9 실행환경과 원본 코드 호환성

확인일: 2026-11-16 (Asia/Seoul). STEP2.7의 `/workspace/venvs/kookmin-step27`를 그대로 사용했다. 설치·업데이트·다운그레이드는 하지 않았다. 지정된 Torch/ncps/hmmlearn 및 기존 환경의 의존성 핀과 현재 버전 차이0건, pip check도 PASS였다.

| 패키지/환경 | 실제 버전 |
|---|---|
| Python | 3.12.14 |
| torch | 2.10.0+cpu |
| ncps | 1.0.1 |
| hmmlearn | 0.3.3 |
| numpy | 2.3.5 |
| pandas | 2.2.3 |
| scikit-learn | 1.8.0 |
| scipy | 1.17.0 |
| future | 1.0.0 |
| sympy | 1.14.0 |
| networkx | 3.7 |
| filelock | 4.2.4 |
| fsspec | 2026.9.0 |
| jinja2 | 3.1.6 |
| MarkupSafe | 3.0.3 |


원본 Notebook Python 메타데이터는3.12.0이고 현재는3.12.14다. 이 차이를 기록했으며 임의로 버전을 변경하지 않았다. 원본 ncps/hmmlearn의 과거 실제 버전은 여전히 미확인이다. 따라서 이번 고정 참조 환경의 호환성 PASS를 과거 환경·성능·checkpoint의 완전 재현으로 주장하지 않는다.

## 실제 실행 조건

Torch2.10.0+cpu, CUDA build=None, CPU tensor, FP32, AMP 비활성이다. GPU 사용 가능 여부 조회나 GPU 이동은 하지 않았다. torch thread1, OMP/MKL/OpenBLAS thread1, 프로세스 시작 전 PYTHONHASHSEED=2, deterministic algorithms=True로 실행했다. 이 설정은 합성 프로세스에만 적용했다.

ncps LTC wrapper/cell의 실제 소스 SHA-256은 기존 참조와 일치한다.

- wrapper: `bbf3127013d3969994ecf0debf4eb37b56db750475ee71646a9decdf1aaf3026`
- cell: `167a9d6e1f4dc653ce21420010709e1c995716e53ad0d8bbc2d53c19c40b123f`

공식 참조는 PyPI ncps1.0.1과 기존 고정 ncps source commit695ec22d7d1831f2ced67346ef7d2f08c525bd47다. 새 패키지 버전으로 바꾸지 않았다. 설치된 constructor signature와 원본의 입력인자를 먼저 확인한 후 원래 RecurrentModel/LNNModel/CfCModel/FocalLoss 정의를 정확한 해시로 재사용했다.

실제 constructor·parameter count·forward/backward·optimizer/scheduler·checkpoint 복원·재현성은 다섯2피처 모델 모두PASS였다. LTC wrapper 제약True와 cell Softplus도 일치했다. dt=1은 원본처럼 한 관측당 수치 step이며, 이번 검사가 물리적 ‘하루’의 시간상수 단위를 입증하지는 않는다.

## 적용 한계

RAW5피처 모델은 정적 parameter count만 확인한 상태다. 원본 RAW/LOG 채널의 서로 다른 피처·시드·실증 입력 정렬이나 전체 실험의 결정성을 검증한 것이 아니다. 같은2피처 shape를 사용하는 향후 F1 구현에 필요한 기초 호환성 증거이며, 실제 가격/PIT/최종 데이터 gate는 별도로 남는다.

환경 상세·버전 차이·원본 코드 한계는 manifests/step29_runtime_environment.json에 기록했다. 실제 금융 데이터·기존 성능표·원본 파일은 변경하지 않았다.
