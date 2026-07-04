"""
DB 세션 관리 — finance.db (read-only) + bar_storage.db (read-write)
"""
from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.db.database import FINANCE_DB_URL, BAR_DB_URL, BAR_DB_PATH

# ── finance.db (infoGetherAPI 공유 — read-only) ──

finance_engine = create_engine(
    FINANCE_DB_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)
FinanceSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=finance_engine,
)

# ── BAR 데이터 스토리지 (자신 DB — read-write) ──

bar_engine = create_engine(
    BAR_DB_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)
BarSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=bar_engine,
)


def get_finance_db() -> Session:
    """finance.db 세션 의존성 인젝션 (read-only)"""
    db = FinanceSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_bar_db() -> Session:
    """bar_storage.db 세션 의존성 인젝션 (read-write)"""
    db = BarSessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_bar_db():
    """BAR 데이터 DB 스키마 생성"""
    from app.db.models import BarBase
    BAR_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    BarBase.metadata.create_all(bind=bar_engine)
