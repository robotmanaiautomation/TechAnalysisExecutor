"""
DB 설정 — infoGetherAPI finance.db (read-only) + 자체 BAR 데이터 DB
"""
from pathlib import Path

# infoGetherAPI finance.db 경로 (로컬 개발 기준)
FINANCE_DB_PATH = Path(__file__).resolve().parent.parent.parent.parent / "infoGetherAPI" / "data" / "finance.db"

# 자체 BAR 데이터 스토리지 (TechAnalysisExecutor 내부)
BAR_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "bar_storage.db"

# SQLite URI
FINANCE_DB_URL = f"sqlite:///{FINANCE_DB_PATH}"
BAR_DB_URL = f"sqlite:///{BAR_DB_PATH}"
