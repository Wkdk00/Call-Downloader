from src.database import Base
from sqlalchemy import Column, Integer, String, LargeBinary, DateTime

class Files(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    fileId = Column(String)
    filedata = Column(LargeBinary)
    date = Column(DateTime)
    agentId = Column(String)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    hashed_password = Column(String)