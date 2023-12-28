import uuid

from asyncpg import Connection
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.settings.config import settings


# fix asyncpg.exceptions.InvalidSQLStatementNameError:
# prepared statement "__asyncpg_stmt_4c" does not exist
# discussion
# https://github.com/sqlalchemy/sqlalchemy/issues/6467#issuecomment-1187494311
class SQLAlchemyConnection(Connection):
    def _get_unique_id(self, prefix: str) -> str:
        return f'__asyncpg_{prefix}_{uuid.uuid4()}__'


engine: AsyncEngine = create_async_engine(
    url=settings().db.dsn,
    echo=True,
    connect_args={
        'statement_cache_size': 0,
        'prepared_statement_cache_size': 0,
        'connection_class': SQLAlchemyConnection,
    },
    pool_pre_ping=True,
    poolclass=NullPool,
)
async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

metadata = MetaData(
    naming_convention={
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s',
    },
)


class Base(AsyncAttrs, DeclarativeBase):
    metadata = metadata
