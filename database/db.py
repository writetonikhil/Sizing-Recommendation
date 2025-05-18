from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class ResourceUsage(Base):
    __tablename__ = 'resource_usage'
    id = Column(Integer, primary_key=True)
    index_val = Column(Integer)
    cpu = Column(Float)
    ram = Column(Float)
    disk = Column(Float)
    network = Column(Float)

def get_engine():
    db_url = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    return create_engine(db_url)
