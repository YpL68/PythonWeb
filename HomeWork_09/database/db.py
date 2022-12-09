from pathlib import Path
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path(__file__).parent.parent
DATABASE = "sqlite:///" + str(BASE_DIR/"database"/"assist.db")

engine = create_engine(DATABASE, echo=False)

DBSession = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def session_scope():
    session = DBSession()
    session.execute("PRAGMA foreign_keys = 1")
    try:
        yield session
    except Exception as err:
        raise err
    finally:
        session.close()
