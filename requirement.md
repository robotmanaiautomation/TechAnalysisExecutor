# TechAnalysisExcuter 요구사항

## 프로젝트 개요

infoGetherAPI가 수집한 금융 데이터 + 사용자가 CSV로 추가로 입력하는 BAR 데이터(OHLCV)를 기반으로, 오픈소스 Python 라이브러리를 활용하여 기술적 분석을 수행하고 차트를 시각화하는 시스템.

## 핵심 목적

1. **기술적 분석 자동화**: 이동평균, RSI, MACD, 볼린저밴드 등 주요 지표 계산
2. **차트 시각화**: 가격 차트 + 기술적 지표 오버레이 차트 생성
3. **다양한 데이터 소스 지원**: infoGetherAPI 수집 데이터 + 사용자 CSV 입력
4. **Web API 제공**: 분석 결과와 차트 이미지를 HTTP API로 제공

## 데이터 소스

### 1. infoGetherAPI 연동
- infoGetherAPI(127.0.0.1:8000)에서 수집된 실시간/일별 가격 데이터 조회
- SQLite DB 직접 읽기 또는 API 엔드포인트 활용

### 2. BAR 데이터 (CSV 입력)
- 사용자가 직접 CSV 파일을 업로드하여 BAR 데이터 추가
- 지원 포맷: 날짜, Open, High, Low, Close, Volume (기존 TA 라이브러리 호환)
- 업로드된 BAR 데이터는 별도 스토리지 관리

## 사용 라이브러리

### 기술적 분석
- **TA-Lib** 또는 **pandas-ta**: 주요 기술적 지표 계산
  - 이동평균 (SMA, EMA)
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - 볼린저밴드
  - 스토캐스틱
  - OBV (On-Balance Volume)

### 차트 시각화
- **mplfinance**: 캔들스틱 차트 + 지표 오버레이
- **matplotlib**: 기본 차트 생성 (서버 측 렌더링)

### Web 프레임워크
- **FastAPI**: REST API 서버
- **uvicorn**: ASGI 서버

### 기타
- **pandas**: 시계열 데이터 처리
- **numpy**: 수치 계산

## API 엔드포인트

### BAR 데이터 관리
- `POST /api/bar/upload` — CSV 파일 업로드 (티커명, 데이터 기간 포함)
- `GET /api/bar/{ticker}` — 티커별 BAR 데이터 조회
- `DELETE /api/bar/{ticker}` — 티커별 BAR 데이터 삭제

### 기술적 분석
- `GET /api/analysis/{ticker}` — 기술적 지표 계산 결과 (JSON)
  - 지표 목록 파라미터: `?indicators=rsi,sma,macd`
  - 기간 파라미터: `?days=30` (기본값 30)

### 차트 시각화
- `GET /api/chart/{ticker}` — 차트 이미지 (PNG)
  - 차트 타입: `?type=candle` (캔들스틱) / `?type=line` (선 차트)
  - 오버레이 지표: `?overlay=sma,ema,bb`
  - 기간: `?days=30`

## 시스템 요구사항

- Python 3.9+ 호환 (infoGetherAPI 환경과 일치 — `|` union 연산자 불가, `Optional` 사용)
- 포트: 8002 (infoGetherAPI:8000, PortfolioManager:8001 과 구분)
- 호스트: 127.0.0.1 (로컬 개발)
- SQLite 또는 In-memory 스토리지 (BAR 데이터 관리용)

## 분석 대상

- infoGetherAPI에서 수집하는 10개 티커 (AMD, C, SPCX, GOOG, JPM, KO, TSM, XOM, DGRW, VOO) 자동 지원
- CSV 업로드를 통한 추가 티커 분석 가능

## 향후 확장

- 거래 신호 생성 (매수/매도 신호)
- 백테스팅 기능
- WebSocket 기반 실시간 차트 업데이트
