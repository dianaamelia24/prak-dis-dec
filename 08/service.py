from typing import List
from fastapi import Depends, FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Sdm(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    npp: str
    nama: str


class AsetServer(SQLModel, table=True):
    __tablename__ = "aset_server"

    id: int | None = Field(default=None, primary_key=True)
    jumlah_core: int
    kode_rak: str
    nama_server: str
    aktif: bool
    penggunaan_cpu: float


engine = create_engine("sqlite:///departemen-sdm.db")


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.get("/sdm/", response_model=List[Sdm])
def read_sdm(session: Session = Depends(get_session)):
    statement = select(Sdm)
    results = session.exec(statement).all()
    return results


@app.get("/aset-server/", response_model=List[AsetServer])
def read_aset_server(session: Session = Depends(get_session)):
    statement = select(AsetServer)
    results = session.exec(statement).all()
    return results