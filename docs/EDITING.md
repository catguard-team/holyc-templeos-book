# 책과 예제 편집

## 원고 → 오프라인 HTML

`manuscript/content.py`의 `PAGES`가 원고 정본입니다. `tools/build_book.py`는 이를 읽어 `book/index.html`, `manuscript/pages.json`, 코드 포함 대조 기록을 생성합니다.

```sh
python3 tools/build_book.py
```

Windows는 `py -3` 또는 `python`을 사용합니다. Python-Markdown이 `tools/vendor/markdown/`에 들어 있어 pip 설치나 인터넷이 필요하지 않습니다. 그림·스타일·글꼴도 로컬 파일을 참조합니다. `book/`만 따로 옮기면 상위의 `assets/fonts/`를 찾을 수 없으므로 전체 폴더를 함께 보관하세요.

공개 글꼴은 Noto Sans KR과 IBM Plex Mono입니다. HTML은 화면과 브라우저 인쇄에 사용할 수 있으나 글꼴·브라우저 조판 차이 때문에 기존 InDesign PDF와 줄바꿈·페이지 수가 같다는 보장은 없습니다. 이 릴리스의 인쇄 정본은 `book/HOLYC_TEMPLEOS_A4.pdf` 80쪽입니다.

## InDesign 원본

- `editable/indesign/HOLYC_TEMPLEOS_A4.indd`: Adobe InDesign 2026 (21.6)에서 저장하고 다시 연 원본.
- `editable/indesign/HOLYC_TEMPLEOS_A4.idml`: 교환·이전 버전용 원본. 버전에 따라 재조판이 필요할 수 있습니다.
- 두 파일 모두 텍스트·도형을 편집할 수 있습니다. 책은 벡터 도형과 텍스트 중심이며 원본 글꼴 프로그램은 포함하지 않습니다.

원래 조판에 사용한 윤디자인 글꼴은 해당 라이선스를 가진 macOS/Windows 환경에서 사용하세요. 없으면 InDesign의 글꼴 찾기/바꾸기로 대체한 뒤 overset과 페이지 나눔을 다시 점검합니다. Noto Sans KR 등 공개 글꼴을 제공하지만 완전히 같은 조판이 되지는 않습니다. 포함된 PDF의 임베딩 서체를 추출·재배포하는 경로는 제공하지 않습니다.

Linux에는 Adobe InDesign 네이티브 버전이 없습니다. Linux에서의 편집·재생성은 원고/HTML 경로입니다. 원고를 수정한다고 기존 INDD/PDF가 자동 갱신되지는 않습니다. 출판용 PDF를 변경할 때는 InDesign 편집본과 원고를 함께 맞추고 출력물을 검수하세요.

## 예제 수정

호스트의 `examples/*.HC`는 UTF-8/ASCII·LF 정본입니다. TempleOS의 `C:/Home/Book/*.HC`는 출하 시 같은 바이트를 복사한 독립 파일입니다. 호스트와 게스트 사이에 공유 폴더나 자동 동기화를 설정하지 않았습니다.

가장 쉬운 실습은 VM 안에서 `Ed("MYWORK.HC");`로 새 파일을 작성하고 Esc로 저장한 뒤 `#include "MYWORK.HC";`로 실행하는 것입니다. 이미 정의한 전역 변수·함수를 반복 수정하다 충돌하면 새 터미널 작업이나 VM 재시작으로 깨끗한 세션을 만드세요.

유지관리자가 전체 정본을 갱신할 때는 `docs/ARCHIVE.md`의 이미지 생성 절차를 사용합니다. 출하용 이미지를 바꿀 때 예제 바이트 일치, 새 실습장 복원, 실제 부팅, 재시작 후 파일 유지와 전체 해시 목록을 다시 검증합니다.
