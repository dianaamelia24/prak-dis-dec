# Laporan Praktikum Sistem Terdistribusi dan Terdesentralisasi

## Pertemuan 07: Containerisasi Aplikasi Flask dengan Docker dan Podman

### Identitas

- Nama: **Diana Amelia**
- NIM: **255410042**
- Kelas: **Informatika-1**

## 1. Tujuan

1. Memahami konsep containerisasi pada aplikasi.
2. Menyiapkan lingkungan Python menggunakan `uv`.
3. Menjalankan aplikasi Flask secara lokal.
4. Membuat image aplikasi menggunakan Docker.
5. Menjalankan dan menguji aplikasi Flask di dalam container Docker.
6. Menggunakan Podman sebagai alternatif runtime container.
7. Membandingkan alur pembuatan dan pengelolaan container menggunakan Docker dan Podman.

## 2. Dasar Teori

### 2.1 Container

Container adalah lingkungan terisolasi yang mengemas aplikasi beserta dependensi
dan konfigurasi yang dibutuhkan untuk menjalankannya. Berbeda dengan virtual
machine yang menjalankan sistem operasi lengkap, container berbagi kernel host
sehingga umumnya lebih ringan dan cepat dijalankan.

### 2.2 Image dan Container

Image adalah template yang bersifat relatif tetap dan digunakan sebagai dasar
pembuatan container. Container merupakan instance berjalan dari image. Satu image
dapat digunakan untuk membuat beberapa container dengan konfigurasi yang berbeda.

### 2.3 Dockerfile

Dockerfile adalah berkas instruksi untuk membangun image. Pada praktikum ini,
Dockerfile menggunakan image dasar Python 3.14, menyalin source code aplikasi ke
direktori `/app`, memasang dependensi, menginisialisasi database Flask, membuka
port `5000`, dan menjalankan Flask pada seluruh interface container.

### 2.4 Docker dan Podman

Docker dan Podman sama-sama menyediakan perintah untuk membuat image dan
menjalankan container. Docker menggunakan daemon sebagai komponen utama,
sedangkan Podman dapat berjalan tanpa daemon dan mendukung pendekatan rootless.
Keduanya dapat menjalankan image dengan format OCI yang kompatibel.

## 3. Alat dan Bahan

- Komputer atau laptop.
- Ubuntu 26.04 pada lingkungan WSL.
- Git.
- Repository Flask: [pallets/flask](https://github.com/pallets/flask).
- Python 3.14.4.
- `uv` versi `0.13.7`.
- Docker versi `29.9.2`.
- Podman versi `5.7.0`.
- Terminal atau command line.
- Browser untuk menguji aplikasi.

## 4. Langkah Pengerjaan

## 4.0 Tugas 0

1. Contoh Vendor atau Komunitas SaaS, PaaS, dan IaaS

Cloud Computing merupakan teknologi komputasi yang menyediakan sumber daya teknologi informasi melalui jaringan internet. Dalam pendekatan XaaS (Everything as a Service), penyedia layanan (provider) menyediakan berbagai sumber daya komputasi sebagai layanan yang dapat digunakan oleh konsumen.

Berikut contoh vendor untuk masing-masing kategori:

Kategori

Vendor

Contoh Layanan

SaaS (Software as a Service)

Google

Google Workspace

PaaS (Platform as a Service)

Heroku

Heroku Platform

IaaS (Infrastructure as a Service)

Amazon Web Services (AWS)

Amazon EC2

2. Penjelasan Service dari Masing-Masing Vendor

A. SaaS – Google Workspace

Google Workspace merupakan kumpulan aplikasi berbasis cloud yang dapat digunakan langsung melalui internet. Pengguna tidak perlu memasang dan mengelola server aplikasi sendiri.

Layanan yang disediakan antara lain:

Gmail – layanan surat elektronik untuk mengirim dan menerima pesan.

Google Drive – layanan penyimpanan file secara online.

Google Docs – aplikasi pengolah dokumen berbasis cloud.

Google Sheets – aplikasi pengolah data berbentuk spreadsheet.

Google Meet – layanan komunikasi dan konferensi video.

Pada model SaaS, provider mengelola aplikasi beserta platform dan infrastrukturnya. Pengguna berinteraksi dengan aplikasi yang telah disediakan.

B. PaaS – Heroku

Heroku merupakan platform cloud untuk mengembangkan, menjalankan, dan mengelola aplikasi tanpa mengharuskan pengembang mengelola infrastruktur server secara langsung.

Layanan yang disediakan antara lain:

Application Deployment – memungkinkan pengembang melakukan deployment aplikasi ke lingkungan cloud.

Runtime Environment – menyediakan lingkungan untuk menjalankan aplikasi.

Database Service – menyediakan layanan database, misalnya Heroku Postgres.

Application Scaling – memungkinkan kapasitas aplikasi disesuaikan dengan kebutuhan.

Application Monitoring – membantu memantau kondisi dan performa aplikasi.

Pada model PaaS, provider menyediakan infrastruktur dan platform untuk menjalankan aplikasi. Pengembang dapat berfokus pada pembuatan aplikasi tanpa mengelola server, sistem operasi, dan lingkungan runtime secara langsung.

C. IaaS – Amazon Web Services (AWS)

Amazon EC2 (Elastic Compute Cloud) merupakan layanan AWS yang menyediakan sumber daya komputasi berupa server virtual. Pengguna dapat menjalankan sistem operasi dan aplikasi sesuai kebutuhannya.

Layanan yang disediakan antara lain:

Virtual Machine – menyediakan mesin virtual yang dapat digunakan sebagai server.

Computing Resources – menyediakan sumber daya CPU dan RAM sesuai spesifikasi yang dipilih.

Storage – menyediakan media penyimpanan untuk data dan aplikasi melalui layanan penyimpanan AWS.

Networking – menyediakan konfigurasi jaringan virtual untuk menghubungkan server dengan jaringan lain.

Scalability – memungkinkan kapasitas komputasi ditambah atau dikurangi sesuai kebutuhan.

Pada model IaaS, provider menyediakan infrastruktur seperti server, penyimpanan, dan jaringan. Pengguna memiliki kendali lebih besar untuk mengatur sistem operasi, middleware, aplikasi, serta konfigurasi lingkungan komputasi.

3. Visualisasi Arsitektur XaaS
   (images/Visualisasi Arsitektur XaaS.png)

### 4.1 Memeriksa dan Menyiapkan `uv`

Pemeriksaan dimulai dengan melihat versi `uv` menggunakan:

```bash
uv --version
```

Screenshot menunjukkan `uv 0.13.7` telah tersedia. Selanjutnya repository Flask
di-clone ke direktori kerja:

```bash
git clone https://github.com/pallets/flask
```

Proses clone selesai dengan berhasil, ditandai oleh pesan `Resolving deltas:
100%`. Repository kemudian disalin ke folder aplikasi `flask-app` dan isi folder
diperiksa menggunakan `ls -la`.

![Pemeriksaan versi uv](images/01-cek%20uv%20version.png)

![Clone repository Flask](images/02-menjalankan%20git%20clone.png)

![Pembuatan folder aplikasi Flask](images/03-membuat%20folder%20dan%20aplikasi%20flask.png)

### 4.2 Membuat Environment Python dan Memasang Dependensi

Environment Python 3.14.4 dibuat dengan perintah:

```bash
uv python install 3.14.4
uv venv --python 3.14.4
source .venv/bin/activate
python --version
```

Hasil pemeriksaan menunjukkan environment berhasil aktif dan menggunakan
`Python 3.14.4`. Dependensi aplikasi kemudian dipasang secara editable:

```bash
uv pip install -e .
```

Output menunjukkan delapan paket berhasil dipasang, termasuk Flask `3.1.3`,
Werkzeug `3.1.9`, Jinja2 `3.1.6`, dan Click `8.1.5`. Database Flask diinisialisasi
dengan `flask --app flaskr init-db`.

![Pembuatan environment Python 3.14.4](images/04-membuat%20environment%20Python%203.14.4.png)

![Pemasangan paket aplikasi](images/05-Menginstal%20paket%20aplikasi.png)

### 4.3 Menjalankan Aplikasi Flask Secara Lokal

Aplikasi dijalankan menggunakan:

```bash
flask --app flaskr run
```

Server development Flask berjalan pada `http://127.0.0.1:5000`. Pengujian
melalui browser pada `localhost:5000` menampilkan halaman Flaskr dengan judul
**Posts** serta tautan **Register** dan **Log In**. Log server juga mencatat
request `GET /` dengan status `200`.

![Aplikasi Flask pada localhost:5000](images/06-Menjalankan%20localhost%205000.png)

### 4.4 Membuat Dockerfile

Dockerfile dibuat pada direktori aplikasi dengan isi utama berikut:

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

Instruksi tersebut menetapkan Python 3.14 sebagai image dasar, menempatkan
aplikasi pada `/app`, memasang aplikasi, menginisialisasi database, dan
menjalankan server agar dapat diakses dari luar container.

![Pembuatan Dockerfile](images/07-membuat%20aplikasi%20CA-docker.png)

![Isi Dockerfile](images/08-kode%20aplikasi%20CA-docker.png)

### 4.5 Membangun Image dan Menjalankan Container dengan Docker

Status Docker diperiksa melalui `groups` dan `docker info`. Output menunjukkan
Docker Client versi `29.9.2` dan konteks `default` tersedia. Image dibuat dengan:

```bash
docker build -f Dockerfile -t flaskr:1.0.0 .
```

Proses build selesai dengan status `[+] Building ... FINISHED` dan menghasilkan
image `flaskr:1.0.0`. Keberadaan image diperiksa menggunakan:

```bash
docker images
```

Container kemudian dijalankan pada port host `5001` yang diteruskan ke port
`5000` di dalam container:

```bash
docker run -d --name flaskr-docker -p 5001:5000 flaskr:1.0.0
docker ps
```

Output `docker ps` menunjukkan container `flaskr-docker` berstatus **Up** dan
mapping port `0.0.0.0:5001->5000/tcp`. Aplikasi berhasil diakses melalui
`http://localhost:5001` dan menampilkan halaman Flaskr.

![Mengaktifkan dan memeriksa Docker](images/09-mengakifkan%20docker.png)

![Membangun Docker image](images/10-membuat%20docker%20image.png)

![Memeriksa Docker image](images/11-menjalankan%20docker%20image.png)

![Menjalankan Docker container](images/12-menjalankan%20docker%20container.png)

![Pengujian aplikasi pada port 5001](images/13-menjalankan%20localhost%205001.png)

### 4.6 Menghentikan dan Menghapus Container Docker

Setelah pengujian selesai, container dihentikan dan dihapus menggunakan:

```bash
docker stop flaskr-docker
docker rm flaskr-docker
```

Output mengembalikan nama `flaskr-docker` pada kedua perintah, yang menunjukkan
container berhasil dihentikan dan dihapus.

![Menghentikan dan menghapus Docker container](images/13a-menghentikan%20docker%20container.png)

### 4.7 Memasang dan Memeriksa Podman

Podman dipasang menggunakan:

```bash
sudo apt install podman -y
```

Versi Podman kemudian diperiksa:

```bash
podman --version
```

Hasilnya adalah `podman version 5.7.0`. Perintah `podman info` menampilkan
arsitektur `amd64`, backend database `sqlite`, distribusi Ubuntu, serta
peringatan bahwa `/` bukan shared mount untuk rootless container. Peringatan
tersebut dicatat sebagai informasi konfigurasi lingkungan, bukan kegagalan
instalasi.

![Instalasi Podman](images/14-menginstal%20podman.png)

![Pemeriksaan versi Podman](images/15-cek%20versi%20podman.png)

![Pemeriksaan konfigurasi Podman](images/16-memeriksa%20konfigurasi%20podman.png)

### 4.8 Membangun dan Menjalankan Container dengan Podman

Image yang sama dibangun menggunakan Podman:

```bash
podman build -f Dockerfile -t flaskr:1.0.0 .
```

Proses build menyelesaikan seluruh tahap Dockerfile dan menghasilkan image
`localhost/flaskr:1.0.0`. Daftar image diperiksa dengan:

```bash
podman images
```

Container dijalankan menggunakan:

```bash
podman run -d --name flaskr-podman -p 5001:5000 flaskr:1.0.0
podman ps
```

Output `podman ps` menunjukkan container `flaskr-podman` berstatus **Up** dengan
mapping `0.0.0.0:5001->5000/tcp`. Hal ini membuktikan image aplikasi yang sama
dapat dijalankan menggunakan Podman.

![Membangun image dengan Podman](images/17-membuat%20podman%20image.png)

![Memeriksa Podman image](images/18-memeriksa%20podman%20image.png)

![Menjalankan Podman container](images/19-menjalankan%20docker%20container.png)

### 4.9 Menghentikan dan Menghapus Container Podman

Container Podman dihentikan dan dihapus dengan:

```bash
podman stop flaskr-podman
podman rm flaskr-podman
podman ps -a
```

Perintah `podman ps -a` tidak lagi menampilkan container `flaskr-podman`, sehingga
container telah berhasil dibersihkan setelah pengujian.

![Menghentikan dan menghapus Podman container](images/21-menghentikan%20podman%20container.png)

## 5. Hasil Praktikum

| No. | Tahap               | Hasil yang Terlihat                                                          |
| --- | ------------------- | ---------------------------------------------------------------------------- |
| 1   | Pemeriksaan `uv`    | `uv 0.13.7` tersedia.                                                        |
| 2   | Clone repository    | Repository Flask berhasil di-clone dari GitHub.                              |
| 3   | Environment Python  | Python `3.14.4` berhasil dipasang dan environment aktif.                     |
| 4   | Dependensi aplikasi | Delapan paket berhasil dipasang dengan `uv pip install -e .`.                |
| 5   | Aplikasi lokal      | Flaskr berjalan pada `localhost:5000` dan menampilkan halaman Posts.         |
| 6   | Dockerfile          | Dockerfile dibuat dengan base image `python:3.14` dan port container `5000`. |
| 7   | Docker image        | Image `flaskr:1.0.0` berhasil dibuat dengan Docker.                          |
| 8   | Docker container    | `flaskr-docker` berjalan pada host port `5001`.                              |
| 9   | Pengujian Docker    | Aplikasi dapat dibuka melalui `localhost:5001`.                              |
| 10  | Podman              | Podman `5.7.0` berhasil dipasang dan dikonfigurasi.                          |
| 11  | Podman image        | Image `localhost/flaskr:1.0.0` berhasil dibuat.                              |
| 12  | Podman container    | `flaskr-podman` berjalan pada host port `5001`.                              |
| 13  | Pembersihan         | Container Docker dan Podman berhasil dihentikan serta dihapus.               |

## 6. Analisis

Praktikum menunjukkan bahwa aplikasi Flask dapat dipindahkan dari lingkungan
pengembangan lokal ke lingkungan container tanpa mengubah struktur utama
aplikasi. Pada tahap lokal, aplikasi berjalan langsung pada environment Python
3.14.4 dan dapat diakses melalui port `5000`. Setelah dibuat menjadi image,
aplikasi memiliki lingkungan eksekusi yang lebih konsisten karena Python,
source code, dependensi, dan inisialisasi database didefinisikan melalui
Dockerfile.

Pemetaan port menjadi bagian penting pada saat container dijalankan. Flask
mendengarkan port `5000` di dalam container, sedangkan port host `5001`
digunakan untuk mengakses layanan dari browser. Dengan demikian, format
`-p 5001:5000` berarti port `5001` pada host diteruskan ke port `5000` pada
container.

Docker dan Podman menggunakan instruksi Dockerfile yang sama dan menghasilkan
image aplikasi yang dapat dijalankan dengan alur perintah yang serupa. Perbedaan
nama image pada daftar Podman, yaitu `localhost/flaskr:1.0.0`, menunjukkan
penamaan registry lokal Podman. Hasil pengujian membuktikan bahwa aplikasi yang
sama dapat dijalankan pada kedua runtime.

Pembuatan container juga memisahkan siklus hidup aplikasi dari image. Container
dapat dihentikan dan dihapus tanpa harus membangun ulang image. Karena itu,
image berfungsi sebagai artefak aplikasi, sedangkan container berfungsi sebagai
instance sementara yang dapat dibuat ulang sesuai kebutuhan.

## 7. Kendala dan Solusi

| Kendala yang Ditemukan                                                       | Solusi atau Pemahaman yang Diperoleh                                                     |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Aplikasi membutuhkan versi Python tertentu.                                  | Memasang Python `3.14.4` dan membuat virtual environment dengan `uv`.                    |
| Dependensi belum tersedia pada environment baru.                             | Menjalankan `uv pip install -e .` sebelum menjalankan aplikasi.                          |
| Aplikasi Flask di dalam container harus dapat diakses dari host.             | Menjalankan Flask dengan `--host=0.0.0.0` dan memetakan port `5001:5000`.                |
| Container perlu diuji tanpa mengganggu layanan lokal pada port 5000.         | Menggunakan port host `5001` untuk container.                                            |
| Terdapat peringatan pada `podman info` mengenai `/` yang bukan shared mount. | Peringatan dicatat sebagai informasi konfigurasi rootless; build dan run tetap berhasil. |
| Container tidak lagi diperlukan setelah pengujian.                           | Menjalankan `docker stop`/`docker rm` dan `podman stop`/`podman rm`.                     |

## 8. Kesimpulan

Praktikum pertemuan ketujuh berhasil menerapkan containerisasi pada aplikasi
Flask. Aplikasi berhasil dijalankan secara lokal menggunakan Python 3.14.4,
kemudian dikemas menjadi image `flaskr:1.0.0` menggunakan Dockerfile. Image
tersebut berhasil dijalankan dengan Docker dan diakses melalui
`http://localhost:5001`.

Podman juga berhasil dipasang dengan versi `5.7.0`, digunakan untuk membangun
image, dan menjalankan aplikasi Flask pada port yang sama. Hasil ini
menunjukkan bahwa Docker dan Podman dapat menjalankan aplikasi dari Dockerfile
yang sama. Setelah pengujian selesai, seluruh container berhasil dihentikan dan
dihapus, sedangkan image tetap menjadi artefak yang dapat digunakan kembali.

## 9. Referensi

1. [Flask Documentation](https://flask.palletsprojects.com/)
2. [Docker Documentation](https://docs.docker.com/)
3. [Podman Documentation](https://docs.podman.io/)
4. [uv Documentation](https://docs.astral.sh/uv/)
5. [Repository Flask](https://github.com/pallets/flask)
