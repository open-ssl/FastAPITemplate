from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    Table,
    Column,
    JSON,
    Boolean,
)

from src.database import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class Role(DeclarativeBase):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)

    def as_tuple(self) -> tuple:
        return self.id, self.name, self.permissions


class User(DeclarativeBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey("role.id"))
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


# Create models.py by sqlalchemy engine
# engine = sqlalchemy.create_engine(DATABASE_URL)
# meta_data.create_all(engine)
