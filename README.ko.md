# claude-skills

[Claude Code](https://claude.ai/code)용 커스텀 스킬 모음. `skills` CLI로 한 줄에 설치 가능합니다.

→ English README is available at [README.md](README.md).

---

## 스킬 목록

| 스킬 | 설명 |
|------|------|
| [exam-master](skills/exam-master/) | 강화학습 + 인지과학 기반 적응형 시험 준비 |
| [pdf-to-markdown](skills/pdf-to-markdown/) | 암호화 PDF → 구조화 Markdown 자동 변환 |

---

## 사전 요구 사항

스킬을 설치하기 전에 아래 항목을 먼저 준비해주세요.

- **[Claude Code](https://claude.ai/code)** — 스킬이 실행되는 AI 코딩 도구
- **[oh-my-claudecode](https://github.com/chiper-inc/oh-my-claudecode)** — `/스킬이름` 명령어를 가능하게 해주는 스킬 런타임
- **Python 3.9+** — `pdf-to-markdown` 스킬에만 필요

> oh-my-claudecode를 아직 설정하지 않았다면, Claude Code 내에서 `/oh-my-claudecode:omc-setup`을 먼저 실행해주세요.

---

## 설치 방법

### 1. `skills` CLI 설치 (최초 1회)

```bash
npm install -g skills
```

### 2. 원하는 스킬 설치

```bash
# 시험 준비 스킬
npx skills add Donghyun-Jeong/claude-skills@exam-master

# PDF → Markdown 변환 스킬
npx skills add Donghyun-Jeong/claude-skills@pdf-to-markdown
```

### 3. Claude Code에서 바로 사용

```
/exam-master /강의자료/경로/
/pdf-to-markdown lecture.pdf -p "비밀번호"
```

설치 후 즉시 사용할 수 있습니다.

---

## 스킬 상세 설명

### exam-master

> 강화학습 + 인지과학 기반 적응형 시험 준비 스킬

`exam-master`는 강의 자료(Markdown 파일)를 분석하고, **8단계 적응형 학습 루프**를 실행합니다. 간격 반복, 적응형 난이도, 자기 설명 채점을 통해 학습 효과를 극대화합니다.

#### 8단계 실행 흐름

```
Pre-flight   자료 로드 + 간격 반복 복습 스케줄 확인
    ↓
STEP 0       사전 회상 — 지금 알고 있는 것을 먼저 꺼내보기
    ↓
STEP 1       강의 자료 전체에서 핵심 개념 추출
    ↓
STEP 2       개념 그래프 구성 (관계 유형 명시)
    ↓
STEP 3       예상 출제 유형 예측
    ↓
STEP 4       적응형 난이도로 N문제 생성
    ↓
STEP 5       자기 설명 + 문제별 즉시 채점
    ↓
STEP 6       오답 노트 저장 (간격 반복 스케줄 포함)
    ↓
STEP 7       인터리빙 재출제 5문제 → 루프 반복 여부 확인
```

#### 강화학습 원리

- **보상 기반 정책 업데이트**: 맞히면 다음 문제 난이도가 올라가고, 틀리면 낮아집니다.
- **오답 버퍼**: 틀린 개념을 버퍼에 저장하고, 복습 간격을 동적으로 조정합니다 (1일 → 3일 → 7일).
- **연속 오답 벌점**: 같은 개념을 3회 이상 연속으로 틀리면 복습 주기를 더 길게 설정합니다.

#### 인지과학 원리

- **사전 회상 (STEP 0)**: 자료를 읽기 *전에* 먼저 기억을 꺼내봅니다. 수동적으로 다시 읽는 것보다 훨씬 높은 학습 효과(테스팅 효과)를 냅니다.
- **추론 과정 평가**: 최종 답뿐만 아니라 사고 과정도 채점합니다. 메타인지 모니터링을 유도합니다.
- **개념 그래프 (STEP 2)**: 개념 간 관계를 시각적 스키마로 구성해, 단순 암기가 아닌 구조적 이해를 훈련합니다.

#### 난이도 체계

| 레벨 | 유형 | 설명 |
|------|------|------|
| L1 | 암기 | 정의, 이름 답하기 |
| L2 | 설명 | why/how 서술 |
| L3 | 복합 추론 | 2개 이상 개념 연결 |
| L4 | 적용 | 시나리오 설계·응용 |
| L5 | 오개념/함정 | 흔한 오해를 검증하는 역질문 |

#### 사용법

```
/exam-master /강의자료/경로/
```

예시:
```
/exam-master ~/Documents/데이터베이스/
/exam-master ~/Documents/알고리즘/week3/
```

> 강의 자료는 `.md` 형식이어야 합니다. PDF가 있다면 `pdf-to-markdown`으로 먼저 변환해주세요.

**두 스킬 함께 쓰기:**
```
/pdf-to-markdown lecture.pdf -p "비밀번호"
/exam-master ./
```

---

### pdf-to-markdown

> 암호화 PDF를 구조화된 Markdown으로 자동 변환

`pdf-to-markdown`은 복호화 → 텍스트 추출 → 정제 → Claude 정제까지 전체 파이프라인을 자동화합니다. 결과물은 `exam-master`나 다른 도구에서 바로 활용할 수 있는 구조화된 `.md` 파일입니다.

#### 변환 파이프라인

```
PDF (암호화) → 복호화 → 텍스트 추출 → 정제 → raw .md → Claude 정제 → 최종 .md
```

1. **복호화** — `pypdf`로 비밀번호 제거
2. **추출** — `pdfplumber`로 구조 감지하며 텍스트 추출:
   - 폰트 크기 기반 헤딩 감지 (h1/h2/h3)
   - 불릿/번호 리스트 감지
   - 테이블 → Markdown 파이프 테이블
   - 모노스페이스 폰트 → 코드 블록
3. **정제** — 반복 헤더/푸터 제거, 인코딩 아티팩트 수정, 공백 정규화
4. **Claude 정제** — Claude가 raw 출력물을 읽고 헤딩 계층, 테이블 정렬, 리스트 형식을 최종 정리

#### 사용법

**기본 (Claude Code에서):**
```
/pdf-to-markdown lecture.pdf -p "비밀번호"
```

**스크립트 직접 실행:**
```bash
# 단일 파일
python3 ~/.claude/skills/pdf-to-markdown/scripts/convert_pdf.py \
  -i lecture.pdf -p "비밀번호" -o lecture.md

# 폴더 내 모든 PDF 배치 변환
python3 ~/.claude/skills/pdf-to-markdown/scripts/convert_pdf.py \
  --input-dir ./pdfs/ -p "비밀번호" --output-dir ./markdown/

# 페이지 범위 지정
python3 ~/.claude/skills/pdf-to-markdown/scripts/convert_pdf.py \
  -i lecture.pdf -p "비밀번호" --pages 1-50
```

#### CLI 옵션

| 옵션 | 단축 | 설명 |
|------|------|------|
| `--input` | `-i` | 입력 PDF 파일 경로 |
| `--input-dir` | | 배치 모드: 입력 디렉토리 |
| `--password` | `-p` | PDF 비밀번호 |
| `--output` | `-o` | 출력 Markdown 파일 경로 |
| `--output-dir` | | 배치 모드: 출력 디렉토리 |
| `--pages` | | 페이지 범위 (예: `1-50`) |

#### 의존성

Python 의존성(`pdfplumber`, `pypdf`)은 **첫 실행 시 자동으로 설치**됩니다. 별도 설정이 필요 없습니다.

---

## 추천 워크플로우

암호화된 PDF 강의 자료가 있고 시험이 다가오고 있다면:

```bash
# Step 1: 모든 PDF를 Markdown으로 변환
/pdf-to-markdown ./강의자료/ -p "비밀번호"

# Step 2: 적응형 시험 준비 시작
/exam-master ./강의자료/
```

개념 추출, 적응형 문제 출제, 채점, 간격 반복 스케줄 관리까지 Claude가 알아서 처리합니다.

---

## 라이선스

MIT
