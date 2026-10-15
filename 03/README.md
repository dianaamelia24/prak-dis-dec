# Laporan Praktikum Sistem Terdistribusi dan Terdesentralisasi

## Pertemuan 03: Sinkronisasi pada Sistem Terdistribusi

### Identitas

- Nama: **Diana Amelia**
- NIM: **255410042**
- Kelas: **Informatika-1**

## 1. Tujuan

1. Memahami pentingnya sinkronisasi waktu pada sistem terdistribusi.
2. Menjelaskan cara kerja sinkronisasi waktu menggunakan NTP.
3. Memahami penggunaan vector clock untuk menentukan hubungan kausalitas event.
4. Mengamati dampak ketidaksinkronan pada program multithreaded.
5. Menjelaskan data race dan cara mencegahnya menggunakan lock.
6. Menjelaskan deadlock serta pengaruh urutan pengambilan lock.
7. Memahami proses pemilihan leader pada simulasi algoritma Raft.
8. Membuat contoh penggunaan ulang class atau fungsi dari program praktikum.

## 2. Dasar Teori

### 2.1 Sinkronisasi Waktu

Sinkronisasi waktu adalah proses menyamakan waktu pada beberapa komputer atau
node. Pada sistem terdistribusi, waktu digunakan untuk memberi timestamp,
mengurutkan kejadian, dan mencatat aktivitas. Network Time Protocol (NTP)
melakukan sinkronisasi dengan membandingkan waktu komputer terhadap server waktu.
Chrony dapat digunakan pada Linux, *BSD*, dan macOS, sedangkan NetTime
digunakan pada Windows.

NTP tidak sekadar mengganti jam secara langsung. Client mengirim permintaan ke
server, memperkirakan delay jaringan dan offset waktu, kemudian menyesuaikan jam
secara bertahap. Cara ini mengurangi gangguan terhadap aplikasi yang sedang
berjalan.

### 2.2 Vector Clock

Vector clock adalah struktur data berupa array bilangan yang digunakan untuk
melacak urutan kausal event pada beberapa proses. Setiap proses memiliki satu
posisi pada vector. Aturan dasarnya adalah:

- event lokal menaikkan nilai pada posisi proses itu sendiri;
- proses pengirim menaikkan clock sebelum mengirim pesan;
- proses penerima mengambil nilai maksimum dari clock lokal dan clock pesan,
  kemudian menaikkan clock miliknya;
- event A terjadi sebelum B apabila semua komponen vector A kurang dari atau
  sama dengan B dan sekurang-kurangnya satu komponennya lebih kecil;
- dua event disebut concurrent apabila tidak ada yang terjadi sebelum event
  lainnya.

### 2.3 Data Race dan Deadlock

Data race terjadi ketika beberapa thread mengakses data bersama pada waktu yang
berdekatan dan setidaknya salah satunya melakukan perubahan, tanpa pengaturan
akses yang memadai. Akibatnya, pemeriksaan kondisi dan perubahan data dapat
terjadi berdasarkan nilai yang sudah tidak sesuai.

Deadlock adalah keadaan ketika thread saling menunggu resource yang tidak akan
pernah dilepaskan. Salah satu pola deadlock adalah thread pertama memegang Lock A
dan menunggu Lock B, sementara thread kedua memegang Lock B dan menunggu Lock A.

### 2.4 Algoritma Raft

Raft adalah algoritma konsensus yang menggunakan beberapa node dengan status
`FOLLOWER`, `CANDIDATE`, dan `LEADER`. Follower yang tidak menerima heartbeat
dalam batas waktu tertentu memulai pemilihan dengan menaikkan term dan memilih
dirinya sendiri. Jika memperoleh suara mayoritas, node berubah menjadi leader.
Leader kemudian mengirim heartbeat dan dapat menerima command untuk dicatat pada
log.

## 3. Alat dan Bahan

- Laptop atau komputer dengan Windows.
- Python 3.
- Python threading dan library standar `time`, `random`, serta `enum`.
- NetTime untuk sinkronisasi waktu ke server NTP.
- Text editor atau Visual Studio Code.
- Source code pada folder [03](../03/):
  [vclocks.py](vclocks.py), [multithreads-example.py](multithreads-example.py),
  [race-conditions-01.py](race-conditions-01.py),
  [race-conditions-02.py](race-conditions-02.py),
  [deadlock-01.py](deadlock-01.py), [deadlock-02.py](deadlock-02.py), dan
  [raft.py](raft.py).

## 4. Langkah Pengerjaan

### 4.1 Sinkronisasi Waktu dengan NetTime

NetTime diinstal pada Windows, kemudian dijalankan dengan hak akses yang
diperlukan. Pada pengaturan server waktu digunakan server NTP yang tersedia.
Setelah konfigurasi disimpan, proses sinkronisasi dijalankan dan waktu komputer
disesuaikan dengan waktu server.

NetTime mengirim permintaan waktu ke server NTP, menerima informasi waktu,
menghitung perbedaan waktu komputer dengan server, lalu melakukan penyesuaian.
Hasil instalasi dan konfigurasi didokumentasikan pada gambar berikut.

![Instalasi dan konfigurasi NetTime](images/01-Install%20Nettime.png)

### 4.2 Menjalankan Vector Clock

Program dijalankan dengan perintah berikut:

```bash
python .\vclocks.py
```

Program membuat tiga proses, yaitu P0, P1, dan P2. P0 melakukan event lokal,
mengirim pesan kepada P1, P2 melakukan event lokal, kemudian P1 mengirim pesan
kepada P2. Setiap pesan membawa salinan vector clock pengirim.

![Keluaran program vector clock](images/02-vclockspy-output.png)

### 4.3 Menjalankan Program Multithreaded

Program contoh dijalankan menggunakan:

```bash
python .\multithreads-example.py
```

Lima thread A sampai E dimulai hampir bersamaan. Perintah `join()` membuat
program menunggu semua thread selesai sebelum mencetak `All tasks completed.`.
Program dijalankan beberapa kali untuk mengamati bahwa urutan keluaran dapat
berbeda.

![Keluaran multithreaded](images/03-multithreads-output.png)

### 4.4 Mengamati Data Race

Contoh tanpa lock dijalankan dengan:

```bash
python .\race-conditions-01.py
```

Kemudian contoh yang menggunakan `threading.Lock` dijalankan dengan:

```bash
python .\race-conditions-02.py
```

Kedua thread mencoba menarik saldo sebesar Rp80 dari saldo awal Rp100. Hasil
kedua program dibandingkan untuk melihat pengaruh sinkronisasi.

![Data race tanpa lock](images/04-race-conditions-01.png)

![Pencegahan data race dengan lock](images/05-race-conditions-2.png)

### 4.5 Mengamati Penggunaan Lock

Program [deadlock-01.py](deadlock-01.py) dan [deadlock-02.py](deadlock-02.py)
dijalankan dengan perintah:

```bash
python .\deadlock-01.py
python .\deadlock-02.py
```

Keluaran dan perilaku kedua program dicatat. Jika program berhenti menunggu,
proses dihentikan setelah kondisi tersebut diamati.

![Keluaran deadlock-01](images/06-deadlock-01.png)

![Keluaran deadlock-02](images/07-deadlock-2.png)

### 4.6 Menjalankan Simulasi Raft

Simulasi dijalankan dengan:

```bash
python .\raft.py
```

Program menjalankan 20 langkah simulasi. Pada setiap langkah, status node,
term, dan panjang log ditampilkan. Timeout acak digunakan untuk memicu pemilihan
leader jika heartbeat belum diterima.

![Keluaran simulasi Raft](images/08-raftpy.png)

## 5. Hasil Praktikum

### 5.1 Hasil Sinkronisasi Waktu

NetTime berhasil digunakan untuk mengatur sinkronisasi waktu melalui server NTP.
Prosesnya meliputi pemilihan server, pengiriman permintaan, perhitungan selisih
waktu, dan penyesuaian jam komputer. Bukti konfigurasi terdapat pada gambar
instalasi NetTime.

### 5.2 Hasil Vector Clock

Urutan perubahan vector clock pada source code adalah sebagai berikut:

| Tahap | P0 | P1 | P2 |
| --- | --- | --- | --- |
| Kondisi awal | `[0, 0, 0]` | `[0, 0, 0]` | `[0, 0, 0]` |
| P0 event lokal | `[1, 0, 0]` | `[0, 0, 0]` | `[0, 0, 0]` |
| P0 mengirim pesan | `[2, 0, 0]` | `[2, 1, 0]` | `[0, 0, 0]` |
| P2 event lokal | `[2, 0, 0]` | `[2, 1, 0]` | `[0, 0, 1]` |
| P1 mengirim ke P2 | `[2, 0, 0]` | `[2, 2, 0]` | `[2, 2, 2]` |

Keluaran pemeriksaan kausalitas adalah:

```text
VC0 happens before VC1: True
VC1 happens before VC0: False
VC0 is concurrent with VC2: False
```

Hasil tersebut sesuai dengan perhitungan manual. P0 terjadi sebelum P1 karena
vector P0 `[2, 0, 0]` seluruh komponennya tidak lebih besar daripada vector P1
`[2, 2, 0]` dan ada komponen yang lebih kecil. P1 tidak terjadi sebelum P0.
P0 juga tidak concurrent dengan P2 karena P0 terjadi sebelum vector P2
`[2, 2, 2]`.

### 5.3 Hasil Multithreaded

Waktu mulai dan selesai tiap task dipengaruhi oleh scheduler serta delay
masing-masing thread. Task D dengan delay satu detik umumnya selesai paling
awal, sedangkan task C dengan delay sembilan detik umumnya selesai paling akhir.
Namun, urutan pesan `starting` dan pesan selesai tidak sebaiknya dianggap sebagai
urutan sekuensial karena seluruh thread berjalan secara konkuren.

### 5.4 Hasil Data Race

Pada [race-conditions-01.py](race-conditions-01.py), kedua thread dapat
membaca saldo Rp100 sebelum salah satunya menyelesaikan pengurangan. Karena itu,
keduanya dapat melewati pemeriksaan `balance >= amount`, sehingga saldo akhir
dapat menjadi tidak sesuai dengan aturan saldo dan bahkan dapat tercetak negatif.
Nilai yang terlihat dapat berbeda antarpelaksanaan.

Pada [race-conditions-02.py](race-conditions-02.py), blok `with
counter_lock` memastikan hanya satu thread yang memeriksa dan mengubah saldo
pada satu waktu. Thread kedua baru memeriksa saldo setelah thread pertama
selesai. Dengan saldo Rp100 dan penarikan Rp80, hanya satu penarikan yang
seharusnya berhasil dan saldo akhir menjadi Rp20.

### 5.5 Hasil Penggunaan Lock

Pada [deadlock-01.py](deadlock-01.py), setiap thread melepaskan lock pertama
sebelum mencoba memperoleh lock kedua. Selain itu, pemanggilan `acquire` memakai
timeout. Berdasarkan implementasi ini, program tidak mempertahankan dua lock
secara bersamaan sehingga pola circular wait tidak terbentuk.

Sebaliknya, [deadlock-02.py](deadlock-02.py) menggunakan urutan berbeda:
Thread 1 mengunci A lalu menunggu B, sedangkan Thread 2 mengunci B lalu
menunggu A. Keduanya menahan lock yang dimiliki dan menunggu lock milik thread
lain. Kondisi ini membentuk circular wait dan `join()` dapat menunggu tanpa
batas, sehingga program tampak berhenti.

### 5.6 Hasil Simulasi Raft

Semua node awalnya berstatus follower. Setelah timeout pemilihan tercapai, node
menjadi candidate, menaikkan term, dan memberikan suara kepada dirinya sendiri.
Source code menyederhanakan proses pemungutan suara dengan menganggap node lain
memberikan suara, sehingga candidate memperoleh mayoritas dan menjadi leader.
Keluaran kemudian menampilkan pesan seperti:

```text
Node 1 elected leader in term 1
Node 1: LEADER | Term 1 | Log len 0
```

Nomor node dan term dapat berbeda karena timeout menggunakan nilai acak. Leader
mengirim heartbeat kepada follower. Pada langkah tertentu leader menambahkan
command ke log, sehingga panjang log bertambah.

![Keluaran tambahan multithreaded](images/09-multithreads-output2.png)

## 6. Analisis

Praktikum menunjukkan bahwa sinkronisasi pada sistem terdistribusi memiliki
beberapa bentuk. Sinkronisasi waktu menyamakan referensi waktu antarkomputer,
sedangkan vector clock tidak menyamakan jam fisik. Vector clock justru
menyimpan informasi kausalitas sehingga hubungan antar-event tetap dapat
diketahui walaupun waktu fisik node berbeda.

Pada program multithreaded, `start()` membuat beberapa thread berjalan secara
bersamaan dan `join()` hanya mengatur kapan thread utama melanjutkan eksekusi.
`join()` tidak menentukan urutan kerja thread. Oleh sebab itu, output dapat
berubah walaupun source code tidak berubah.

Race condition muncul karena operasi memeriksa saldo lalu mengurangi saldo
bukan satu operasi atomik. Lock mengubah bagian tersebut menjadi critical
section. Hasilnya, thread lain tidak dapat menyela di antara pemeriksaan dan
perubahan saldo.

Deadlock memiliki penyebab yang berbeda dari race condition. Pada deadlock,
nilai data belum tentu salah, tetapi thread tidak dapat melanjutkan karena
saling menunggu. Penguncian resource dengan urutan yang konsisten, timeout,
atau pelepasan lock sebelum mengambil lock lain dapat digunakan untuk
mengurangi risiko tersebut.

Simulasi Raft memperlihatkan pola konsensus secara sederhana: timeout memicu
pergantian state, term membedakan periode pemilihan, suara mayoritas memilih
leader, dan heartbeat menjaga follower tetap mengikuti leader. Implementasi ini
belum merupakan Raft lengkap karena replikasi log dan RPC masih disederhanakan.

## 7. Kendala dan Solusi

| Kendala yang Ditemukan | Solusi atau Pemahaman yang Diperoleh |
| --- | --- |
| Output thread dapat berbeda setiap kali program dijalankan. | Output dicatat sebagai hasil konkuren, bukan sebagai urutan tetap. |
| Data race tidak selalu tampak pada setiap eksekusi. | Delay `time.sleep(0.01)` memperbesar peluang interleaving dan hasil dibandingkan dengan versi ber-lock. |
| Program `deadlock-02.py` dapat menunggu tanpa selesai. | Kondisi circular wait diamati dan proses dihentikan setelah bukti deadlock diperoleh. |
| Hasil pemilihan leader Raft dapat berubah. | Timeout acak dan nomor node yang terpilih dijelaskan sebagai bagian dari simulasi. |
| Vector clock sulit dibaca hanya dari output. | Setiap event ditulis ulang dalam tabel dan dibandingkan dengan perhitungan manual. |
| Waktu komputer perlu disesuaikan dengan server. | NetTime dikonfigurasi menggunakan server NTP sebelum sinkronisasi dijalankan. |

## 8. Kesimpulan

Praktikum modul 3 berhasil menunjukkan bahwa sinkronisasi diperlukan untuk
menjaga keteraturan dan konsistensi pada sistem terdistribusi. NetTime
menyinkronkan waktu komputer melalui NTP, sedangkan vector clock membantu
menentukan hubungan kausalitas tanpa bergantung pada jam fisik.

Program multithreaded memperlihatkan bahwa pola output tidak selalu dapat
diprediksi. Race condition terjadi ketika saldo bersama diakses tanpa lock dan
dapat dicegah menggunakan `threading.Lock`. Deadlock berkaitan dengan urutan
pengambilan resource; dua thread yang saling menunggu dapat membuat program
berhenti. Terakhir, simulasi Raft menunjukkan perubahan follower menjadi
candidate dan leader berdasarkan timeout, term, serta suara mayoritas.

## 9. Referensi

1. [Chrony Project](https://chrony-project.org/)
2. [NetTime](https://www.timesynctool.com/)
3. [Python `threading` documentation](https://docs.python.org/3/library/threading.html)
4. [Python `time` documentation](https://docs.python.org/3/library/time.html)
5. [Raft Consensus Algorithm](https://raft.github.io/)
6. Source code praktikum pada folder [03](../03/).