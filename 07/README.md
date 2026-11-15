# Laporan Praktikum Sistem Terdistribusi dan Terdesentralisasi

## Pertemuan 07: Containerisasi Aplikasi Flask dengan Docker dan Podman

### Identitas

- Nama: **Diana Amelia**
- NIM: **255410042**
- Kelas: **Informatika-1**

## 1. Tujuan

1. Memahami konsep cloud computing dan model layanan XaaS.
2. Memahami konsep image dan container.
3. Menyiapkan lingkungan Python menggunakan `uv`.
4. Menjalankan aplikasi Flask secara lokal.
5. Membuat image aplikasi menggunakan Dockerfile.
6. Menjalankan dan menguji aplikasi Flask menggunakan Docker.
7. Menggunakan Podman sebagai alternatif runtime container.
8. Membandingkan proses containerisasi menggunakan Docker dan Podman.

## 2. Dasar Teori

### 2.1 Cloud Computing dan XaaS

Cloud computing adalah teknologi yang menyediakan sumber daya komputasi melalui
jaringan internet. XaaS (*Everything as a Service*) merupakan pendekatan yang
menyediakan sumber daya tersebut dalam bentuk layanan.

Model layanan yang dibahas dalam praktikum ini adalah:

- **SaaS (Software as a Service)**: pengguna langsung menggunakan aplikasi yang
  disediakan oleh provider. Contohnya Google Workspace.
- **PaaS (Platform as a Service)**: provider menyediakan platform untuk
  mengembangkan dan menjalankan aplikasi. Contohnya Heroku.
- **IaaS (Infrastructure as a Service)**: provider menyediakan infrastruktur
  virtual seperti server, penyimpanan, dan jaringan. Contohnya Amazon EC2.

### 2.2 Container

Container adalah lingkungan terisolasi yang mengemas aplikasi, dependensi, dan
konfigurasi yang dibutuhkan untuk menjalankan aplikasi. Container lebih ringan
daripada virtual machine karena berbagi kernel dengan sistem operasi host.

### 2.3 Image dan Container

Image adalah template yang digunakan sebagai dasar pembuatan container.
Container adalah instance berjalan dari sebuah image. Satu image dapat digunakan
untuk membuat beberapa container.

### 2.4 Dockerfile

Dockerfile adalah berkas yang berisi instruksi untuk membangun image. Instruksi
tersebut dapat menentukan image dasar, direktori kerja, dependensi, port, dan
perintah untuk menjalankan aplikasi.

### 2.5 Docker dan Podman

Docker dan Podman merupakan alat untuk membangun image dan menjalankan container.
Docker menggunakan daemon sebagai komponen utama, sedangkan Podman dapat
berjalan tanpa daemon dan mendukung pendekatan rootless. Keduanya mendukung
image dengan format OCI yang kompatibel.

## 3. Alat dan Bahan

- Komputer atau laptop.
- Ubuntu pada lingkungan WSL.
- Git.
- Repository Flask: [pallets/flask](https://github.com/pallets/flask).
- Python 3.14.4.
- `uv` versi `0.13.7`.
- Docker versi `29.9.2`.
- Podman versi `5.7.0`.
- Terminal atau command line.
- Browser untuk menguji aplikasi.

## 4. Langkah Pengerjaan

### 4.1 Tugas 0: Vendor dan Arsitektur XaaS

#### 4.1.1 Contoh Vendor SaaS, PaaS, dan IaaS

| Kategori | Vendor | Contoh layanan |
| --- | --- | --- |
| SaaS (*Software as a Service*) | Google | Google Workspace |
| PaaS (*Platform as a Service*) | Heroku | Heroku Platform |
| IaaS (*Infrastructure as a Service*) | Amazon Web Services (AWS) | Amazon EC2 |

#### 4.1.2 Penjelasan Layanan

**a. SaaS - Google Workspace**

Google Workspace merupakan kumpulan aplikasi berbasis cloud yang dapat
digunakan langsung melalui internet. Pengguna tidak perlu memasang dan
mengelola server aplikasi sendiri. Contoh layanannya adalah Gmail, Google
Drive, Google Docs, Google Sheets, dan Google Meet.

Pada model SaaS, provider mengelola aplikasi, platform, dan infrastrukturnya.
Pengguna cukup berinteraksi dengan aplikasi yang telah disediakan.

**b. PaaS - Heroku**

Heroku merupakan platform cloud untuk mengembangkan, menjalankan, dan mengelola
aplikasi tanpa mengharuskan pengembang mengelola infrastruktur server secara
langsung. Layanannya meliputi application deployment, runtime environment,
database service, application scaling, dan application monitoring.

Pada model PaaS, provider menyediakan infrastruktur dan platform untuk
menjalankan aplikasi. Pengembang dapat berfokus pada pembuatan aplikasi.

**c. IaaS - Amazon EC2**

Amazon EC2 (*Elastic Compute Cloud*) merupakan layanan AWS yang menyediakan
sumber daya komputasi berupa server virtual. Layanannya meliputi virtual
machine, CPU dan RAM, storage, networking, serta scalability.

Pada model IaaS, provider menyediakan infrastruktur seperti server,
penyimpanan, dan jaringan. Pengguna memiliki kendali lebih besar atas sistem
operasi, middleware, aplikasi, dan konfigurasi lingkungan komputasi.

#### 4.1.3 Visualisasi Arsitektur XaaS

Visualisasi berikut menunjukkan hubungan antara cloud consumer, internet, dan
cloud provider pada model SaaS, PaaS, serta IaaS. Perbedaan tanggung jawab
provider dan pengguna ditunjukkan melalui lapisan aplikasi, platform, sistem
operasi, virtualisasi, server, storage, dan network.

![Visualisasi arsitektur XaaS](images/Visualisasi%20Arsitektur%20XaaS.png)

### 4.2 Memeriksa `uv` dan Clone Repository

Versi `uv` diperiksa menggunakan:

```bash
uv --version
```

Hasil pemeriksaan menunjukkan `uv 0.13.7` telah tersedia. Repository Flask
kemudian di-clone:

```bash
git clone https://github.com/pallets/flask
```

Proses clone berhasil dan repository disalin ke direktori kerja aplikasi
`flask-app`.

![Pemeriksaan versi uv](images/01-cek%20uv%20version.png)

![Clone repository Flask](images/02-menjalankan%20git%20clone.png)

![Pembuatan folder aplikasi Flask](images/03-membuat%20folder%20dan%20aplikasi%20flask.png)

### 4.3 Membuat Environment Python dan Memasang Dependensi

Environment Python 3.14.4 dibuat dengan perintah:

```bash
uv python install 3.14.4
uv venv --python 3.14.4
source .venv/bin/activate
python --version
```

Environment berhasil aktif dan menggunakan Python `3.14.4`. Dependensi aplikasi
dipasang secara editable:

```bash
uv pip install -e .
```

Delapan paket berhasil dipasang, termasuk Flask `3.1.3`, Werkzeug `3.1.9`,
Jinja2 `3.1.6`, dan Click `8.1.5`. Database Flask diinisialisasi menggunakan:

```bash
flask --app flaskr init-db
```

![Pembuatan environment Python 3.14.4](images/04-membuat%20environment%20Python%203.14.4.png)

![Pemasangan paket aplikasi](images/05-Menginstal%20paket%20aplikasi.png)

### 4.4 Menjalankan Aplikasi Flask Secara Lokal

Aplikasi dijalankan menggunakan:

```bash
flask --app flaskr run
```

Server Flask berjalan pada `http://127.0.0.1:5000`. Pengujian melalui browser
menampilkan halaman Flaskr dengan judul **Posts** serta tautan **Register** dan
**Log In**. Log server mencatat request `GET /` dengan status `200`.

![Aplikasi Flask pada localhost:5000](images/06-Menjalankan%20localhost%205000.png)

### 4.5 Membuat Dockerfile

Dockerfile dibuat pada direktori aplikasi dengan instruksi utama sebagai berikut:

```dockerfile
FROM python:3.14

RUN mkdir /app
WORKDIR /app
ADD ./app/
RUN pip install -e
RUN flask --app flaskr init-db

EXPOSE 5000
CMD ["flask", "--app", "flaskr", "run", "--host=0.0.0.0", "--port=5000"]
```

Dockerfile tersebut menggunakan Python 3.14 sebagai image dasar, menempatkan
aplikasi pada `/app`, memasang dependensi, menginisialisasi database, membuka
port `5000`, dan menjalankan Flask agar dapat diakses dari luar container.

![Pembuatan Dockerfile](images/07-membuat%20aplikasi%20CA-docker.png)

![Isi Dockerfile](images/08-kode%20aplikasi%20CA-docker.png)

### 4.6 Membangun dan Menjalankan Container dengan Docker

Docker diperiksa melalui perintah `groups` dan `docker info`. Output
menunjukkan Docker Client versi `29.9.2` dengan konteks `default`.

Image dibangun menggunakan:

```bash
docker build -f Dockerfile -t flaskr:1.0.0 .
docker images
```

Proses build selesai dengan status **FINISHED** dan menghasilkan image
`flaskr:1.0.0`. Container kemudian dijalankan dengan pemetaan port host `5001`
ke port container `5000`:

```bash
docker run -d --name flaskr-docker -p 5001:5000 flaskr:1.0.0
docker ps
```

Container `flaskr-docker` berstatus **Up**. Aplikasi berhasil diakses melalui
`http://localhost:5001` dan menampilkan halaman Flaskr.

![Mengaktifkan dan memeriksa Docker](images/09-mengakifkan%20docker.png)

![Membangun Docker image](images/10-membuat%20docker%20image.png)

![Memeriksa Docker image](images/11-menjalankan%20docker%20image.png)

![Menjalankan Docker container](images/12-menjalankan%20docker%20container.png)

![Pengujian aplikasi pada port 5001](images/13-menjalankan%20localhost%205001.png)

### 4.7 Menghentikan dan Menghapus Container Docker

Container Docker dihentikan dan dihapus setelah pengujian:

```bash
docker stop flaskr-docker
docker rm flaskr-docker
```

Kedua perintah berhasil mengembalikan nama `flaskr-docker`, sehingga container
telah dihentikan dan dihapus.

![Menghentikan dan menghapus Docker container](images/13a-menghentikan%20docker%20container.png)

### 4.8 Memasang dan Memeriksa Podman

Podman dipasang menggunakan:

```bash
sudo apt install podman -y
```

Versi Podman diperiksa dengan:

```bash
podman --version
```

Hasilnya adalah `podman version 5.7.0`. Perintah `podman info` menampilkan
arsitektur `amd64`, backend database `sqlite`, dan distribusi Ubuntu. Terdapat
peringatan bahwa `/` bukan shared mount untuk rootless container, tetapi
peringatan tersebut tidak menghalangi proses build dan run.

![Instalasi Podman](images/14-menginstal%20podman.png)

![Pemeriksaan versi Podman](images/15-cek%20versi%20podman.png)

![Pemeriksaan konfigurasi Podman](images/16-memeriksa%20konfigurasi%20podman.png)

### 4.9 Membangun dan Menjalankan Container dengan Podman

Image dibangun menggunakan Dockerfile yang sama:

```bash
podman build -f Dockerfile -t flaskr:1.0.0 .
podman images
```

Proses build menghasilkan image `localhost/flaskr:1.0.0`. Container dijalankan
dengan perintah:

```bash
podman run -d --name flaskr-podman -p 5001:5000 flaskr:1.0.0
podman ps
```

Container `flaskr-podman` berstatus **Up** dengan pemetaan
`0.0.0.0:5001->5000/tcp`. Hasil tersebut membuktikan aplikasi yang sama dapat
dijalankan menggunakan Podman.

![Membangun image dengan Podman](images/17-membuat%20podman%20image.png)

![Memeriksa Podman image](images/18-memeriksa%20podman%20image.png)

![Menjalankan Podman container](images/19-menjalankan%20docker%20container.png)

![Menguji aplikasi Podman](images/20-menguji%20aplikasi%20podman.png)

### 4.10 Menghentikan dan Menghapus Container Podman

Container Podman dihentikan dan dihapus dengan:

```bash
podman stop flaskr-podman
podman rm flaskr-podman
podman ps -a
```

Output `podman ps -a` tidak lagi menampilkan `flaskr-podman`, sehingga container
berhasil dibersihkan setelah pengujian.

![Menghentikan dan menghapus Podman container](images/21-menghentikan%20podman%20container.png)

## 5. Hasil Praktikum

| No. | Tahap | Hasil yang Terlihat |
| --- | --- | --- |
| 1 | Tugas 0 XaaS | Vendor SaaS, PaaS, dan IaaS serta visualisasi arsitektur berhasil disusun. |
| 2 | Pemeriksaan `uv` | `uv 0.13.7` tersedia. |
| 3 | Clone repository | Repository Flask berhasil di-clone dari GitHub. |
| 4 | Environment Python | Python `3.14.4` berhasil dipasang dan environment aktif. |
| 5 | Dependensi aplikasi | Delapan paket berhasil dipasang dengan `uv pip install -e .`. |
| 6 | Aplikasi lokal | Flaskr berjalan pada `localhost:5000` dan menampilkan halaman Posts. |
| 7 | Dockerfile | Dockerfile dibuat dengan base image `python:3.14` dan port container `5000`. |
| 8 | Docker image | Image `flaskr:1.0.0` berhasil dibuat dengan Docker. |
| 9 | Docker container | `flaskr-docker` berjalan pada host port `5001`. |
| 10 | Pengujian Docker | Aplikasi dapat dibuka melalui `localhost:5001`. |
| 11 | Podman | Podman `5.7.0` berhasil dipasang dan dikonfigurasi. |
| 12 | Podman image | Image `localhost/flaskr:1.0.0` berhasil dibuat. |
| 13 | Podman container | `flaskr-podman` berjalan pada host port `5001`. |
| 14 | Pembersihan | Container Docker dan Podman berhasil dihentikan serta dihapus. |

## 6. Analisis

Tugas 0 menunjukkan bahwa XaaS membagi layanan cloud berdasarkan tingkat
abstraksi dan tanggung jawab pengguna. Pada SaaS, pengguna langsung
menggunakan aplikasi. Pada PaaS, pengguna berfokus pada pengembangan aplikasi,
sedangkan provider mengelola platform. Pada IaaS, pengguna memiliki kendali
lebih besar terhadap sistem operasi dan aplikasi, sementara provider mengelola
infrastruktur dasar.

Pada tahap awal, aplikasi Flask berjalan langsung pada environment Python
3.14.4 dan dapat diakses melalui port `5000`. Setelah dibuat menjadi image,
aplikasi memiliki lingkungan eksekusi yang lebih konsisten karena source code,
dependensi, konfigurasi, dan proses inisialisasi database didefinisikan melalui
Dockerfile.

Pemetaan port menjadi bagian penting saat menjalankan container. Flask
mendengarkan port `5000` di dalam container, sedangkan port host `5001`
digunakan agar aplikasi dapat diakses dari browser. Dengan demikian,
`-p 5001:5000` berarti port `5001` pada host diteruskan ke port `5000` pada
container.

Docker dan Podman dapat menggunakan Dockerfile yang sama untuk membangun dan
menjalankan aplikasi. Perbedaan nama image pada Podman, yaitu
`localhost/flaskr:1.0.0`, menunjukkan penamaan registry lokal Podman. Hasil
praktikum membuktikan bahwa aplikasi yang sama dapat dijalankan menggunakan
kedua runtime.

Image dan container memiliki siklus hidup yang berbeda. Image tetap dapat
digunakan untuk membuat container baru, sedangkan container dapat dihentikan
dan dihapus setelah pengujian tanpa perlu membangun ulang image.

## 7. Kendala dan Solusi

| Kendala yang ditemukan | Solusi atau pemahaman yang diperoleh |
| --- | --- |
| Aplikasi membutuhkan versi Python tertentu. | Memasang Python `3.14.4` dan membuat virtual environment dengan `uv`. |
| Dependensi belum tersedia pada environment baru. | Menjalankan `uv pip install -e .` sebelum menjalankan aplikasi. |
| Flask di dalam container harus dapat diakses dari host. | Menjalankan Flask dengan `--host=0.0.0.0` dan memetakan port `5001:5000`. |
| Container perlu diuji tanpa mengganggu layanan lokal pada port 5000. | Menggunakan port host `5001` untuk container. |
| Terdapat peringatan pada `podman info` mengenai `/` yang bukan shared mount. | Peringatan dicatat sebagai informasi konfigurasi rootless; build dan run tetap berhasil. |
| Container tidak diperlukan setelah pengujian. | Menjalankan `docker stop`/`docker rm` dan `podman stop`/`podman rm`. |

## 8. Kesimpulan

Praktikum pertemuan ketujuh berhasil membahas model layanan cloud XaaS dan
menerapkan containerisasi pada aplikasi Flask. Tugas 0 menghasilkan penjelasan
SaaS, PaaS, IaaS, serta visualisasi arsitektur yang menunjukkan pembagian
tanggung jawab antara pengguna dan cloud provider.

Aplikasi Flask berhasil dijalankan secara lokal menggunakan Python 3.14.4,
kemudian dikemas menjadi image `flaskr:1.0.0` menggunakan Dockerfile. Image
berhasil dijalankan dengan Docker dan diakses melalui `localhost:5001`.

Podman versi `5.7.0` juga berhasil digunakan untuk membangun image dan
menjalankan aplikasi pada port yang sama. Dengan demikian, Docker dan Podman
dapat menjalankan aplikasi dari Dockerfile yang sama. Container Docker dan
Podman berhasil dihentikan serta dihapus setelah pengujian.

## 9. Referensi

1. [Flask Documentation](https://flask.palletsprojects.com/)
2. [Docker Documentation](https://docs.docker.com/)
3. [Podman Documentation](https://docs.podman.io/)
4. [uv Documentation](https://docs.astral.sh/uv/)
5. [Repository Flask](https://github.com/pallets/flask)
