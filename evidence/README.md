# 검증 기록 읽기

2026-11-08 제작·공개 준비 기록입니다. `public-validation.json`이 공개판 실행·보존 검증의 요약이며, 이전 로컬 조판·원본 ISO 실습 기록은 아래 파일에 구분해 보관합니다.

## 공개판 검증

- 준비된 2 GiB FAT32 디스크를 원본 TempleOS 설치기로 생성하고, 예제 24개·QA 파일 2개·시작 파일을 호스트 정본과 바이트 단위 대조했습니다.
- macOS Apple Silicon / QEMU 11.1.3 TCG와 Linux ARM64 Debian / QEMU 7.2.22 TCG에서 압축 정본을 **서로 다른 새 폴더에 복원**했습니다. 폴더 이름에 한글·공백·쉼표를 포함했습니다.
- 각 호스트에서 원래 TempleOS 5.03을 부팅하고 24개 예제를 실행했습니다. 18개 비대화형 출력, 이름 입력, 도형·팔레트, 좌우 이동, 일곱 등불의 켜기·무효 키·초기화를 확인했습니다.
- Linux는 Docker 안의 실제 Linux QEMU 프로세스를 사용한 headless/QMP 검증입니다. Linux 데스크톱의 창 관리자나 물리 키보드·스피커를 시험한 것은 아닙니다.
- Windows는 전용 CMD 실행기와 Python의 Windows 경로/인수 구성 검사를 포함합니다. **Windows 네이티브 부팅과 Windows 오디오 출력은 미검증**입니다. macOS Intel도 이번 실측 호스트가 아닙니다.
- 원고→HTML 생성은 macOS와 Linux에서 완료했습니다. HTML용 글꼴·Markdown 모듈은 저장소에 함께 있습니다.
- 예제의 화면·입력 테스트는 `tests/run_vm_qa.py`, 복원/보존/잠금/무결성 검사는 `tests/test_launcher.py`로 재현합니다. QMP 자동 입력은 호스트 전용 검사 도구이며 일반 사용자는 필요하지 않습니다.

재시작 후 보존, 소리 캡처, 파일 해시 결과는 해당 JSON 및 로그의 실제 결과를 기준으로 합니다. 화면 증거는 `screenshots/`에 있습니다. 이전 이미지 생성 과정에서 빠른 자동 키 입력으로 발생한 입력 오류는 출하 정본과 분리해 로컬에서 수정했으며, 최종 검사는 완성된 정본을 새로 복원해 수행했습니다.

## 원래 책 제작 검증

| 파일 | 대상 |
|---|---|
| `verification.json` | A4 80쪽, 예제 24개, 원고·코드·전체 지면 검수 |
| `native-reopen.json` | InDesign 저장·재열기, 넘침/누락 서체 0, 책갈피·링크 |
| `native-text-comparison.json` | 원고 PDF와 네이티브 PDF의 쪽별 순서 있는 본문 대조 |
| `code-inclusions.json`, `examples-manifest.json` | 예제 정본과 책 코드 포함 범위 |
| `vm-validation.json`, `vm-verified.log` | 초기 macOS 원본 Live ISO + 일회용 전송 디스크의 24개 예제 검사 |
| `sources.json`, `source-manifest.json`, `claim-audit.json` | 출처, 원본 고정 해시, 전기·신앙·기술적 사실의 서술 원칙 |
| `pdf-public-metadata.json` | 공개 PDF의 깨진 제목 메타데이터만 교정. 80쪽 렌더·본문·링크·책갈피 불변 확인 |
| `archive-provenance.json` | 배포 자료의 원본 URL·라이선스·해시 |

이전 기록의 `<original-workspace>` 같은 경로와 과거 보조 파일 참조는 원래 제작 환경을 가리킵니다. 공개 저장소의 구조로 모든 과거 경로를 재현한 것은 아닙니다. 현재 파일 위치는 루트 README와 전체 `archive-manifest.json`을 기준으로 사용하세요. 검증 증거가 있는 범위를 넘겨 운영체제 지원이나 제3자 승인을 주장하지 않습니다.
