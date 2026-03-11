---
name: pptx-to-markdown
description: >-
  PowerPoint(.pptx) 강의 슬라이드를 구조화된 markdown으로 변환. 슬라이드 제목/본문/테이블/발표자 노트 추출,
  중첩 리스트 보존, 이미지 플레이스홀더 처리까지 자동화.
  "PPTX를 마크다운으로", "파워포인트 변환", "강의 슬라이드 변환", "pptx 텍스트 추출",
  "슬라이드 markdown 변환", "PPT 변환" 요청 시 사용.
triggers:
  - PPTX를 마크다운으로
  - pptx-to-markdown
  - 파워포인트 변환
  - 강의 슬라이드 변환
  - pptx 텍스트 추출
  - 슬라이드 markdown 변환
  - PPT 변환
argument-hint: "<PPTX_경로>"
---

# PPTX to Markdown

PowerPoint 강의 슬라이드를 구조화된 markdown으로 변환.

## Quick Start

### 단일 파일
```bash
python3 scripts/convert_pptx.py -i lecture.pptx -o lecture.md
```

### 배치 (폴더 내 모든 PPTX)
```bash
python3 scripts/convert_pptx.py --input-dir ./slides/ --output-dir ./markdown/
```

### 슬라이드 범위 지정
```bash
python3 scripts/convert_pptx.py -i lecture.pptx --slides 1-30
```

### 발표자 노트 제외
```bash
python3 scripts/convert_pptx.py -i lecture.pptx --no-notes
```

## Workflow

### 1. 스크립트 실행

`scripts/convert_pptx.py` 실행. 의존성(python-pptx)은 자동 설치됨.

파이프라인:
1. **Load**: python-pptx로 PPTX 파일 열기
2. **Extract**: 슬라이드별 구조 추출
   - Title placeholder → `## Slide N: 제목`
   - Body placeholder bullet → indent level 기반 중첩 리스트 (`-`, `  -`)
   - Subtitle placeholder → 이탤릭 부제목
   - Table shape → markdown pipe table
   - Image/Chart shape → `[이미지: 이름]` / `[차트]` 플레이스홀더
   - Speaker notes → `> **Notes:**` 블록쿼트
3. **Clean**: 빈 슬라이드 제거, 공백 정규화
4. **Output**: 슬라이드별 섹션으로 구성된 markdown 파일 생성

### 2. Claude 정제

스크립트 출력물은 raw markdown. Claude가 읽고 다음을 개선:

1. 출력된 .md 파일을 Read로 읽기
2. 다음 기준으로 정제:
   - 헤딩 계층 구조 수정
   - 리스트 마커 통일
   - 테이블 정렬 및 빈 셀 처리
   - 불필요한 슬라이드 구분선 정리
   - 내용 기반으로 의미 없는 슬라이드 통합
3. 정제된 내용을 같은 파일에 Write

## CLI 옵션

| 옵션 | 단축 | 설명 |
|------|------|------|
| `--input` | `-i` | 입력 PPTX 파일 경로 |
| `--input-dir` | | 배치 모드: 입력 디렉토리 |
| `--output` | `-o` | 출력 markdown 파일 경로 |
| `--output-dir` | | 배치 모드: 출력 디렉토리 |
| `--slides` | | 슬라이드 범위 (예: `1-20`) |
| `--no-notes` | | 발표자 노트 제외 |

## Scripts

- `scripts/convert_pptx.py`: 메인 변환 파이프라인 (load → extract → clean → markdown)
- `scripts/ensure_deps.py`: python-pptx 자동 설치

## Troubleshooting

텍스트 깨짐, 이미지 전용 슬라이드, 복잡한 레이아웃 등의 문제는 [troubleshooting.md](references/troubleshooting.md) 참조.
