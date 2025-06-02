from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "postgresql://postgres:altow12@localhost/testdb"
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
