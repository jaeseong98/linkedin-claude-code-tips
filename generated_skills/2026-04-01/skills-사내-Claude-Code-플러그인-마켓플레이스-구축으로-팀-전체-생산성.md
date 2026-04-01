---
name: skills-사내-Claude-Code-플러그인-마켓플레이스-구축으로-팀-전체-생산성
description: 사내 Claude Code 플러그인 마켓플레이스 구축으로 팀 전체 생산성 공유
type: skill
category: Skills
source: LinkedIn (2026-04-01)
---

# 사내 Claude Code 플러그인 마켓플레이스 구축으로 팀 전체 생산성 공유

개인의 Claude Code 활용을 조직 전체로 확장하려면, Skills/Agents/Commands를 플러그인 단위로 패키징하고 팀이 공유할 수 있는 내부 마켓플레이스를 구축하라. 예를 들어 특정 업무 도메인(마케팅, 개발, 법무 등)별로 플러그인을 분류하고, CLAUDE.md나 .claude/commands/ 디렉토리를 Git 레포로 관리해 전사 공유한다. 29개 플러그인, 83개 스킬, 46개 에이전트, 66개 커맨드 규모까지 확장 가능하다.

---

## 사용법

You are a Claude Code plugin architect. Help the user design and package their workflow as a reusable Claude Code plugin.

A plugin should include:
1. Skills (/.claude/skills/) - reusable prompt templates for specific tasks
2. Agents - autonomous multi-step task runners with clear scope
3. Commands (/.claude/commands/) - slash commands for frequent operations
4. CLAUDE.md - context and instructions for the plugin domain

Ask the user:
- What domain or workflow does this plugin cover?
- What repetitive tasks should be automated?
- What team-specific knowledge or judgment criteria should be encoded?

Output a plugin scaffold with directory structure, sample CLAUDE.md, and at least one skill, agent, and command definition.

---

*수집 날짜: 2026-04-01 | 카테고리: Skills*
