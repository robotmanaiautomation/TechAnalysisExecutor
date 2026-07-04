"""
수익률 차트 생성 서비스
수익률 계산 결과를 Chart.js 호환 포맷과 plotly figure로 변환합니다.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

from app.services.return_service import compute_return_chart


def format_for_chartjs(
    chart_data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Chart.js 호환 포맷으로 변환.

    Args:
        chart_data: compute_return_chart 결과

    Returns:
        {
            "labels": [str, ...],       # 타임스탬프 문자열
            "datasets": [
                {
                    "label": "AAPL",
                    "data": [float, ...],  # NaN은 null로
                    "borderColor": "...",
                    "backgroundColor": "rgba(..., 0.1)"
                }, ...
            ]
        }
    """
    colors = [
        "rgba(54, 162, 235, 1)",   # Blue
        "rgba(255, 99, 132, 1)",    # Red
        "rgba(75, 192, 192, 1)",    # Teal
        "rgba(255, 206, 86, 1)",    # Yellow
        "rgba(153, 102, 255, 1)",   # Purple
        "rgba(255, 159, 64, 1)",    # Orange
        "rgba(199, 199, 199, 1)",   # Gray
        "rgba(83, 102, 255, 1)",    # Indigo
    ]

    labels = chart_data["timestamps"]
    tickers = chart_data["tickers"]
    data = chart_data["data"]

    datasets = []
    for i, ticker in enumerate(tickers):
        values = data.get(ticker, [])
        # NaN을 null로 변환 (Chart.js에서 끊김 처리)
        cleaned = [None if (v != v) else v for v in values]  # NaN check

        color = colors[i % len(colors)]
        datasets.append({
            "label": ticker,
            "data": cleaned,
            "borderColor": color,
            "backgroundColor": color.replace("1)", "0.1)"),
            "tension": 0.1,
            "fill": False,
        })

    return {
        "labels": labels,
        "datasets": datasets,
    }


def create_plotly_chart(
    chart_data: Dict[str, Any],
    title: str = "수익률 추이",
) -> Dict[str, Any]:
    """
    plotly 기반 수익률 차트 생성 (다중 선그래프).

    Args:
        chart_data: compute_return_chart 결과
        title: 차트 제목

    Returns:
        plotly figure JSON (to_json() 결과)
    """
    timestamps = chart_data["timestamps"]
    tickers = chart_data["tickers"]
    data = chart_data["data"]

    if not tickers or not timestamps:
        # 빈 데이터 — 기본 빈 차트 반환
        fig = go.Figure()
        fig.update_layout(
            title=title,
            xaxis_title="시간",
            yaxis_title="수익률 (%)",
        )
        return pio.to_json(fig)

    # 타임스탬프 파싱
    parsed_times = []
    for ts in timestamps:
        try:
            parsed_times.append(pd.to_datetime(ts))
        except Exception:
            parsed_times.append(pd.NaT)

    fig = go.Figure()

    colors = px.colors.qualitative.Set1

    for i, ticker in enumerate(tickers):
        values = data.get(ticker, [])
        # NaN을 None으로 — plotly는 None을 끊김으로 처리
        cleaned = [None if (v != v) else v for v in values]

        color = colors[i % len(colors)]
        fig.add_trace(go.Scatter(
            x=parsed_times,
            y=cleaned,
            mode="lines",
            name=ticker,
            line=dict(color=color, width=2),
            connectgaps=False,
        ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        xaxis_title="시간",
        yaxis_title="수익률 (%)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        template="plotly_white",
        height=400,
    )

    return pio.to_json(fig)


def generate_return_chart(
    tickers: List[str],
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    chart_type: str = "chartjs",  # "chartjs" | "plotly"
) -> Dict[str, Any]:
    """
    수익률 차트 데이터 생성 (엔드포인트에서 호출).

    Args:
        tickers: 티커 목록
        start_date: 시작일
        end_date: 종료일
        chart_type: 차트 포맷 ("chartjs" 또는 "plotly")

    Returns:
        chart_type에 따른 차트 데이터
    """
    # 1. 수익률 계산 + alignment
    chart_data = compute_return_chart(tickers, start_date, end_date)

    # 2. 포맷 변환
    if chart_type == "plotly":
        return create_plotly_chart(chart_data)
    else:
        return format_for_chartjs(chart_data)
