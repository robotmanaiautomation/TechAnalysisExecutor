# TechAnalysisExecutor - 진행 상황

## 현재 상태
- **프로젝트 단계**: Phase 1 (스캐폴딩) — docs 서브모듈만 연결됨
- **실제 소스 코드**: 없음
- **pyproject.toml**: 작성됨 (FastAPI, uvicorn, pandas, pandas-ta, plotly 등 의존성 정의)

---

## 요구사항 대 실제 구현 비교 체크리스트

> ⚠️ **현재 프로젝트는 Phase 1 스캐폴딩 단계로, 실제 Python 소스 코드가 전혀 없음.**

### 1. 프로젝트 개요

| 요구사항 | 구현 여부 | 구현 파일 | 비고 |
|----------|-----------|-----------|------|
| 기술적 분석 + 차트 시각화 시스템 | ❌ | — | 소스 코드 없음 |
| 기술적 분석 자동화 (SMA, RSI, MACD 등) | ❌ | — | pandas-ta 의존성만 정의됨 |
| 차트 시각화 (Plotly) | ❌ | — | plotly 의존성만 정의됨 |
| 다양한 데이터 소스 지원 | ❌ | — | — |
| Web API 제공 (FastAPI) | ❌ | — | fastapi 의존성만 정의됨 |

### 2. 데이터 소스

| 요구사항 | 구현 여부 | 구현 파일 | 비고 |
|----------|-----------|-----------|------|
| infoGetherAPI 연동 (127.0.0.1:8000) | ❌ | — | — |
| BAR 데이터 CSV 입력 | ❌ | — | — |

### 3. BAR 데이터 스토리지

| 요구사항 | 구현 여부 | 구현 파일 | 비고 |
|----------|-----------|-----------|------|
| SQLite 스키마 설계 (BAR 데이터 테이블) | ❌ | — | — |
| DB 연결 및 모델 클래스 | ❌ | — | — |
| BAR 데이터 CRUD 함수 | ❌ | — | — |

### 4. API 엔드포인트

| 요구사항 | 구현 여부 | 구현 파일 | 비고 |
|----------|-----------|-----------|------|
| POST /api/bar/upload (CSV 업로드) | ❌ | — | — |
| GET /api/bar/{ticker} (BAR 조회) | ❌ | — | — |
| DELETE /api/bar/{ticker} (BAR 삭제) | ❌ | — | — |
| GET /api/analysis/{ticker} (기술적 분석) | ❌ | — | — |
| GET /api/chart/{ticker} (차트 시각화) | ❌ | — | — |

### 5. 시스템 요구사항

| 요구사항 | 구현 여부 | 구현 파일 | 비고 |
|----------|-----------|-----------|------|
| Python 3.9+ 호환 | ✅ | `pyproject.toml` | requires-python >=3.9 |
| 포트 8002 | ❌ | — | 실제 서버 코드 없음 |
| 호스트 127.0.0.1 | ❌ | — | — |
| SQLite 스토리지 | ❌ | — | — |

### 6. 프로젝트 설정

| 요구사항 | 구현 여부 | 구현 파일 | 비고 |
|----------|-----------|-----------|------|
| GitHub 저장소 + docs 서브모듈 | ✅ | `docs/` | 서브모듈 연결 완료 |
| requirement.md 작성 | ✅ | `requirement.md` | 완료 |
| pyproject.toml 작성 | ✅ | `pyproject.toml` | 의존성 정의 완료 |
| 폴더 구조 생성 | ❌ | — | — |
| 가상 환경 설정 (uv) | ❌ | — | — |
| FastAPI 기본 서버 코드 | ❌ | — | — |

---

## 구현 누락 사항 요약

**전체적으로 구현되지 않음** — Phase 1 스캐폴딩 완료 (docs 서브모듈 연결, requirement.md, pyproject.toml) 이후 중단됨.

1. **프로젝트 폴더 구조** — Python 패키지로 구성되지 않음
2. **가상 환경** — uv 기반 venv 미설정
3. **FastAPI 서버** — 기본 서버 코드 미작성
4. **BAR 데이터 스토리지** — SQLite 스키마, CRUD 미구현
5. **BAR 데이터 API** — 업로드/조회/삭제 엔드포인트 미구현
6. **infoGetherAPI 연동** — 미구현
7. **기술적 분석 엔진** — pandas-ta 기반 지표 계산 미구현
8. **차트 시각화** — plotly 기반 차트 생성 미구현
9. **차트 API** — 차트 응답 엔드포인트 미구현

---

## 마스터 플랜

### Phase 1: 프로젝트 스캐폴딩
- [x] GitHub 저장소 생성 및 docs 서브모듈 연결
- [x] requirement.md 작성
- [ ] 프로젝트 폴더 구조 생성
- [ ] 가상 환경 설정 (uv)
- [ ] FastAPI 기본 서버 코드 작성 및 실행 테스트

### Phase 2: BAR 데이터 스토리지
- [ ] SQLite 스키마 설계 (BAR 데이터 테이블)
- [ ] DB 연결 및 모델 클래스 작성
- [ ] BAR 데이터 CRUD 함수 작성

### Phase 3: BAR 데이터 API
- [ ] POST /api/bar/upload — CSV 업로드 (파일 파싱 + DB 저장)
- [ ] GET /api/bar/{ticker} — 티커별 BAR 데이터 조회
- [ ] DELETE /api/bar/{ticker} — 티커별 BAR 데이터 삭제

### Phase 4: infoGetherAPI 연동
- [ ] infoGetherAPI DB 직접 읽기 (SQLite 연결) 또는 API 조회
- [ ] 데이터 소스 추상화 (infoGetherAPI / CSV BAR 통합)

### Phase 5: 기술적 분석 엔진
- [ ] pandas-ta 기반 지표 계산 함수 (SMA, EMA, RSI, MACD, Bollinger Bands, Stochastic, OBV)
- [ ] 분석 함수: 티커 + 기간 + 지표 목록 → 계산 결과

### Phase 6: 기술적 분석 API
- [ ] GET /api/analysis/{ticker} — 지표 계산 결과 (JSON)

### Phase 7: 차트 시각화
- [ ] mplfinance 기반 차트 생성 함수 (캔들스틱 + 선 차트)
- [ ] 지표 오버레이 기능 (SMA, EMA, Bollinger Bands)

### Phase 8: 차트 API
- [ ] GET /api/chart/{ticker} — 차트 이미지 (PNG) 응답

### Phase 9: 테스트 및 커밋/푸시
- [ ] API 엔드포인트 통합 테스트
- [ ] 커밋 및 GitHub 푸시
