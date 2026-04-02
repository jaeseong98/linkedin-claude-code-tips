# 2026-04-02 Skill Report

## Agent

### 제네릭 컴포넌트를 DB에 저장해 AI가 기존 코드를 자율 재활용하게 만들기



**skill_template:**
```
PostgreSQL 등 로컬 DB에 제네릭 컴포넌트(유틸 함수, 공통 모듈, 아키텍처 패턴)를 저장하고, Claude Code 에이전트가 새 태스크 수행 전 DB에서 관련 기존 코드를 검색·로드하여 재활용하는 파이프라인을 구성하라. MCP 서버를 통해 DB 조회 도구를 에이전트에 연결하고, CLAUDE.md에 '새 기능 구현 전 반드시 기존 제네릭 컴포넌트 DB를 조회할 것'이라는 규칙을 명시하라.
```

---

## MCP

### Figma MCP 서버로 Claude Code에서 피그마 캔버스 직접 수정하기



**skill_template:**
```
# Figma MCP 서버 연동으로 디자인 파일 직접 수정하기

## When to use
피그마 디자인 파일의 컴포넌트를 Claude Code에서 직접 생성·수정하고 싶을 때.

## Steps
1. Figma 공식 MCP 서버를 Claude Code에 등록한다.
2. use_figma 도구를 통해 대상 피그마 파일에 접근한다.
3. 디자인 시스템·색상 변수·컴포넌트 구조를 캔버스에서 참조하며 작업한다.

## Gotchas
- Figma API 토큰 권한(read/write)을 사전에 확인할 것.
- 대규모 파일은 응답 시간이 길어질 수 있으므로 페이지 단위로 접근 권장.
```

---

### MCP --channels 옵션으로 디스코드/텔레그램 메시지 전송 연동



**skill_template:**
```
name: mcp-discord-telegram-channel
description: MCP --channels 옵션을 활용해 Claude Code 실행 결과를 Discord/Telegram 채널로 자동 전송하는 워크플로우 설정 가이드
instructions: |
  1. MCP 서버 설정에서 --channels 플래그를 추가한다.
  2. 대상 채널(Discord webhook URL 또는 Telegram bot token + chat_id)을 환경변수로 등록한다.
  3. Claude Code 실행 완료 후 결과 요약을 해당 채널로 전송하는 파이프라인을 구성한다.
```

---

## Prompting

### 시니어 역할 프롬프트로 코드베이스 전체 리뷰·QA 수행



**skill_template:**
```
# 시니어 엔지니어 코드 리뷰 + QA 스킬

## 사용 시점
1차 기능 구현 완료 후 전체 코드베이스를 점검하고 싶을 때 사용한다.

## 단계
1단계 - 시니어 엔지니어 리뷰: 코드베이스 전체를 읽고 성능 병목, 코드 중복, 접근성 이슈를 진단한 뒤 우선순위별 리팩토링 계획을 작성하라.
2단계 - QA 리드 테스트: 전체 파이프라인의 엣지 케이스, 에러 처리 누락, 데이터 검증 미비 등을 심각도(Critical/High/Medium/Low) 순으로 정리하라.

## Gotchas
- 대규모 코드베이스에서는 모듈 단위로 나눠서 리뷰할 것
- 리팩토링 계획은 바로 실행하지 말고 사용자 확인 후 진행
```

---

### Progressive Disclosure 패턴으로 컨텍스트를 단계적으로 공개하라



**skill_template:**
```
Progressive Disclosure(점진적 공개) 패턴으로 스킬을 설계하라. 에이전트에게 모든 정보를 한 번에 주입하지 말고, 작업 단계별로 필요한 컨텍스트만 점진적으로 공개한다. 1단계: 핵심 규칙과 목표만 제시, 2단계: 구체적 파일·API 스펙 제공, 3단계: 엣지케이스와 예외 처리 안내. 이렇게 하면 토큰 소비를 줄이면서도 에이전트의 정확도를 유지할 수 있다.
```

---

## Skills

### HWPX 문서 편집을 위한 3단계 Skills 기반 워크플로우



**skill_template:**
```
# HWPX 문서 생성 Skill

## 트리거
TRIGGER when: 사용자가 HWPX 또는 한글 파일 생성·편집을 요청할 때

## 사전 조건
- hwpx owpml 모델 레포(한컴 공식)가 로컬에 클론되어 있어야 함
- 편집 대상 HWPX 양식 파일이 준비되어 있어야 함

## 실행 단계
1. owpml 모델 레포를 참조하여 HWPX XML 구조(section, paragraph, run, table 등)를 파악한다.
2. 대상 양식 HWPX 파일을 unzip하여 내부 XML을 분석하고, 각 섹션·표·스타일 매핑을 정리한다.
3. 분석 결과를 기반으로 Python 스크립트(zipfile + xml.etree)를 작성하여 HWPX 문서를 프로그래밍 방식으로 생성·편집한다.
4. 생성된 HWPX 파일을 한컴오피스에서 열어 검증할 수 있도록 경로를 안내한다.

## Gotchas
- HWPX는 ZIP 아카이브이므로 직접 텍스트 편집이 불가하며 반드시 unzip→XML 편집→rezip 과정을 거쳐야 한다.
- owpml 스키마 버전에 따라 태그명이 다를 수 있으므로 대상 파일의 실제 XML을 우선 참조한다.
```

---

### 슬래시(/) 커맨드로 반복 프롬프트를 자동화하라



**skill_template:**
```
# 슬래시 커맨드 활용 가이드

TRIGGER: 사용자가 반복적인 프롬프트 패턴을 입력하거나, 슬래시 커맨드 사용법을 물을 때

## 핵심 원칙
- 3회 이상 반복되는 프롬프트 흐름은 즉시 커스텀 슬래시 커맨드(Skill)로 전환하라
- ~/.claude/commands/ 디렉터리에 .md 파일로 커맨드를 정의하면 /커맨드명 으로 호출 가능
- 프로젝트별 커맨드는 .claude/commands/ 에 저장하여 팀원과 공유 가능

## 사용 예시
- /compact: 긴 대화 컨텍스트 압축
- /review: 코드 리뷰 자동화
- 커스텀 커맨드: 프로젝트 특화 워크플로우 자동 실행
```

---

### 사내 GitHub에 개인 스킬·도구 공유 + 슬랙 배포로 팀 생산성 공유



**skill_template:**
```
사내 Claude Code 플러그인 마켓플레이스를 구축하라. 각 팀원이 만든 Skill 파일(.md)을 사내 GitHub 레포의 skills/ 디렉터리에 PR로 올리고, 슬랙 웹훅으로 신규 스킬 등록 알림을 자동 발송한다. 스킬 파일에는 반드시 name, description, trigger 조건, 사용 예시를 포함해야 한다.
```

---

### QGIS 스킬 패키지를 설치해 자연어로 공간데이터 작업 자동화



**skill_template:**
```
# QGIS GIS 작업 자동화 스킬

TRIGGER: 사용자가 shp, geojson, gpkg 등 공간데이터 파일 처리를 요청하거나, 좌표계 변환, 공간 연산, 지오코딩 등 GIS 관련 작업을 요청할 때

## 사전 조건
- QGIS가 설치되어 있어야 함
- Python에서 qgis.core, osgeo(GDAL/OGR) 모듈 사용 가능해야 함

## 주요 기능
1. 공간 데이터 사전 검수: 좌표계, 속성 구조, 피처 수 확인
2. 좌표계 변환: 단일/일괄 EPSG 변환
3. 포맷 변환: SHP ↔ GeoJSON ↔ GeoPackage
4. 속성 기반 필터링 + 공간 연산 (Buffer, Intersect, Dissolve, Within)
5. 지오코딩: 주소 → 좌표 변환 (VWorld API 등)
6. Geometry 검수 및 오류 수정
7. QGIS 프로젝트 파일(.qgz) 자동 생성
8. 좌표 컬럼으로 LineString geometry 생성

## Gotchas
- 좌표계 미지정 데이터는 반드시 사전 확인 후 처리
- 대용량 파일은 메모리 이슈 가능, 청크 처리 고려
- VWorld 등 외부 API 키는 스킬에 저장해두면 반복 사용 가능
```

---

### 기능명세 입력 시 엣지케이스를 자동 분류하는 스킬 만들기



**skill_template:**
```
# Edge Case Analyzer Skill

## 트리거
사용자가 기능명세 또는 스펙 문서를 입력하고 엣지케이스 분석을 요청할 때

## 지시사항
1. 입력된 기능명세를 파싱하여 주요 플로우를 식별하라.
2. 각 플로우에서 발생 가능한 엣지케이스를 다음 카테고리로 분류하라: 초기화 오류, 세션/인증 오류, 외부 API 오류, 상태값 변이, 네트워크/스트리밍 오류, 결과 처리 오류.
3. 각 엣지케이스에 심각도(높음/중간/낮음)를 부여하라.
4. 결과를 트리 형태의 Mermaid 다이어그램으로 출력하라. 각 노드는 '오류 케이스 → 현재 처리 상태 → 권장 해결 방안' 구조를 따른다.
5. 심각도 '높음' 항목은 빨간색, '중간'은 주황색, '낮음'은 초록색으로 표시하라.

## Gotchas
- 도메인 특화 엣지케이스(결제, 인증 등)는 기능명세에 명시되지 않아도 관련 키워드가 있으면 추론하여 포함할 것.
- 모든 케이스를 완벽히 커버하지 못할 수 있으므로, 출력 마지막에 '추가 검토 권장 영역'을 별도로 안내할 것.
```

---

### 스킬/슬래시 명령 프론트매터에 effort 필드 추가



**skill_template:**
```
name: skill-effort-frontmatter
description: 스킬 프론트매터에 effort 레벨을 지정해 에이전트 추론 깊이를 제어하는 패턴
instructions: |
  스킬 파일 상단 프론트매터에 다음과 같이 effort를 명시한다:
  ---
  effort: quick | medium | thorough
  ---
  quick: 단순 조회·포맷팅 작업에 적합
  medium: 일반적인 코드 생성·리팩터링
  thorough: 아키텍처 설계·복잡한 디버깅에 사용
```

---

## Summary

| Category | Count |
|----------|-------|
| Agent | 1 |
| MCP | 2 |
| Prompting | 2 |
| Skills | 6 |
| **Total** | **11** |