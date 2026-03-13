# marp2pptx

[English](README.md) | [日本語](README.ja.md) | [中文](README.zh.md)

[Marp](https://marp.app/) Markdown 슬라이드를 **자동 글꼴 크기 조정** 기능과 함께 PowerPoint (.pptx)로 변환합니다.

## 왜 만들었나요?

Marp는 Markdown으로 슬라이드를 만드는 훌륭한 도구입니다. 하지만 Marp의 기본 PPTX 내보내기 기능으로 생성된 파일은 내부 구조가 엉망이라 실제로 편집하기가 거의 불가능합니다. 도형 배치가 PowerPoint의 기본 콘텐츠 구성 방식과 맞지 않고, 텍스트 상자가 예상대로 동작하지 않으며, 전체 구조가 나중에 급하게 덧붙인 것 같은 느낌입니다.

**marp2pptx**는 완전히 다른 접근 방식을 취합니다. Marp의 HTML 렌더링을 PPTX로 변환하는 대신, Markdown을 직접 파싱하고 python-pptx를 사용하여 처음부터 PowerPoint를 구축합니다. 결과물은 깔끔하고 편집하기 쉬운 PPTX로, 적절하게 구조화된 도형, 가독성을 최대화하는 자동 크기 조정 글꼴, 그리고 완벽한 CJK 지원을 제공합니다.

## 기능

- **글꼴 자동 조정**: 오버플로 없이 가능한 가장 큰 글꼴 크기를 자동 감지
- **CJK 지원**: 전각/반각을 고려한 텍스트 너비 측정
- **ASCII 아트**: `arch-box`로 표시된 코드 블록을 고정폭 글꼴로 픽셀 단위 정확한 이미지로 렌더링
- **테이블 지원**: HTML 및 Markdown 테이블, 줄바꿈을 고려한 높이 추정
- **디자인 설정**: 색상, 글꼴, 글꼴 크기 범위를 YAML 파일로 외부화
- **겹침 감지**: 생성된 도형의 겹침을 자동으로 확인

## 설치

```bash
pip install git+https://github.com/ebibibi/marp2pptx.git
```

### ASCII 아트용 글꼴

CJK 문자가 포함된 ASCII 아트 렌더링에는 고정폭 CJK 글꼴이 필요합니다:

```bash
# Ubuntu/Debian
sudo apt install fonts-ipafont-gothic

# Fedora
sudo dnf install ipa-gothic-fonts
```

사용 가능한 글꼴을 자동으로 감지합니다 (IPAGothic, Noto Sans Mono CJK, MS Gothic, Osaka, DejaVu).

## 사용법

```bash
# 기본
marp2pptx slides.md

# 출력 경로 지정
marp2pptx slides.md -o presentation.pptx

# 겹침 검사 건너뛰기
marp2pptx slides.md --no-check
```

Python 모듈로도 실행 가능:

```bash
python -m marp2pptx slides.md
```

### Python API

```python
from marp2pptx import convert

output_path, slide_count = convert("slides.md")
```

## 디자인 설정

YAML 파일로 디자인을 커스터마이즈할 수 있습니다. 설정 파일 탐색 순서:

1. `<입력파일>.yaml` (예: `slides.md` → `slides.yaml`)
2. 같은 디렉토리의 `marp2pptx.yaml`
3. 기본 내장값

`slides.yaml` 예시:

```yaml
colors:
  accent: "#FF6600"
  text: "#333333"

fonts:
  main: "Arial"
  mono: "Courier New"

font_ranges:
  default: [40, 14, 36]  # [제목 최대, 본문 최소, 본문 최대]
  small: [36, 12, 28]
```

모든 옵션은 [`default.yaml`](src/marp2pptx/default.yaml)을 참조하세요.

## 지원하는 Markdown 문법

- Marp frontmatter (`---` / `marp: true`)
- 슬라이드 구분자 (`---`)
- 클래스 지시문 (`<!-- _class: lead -->`)
- 배경 이미지 (`![bg right:30% 80%](image.png)`)
- 제목 (h1–h3)
- 글머리 기호 목록 (중첩 지원)
- Markdown 및 HTML 테이블
- 코드 블록
- ASCII 아트 블록 (`<div class="arch-box">`)
- 인라인 서식: **굵게**, *기울임*, `코드`, 링크, `<span class="tag-xxx">`

## 라이선스

MIT
