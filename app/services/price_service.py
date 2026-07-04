"""
티커별 가격 시계열 조회 서비스
infoGetherAPI finance.db의 price_records 테이블에서 티커별 가격 데이터를 조회하여
pandas DataFrame으로 반환합니다.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import FinancialProduct, PriceRecord
from app.db.session import FinanceSessionLocal


def get_finance_db_session() -> Session:
    """finance.db 세션 반환 (사용자 측에서 close 책임)"""
    return FinanceSessionLocal()


def fetch_price_series(
    db: Session,
    ticker: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> pd.DataFrame:
    """
    티커별 가격 시계열 조회.

    Args:
        db: finance.db 세션
        ticker: 조회할 티커 (symbol)
        start_date: 시작일 (None이면 가장 오래된 데이터부터)
        end_date: 종료일 (None이면 최신까지)

    Returns:
        DataFrame with columns: [timestamp, price] — index=None (JSON 직렬화용)
    """
    # 티커 → product_id 매핑
    product = db.execute(
        select(FinancialProduct.id).where(FinancialProduct.symbol == ticker)
    ).scalar_one_or_none()

    if product is None:
        return pd.DataFrame(columns=["timestamp", "price"])

    # 가격 데이터 조회
    query = select(PriceRecord).where(PriceRecord.product_id == product)

    if start_date is not None:
        query = query.where(PriceRecord.timestamp >= start_date)
    if end_date is not None:
        query = query.where(PriceRecord.timestamp <= end_date)

    query = query.order_by(PriceRecord.timestamp.asc())

    records = db.execute(query).scalars().all()

    if not records:
        return pd.DataFrame(columns=["timestamp", "price"])

    df = pd.DataFrame([
        {"timestamp": r.timestamp, "price": r.price}
        for r in records
    ])

    return df


def fetch_price_series_bulk(
    db: Session,
    tickers: List[str],
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> dict[str, pd.DataFrame]:
    """
    다중 티커 가격 시계열 일괄 조회.

    Args:
        db: finance.db 세션
        tickers: 조회할 티커 목록
        start_date: 시작일
        end_date: 종료일

    Returns:
        {ticker: DataFrame} — 없는 티커는 빈 DataFrame 포함
    """
    result = {}
    for ticker in tickers:
        result[ticker] = fetch_price_series(db, ticker, start_date, end_date)
    return result
