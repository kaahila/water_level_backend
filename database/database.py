from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import settings

SQLALCHEMY_DATABASE_URL = "{databasetype}+{engine}://{user}:{password}@{ip}:{port}/{database}".format(
    user=settings.user,
    password=settings.password,
    ip=settings.host,
    databasetype=settings.databasetype,
    database=settings.database,
    engine=settings.engine,
    port=settings.port
    )
if not SQLALCHEMY_DATABASE_URL:
    raise Exception("database_url missing in settings")

connect_args = {}

if "sqlite" in SQLALCHEMY_DATABASE_URL:
    connect_args['check_same_thread'] = True

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
