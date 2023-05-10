from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, Column, String, DateTime, func, ForeignKey
from sqlalchemy_utils import EmailType

PG_DSN = 'postgresql+asyncpg://postgres:masterkey@localhost:5432/aiohttp'
engine = create_async_engine(PG_DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class Users(Base):

    __tablename__='users'

    id = Column(Integer, primary_key=True)
    email = Column(EmailType, nullable=False, unique=True, index=True)
    registration_date = Column(DateTime, server_default=func.now())
    password = Column(String(60), nullable=False)
    first_name = Column(String(length=50))
    last_name = Column(String(length=50))

    def __str__(self):
        return f"{self.id}, {self.email}, {self.registration_date}, {self.password}, {self.first_name}, {self.last_name}"


class Weather(Base):

    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    users = relationship(Users, backref='weather')
    city = Column(String(length=50))
    description = Column(String(length=50))
    temp = Column(Integer)
    created_fild=Column(DateTime, server_default=func.now())

    def __str__(self):
        return f"{self.id}, {self.city}, {self.description}, {self.temp}, {self.created_fild}"
