# exam-master

> 강화학습 + 인지과학 기반 Claude Code 시험 준비 스킬

마크다운 강의자료를 분석해 8단계 적응형 시험 준비 루프를 실행합니다.
사전 회상 → 개념 그래프 출제 → 자기 설명 채점 → 간격 반복 복습.

## 설치

```bash
npx skills add Donghyun-Jeong/claude-skills@exam-master
```

## 사용법

Claude Code에서:

```
/exam-master /path/to/lecture-notes/
```

예시:
```
/exam-master ~/Documents/데이터베이스/
/exam-master ~/Documents/알고리즘/week3/
```

## 주요 기능

- **8단계 학습 루프**: 사전 회상 → 개념 추출 → 그래프 구성 → 출제 예측 → 문제 출제 → 채점 → 오답 노트 → 재출제
- **적응형 난이도**: 이전 세션 점수 기반으로 L1~L5 문제 비중 자동 조정
- **간격 반복**: 오답 개념에 `next_review` 날짜 기록, 다음 세션에 자동 포함
- **오답 노트**: `error-notebook.md`에 세션별 오답/부분 정답 누적 저장
- **레이더 차트**: 개념 영역별 점수를 텍스트 시각화

## 요구 사항

- Claude Code + oh-my-claudecode
- 강의자료가 `.md` 형식으로 저장되어 있어야 함 (PDF는 [pdf-to-markdown](../pdf-to-markdown/) 스킬로 먼저 변환)

## 팁

PDF 강의자료가 있다면 먼저 변환:
```
/pdf-to-markdown lecture.pdf -p "강의비밀번호"
/exam-master ./
```
