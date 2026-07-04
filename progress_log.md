# TechAnalysisExecutor — 진행 로그

> 컨텍스트 오버플로우 시 재개 용도. 각 task를 독립적으로 기록하여 중단 후 재개 가능.
> 현재 진행 task는 **[진행 중]**, 완료된 task는 **[완료]**, 미완료는 **[대기]**.

---

## Phase 1: 프로젝트 스캐폴딩

| # | Task | 상태 | 비고 |
|---|------|------|------|
| 1.1 | 프로젝트 폴더 구조 생성 (app/, app/db/, app/services/, app/routers/, app/models/) | [완료] | uv 기반 venv, setuptools packages 명시 |
| 1.2 | 가상 환경 설정 (uv) 및 의존성 설치 | [완료] | ta로 변경(pandas-ta는 Python 3.12+만), sqlalchemy 추가 |
| 1.3 | FastAPI 기본 서버 코드 (main.py 진입점, uvicorn 설정) | [완료] | 포트 8002, CORS, lifespan에서 BAR DB 초기화 |

## Phase 2: infoGetherAPI DB 연동

| # | Task | 상태 | 비고 |
|---|------|------|------|
| 2.1 | DB 설정 (finance.db 경로 설정, read-only 연결) | [완료] | 상대 경로로 infoGetherAPI data/finance.db 참조 |
| 2.2 | SQLAlchemy 모델 정의 (PriceRecord) | [완료] | FinanceBase: FinancialProduct, PriceRecord |
| 2.3 | DB 세션 관리 (get_db 의존성 인젝션) | [완료] | FinanceSessionLocal + BarSessionLocal |

## Phase 3: BAR 데이터 스토리지 (별도 SQLite)

| # | Task | 상태 | 비고 |
|---|------|------|------|
| 3.1 | BAR 데이터 SQLite 스키마 정의 (bar_data 테이블) | [완료] | BarBase: BarData 모델 정의 |
| 3.2 | BAR 데이터 CRUD 서비스 | [대기] | insert/query/delete |
| 3.3 | CSV 업로드 파싱 서비스 | [대기] | python-multipart + pandas |

## Phase 4: 수익률 계산 서비스 (당장 목표 핵심)

| # | Task | 상태 | 비고 |
|---|------|------|------|
| 4.1 | 티커별 가격 시계열 조회 서비스 (infoGetherAPI DB → pandas DataFrame) | [완료] | fetch_price_series / fetch_price_series_bulk |
| 4.2 | 수익률 계산 로직 (초기 가격 대비 % 변화율) | [완료] | calculate_return — base_price 대비 % |
| 4.3 | 다중 티커 수익률 병합 (모든 티커를 동일 x축으로 alignment) | [완료] | merge_returns — 공통 타임스탬프로 alignment |

## Phase 5: 차트 데이터 생성 (당장 목표 핵심)

| # | Task | 상태 | 비고 |
|---|------|------|------|
| 5.1 | 수익률 선그래프 데이터 생성 (JSON 직렬화: 티커별 날짜+수익률 배열) | [완료] | format_for_chartjs — Chart.js 호환 |
| 5.2 | plotly 기반 수익률 차트 생성 (다중 선그래프) | [완료] | create_plotly_chart — plotly go.Scatter |

## Phase 6: API 엔드포인트 (당장 목표 핵심)

| # | Task | 상태 | 비고 |
|---|------|------|------|
| 6.1 | POST /api/return-chart — 보유 티커 목록 받아 수익률 선그래프 JSON 응답 | [완료] | chartjs/plotly 양방식 지원 |
| 6.2 | GET /api/bar/{ticker} — 티커별 BAR 데이터 조회 | [대기] | |
| 6.3 | POST /api/bar/bulk-fetch — 다중 티커 BAR 데이터 일괄 조회 | [대기] | |
| 6.4 | GET /api/analysis/{ticker} — 기술적 지표 계산 결과 | [대기] | |
| 6.5 | POST /api/analysis/bulk — 다중 티커 기술적 분석 일괄 수행 | [대기] | |
| 6.6 | GET /api/chart/{ticker} — 차트 (JSON/HTML) | [대기] | |

## Phase 7: 기술적 분석 엔진

| # | Task | 상태 | 비고 |
|---|------|------|------|
| 7.1 | pandas-ta 기반 지표 계산 서비스 (SMA, EMA, RSI, MACD, Bollinger Bands) | [대기] | |
| 7.2 | 개별 티커 분석 엔드포인트 구현 | [대기] | |
| 7.3 | 벌크 분석 엔드포인트 구현 | [대기] | |

## Phase 8: BAR 데이터 관리 API

| # | Task | 상태 | 비고 |
|---|------|------|------|
| 8.1 | POST /api/bar/upload — CSV 파일 업로드 | [대기] | |
| 8.2 | DELETE /api/bar/{ticker} — 티커별 BAR 삭제 | [대기] | |

## Phase 9: PortfolioManager 연동 (당장 목표 핵심)

| # | Task | 상태 | 비고 |
|---|------|------|------|
| 9.1 | PortfolioManager 백엔드: GET /portfolios/return-chart — TechAnalysisExecutor 호출 | [대기] | |
| 9.2 | PortfolioManager 프론트엔드: 수익률 추이 차트 뷰 추가 (Chart.js) | [대기] | |

## Phase 10: 테스트 및 배포

| # | Task | 상태 | 비고 |
|---|------|------|------|
| 10.1 | 로컬 테스트 (TechAnalysisExecutor 서버 기동 + 엔드포인트 검증) | [대기] | |
| 10.2 | PortfolioManager ↔ TechAnalysisExecutor 통합 테스트 | [대기] | |
| 10.3 | AnServer 배포 설정 | [대기] | |

---

## 현재 목표

**당장 목표**: PortfolioManager에서 보유 자산들의 수익률 추이를 x축=시간, y축=수익률(%), 선그래프로 표시
**핵심 Phase**: 1 → 2 → 4 → 5 → 6.1 → 9
