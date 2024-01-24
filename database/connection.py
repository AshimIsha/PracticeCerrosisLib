from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



def get_connection():
    engine = create_engine('sqlite:///test.db', connect_args={'check_same_thread': False})
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session()  

def commit(session):
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

def get_db():
    db = get_connection()
    try:
        yield db
    finally:
        db.close()
       