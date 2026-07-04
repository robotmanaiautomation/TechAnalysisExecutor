"""
TechAnalysisExecutor — FastAPI 진입점
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.db.session import init_bar_db
    init_bar_db()
    yield


app = FastAPI(
    title="TechAnalysisExecutor",
    description="기술적 분석 및 차트 시각화 시스템",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS 설정 — PortfolioManager(8080) 및 로컬 개발 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "TechAnalysisExecutor"}
