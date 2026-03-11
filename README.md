# claude-skills

Claude Code용 커스텀 스킬 모음. `npx skills` CLI로 한 줄 설치 가능.

## 스킬 목록

| 스킬 | 설명 | 설치 |
|------|------|------|
| [exam-master](skills/exam-master/) | 강화학습 + 인지과학 기반 시험 준비 | `npx skills add Donghyun-Jeong/claude-skills@exam-master` |
| [pdf-to-markdown](skills/pdf-to-markdown/) | 암호화 PDF → 구조화 Markdown 변환 | `npx skills add Donghyun-Jeong/claude-skills@pdf-to-markdown` |

## 빠른 시작

```bash
# skills CLI 설치 (최초 1회)
npm install -g skills

# 스킬 설치
npx skills add Donghyun-Jeong/claude-skills@exam-master
npx skills add Donghyun-Jeong/claude-skills@pdf-to-markdown
```

설치 후 Claude Code에서 바로 사용:

```
/exam-master /path/to/lecture-notes/
/pdf-to-markdown lecture.pdf -p "PASSWORD"
```

## 요구 사항

- [Claude Code](https://claude.ai/code)
- [oh-my-claudecode](https://github.com/username/oh-my-claudecode) (스킬 시스템 제공)
- Python 3.9+ (pdf-to-markdown 전용)
