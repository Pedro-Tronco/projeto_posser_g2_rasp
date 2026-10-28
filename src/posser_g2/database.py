from pathlib import Path
from collections.abc import Iterator
from contextlib import contextmanager
from sqlmodel import SQLModel, create_engine, Session

from .room import tables as room_tables

DATABASE_PATH = Path(__file__).resolve().parents[2] / "data" / "database.sqlite"
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}",
    connect_args={"check_same_thread": False},
)


def create_all_tables() -> None:
    SQLModel.metadata.create_all(engine)
    
    
@contextmanager
def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session