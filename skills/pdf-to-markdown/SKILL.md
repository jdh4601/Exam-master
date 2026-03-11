---
name: pdf-to-markdown
description: >-
  암호화된 PDF 수업 자료를 깨끗한 structured markdown으로 변환. 비밀번호 제거,
  텍스트 추출(헤딩/리스트/테이블 구조 보존), 정리, LLM 정제까지 자동화.
  "PDF를 마크다운으로", "수업 자료 변환", "PDF 텍스트 추출", "암호 PDF 변환",
  "강의 자료 정리", "PDF markdown 변환" 요청 시 사용.
triggers:
  - PDF를 마크다운으로
  - pdf-to-markdown
  - 수업 자료 변환
  - PDF 텍스트 추출
  - 암호 PDF 변환
  - 강의 자료 정리
  - PDF markdown 변환
argument-hint: "<PDF_경로> [-p <비밀번호>]"
---

# PDF to Markdown

암호화된 PDF 수업 자료를 구조화된 markdown으로 변환.

## Quick Start

### 단일 파일
```bash
python3 scripts/convert_pdf.py -i lecture.pdf -p "PASSWORD" -o lecture.md
```

### 배치 (폴더 내 모든 PDF)
```bash
python3 scripts/convert_pdf.py --input-dir ./pdfs/ -p "PASSWORD" --output-dir ./markdown/
```

### 페이지 범위 지정
```bash
python3 scripts/convert_pdf.py -i lecture.pdf -p "PASSWORD" --pages 1-30
```

## Workflow

### 1. 스크립트 실행

`scripts/convert_pdf.py` 실행. 의존성(pdfplumber)은 자동 설치됨.

파이프라인:
1. **Decrypt**: pypdf로 비밀번호 제거 → 임시 파일 생성
2. **Extract**: pdfplumber로 텍스트 추출 + 구조 감지
   - 폰트 크기 기반 헤딩 감지 (본문 중간값 대비 1.15x~1.6x)
   - 불릿/번호 패턴으로 리스트 감지
   - `extract_tables()`로 테이블 → markdown 파이프 테이블
   - 모노스페이스 폰트 → 코드 블록
3. **Clean**: 반복 헤더/푸터 제거, 인코딩 아티팩트 수정, 공백 정규화
4. **Output**: 구조화된 markdown 파일 생성

### 2. Claude 정제

스크립트 출력물은 raw markdown. Claude가 읽고 다음을 개선:

1. 출력된 .md 파일을 Read로 읽기
2. 다음 기준으로 정제:
   - 헤딩 계층 구조 수정 (h1 → h2 → h3 순서)
   - 리스트 마커 통일 (-, 1., 2.)
   - 테이블 정렬 및 빈 셀 처리
   - 불필요한 줄바꿈 정리
   - 내용 기반으로 누락된 헤딩 추가
3. 정제된 내용을 같은 파일에 Write

정제 프롬프트 예시:
> "이 markdown 파일을 읽고, 수업 자료에 맞게 구조를 개선해줘.
> 헤딩 계층, 리스트, 테이블을 정리하고 AI가 참조하기 좋은 형태로 만들어줘."

## CLI 옵션

| 옵션 | 단축 | 설명 |
|------|------|------|
| `--input` | `-i` | 입력 PDF 파일 경로 |
| `--input-dir` | | 배치 모드: 입력 디렉토리 |
| `--password` | `-p` | PDF 비밀번호 |
| `--output` | `-o` | 출력 markdown 파일 경로 |
| `--output-dir` | | 배치 모드: 출력 디렉토리 |
| `--pages` | | 페이지 범위 (예: `1-10`) |

## Scripts

- `scripts/convert_pdf.py`: 메인 변환 파이프라인 (decrypt → extract → clean → markdown)
- `scripts/ensure_deps.py`: pdfplumber 자동 설치

## Troubleshooting

복호화 실패, 텍스트 깨짐, 테이블 미감지 등의 문제는 [troubleshooting.md](references/troubleshooting.md) 참조.
