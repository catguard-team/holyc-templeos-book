# macOS · Linux · Windows 실행

필요한 것은 Python 3.10 이상, x86-64 시스템 에뮬레이션을 포함한 QEMU, 압축을 푼 이 저장소입니다. 최소 2.1 GiB의 추가 여유 공간을 확보하세요. 게스트 메모리는 512 MiB입니다. 실행 도구는 설치나 다운로드를 자동 수행하지 않습니다.

## macOS

[QEMU 공식 설치 안내](https://www.qemu.org/download/#macos)에 따라 Homebrew를 사용하는 경우:

```sh
brew install qemu python
cd "/내가/압축을 푼/holyc-templeos-book"
python3 tools/launch.py --doctor
bash Start-mac.command
```

Finder에서 `Start-mac.command`를 실행해도 됩니다. 실행 권한이 보존되지 않은 ZIP이라면 위의 `bash` 방법을 사용하세요. Apple Silicon은 ARM 게스트가 아니라 **x86-64 TCG 에뮬레이션**으로 실행합니다. Intel Mac에도 같은 실행 설정을 제공하지만 이번 검증 호스트는 Apple Silicon입니다.

## Linux

Debian/Ubuntu 예시:

```sh
sudo apt install python3 qemu-system-x86 qemu-system-gui
cd "/내가/압축을 푼/holyc-templeos-book"
python3 tools/launch.py --doctor
bash start-linux.sh
```

배포판별 패키지 이름은 [QEMU 공식 안내](https://www.qemu.org/download/#linux)를 확인하세요. Python 3.10 이상이어야 합니다. 일반 실습은 그래픽 데스크톱 세션에서 실행합니다. 서버·컨테이너에는 화면 서버가 없을 수 있으며, 유지관리용 headless 검증과 일반 GUI 실행은 서로 다른 경로입니다. 이 저장소의 Linux 실측은 ARM64 Debian 컨테이너에서 TCG·QMP 화면 캡처를 사용했습니다.

## Windows

1. [Python 공식 Windows 설치 안내](https://docs.python.org/3/using/windows.html)에 따라 Python 3.10 이상을 설치합니다. 터미널에서 `py -3 --version` 또는 `python --version`이 동작해야 합니다.
2. [QEMU 공식 Windows 다운로드 안내](https://www.qemu.org/download/#windows)를 따라 x86-64 시스템 에뮬레이터가 포함된 빌드를 설치합니다. 예: `C:\Program Files\qemu\qemu-system-x86_64.exe`.
3. 전체 ZIP을 쓰기 가능한 일반 폴더에 풉니다. 압축 폴더 안에서 바로 실행하지 마세요.
4. `Start-Windows.cmd`를 더블클릭합니다. 부트 메뉴에서 `1` → Enter를 누릅니다.

PowerShell에서 직접 진단하거나 경로를 지정할 수도 있습니다.

```powershell
py -3 tools\launch.py --doctor
py -3 tools\launch.py --qemu "C:\Program Files\qemu\qemu-system-x86_64.exe"
```

`py`가 없는 설치라면 `python`으로 바꾸세요. 실행 도구는 PATH와 기본 Program Files 경로를 찾으며 공백·한글 경로를 인수 목록으로 전달합니다. **Windows용 실행 경로는 구현했으나 실제 Windows OS에서의 VM 실행은 미검증**입니다. Windows ARM64와 각 배포 빌드의 오디오 지원도 별도 확인이 필요합니다.

## 공통 사용법

```sh
python3 tools/launch.py --prepare
python3 tools/launch.py --state "새 실습장"
python3 tools/launch.py --sound
```

- `--prepare`: QEMU를 실행하지 않고 압축 디스크를 검증·복원합니다. Python만으로 가능합니다.
- `--doctor`: ISO·압축 디스크 해시와 Python/QEMU 버전을 확인합니다.
- `--dry-run`: 실행할 인수를 JSON으로 출력하고 디스크를 변경하지 않습니다.
- `--state`: 새 경로를 선택하면 별도 실습장이 생깁니다. 기존 경로는 저장된 파일을 보존합니다.
- `--sound`: PC speaker를 macOS CoreAudio, Linux PulseAudio, Windows DirectSound에 연결합니다. 해당 QEMU 빌드가 백엔드를 지원해야 합니다. 실패하면 옵션을 빼고 실행할 수 있습니다.

기본 부팅 대상은 하드디스크 C입니다. 원본 부트로더의 `0`은 이전 부트 레코드이고, `2`는 예제를 넣지 않은 D 시스템입니다. **책 실습은 `1`입니다.** ISO는 원래 장치 구성을 충족하기 위해 CD 드라이브에 그대로 연결합니다.

키보드가 호스트에 붙잡히면 QEMU 창의 안내에 따라 보통 Ctrl+Alt+G로 해제합니다. TempleOS 안에서는 영문 입력을 사용합니다. 편집기 `Ed("FILE.HC");`에서 Esc는 저장, Shift+Esc는 취소입니다. 출력/그래픽이 진행 중인 동안 종료하기보다 명령 프롬프트로 돌아온 뒤 QEMU 창을 닫으세요.

## 보존·문제 해결

`state/`에는 변경되는 사용자 디스크와 초기화 영수증이 들어 있습니다. QEMU가 꺼진 상태에서 폴더 전체를 복사하면 다른 호스트에서도 이어서 실행할 수 있습니다. 다른 위치의 백업은 `--state`로 선택합니다. ZIP 정본을 다시 내려받아도 사용자 디스크를 자동 덮어쓰지 않습니다.

- `QEMU not found`: 설치와 PATH를 확인하거나 `--qemu`를 지정합니다.
- `SHA-256 mismatch`: `python3 tools/verify_archive.py`를 실행하고 정본을 다시 받습니다.
- `already in use`: 같은 실습장을 사용 중인 다른 QEMU가 끝난 뒤 재시도합니다.
- `Existing disk ...`: 기존 파일을 보존하고 새 `--state` 경로로 시작합니다.
- 검은 화면: 첫 부팅에는 시간이 걸릴 수 있습니다. UEFI나 ARM 머신으로 바꾸지 말고 제공된 TCG·`pc`·`qemu64` 설정을 사용합니다.
- 원본 예제 복구: 새 실습장을 만들면 24개 정본을 다시 얻습니다. 사용자 작업 디스크를 삭제할 필요가 없습니다.

이 런처에는 실제 디스크 초기화, 네트워크 연결, 자동 업데이트, VM 설치 마법사 자동 입력 기능이 없습니다. 준비된 이미지 복원과 QEMU 실행만 수행합니다.
