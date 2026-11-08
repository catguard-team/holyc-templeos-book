# 이용허락과 제3자 고지

## 프로젝트의 CC0 선언

책의 새 한국어 설명, 신규 HolyC 예제 24개, 새 편집 디자인과 자체 도구를 [CC0 1.0 Universal](../LICENSE)로 공개합니다. 원고·PDF·INDD/IDML·HTML에서도 우리가 권리를 가진 부분에 같은 선언을 적용합니다. 이를 이용하는 데 출처 표시나 동일조건 공유를 의무로 요구하지 않습니다.

CC0는 다른 권리자의 저작물·상표·서체 프로그램을 재허락하는 선언이 아닙니다. 인용문과 원본 화면 등에는 아래 원본 조건이 적용되며, 전기적 서술의 출처는 `evidence/sources.json`과 책 말미에 있습니다. 공식 명칭을 설명 목적으로 사용하며 원저자·유족·보존 관리자의 승인을 주장하지 않습니다.

## TempleOS / HolyC

- 원저자: Terry A. Davis.
- [공식 보존 홈페이지](https://templeos.org/)의 public-domain 안내와 원본 파일의 고지를 유지합니다.
- `archive/templeos/TempleOS.ISO`는 변경하지 않은 원본입니다.
- `archive/templeos/source-c26482b.tar.gz`는 [cia-foundation/TempleOS](https://github.com/cia-foundation/TempleOS)의 고정 커밋 소스입니다. 이는 원저자의 소스를 보존하는 미러이며 이 책의 신규 저작물은 아닙니다.
- 준비된 실습 디스크는 원본 설치 프로그램으로 설치한 시스템에 `C:/Home/Book` 및 `C:/Home/Once.HC`를 추가했습니다. 원본 코드의 지위와 추가 파일의 CC0를 구분합니다.

## QEMU

QEMU는 여러 저자의 자유 소프트웨어입니다. 전체 프로젝트는 GPL v2 기반이며 일부 파일/하위 프로젝트는 별도 조건을 가집니다. [공식 설명](https://www.qemu.org/docs/master/about/license.html), `licenses/QEMU-COPYING.txt`, `licenses/QEMU-LICENSE.txt` 및 아카이브 내부 고지를 함께 읽으세요. **QEMU를 CC0로 바꾸지 않습니다.**

11.1.3 공식 소스 tarball을 바이트 변경 없이 분할 보관합니다. 바이너리를 수정하거나 번들링한 배포가 아닙니다. 각 플랫폼에 설치한 QEMU 바이너리의 라이선스·대응 소스는 해당 배포자의 안내를 따릅니다. Linux 검사에 사용한 Debian QEMU 7.2.22는 실습 호스트 도구이며 이 저장소에 그 바이너리를 배포하지 않습니다.

## 공개 글꼴

| 파일 | 원본 | 조건 |
|---|---|---|
| `NotoSansKR-Variable.ttf` | [Google Fonts / Noto Sans KR](https://github.com/google/fonts/tree/main/ofl/notosanskr) | SIL Open Font License 1.1, `licenses/NotoSansKR-OFL.txt` |
| `IBMPlexMono-Regular.ttf` | [Google Fonts / IBM Plex Mono](https://github.com/google/fonts/tree/main/ofl/ibmplexmono) | SIL Open Font License 1.1, `licenses/IBMPlexMono-OFL.txt` |

이름을 바꾼 것은 배포 파일 경로뿐이며 폰트 프로그램 바이트를 수정하지 않았습니다. 글꼴 자체의 수정·배포는 각 OFL 고지와 Reserved Font Name 조건을 따르세요.

## 조판본의 상용 글꼴

원본 InDesign/PDF는 적법하게 설치된 윤디자인 서체로 조판했습니다. 상용 폰트 프로그램은 이 저장소에 별도 파일로 넣지 않았습니다. PDF의 임베딩 데이터와 INDD/IDML의 서체 참조가 폰트 프로그램의 CC0 공개를 뜻하지 않습니다. 원래 서체로 편집하려면 별도의 이용 권한이 필요합니다. 공개 글꼴 HTML 경로를 대안으로 제공합니다.

## Python-Markdown

`tools/vendor/markdown/`은 Python-Markdown 3.9의 실행용 Python 모듈입니다. [공식 프로젝트](https://github.com/Python-Markdown/markdown), `licenses/Python-Markdown-BSD.md`에 명시된 BSD 계열 조건을 유지합니다. 캐시·실행 환경은 제외하고 원본 모듈을 보관했습니다.

Python 인터프리터·Adobe InDesign·호스트 운영체제·설치 관리자는 이 저장소에 포함하지 않으며 각자의 이용 조건을 따릅니다.
