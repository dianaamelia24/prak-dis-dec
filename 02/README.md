# Laporan Praktikum Sistem Terdistribusi dan Terdesentralisasi

## Pertemuan 02: Komunikasi Antar Proses pada Sistem Terdistribusi

### Identitas

- Nama: **Diana Amelia**
- NIM: **255410042**
- Kelas: **Informatika-1**

## 1. Tujuan

1. Mengidentifikasi proses yang sedang berjalan pada sistem operasi Windows.
2. Mengamati proses yang dibuat ketika sebuah aplikasi dijalankan.
3. Mempelajari cara me-restart dan menghentikan proses menggunakan PowerShell.
4. Membuat dan menjalankan GraphQL server menggunakan Python dan Strawberry.
5. Membuat client yang berkomunikasi dengan GraphQL server melalui HTTP.
6. Menganalisis komunikasi antar proses client dan server pada sistem terdistribusi.

## 2. Dasar Teori

### 2.1 Proses

Proses adalah program yang sedang dieksekusi oleh sistem operasi. Sebuah proses memiliki
kode program, data, resource, serta informasi state seperti stack dan heap. Ketika
aplikasi dijalankan, sistem operasi membuat proses dan memberikan resource yang
dibutuhkan aplikasi tersebut.

Pada satu node, proses dikelola oleh sistem operasi. Sistem operasi bertanggung jawab
terhadap penjadwalan, alokasi resource, penghentian, dan komunikasi antarproses. Pada
Windows, proses dapat diamati melalui Task Manager atau PowerShell. Setiap proses
memiliki Process ID (PID) yang dapat digunakan sebagai identitas untuk melakukan
operasi tertentu, misalnya menghentikan proses.

### 2.2 Komunikasi Antar Proses pada Sistem Terdistribusi

Komunikasi antar proses pada node yang sama relatif sederhana karena proses berada
di bawah pengelolaan sistem operasi yang sama. Sebaliknya, proses yang berada pada
node berbeda tidak dapat menggunakan shared memory karena masing-masing node
memiliki memori dan pengelolaan resource sendiri. Node juga tidak selalu memiliki
clock yang sama.

Oleh karena itu, komunikasi antarproses pada sistem terdistribusi dilakukan melalui
jaringan menggunakan protokol tertentu. Pada praktikum ini, komunikasi dilakukan
antara client dan server melalui HTTP dengan GraphQL sebagai spesifikasi query.
Client mengirimkan request berisi query GraphQL, kemudian server memproses query
tersebut dan mengembalikan response dalam format JSON.

### 2.3 GraphQL dan Strawberry

GraphQL adalah bahasa query untuk API yang memungkinkan client menentukan field data
yang ingin diterima. Server menyediakan schema yang mendefinisikan tipe data dan
operasi yang dapat dipanggil client. Strawberry merupakan library Python yang
digunakan untuk membuat GraphQL schema dan menjalankannya sebagai server ASGI.

Pada praktikum ini, schema menyediakan query `books` yang mengembalikan daftar buku
beserta `title` dan `author`. Client Python mengirimkan query tersebut ke endpoint
`http://127.0.0.1:8000/graphql`.

## 3. Alat dan Bahan

- Komputer dengan sistem operasi Windows.
- PowerShell.
- Python 3.14.
- `uv` sebagai pengelola Python dan virtual environment.
- Paket `strawberry-graphql[cli]`.
- Browser untuk mengakses GraphiQL pada endpoint GraphQL.
- Editor kode.
- Source code `schema.py` dan `client.py`.

## 4. Langkah Pengerjaan

### 4.1 Mengamati proses pada satu node

1. Membuka PowerShell dan mengidentifikasi sistem operasi yang digunakan.
2. Menampilkan proses yang sedang berjalan menggunakan Task Manager.
3. Menampilkan daftar proses melalui PowerShell.
4. Menjalankan aplikasi Notepad.
5. Mencari proses Notepad dan mencatat PID-nya.
6. Menghentikan proses menggunakan perintah `Stop-Process -Id <PID>`.
7. Menjalankan kembali aplikasi tersebut untuk mendapatkan PID baru.
8. Menghentikan proses dengan opsi `-Force` untuk menunjukkan penghentian proses
   secara paksa.

Perintah yang digunakan antara lain:

```powershell
Get-Process
Get-Process -Name notepad
Stop-Process -Id <PID>
Stop-Process -Id <PID> -Force
```

Perintah `Stop-Process` digunakan untuk menghentikan proses berdasarkan PID, bukan
dengan memilih menu keluar dari aplikasi. Proses dapat dijalankan kembali setelah
dihentikan, sehingga sistem operasi akan membuat proses baru dengan PID yang dapat
berbeda.

### 4.2 Menyiapkan workspace dan environment Python

1. Membuat workspace dengan nama `workspace-01`.
2. Memastikan versi `uv` tersedia.
3. Memastikan Python 3.14 telah terpasang.
4. Membuat virtual environment menggunakan Python 3.14.
5. Mengaktifkan virtual environment.

Perintah yang digunakan:

```powershell
uv --version
uv python list
uv venv --python 3.14
.\.venv\Scripts\Activate.ps1
```

### 4.3 Menginstal Strawberry dan membuat GraphQL server

1. Menginstal paket Strawberry GraphQL beserta CLI di dalam environment aktif:

   ```powershell
   uv pip install "strawberry-graphql[cli]"
   ```

2. Membuat file `schema.py`.
3. Mendefinisikan tipe `Book` dengan field `title` dan `author`.
4. Mendefinisikan query `books` yang mengembalikan dua data buku.
5. Membuat schema GraphQL dan object aplikasi ASGI.
6. Menjalankan server dengan perintah:

   ```powershell
   strawberry server schema.py
   ```

7. Membuka alamat `http://127.0.0.1:8000/graphql` pada browser.
8. Memasukkan query berikut pada GraphiQL:

   ```graphql
   {
     books {
       title
       author
     }
   }
   ```

9. Menekan tombol **Run** untuk mengirim query dan melihat response.
10. Menghentikan server menggunakan `Ctrl+C` pada terminal yang menjalankan server.

### 4.4 Membuat dan menjalankan client

1. Membuat file `client.py`.
2. Menentukan URL GraphQL pada `http://127.0.0.1:8000/graphql`.
3. Membuat payload JSON yang berisi query GraphQL.
4. Mengirim request HTTP `POST` menggunakan `urllib.request`.
5. Membaca response server dan menampilkannya dalam format JSON.
6. Menjalankan client ketika server masih aktif.
7. Menjalankan kembali client ketika server sudah dihentikan untuk mengamati
   perbedaan hasil komunikasi.

Isi inti query pada client adalah:

```python
query = """
{
  books {
    title
    author
  }
}
"""
```

## 5. Hasil Praktikum

### 5.1 Hasil pengamatan proses

Pada sistem operasi Windows berhasil ditampilkan berbagai proses melalui Task
Manager dan PowerShell. Setelah Notepad dijalankan, proses Notepad muncul pada
daftar proses dan memiliki PID tertentu. Proses tersebut berhasil dihentikan
berdasarkan PID menggunakan PowerShell tanpa menggunakan perintah keluar dari
Notepad. Ketika aplikasi dijalankan kembali, proses dan PID baru muncul. Hal ini
menunjukkan bahwa PID merupakan identitas proses pada saat proses tersebut aktif,
bukan identitas permanen aplikasinya.

![Sistem operasi dan PowerShell](images/01-powershell-dan-sistem-operasi.png)

*Gambar 1. Identifikasi sistem operasi melalui PowerShell.*

![Proses pada Task Manager](images/02-daftar-proses-task-manager.png)

*Gambar 2. Daftar proses yang berjalan pada Task Manager.*

![Proses pada PowerShell](images/03-daftar-proses-powershell.png)

*Gambar 3. Daftar proses yang ditampilkan melalui PowerShell.*

![Notepad dijalankan](images/04-notepad-dijalankan.png)

*Gambar 4. Aplikasi Notepad dijalankan.*

![PID Notepad](images/05-pid-notepad.png)

*Gambar 5. PID proses Notepad ditemukan.*

![Menghentikan proses berdasarkan PID](images/06-stop-proses-dengan-pid.png)

*Gambar 6. Proses Notepad dihentikan menggunakan PID.*

![PID baru setelah aplikasi dijalankan kembali](images/07-aplikasi-dan-pid-baru.png)

*Gambar 7. Aplikasi dijalankan kembali dan memiliki PID baru.*

![Force kill proses](images/08-force-kill-proses.png)

*Gambar 8. Proses dihentikan menggunakan opsi `-Force`.*

### 5.2 Hasil pembuatan GraphQL server

Workspace `workspace-01` berhasil dibuat pada Windows. Python 3.14 terdeteksi,
virtual environment berhasil diaktifkan, dan paket Strawberry GraphQL berhasil
diinstal. File `schema.py` dapat dijalankan sebagai server GraphQL pada port 8000.

![Workspace workspace-01](images/09-workspace-01-windows.png)

*Gambar 9. Workspace `workspace-01` dibuat.*

![Versi uv](images/10-uv-version-windows.png)

*Gambar 10. Pemeriksaan versi `uv`.*

![Python 3.14](images/11-python-314-installed-windows.png)

*Gambar 11. Python 3.14 terpasang pada sistem.*

![Virtual environment aktif](images/12-virtual-environment-aktif-windows.png)

*Gambar 12. Virtual environment berhasil dibuat dan diaktifkan.*

![Instalasi Strawberry](images/13-instalasi-strawberry-windows.png)

*Gambar 13. Paket Strawberry GraphQL diinstal.*

![Isi schema.py](images/14-isi-schema-windows.png)

*Gambar 14. Source code GraphQL server pada `schema.py`.*

![GraphQL server aktif](images/15-graphql-server-aktif-windows.png)

*Gambar 15. GraphQL server aktif pada port 8000.*

### 5.3 Hasil query GraphQL

Query `books` berhasil dijalankan melalui GraphiQL. Server mengembalikan dua
data buku, yaitu **Perahu Kertas** karya **Dee Lestari** dan **Dilan 1990** karya
**Pidi Baiq**. Response yang diperoleh memiliki bentuk:

```json
{
  "data": {
    "books": [
      {
        "title": "Perahu Kertas",
        "author": "Dee Lestari"
      },
      {
        "title": "Dilan 1990",
        "author": "Pidi Baiq"
      }
    ]
  }
}
```

![Query dan response GraphQL](images/16-query-dan-response-windows.png)

*Gambar 16. Query `books` dan response pada GraphiQL.*

![Server dihentikan](images/17-memberhentikan-query-dan-response-windows.png)

*Gambar 17. Server dihentikan dari terminal menggunakan `Ctrl+C`.*

### 5.4 Hasil komunikasi client-server

Client Python berhasil mengirim request `POST` ke endpoint GraphQL dan menerima
response JSON dari server. Hasil ini menunjukkan bahwa proses client dan proses
server dapat berkomunikasi melalui jaringan lokal walaupun keduanya merupakan
proses yang terpisah.

![Request GraphQL dari PowerShell](images/18-request-graphql-powershell.png)

*Gambar 18. Request GraphQL dikirim dari PowerShell.*

![Client GraphQL berhasil](images/19-client-graphql-berhasil-windows.png)

*Gambar 19. Client berhasil menerima response dari GraphQL server.*

![Source code client](images/20-isi-client-windows.png)

*Gambar 20. Isi source code `client.py`.*

![Client GraphQL berhasil](images/22-client-graphql-berhasil-windows.png)

*Gambar 21. Pengujian client kembali berhasil saat server aktif.*

Ketika server tidak aktif, client tidak dapat membangun koneksi ke endpoint
GraphQL. Kondisi tersebut menghasilkan error koneksi. Hal ini sesuai dengan
mekanisme komunikasi client-server karena client membutuhkan server yang sedang
listen pada alamat dan port tujuan.

![Kendala saat menjalankan perintah](images/19-kendala-saat-perintah.png)

*Gambar 22. Kendala saat menjalankan salah satu perintah pada proses praktikum.*

![Client saat server tidak aktif](images/23-client-server-tidak-aktif-windows.png)

*Gambar 23. Client gagal berkomunikasi ketika server tidak aktif.*

## 6. Analisis

Praktikum bagian pertama memperlihatkan bahwa sistem operasi mengelola proses
dengan memberikan PID dan menyediakan operasi untuk melihat maupun menghentikan
proses. Penghentian berdasarkan PID berbeda dengan menutup aplikasi melalui
antarmuka karena perintah tersebut langsung ditujukan kepada proses yang sedang
berjalan. Setelah proses dihentikan dan aplikasi dijalankan kembali, PID dapat
berubah karena sistem operasi membuat instance proses yang baru.

Pada bagian kedua, `schema.py` berperan sebagai server yang menunggu request pada
endpoint GraphQL, sedangkan `client.py` berperan sebagai client yang meminta data.
Client tidak perlu mengetahui bagaimana server menyimpan atau membentuk daftar
buku. Client cukup mengirimkan field yang dibutuhkan melalui query GraphQL dan
server mengembalikan data sesuai schema.

Walaupun pengujian dilakukan pada `127.0.0.1`, konsep komunikasinya tetap
merepresentasikan komunikasi antar proses melalui jaringan. Client dan server
berkomunikasi menggunakan request dan response HTTP, bukan shared memory.
Kegagalan client ketika server dihentikan juga menunjukkan adanya ketergantungan
availability: request hanya dapat diproses apabila server aktif dan endpoint
tujuan dapat dijangkau.

## 7. Kendala dan Solusi

| Kendala | Solusi |
| --- | --- |
| Perintah atau environment belum sesuai saat menyiapkan workspace. | Memeriksa kembali posisi folder, versi `uv`, dan aktivasi virtual environment sebelum menjalankan perintah berikutnya. |
| Client tidak berhasil terhubung ke server. | Memastikan server GraphQL sudah dijalankan pada port 8000 sebelum menjalankan `client.py`. |
| Client menghasilkan error ketika server dihentikan. | Menjalankan kembali server dengan `strawberry server schema.py`, lalu mengulangi request client. |
| Proses harus dihentikan tanpa menggunakan menu keluar aplikasi. | Mencari PID dengan `Get-Process`, kemudian menggunakan `Stop-Process -Id <PID>` atau opsi `-Force`. |

## 8. Kesimpulan

1. Proses pada Windows dapat diamati melalui Task Manager dan PowerShell.
2. Setiap proses memiliki PID yang dapat digunakan untuk mengidentifikasi dan
   menghentikan proses.
3. Proses yang dijalankan kembali dapat memperoleh PID baru.
4. Strawberry dapat digunakan untuk membuat GraphQL server dengan Python.
5. Client dapat berkomunikasi dengan server melalui HTTP menggunakan query GraphQL
   dan menerima response dalam format JSON.
6. Server harus aktif dan dapat dijangkau agar request dari client berhasil.
7. Praktikum menunjukkan perbedaan antara pengelolaan proses pada satu node dan
   komunikasi antarproses melalui jaringan.

## 9. Referensi

1. Modul 2 Praktikum Sistem Terdistribusi dan Terdesentralisasi, **Komunikasi
   Antar Proses pada Sistem Terdistribusi**, Universitas Teknologi Digital
   Indonesia.
2. Strawberry GraphQL. [https://strawberry.rocks/](https://strawberry.rocks/)
3. Dokumentasi Python. [https://docs.python.org/3/](https://docs.python.org/3/)
4. Dokumentasi Microsoft PowerShell, perintah `Get-Process` dan
   `Stop-Process`. [https://learn.microsoft.com/powershell/](https://learn.microsoft.com/powershell/)
