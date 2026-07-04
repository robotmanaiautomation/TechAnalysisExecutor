"""
수익률 차트 API 엔드포인트
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.chart_service import generate_return_chart

router = APIRouter(prefix="/api", tags=["return-chart"])


class ReturnChartRequest(BaseModel):
    """수익률 차트 요청 바디"""
    tickers: List[str]
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    chart_type: str = "chartjs"


@router.post("/return-chart")
def post_return_chart(request: ReturnChartRequest):
    """
    보유 티커 목록을 받아 수익률 선그래프 데이터를 반환.

    - tickers: 티커 목록 (symbol)
    - start_date: 시작일 (ISO 형식, 선택)
    - end_date: 종료일 (ISO 형식, 선택)
    - chart_type: 차트 포맷 ("chartjs" 또는 "plotly", 기본: chartjs)
    """
    if not request.tickers:
        raise HTTPException(status_code=400, detail="tickers는 비워둘 수 없습니다")

    start_date = None
    end_date = None

    if request.start_date:
        try:
            start_date = datetime.fromisoformat(request.start_date)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"start_date 형식 오류: {request.start_date} (ISO 형식 필요)",
            )

    if request.end_date:
        try:
            end_date = datetime.fromisoformat(request.end_date)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"end_date 형식 오류: {request.end_date} (ISO 형식 필요)",
            )

    chart_data = generate_return_chart(
        tickers=request.tickers,
        start_date=start_date,
        end_date=end_date,
        chart_type=request.chart_type,
    )

    return {
        "status": "ok",
        "chart_type": request.chart_type,
        "data": chart_data,
    }
