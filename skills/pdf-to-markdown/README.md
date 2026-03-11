# pdf-to-markdown

> 암호화된 PDF 수업 자료를 구조화된 Markdown으로 자동 변환하는 Claude Code 스킬

비밀번호 제거 → 텍스트/테이블/헤딩 구조 추출 → Claude 정제까지 원스톱 자동화.

## 설치

```bash
npx skills add Donghyun-Jeong/claude-skills@pdf-to-markdown
```

## 사용법

Claude Code에서 스킬 호출 후, 내부적으로 Python 스크립트를 실행합니다.

```
/pdf-to-markdown lecture.pdf -p "비밀번호"
```

또는 직접 스크립트 실행:

```bash
# 단일 파일
python3 ~/.claude/skills/pdf-to-markdown/scripts/convert_pdf.py \
  -i lecture.pdf -p "PASSWORD" -o lecture.md

# 폴더 전체 배치 변환
python3 ~/.claude/skills/pdf-to-markdown/scripts/convert_pdf.py \
  --input-dir ./pdfs/ -p "PASSWORD" --output-dir ./markdown/

# 페이지 범위 지정
python3 ~/.claude/skills/pdf-to-markdown/scripts/convert_pdf.py \
  -i lecture.pdf -p "PASSWORD" --pages 1-50
```

## 주요 기능

- **자동 복호화**: pypdf로 비밀번호 제거
- **구조 감지**: 폰트 크기 기반 헤딩(h1/h2/h3), 불릿/번호 리스트, 테이블, 코드 블록
- **자동 정제**: 반복 헤더/푸터 제거, 인코딩 아티팩트 수정
- **Claude 정제**: 추출 후 Claude가 헤딩 계층·테이블·리스트 구조를 최종 정리
- **배치 모드**: 폴더 내 모든 PDF를 한 번에 처리

## 요구 사항

- Python 3.9+
- 의존성은 첫 실행 시 자동 설치: `pdfplumber`, `pypdf`

## 변환 흐름

```
PDF (암호화) → decrypt → extract → clean → raw .md → Claude 정제 → 최종 .md
```

## 이 스킬과 함께 사용하면 좋은 스킬

변환된 마크다운으로 바로 시험 준비:

```
/pdf-to-markdown lecture.pdf -p "비밀번호"
/exam-master ./
```

## 문제 해결

[troubleshooting.md](references/troubleshooting.md) 참조.
