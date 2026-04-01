# 목표
`data/2026-04-01.json`을 읽어서 skill_worthy가 true인 팁들만 모아
`reports/2026-04-01-skill-report.md` 파일을 생성하라.

# 보고서 형식
- 제목: "# 2026-04-01 Skill 후보 보고서"
- 카테고리별로 섹션 구분 (## Agent, ## Config, ## Skills, ## MCP ...)
- 각 팁마다: 제목(###), 내용, skill_template
- 마지막에 "## 요약" 섹션: 총 카테고리별 개수 표

# 완료 조건
`reports/2026-04-01-skill-report.md` 파일이 존재하면 종료.
파일이 이미 존재하면 아무것도 하지 말고 "이미 완료됨"을 출력하고 종료.
