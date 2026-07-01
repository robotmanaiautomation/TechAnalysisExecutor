# TechAnalysisExecutor - 진행 상황

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
