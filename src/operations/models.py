from sqlalchemy import (
    Integer,
    String,
    TIMESTAMP,
    Table,
    Column,
)

from src import BaseMetadata

operation = Table(
    "operation",
    BaseMetadata,
    Column("id", Integer, primary_key=True),
    Column("quantity", String),
    Column("figi", String),
    Column("instrument_type", String, nullable=True),
    Column("date", TIMESTAMP),
    Column("type", String),
)
