"""
SQLAlchemy ORM 모델 — finance.db (read-only) + BAR 데이터 스토리지
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import DeclarativeBase

# ── finance.db (infoGetherAPI 공유, read-only) ──

class FinanceBase(DeclarativeBase):
    """finance.db 전용 base"""

class FinancialProduct(FinanceBase):
    __tablename__ = "financial_products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(50), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    product_type = Column(String(50), nullable=False)
    currency = Column(String(10), nullable=True)
    api_source = Column(String(100), nullable=True)
    source = Column(String(50), nullable=True)
    fetch_interval = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class PriceRecord(FinanceBase):
    __tablename__ = "price_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    volume = Column(Float, nullable=True)
    timestamp = Column(DateTime, nullable=False)
    source = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

# ── BAR 데이터 스토리지 (자신 DB, read-write) ──

class BarBase(DeclarativeBase):
    """bar_storage.db 전용 base"""

class BarData(BarBase):
    """BAR 데이터 (OHLCV)"""
    __tablename__ = "bar_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(50), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    open_price = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=True)
    source = Column(String(50), nullable=True)  # 'csv_upload' or 'api_sync'
    created_at = Column(DateTime, server_default=func.now())
