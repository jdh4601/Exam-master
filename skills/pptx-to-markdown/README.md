# pptx-to-markdown

> PowerPoint 강의 슬라이드를 구조화된 Markdown으로 자동 변환하는 Claude Code 스킬

슬라이드 제목/본문/테이블 추출 → 발표자 노트 포함 → Claude 정제까지 원스톱 자동화.

## 설치

```bash
npx skills add jdh4601/Exam-master@pptx-to-markdown
```

## 사용법

Claude Code에서 스킬 호출 후, 내부적으로 Python 스크립트를 실행합니다.

```
/pptx-to-markdown lecture.pptx
```

또는 직접 스크립트 실행:

```bash
# 단일 파일
python3 ~/.claude/skills/pptx-to-markdown/scripts/convert_pptx.py \
  -i lecture.pptx -o lecture.md

# 폴더 전체 배치 변환
python3 ~/.claude/skills/pptx-to-markdown/scripts/convert_pptx.py \
  --input-dir ./slides/ --output-dir ./markdown/

# 슬라이드 범위 지정
python3 ~/.claude/skills/pptx-to-markdown/scripts/convert_pptx.py \
  -i lecture.pptx --slides 1-30

# 발표자 노트 제외
python3 ~/.claude/skills/pptx-to-markdown/scripts/convert_pptx.py \
  -i lecture.pptx --no-notes
```

## 주요 기능

- **슬라이드 구조 보존**: 제목 → `## Slide N: 제목`, 본문 bullet → 중첩 리스트
- **발표자 노트 포함**: Speaker notes를 `> Notes:` 블록쿼트로 추출 (강의 자료에 핵심!)
- **테이블 변환**: Table shape를 markdown pipe table로 변환
- **이미지 플레이스홀더**: 이미지/차트를 `[이미지: 이름]` / `[차트]`로 표시
- **Claude 정제**: 추출 후 Claude가 구조를 최종 정리
- **배치 모드**: 폴더 내 모든 PPTX를 한 번에 처리

## 요구 사항

- Python 3.9+
- 의존성은 첫 실행 시 자동 설치: `python-pptx`

## 변환 흐름

```
PPTX → load → extract per slide → clean → raw .md → Claude 정제 → 최종 .md
```

## 출력 예시

```markdown
<!-- source: lecture.pptx | slides: 42 -->

## Slide 1: 운영체제 개요

- 운영체제의 정의
  - 하드웨어와 소프트웨어 사이의 인터페이스
  - 자원 관리자

> **Notes:**
> 오늘 강의의 핵심 개념. 시험에 자주 출제됨.

---

## Slide 2: 프로세스 vs 스레드

| 구분 | 프로세스 | 스레드 |
|------|---------|--------|
| 메모리 | 독립 | 공유 |
| 생성 비용 | 높음 | 낮음 |
```

## 이 스킬과 함께 사용하면 좋은 스킬

변환된 마크다운으로 바로 시험 준비:

```
/pptx-to-markdown lecture.pptx
/exam-master ./
```

## 문제 해결

[troubleshooting.md](references/troubleshooting.md) 참조.
