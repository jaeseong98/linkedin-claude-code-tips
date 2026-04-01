---
name: skills-동일-프롬프트-흐름을-3회-이상-반복하면-즉시-Skill로-만들기
description: 동일 프롬프트 흐름을 3회 이상 반복하면 즉시 Skill로 만들기
type: skill
category: Skills
source: LinkedIn (2026-04-01)
---

# 동일 프롬프트 흐름을 3회 이상 반복하면 즉시 Skill로 만들기

'세 번 이상 반복되면 스킬로 만들어 두세요'는 원칙을 실천한다. 자주 쓰는 프롬프트 패턴(예: 엔티티 생성 → 리포지토리 → 서비스 → 컨트롤러 순서로 CRUD 생성)을 /project:슬래시명령어로 저장해두면, 매번 긴 지시를 타이핑하지 않고 단일 커맨드로 재현할 수 있다. .claude/commands/ 디렉터리에 마크다운 파일로 관리한다.

---

## 사용법

당신은 Spring Boot 프로젝트의 CRUD 레이어를 일관되게 생성하는 전문가입니다.

다음 순서로 코드를 생성하세요:
1. JPA Entity 클래스 (CLAUDE.md의 네이밍 규칙 준수)
2. Spring Data JPA Repository interface
3. Service interface + ServiceImpl 클래스
4. RestController (DTO 분리)
5. 각 레이어별 단위 테스트

대상 도메인: $ARGUMENTS

생성 전 반드시 CLAUDE.md를 확인하여 프로젝트 규칙을 따르세요.

---

*수집 날짜: 2026-04-01 | 카테고리: Skills*
