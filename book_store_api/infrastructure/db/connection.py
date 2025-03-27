from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.ext.asyncio import create_async_engine

from book_store_api.config import Config

# engine = create_async_engine(Config.DATABASE_URI, echo=True)

metadata = MetaData()

member_table = Table(
    "member",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("email", String, unique=True, nullable=False),
    Column("created_at", DateTime, default=datetime.today()),
)

book_table = Table(
    "book",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False),
    Column("author", String, nullable=False),
    Column("is_borrowed", Boolean, default=False),
    Column("borrowed_date", DateTime, nullable=True),
    Column("borrowed_by", Integer, ForeignKey(member_table.c.id), nullable=True),
    Column("created_at", DateTime, default=datetime.today()),
)

# Engine setup
engine = create_async_engine(Config.DATABASE_URI, echo=True)
