from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, Column, String, DateTime, func, ForeignKey, Text
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


class Advertisement(Base):

    __tablename__ = 'advertisement'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    users = relationship(Users, backref='advertisement')
    title = Column(String(length=50))
    description = Column(Text)
    created_fild=Column(DateTime, server_default=func.now())

    def __str__(self):
        return f"{self.id}, {self.id_user}, {self.title}, {self.description}, {self.created_fild}"
