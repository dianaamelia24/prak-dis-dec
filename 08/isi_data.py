from sqlmodel import Field, Session, SQLModel, create_engine


class AsetServer(SQLModel, table=True):
    __tablename__ = "aset_server"

    id: int | None = Field(default=None, primary_key=True)
    jumlah_core: int
    kode_rak: str
    nama_server: str
    aktif: bool
    penggunaan_cpu: float


engine = create_engine("sqlite:///departemen-sdm.db")

data_server = [
    AsetServer(jumlah_core=4, kode_rak="RK-01", nama_server="srv-web-01", aktif=True, penggunaan_cpu=23.5),
    AsetServer(jumlah_core=8, kode_rak="RK-01", nama_server="srv-db-01", aktif=True, penggunaan_cpu=54.2),
    AsetServer(jumlah_core=4, kode_rak="RK-02", nama_server="srv-cache-01", aktif=False, penggunaan_cpu=0.0),
    AsetServer(jumlah_core=16, kode_rak="RK-02", nama_server="srv-app-01", aktif=True, penggunaan_cpu=71.8),
    AsetServer(jumlah_core=8, kode_rak="RK-03", nama_server="srv-log-01", aktif=True, penggunaan_cpu=18.4),
]

with Session(engine) as session:
    session.add_all(data_server)
    session.commit()

print("Berhasil memasukkan 5 data ke tabel aset_server.")