---
name: skills-HWPX 문서 편집을 위한 3단계 Skills 기반 워크플로우
description: HWPX 문서 편집을 위한 3단계 Skills 기반 워크플로우
type: skill
category: Skills
source: LinkedIn (2026-04-02)
---

# HWPX 문서 편집을 위한 3단계 Skills 기반 워크플로우



---

## Usage

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

---

*Collected: 2026-04-02 | Category: Skills*