import configparser
import pathlib

from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


file_config = pathlib.Path(__file__).parent.parent.joinpath('conf/config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DEV', 'USER')
password = config.get('DEV', 'PASSWORD')
domain = config.get('DEV', 'DOMAIN')
port = config.get('DEV', 'PORT')
db_name = config.get('DEV', 'DB_NAME')

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@{domain}:{port}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, max_overflow=5)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()
