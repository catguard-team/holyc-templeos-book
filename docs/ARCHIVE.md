# 보존·무결성 검사·복원

이 저장소와 릴리스 ZIP에는 책, 편집 원본, 예제, 원본 ISO, 고정된 TempleOS 소스, 준비된 실습 디스크, QEMU 소스, 공개 글꼴, HTML 생성 의존성이 들어 있습니다. `git clone`만으로 파일을 얻으며 LFS·서브모듈·외부 다운로드 후크를 사용하지 않습니다.

## 전체 파일 검사

```sh
python3 tools/verify_archive.py
```

Windows에서는 `py -3`을 사용합니다. `archive-manifest.json`에 기록된 정본의 경로·크기·SHA-256을 검사합니다. 새로 생성되는 `state/`, `dist/`, Git 메타데이터·캐시는 대상이 아닙니다. 원고나 코드를 수정했다면 해당 파일의 정본 해시와 달라지는 것이 정상입니다. 이 목록은 무결성 대조용이며 출판자의 전자서명은 아닙니다.

## 원본 TempleOS

- 원본 ISO: `archive/templeos/TempleOS.ISO`
- 다운로드 출처: [TempleOS Downloads](https://templeos.org/Downloads/)
- SHA-256: `5d0fc944e5d89c155c0fc17c148646715bc1db6fa5750c0b913772cfec19ba26`
- 소스 미러: [cia-foundation/TempleOS](https://github.com/cia-foundation/TempleOS)
- 고정 커밋: `c26482bb6ad3f80106d28504ec5db3c6a360732c`
- 전체 소스: `archive/templeos/source-c26482b.tar.gz` (`git archive`로 생성, Git 이력 제외)

ISO와 미러 소스는 각각 보존한 자료입니다. 미러 커밋으로 ISO를 비트 단위 재현했다고 주장하지 않습니다. ISO 안에는 원저자의 소스·도움말·게임이 함께 들어 있습니다. 책의 인물 관련 외부 기사·동영상 전체는 재배포하지 않고 서지와 URL로 안내합니다.

## 준비된 실습 디스크

`runtime/TempleOS-book.img.gz`는 새 2 GiB 파일에 원본 ISO의 설치 프로그램을 실행하고, 예제 폴더와 시작 파일만 추가한 디스크입니다. 원본 커널이나 언어 구현을 책에 맞춰 바꾸지 않았습니다. `runtime/manifest.json`에 압축본과 복원본의 크기·SHA-256을 기록합니다.

첫 실행은 새 `state/TempleOS.img`로 복원한 뒤 전체 해시를 확인합니다. 이후에는 수정된 사용자 디스크를 그대로 사용합니다. `initialized.json`은 초기 복원의 기록이며 사용 후 디스크를 정본 해시로 되돌리는 장치가 아닙니다. 디스크가 정상인지 진단하는 파일시스템 검사 도구도 아닙니다.

유지관리자는 VM을 닫은 뒤 `python3 tools/check_guest_files.py state/TempleOS.img`로 출하 예제 24개·QA 파일 2개·시작 파일의 바이트를 대조할 수 있습니다. 예제를 직접 수정한 사용자 디스크는 이 대조에서 차이가 나는 것이 정상입니다.

출하 이미지 생성 기록:

1. 새 2 GiB sparse raw 파일을 만들고 QEMU `pc`, `qemu64`, TCG, 512 MiB, IDE에 연결.
2. 원본 ISO로 부팅하고 설치 마법사에서 빈 가상 디스크에 설치. 원본 MBR과 C/D 시스템 유지.
3. `tools/fat32_image.py`로 새 전송 이미지 생성. `examples/*.HC`, `tools/guest/START.HC`, `tools/guest/SETUP.HC`, `tests/guest/*.HC`와 ASCII README를 포함.
4. 전송 이미지를 IDE primary slave에 연결. 원본 C로 부팅하고 `Mount;`로 해당 가상 장치를 E에 마운트.
5. `#include "E:/SETUP.HC";` 실행. `C:/Home/Book`, 그 아래 `QA`, 시작 파일 `C:/Home/Once.HC`만 추가. SETUP은 기존 READY 표시가 있으면 거부.
6. VM을 닫고 전송 이미지를 제거. ISO는 CD에 유지. C 부팅과 예제 바이트 일치를 확인.
7. 정지된 디스크를 gzip(mtime=0)으로 보관하고 새 디렉터리에 복원하여 실제 부팅·예제·재시작 후 저장을 검사.

이 절차는 유지관리용이며 일반 사용자는 설치 마법사를 실행할 필요가 없습니다. `SETUP.HC`를 개인 작업 디스크에 실행하지 마세요. 변경 이력 전체를 재현하는 자동 빌더는 아니며 출하 디스크 자체와 구성 소스를 함께 보관하는 방식입니다.

## QEMU 원본 소스 복원

QEMU 11.1.3 공식 소스 tarball을 GitHub 개별 파일 한도 안에서 보관하기 위해 48 MiB 단위로 나눴습니다. 복원 명령:

```sh
python3 tools/restore_qemu_source.py "qemu-11.1.3.tar.xz"
```

각 조각과 합친 파일의 크기·SHA-256을 검사하며 기존 출력 파일을 덮어쓰지 않습니다. 원본 전체 크기는 141,819,712바이트이고 SHA-256은 `5a8289c7940dc77d3873c81a6c29ba3afe1446fc9d36e77fa1658cdbecb84b22`입니다.

출처는 [QEMU 공식 배포 서버](https://download.qemu.org/qemu-11.1.3.tar.xz)입니다. 분리 서명과 공개 키도 함께 보관합니다. 별도의 임시 GPG 키 저장소에서 다음 fingerprint의 유효한 서명을 확인했습니다.

```text
CEACC9E15534EBABB82D3FA03353C9CEF108B584
```

이는 보존된 tarball에 대한 서명 검증이며 개인 신뢰망 설정을 대신하지 않습니다. 소스 빌드에 필요한 컴파일러·시스템 라이브러리·각 운영체제의 전체 패키지 미러는 보관하지 않습니다. 일반 실행에는 공식 안내를 따라 QEMU를 설치하는 방법을 권합니다.

## 완전한 오프라인 사용의 경계

다운로드 완료 후 책 읽기, HTML 재생성, 디스크 복원에는 로컬 Python만 필요합니다. TempleOS 실습에는 로컬 QEMU가 추가로 필요합니다. 설치된 도구가 있으면 이 기능들은 외부 서버·API·패키지 설치에 의존하지 않습니다.

호스트 운영체제, Python/QEMU의 플랫폼별 설치 프로그램, Adobe InDesign, 상용 서체, 인용 기사/영상 전체, Python/QEMU 빌드 의존성의 전체 저장소는 포함하지 않습니다. 컴퓨터 손실까지 대비하려면 사용하는 호스트 설치 미디어와 Python/QEMU 설치 패키지도 각 배포자의 조건에 맞게 별도로 보관하세요.

## 릴리스 제작

```sh
python3 -m unittest discover -s tests -v
python3 tools/build_book.py
python3 tools/make_release.py
python3 tools/verify_archive.py
```

`make_release.py`는 로컬 정본 파일의 목록과 `dist/holyc-templeos-book-v1.0.0.zip`, 체크섬을 만듭니다. 업로드나 Git 작업, 유료 호출, CI를 실행하지 않습니다. 릴리스 전 실제 호스트 검증 범위와 `evidence/README.md`를 함께 갱신하세요.
