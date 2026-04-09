---
name: skills-QGIS 스킬 패키지를 설치해 자연어로 공간데이터 작업 자동화
description: QGIS 스킬 패키지를 설치해 자연어로 공간데이터 작업 자동화
type: skill
category: Skills
source: LinkedIn (2026-04-02)
---

# QGIS 스킬 패키지를 설치해 자연어로 공간데이터 작업 자동화



---

## Usage

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

---

*Collected: 2026-04-02 | Category: Skills*