from datetime import datetime

from sqlalchemy import (
    MetaData,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    Table,
    Column,
    JSON,
    Boolean,
)

metadata = MetaData()


role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey("role.id")),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)

# Create models by sqlalchemy engine
# engine = sqlalchemy.create_engine(DATABASE_URL)
# meta_data.create_all(engine)
