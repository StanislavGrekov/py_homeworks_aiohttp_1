from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import JSON, INTEGER, Column

PG_DSN = 'postgresql+asyncpg://postgres:masterkey@localhost:5432/aiohttp'
engine = create_async_engine(PG_DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class Weather_data(Base):
    __tablename__ = 'weather_data'
    id = Column(INTEGER, primary_key=True)
    json = Column(JSON)