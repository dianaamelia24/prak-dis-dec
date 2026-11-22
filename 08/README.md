# Laporan Praktikum Sistem Terdistribusi dan Terdesentralisasi

## Pertemuan 08: Pembuatan REST API dengan FastAPI dan SQLite

### Identitas

- Nama: **Diana Amelia**
- NIM: **255410042**
- Kelas: **Informatika-1**

## 1. Tujuan

1. Memahami cara membuat virtual environment pada proyek Python.
2. Menggunakan FastAPI dan SQLModel untuk membangun REST API.
3. Membuat serta mengelola database SQLite.
4. Membuat model tabel dan endpoint untuk membaca data.
5. Memasukkan data aset server ke dalam database.
6. Menguji endpoint REST API melalui browser dan `curl.exe`.
7. Mendokumentasikan proses dan hasil praktikum.

## 2. Dasar Teori

### 2.1 REST API

REST API adalah antarmuka yang digunakan untuk pertukaran data melalui protokol HTTP. Klien mengirim permintaan ke URL tertentu dan menerima respons dalam format seperti JSON. Pada praktikum ini, FastAPI menyediakan aplikasi server dan endpoint HTTP.

### 2.2 FastAPI

FastAPI merupakan framework Python untuk membangun REST API. FastAPI menggunakan tipe data Python untuk melakukan validasi, menghasilkan dokumentasi otomatis, dan mendefinisikan respons API. Uvicorn digunakan sebagai server ASGI untuk menjalankan aplikasi FastAPI.

### 2.3 SQLModel dan SQLite

SQLModel adalah library yang menggabungkan fitur SQLAlchemy dan Pydantic untuk pemodelan database. Model dapat digunakan sebagai representasi tabel sekaligus sebagai tipe data respons API.

SQLite adalah database relasional berbasis file. Pada praktikum ini, database disimpan pada file `departemen-sdm.db`, sehingga data tetap tersimpan meskipun aplikasi server dihentikan.

### 2.4 Dependency dan Session Database

Fungsi `get_session()` digunakan untuk menyediakan objek `Session` kepada endpoint FastAPI. Objek ini mengelola koneksi dan operasi terhadap database. Dengan `Depends`, session dibuat saat permintaan diterima dan ditutup setelah proses selesai.

## 3. Alat dan Bahan

- Komputer atau laptop dengan Windows.
- Python versi 3.14.4.
- Uvicorn sebagai server ASGI.
- FastAPI.
- SQLModel.
- SQLite dan SQLite3 CLI.
- Virtual environment Python.
- Windows PowerShell dan `curl.exe`.
- Browser untuk membuka dokumentasi atau endpoint.
- Repository GitHub: [prak-dis-dec](https://github.com/dianaamelia24/prak-dis-dec).

## 4. Langkah Pengerjaan

### 4.1 Memeriksa Versi Python

Pemeriksaan Python dilakukan melalui Windows PowerShell dengan perintah:

```powershell
py --version
uv python install 3.14.4
py -m uv add
```

Hasil pemeriksaan menunjukkan bahwa Python 3.14.4 telah tersedia pada komputer dan dapat digunakan untuk membuat proyek praktikum.

![Pemeriksaan dan penggunaan Python 3.14.4](images/1-menggunakan%20python%203.14.4.png)

### 4.2 Membuat Virtual Environment

Virtual environment dibuat untuk mengisolasi dependensi proyek agar tidak bertabrakan dengan lingkungan Python lain. Langkahnya dilakukan dengan perintah:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\activate.ps1
```

Perintah `Set-ExecutionPolicy` memungkinkan skrip virtual environment dijalankan pada pengguna Windows saat ini. Setelah aktivasi, prompt PowerShell menampilkan nama lingkungan `.venv`, yang menunjukkan bahwa virtual environment telah aktif.

![Pembuatan dan aktivasi virtual environment](images/2-membuat%20dan%20aktifkan%20virtual%20environment.png)

### 4.3 Menginstal FastAPI dan SQLModel

Paket FastAPI dan SQLModel dipasang pada virtual environment dengan perintah:

```powershell
uv pip install "fastapi[standard]" sqlmodel
```

Paket tersebut membawa FastAPI beserta paket pendukungnya, seperti Uvicorn untuk server, Pydantic untuk validasi data, dan SQLAlchemy sebagai pengelola database. Setelah proses selesai, paket dapat digunakan oleh aplikasi pada folder `08`.

![Proses instalasi FastAPI dan SQLModel](images/3-menginstal%20paket%20fastapi%20dan%20sqlmodel.png)

### 4.4 Membuat Database dan Tabel SDM

Database dibuat menggunakan SQLite3 CLI dengan perintah:

```powershell
sqlite3.exe departemen-sdm.db
```

Kemudian dibuat tabel `sdm` dengan struktur `id`, `npp`, dan `nama`:

```sql
CREATE TABLE sdm (
    id INTEGER PRIMARY KEY,
    npp CHAR(6),
    nama VARCHAR(50)
);
```

Kolom `id` digunakan sebagai kunci utama, `npp` menyimpan nomor pokok pegawai, dan `nama` menyimpan nama karyawan. Tiga data awal dimasukkan ke tabel menggunakan perintah `INSERT INTO sdm` dan ditampilkan menggunakan `SELECT * FROM sdm`. Hasilnya memuat tiga karyawan dengan NPP `112233`, `223344`, dan `334455`.

![Pembuatan database dan tabel SDM](images/4-membuat%20database%20dan%20tabel%20sdm%20di%20sqlite.png)

### 4.5 Membuat Aplikasi dan Model Data

Aplikasi dibuat pada file `service.py`. File tersebut berisi model `Sdm` dan `AsetServer` serta endpoint untuk membaca data dari database.

Model `Sdm` menggunakan tabel bernama `sdm` dan memiliki field `id`, `npp`, serta `nama`. Model `AsetServer` menggunakan tabel `aset_server` dan memiliki field:

- `id`;
- `jumlah_core`;
- `kode_rak`;
- `nama_server`;
- `aktif`; dan
- `penggunaan_cpu`.

Database dihubungkan menggunakan SQLModel dengan perintah:

```python
engine = create_engine("sqlite:///departemen-sdm.db")
```

Fungsi `get_session()` menghasilkan session database melalui `Session(engine)`. Aplikasi FastAPI kemudian menyediakan dua endpoint, yaitu:

- `GET /sdm/` untuk mengambil data karyawan;
- `GET /aset-server/` untuk mengambil data aset server.

### 4.6 Menjalankan Server FastAPI

Server dijalankan dari folder `08` menggunakan perintah:

```powershell
python -m uvicorn service:app --reload
```

Uvicorn menjalankan objek `app` pada modul `service.py`. Opsi `--reload` membuat server memuat ulang aplikasi secara otomatis ketika file kode berubah. Hasil pemeriksaan menunjukkan server berjalan pada alamat `http://127.0.0.1:8000` dengan proses startup dan shutdown yang berhasil.

![Menjalankan server FastAPI](images/5-menjalankan%20server%20fastapi.png)

### 4.7 Menguji Endpoint SDM

Setelah server aktif, endpoint SDM dibuka pada browser melalui:

```text
http://localhost:8000/sdm/
```

Browser menampilkan respons JSON yang berisi tiga karyawan. Endpoint juga diuji menggunakan `curl.exe`:

```powershell
curl.exe http://localhost:8000/sdm/
```

Respons dari `curl.exe` memiliki struktur JSON yang sama dengan hasil pada browser.

![Hasil endpoint SDM pada browser](images/6-menjalankan%20localhost%208000.png)

![Pengujian endpoint SDM menggunakan curl.exe](images/7-menguji%20endpoint%20menggunakan%20curl.exe.png)

### 4.8 Membuat dan Mengisi Tabel Aset Server

Tugas lanjutan membuat tabel `aset_server` pada database yang sama. Tabel dibuat menggunakan SQLite3 CLI dengan kolom `jumlah_core`, `kode_rak`, `nama_server`, `aktif`, dan `penggunaan_cpu`.

```sql
CREATE TABLE aset_server (
    id INTEGER PRIMARY KEY,
    jumlah_core INT,
    kode_rak CHAR(5),
    nama_server VARCHAR(50),
    aktif BOOL,
    penggunaan_cpu FLOAT
);
```

Data tabel kemudian dimasukkan melalui file `isi_data.py`. Skrip tersebut membuat lima objek `AsetServer` dan menyimpannya menggunakan satu session database:

```python
session.add_all(data_server)
session.commit()
```

![Pembuatan tabel aset_server](images/8-membuat%20tabel%20baru%20aset-server%20%28tugas%29.png)

![Menjalankan skrip isi_data.py](images/9-menjalankan%20python%20isi_data.py.png)

Lima data aset server yang dimasukkan adalah:

| Nama Server  | Jumlah Core | Kode Rak | Aktif | Penggunaan CPU |
| ------------ | ----------: | -------- | ----- | -------------: |
| srv-web-01   |           4 | RK-01    | true  |           23.5 |
| srv-db-01    |           8 | RK-01    | true  |           54.2 |
| srv-cache-01 |           4 | RK-02    | false |            0.0 |
| srv-app-01   |          16 | RK-02    | true  |           71.8 |
| srv-log-01   |           8 | RK-03    | true  |           18.4 |

### 4.9 Menjalankan Endpoint Aset Server

Server FastAPI dijalankan kembali dan endpoint aset server diuji pada alamat:

```text
http://localhost:8000/aset-server/
```

Hasil pengujian dengan `curl.exe` menunjukkan lima objek server dalam format JSON. Setiap objek memuat `id`, `jumlah_core`, `kode_rak`, `nama_server`, `aktif`, dan `penggunaan_cpu`.

Endpoint tersebut juga dapat dibuka melalui browser dan menampilkan daftar aset server dalam format JSON yang sama.

![Menjalankan ulang server untuk endpoint aset-server](images/10-menjalankan%20server%20fastapi%20menggunakan%20endpoint.png)

![Pengujian endpoint aset-server menggunakan curl.exe](images/11-menampilkan%20hasil%20endpoint%20menggunakan%20curl.exe.png)

![Hasil endpoint aset-server pada browser](images/12-menjalankan%20localhost%208000%20aset-server.png)

## 5. Hasil Praktikum

Hasil praktikum yang berhasil diperoleh adalah sebagai berikut:

| No. | Tahap                | Hasil                                                                        |
| --- | -------------------- | ---------------------------------------------------------------------------- |
| 1   | Lingkungan Python    | Python 3.14.4 tersedia.                                                      |
| 2   | Virtual environment  | Direktori `.venv` berhasil dibuat dan diaktifkan.                            |
| 3   | Paket aplikasi       | FastAPI dan SQLModel beserta dependensinya berhasil dipasang.                |
| 4   | Database             | File `departemen-sdm.db` berhasil dibuat.                                    |
| 5   | Tabel SDM            | Tabel `sdm` berisi tiga data karyawan.                                       |
| 6   | Endpoint SDM         | `GET /sdm/` berhasil mengembalikan tiga data karyawan dalam JSON.            |
| 7   | Server               | Uvicorn berhasil menjalankan aplikasi pada `http://127.0.0.1:8000`.          |
| 8   | Tabel aset server    | Tabel `aset_server` berhasil dibuat pada database.                           |
| 9   | Data aset server     | Lima data aset server berhasil dimasukkan dan disimpan.                      |
| 10  | Endpoint aset server | `GET /aset-server/` berhasil mengembalikan lima data aset server dalam JSON. |

## 6. Analisis

Praktikum menunjukkan hubungan antara model Python, database SQLite, dan REST API. Model `Sdm` dan `AsetServer` menentukan nama tabel serta jenis data setiap kolom. Ketika endpoint dipanggil, `get_session()` membuat session database, `select()` membangun perintah pembacaan data, dan `session.exec(statement).all()` mengambil seluruh baris hasil pencarian.

Pada endpoint `/sdm/`, FastAPI mengubah objek atau koleksi model SQLModel menjadi respons JSON. Nilai `npp` dan `nama` yang ditampilkan pada browser berasal dari tabel `sdm` pada database. Hal yang sama terjadi pada endpoint `/aset-server/`, tetapi sumbernya adalah tabel `aset_server`.

Penggunaan virtual environment berperan untuk memastikan versi paket yang dipakai aplikasi tidak bergantung pada lingkungan Python global. FastAPI dan SQLModel memungkinkan pengembangan API yang ringkas karena validasi, pemodelan tabel, dan dokumentasi dapat ditulis dengan kode Python.

Pengujian melalui browser dan `curl.exe` juga membuktikan bahwa hasil API dapat diakses oleh klien HTTP yang berbeda. Browser menampilkan respons sebagai permintaan langsung, sedangkan `curl.exe` menampilkan respons JSON dari terminal. Uvicorn berperan sebagai server yang menerima permintaan dan meneruskannya ke route FastAPI.

Skrip `isi_data.py` menyimpan lima data sekaligus menggunakan `session.add_all()` dan `session.commit()`. Proses commit memastikan perubahan tersimpan pada file database. Data tersebut dapat dibaca kembali oleh endpoint tanpa perlu menjalankan skrip pengisian data lagi.

## 7. Kendala dan Solusi

| Kendala yang Ditemukan                            | Solusi atau Pemahaman yang Diperoleh                                                                                                     |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Skrip virtual environment belum dapat dijalankan. | Menjalankan `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` agar skrip aktivasi pada sesi pengguna diperbolehkan. |
| Paket FastAPI atau SQLModel belum tersedia.       | Memasang paket pada virtual environment aktif menggunakan `uv pip install "fastapi[standard]" sqlmodel`.                                 |
| Server belum dapat menerima permintaan.           | Menjalankan Uvicorn pada folder yang memuat `service.py` dengan perintah `python -m uvicorn service:app --reload`.                       |
| Data aset server belum tersedia pada endpoint.    | Membuat tabel `aset_server`, menjalankan `isi_data.py`, lalu memastikan session melakukan `commit()`.                                    |
| Database tidak dapat ditemukan oleh aplikasi.     | Menjalankan perintah pada folder `08` agar `sqlite:///departemen-sdm.db` mengarah ke file database pada folder tersebut.                 |
| Endpoint perlu diuji secara praktis.              | Membuka alamat `localhost:8000/sdm/` atau `/aset-server/` pada browser dan `curl.exe`.                                                   |

## 8. Kesimpulan

Praktikum berhasil membangun REST API menggunakan FastAPI, SQLModel, dan SQLite. Python 3.14.4 digunakan dalam virtual environment `.venv`, sedangkan Uvicorn menjalankan aplikasi pada alamat `127.0.0.1:8000`.

Database `departemen-sdm.db` berisi tabel `sdm` dan `aset_server`. Tabel `sdm` memuat tiga data karyawan, sedangkan tabel `aset_server` memuat lima aset server beserta jumlah core, kode rak, status aktif, dan penggunaan CPU.

Endpoint `GET /sdm/` dan `GET /aset-server/` berhasil mengembalikan data dalam format JSON. Pengujian melalui browser dan `curl.exe` membuktikan bahwa API dapat diakses sebagai layanan HTTP dan dapat digunakan sebagai dasar pengembangan sistem terdistribusi.

## 9. Referensi

1. [Dokumentasi FastAPI](https://fastapi.tiangolo.com/)
2. [Dokumentasi SQLModel](https://sqlmodel.tiangolo.com/)
3. [Dokumentasi SQLite](https://www.sqlite.org/docs.html)
4. [Dokumentasi Python](https://docs.python.org/)
