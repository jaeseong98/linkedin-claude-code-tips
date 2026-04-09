# 2026-04-07 Skill Execution Report

*Executed at: 2026-04-07T20:09:58.950537*

## 1. tmux 기반 멀티 Claude Code 오케스트레이션으로 사람 병목 제거

**추천 이유:** 유일한 후보

**실행 프롬프트:**
```
# tmux 기반 멀티 Claude Code 오케스트레이터 구성

## 언제 사용하나
여러 Claude Code 에이전트를 동시에 운영하면서 에이전트 간 맥락 전달이 필요할 때. 사람이 컨텍스트 스위칭 병목이 되는 상황을 해소하고 싶을 때.

## 구성 방법
1. tmux session/window/pane으로 에이전트 위계를 설계한다 (조직구조처럼 정보의 위계를 둔다)
2. 각 pane에서 독립적인 Claude Code 인스턴스를 실행한다
3. 세션 간 메시징은 `tmux send-keys -t <target-pane>` 으로 처리한다
4. 큰 맥락은 파일로 작성 후 파일 경로와 함께 핸드오프한다
5. 원격 에이전트가 필요하면 tmux 세션에 ssh를 열어 리모트 Claude Code와 통신한다

## Gotchas
- tmux send-keys의 문자열 이스케이프에 주의 (특수문자, 줄바꿈)
- 에이전트 수가 많아지면 pane 관리가 복잡해지므로 session/window/pane 네이밍 컨벤션을 미리 정할 것
- 각 에이전트의 컨텍스트 윈도우 한계를 고려해 핸드오프 파일 크기를 적절히 관리할 것
```

**실행 결과:**

파일 쓰기 권한이 필요합니다. 승인해 주시면 파일을 생성하겠습니다. 

생성할 파일들과 전체 적용 결과를 먼저 마크다운으로 정리해 드리겠습니다.

---

# tmux 기반 멀티 Claude Code 오케스트레이션 — 적용 결과

## 프로젝트 매핑

현재 `daily_job.py`의 **8단계 순차 파이프라인**을 4개의 독립 Claude Code 에이전트로 분리합니다.

```
기존 (단일 프로세스, 순차 실행):
  Step 1~8 → 한 번에 하나씩, 사람이 모니터링

적용 후 (tmux 멀티 에이전트):
  ┌─────────────────────────────────────────────────────┐
  │ tmux session: linkedin-tips                         │
  │                                                     │
  │  Window 0: orchestrator  ← 실시간 모니터링 대시보드 │
  │  Window 1: scraper       ← 크롤링 에이전트          │
  │  Window 2: analyzer      ← 분석 에이전트            │
  │  Window 3: skill-gen     ← Skill 생성 에이전트      │
  │  Window 4: publisher     ← 마켓플레이스 배포        │
  │                                                     │
  │  핸드오프: handoff/*.flag 파일 기반 자동 대기/시작   │
  └─────────────────────────────────────────────────────┘
```

## 생성 파일 (3개)

### 1. `scripts/tmux_orchestrator.sh` — 메인 오케스트레이터

| 항목 | 설명 |
|------|------|
| **역할** | tmux 세션 생성 → 에이전트 프롬프트 생성 → 4개 에이전트 동시 실행 |
| **핸드오프** | `handoff/` 디렉터리에 `.flag` 파일로 단계 완료 신호 전달 |
| **모니터링** | Window 0에서 `watch -n 5`로 플래그/산출물 실시간 감시 |

**실행 옵션:**
```bash
bash scripts/tmux_orchestrator.sh           # 전체 4-agent 파이프라인
bash scripts/tmux_orchestrator.sh --scrape   # 크롤링만
bash scripts/tmux_orchestrator.sh --analyze  # 분석만
bash scripts/tmux_orchestrator.sh --attach   # 기존 세션 연결
```

**에이전트 흐름:**
```
scraper ──flag──► analyzer ──flag──► skill-gen ──flag──► publisher
  (즉시)     (대기→시작)      (대기→시작)       (대기→시작)
```

### 2. `scripts/tmux_status.sh` — 상태 확인 유틸리티

세션 밖에서 파이프라인 진행 상태를 한눈에 확인:
```bash
bash scripts/tmux_status.sh
# 출력 예:
#  [ON] tmux 세션: 실행 중
#  -- 핸드오프 플래그 --
#    [v] Step 1: 크롤링 완료 (15개)
#    [v] Step 2: 분석 완료
#    [ ] Step 3: Skill 생성 완료
#    [ ] Step 4: 배포 완료
```

### 3. `scripts/tmux_cleanup.sh` — 정리 스크립트

tmux 세션 종료 + 핸드오프 파일을 `handoff/archive/YYYY-MM-DD/`로 아카이브:
```bash
bash scripts/tmux_cleanup.sh
```

## 핸드오프 프로토콜

| 파일 | 생산자 | 소비자 | 내용 |
|------|--------|--------|------|
| `handoff/prompt_*.md` | orchestrator | 각 에이전트 | 역할별 지시사항 |
| `handoff/scrape_result.json` | scraper | analyzer | 크롤링 원본 데이터 |
| `handoff/scraper_done.flag` | scraper | analyzer | 완료 신호 + 건수 |
| `handoff/analysis_result.json` | analyzer | skill-gen | 분석 결과 |
| `handoff/analyzer_done.flag` | analyzer | skill-gen | 완료 신호 |
| `handoff/skillgen_done.flag` | skill-gen | publisher | 완료 신호 |
| `handoff/pipeline_done.flag` | publisher | monitor | 전체 완료 |

## 네이밍 컨벤션

```
Session:  linkedin-tips
Window:   {역할} (orchestrator, scraper, analyzer, skill-gen, publisher)
Flag:     {역할}_done.flag
Prompt:   prompt_{역할}.md
Archive:  handoff/archive/YYYY-MM-DD/
```

## tmux 키보드 단축키 가이드

| 키 | 동작 |
|----|------|
| `Ctrl+B` → `0~4` | 윈도우(에이전트) 전환 |
| `Ctrl+B` → `n/p` | 다음/이전 윈도우 |
| `Ctrl+B` → `d` | 세션 분리 (백그라운드 유지) |
| `Ctrl+B` → `w` | 윈도우 목록 보기 |

## Gotchas (주의사항)

1. **tmux 설치 필요** — Windows에서는 WSL 또는 MSYS2에서 실행
2. **`tmux send-keys` 이스케이프** — 프롬프트에 `'`(작은따옴표) 포함 시 `'\''`로 이스케이프
3. **컨텍스트 윈도우 한계** — 핸드오프 JSON은 필요한 필드만 포함 (전체 게시글 본문 X, 요약만 전달)
4. **`.gitignore` 업데이트 필요** — `handoff/` 디렉터리 추가 권장
5. **동시 실행 아님** — 핸드오프 기반 순차 실행이지만, 각 에이전트가 독립 컨텍스트를 가져 **사람이 윈도우를 오가며 개입할 필요 없음** → 병목 제거

## CLAUDE.md 추가 권장 내용

```markdown
## tmux 멀티 에이전트 오케스트레이션
- `bash scripts/tmux_orchestrator.sh`로 4-agent 파이프라인 실행
- 핸드오프: `handoff/` 디렉터리 (`.flag` 파일 기반 신호 전달)
- 상태 확인: `bash scripts/tmux_status.sh`
- 정리: `bash scripts/tmux_cleanup.sh`
```

---

> **파일 쓰기 권한을 승인해 주시면** 위 3개 스크립트 파일(`tmux_orchestrator.sh`, `tmux_status.sh`, `tmux_cleanup.sh`)을 `scripts/` 디렉터리에 생성하고, `.gitignore`에 `handoff/` 항목을 추가하겠습니다.

---
