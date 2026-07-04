"""
수익률 계산 서비스
티커별 가격 시계열 기반으로 초기 가격 대비 누적 수익률(%)을 계산하고,
다중 티커를 동일 x축(time)으로 alignment하여 반환합니다.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd

from app.services.price_service import (
    fetch_price_series,
    fetch_price_series_bulk,
    get_finance_db_session,
)


def calculate_return(df: pd.DataFrame, base_price: Optional[float] = None) -> pd.DataFrame:
    """
    단일 티커의 누적 수익률 계산.

    Args:
        df: fetch_price_series 결과 DataFrame (columns: timestamp, price)
        base_price: 기준 가격 (None이면 첫 번째 레코드의 가격 사용)

    Returns:
        DataFrame with columns: [timestamp, return_pct]
        return_pct = (price - base_price) / base_price * 100
    """
    if df.empty:
        return pd.DataFrame(columns=["timestamp", "return_pct"])

    if base_price is None:
        base_price = df["price"].iloc[0]

    if base_price == 0:
        return pd.DataFrame(columns=["timestamp", "return_pct"])

    df = df.copy()
    df["return_pct"] = ((df["price"] - base_price) / base_price * 100).round(4)
    return df[["timestamp", "return_pct"]]


def merge_returns(
    returns_by_ticker: Dict[str, pd.DataFrame],
) -> Dict[str, Any]:
    """
    다중 티커 수익률 병합 — 동일 x축(time)으로 alignment.

    Args:
        returns_by_ticker: {ticker: DataFrame(timestamp, return_pct)}

    Returns:
        {
            "timestamps": [str, ...],  # 정렬된 공통 타임스탬프
            "tickers": [str, ...],      # 티커 목록
            "data": {ticker: [float, ...]}  # 티커별 수익률 배열 (NaN 포함)
        }
    """
    # 빈 데이터프레임은 제외
    valid = {t: df for t, df in returns_by_ticker.items() if not df.empty}
    if not valid:
        return {"timestamps": [], "tickers": [], "data": {}}

    # 모든 타임스탬프를 고유한 정렬된 목록으로
    all_timestamps = set()
    for df in valid.values():
        all_timestamps.update(df["timestamp"].tolist())

    timestamps = sorted(all_timestamps)

    # 티커별 수익률을 타임스탬프 인덱스로 alignment
    tickers = list(valid.keys())
    data = {}
    for ticker in tickers:
        df = valid[ticker]
        # timestamp를 인덱스로
        indexed = df.set_index("timestamp")["return_pct"]
        # 공통 타임스탬프로 재인덱싱 (NaN 허용)
        aligned = indexed.reindex(timestamps)
        data[ticker] = aligned.tolist()

    # timestamp를 ISO 문자열로 직렬화
    ts_strings = [ts.isoformat() if isinstance(ts, datetime) else str(ts) for ts in timestamps]

    return {
        "timestamps": ts_strings,
        "tickers": tickers,
        "data": data,
    }


def compute_return_chart(
    tickers: List[str],
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> Dict[str, Any]:
    """
    다중 티커 수익률 차트 데이터 생성 (일괄 처리).

    PortfolioManager에서 호출할 메인 서비스 함수.

    Args:
        tickers: 티커 목록 (symbol)
        start_date: 시작일 (None이면 가장 오래된 데이터부터)
        end_date: 종료일 (None이면 최신까지)

    Returns:
        merge_returns 결과 (JSON 직렬화 가능)
    """
    db = get_finance_db_session()
    try:
        # 1. 티커별 가격 시계열 조회
        price_series = fetch_price_series_bulk(db, tickers, start_date, end_date)

        # 2. 티커별 수익률 계산
        returns = {}
        for ticker, df in price_series.items():
            returns[ticker] = calculate_return(df)

        # 3. 동일 x축 alignment
        chart_data = merge_returns(returns)

        return chart_data
    finally:
        db.close()
