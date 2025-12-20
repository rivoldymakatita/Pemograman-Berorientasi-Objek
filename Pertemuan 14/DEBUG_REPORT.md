1. Deskripsi Bug
Ditemukan kesalahan logika pada fungsi hitung_diskon di mana harga akhir yang dihasilkan jauh melebihi ekspektasi. Masalah utama terletak pada penambahan pajak (PPN) 10% yang terjadi sebanyak dua kali, sehingga harga yang seharusnya mendapatkan diskon justru menjadi lebih mahal dari harga awal.


2. Skenario Pengujian
Input: harga_awal = 1000, persentase_diskon = 10.

Ekspektasi: 900.0 (Harga setelah diskon 10% tanpa PPN).

Hasil Aktual: 1089.0.


3. Langkah Penelusuran (Trace Log) menggunakan pdb
Berikut adalah langkah-langkah yang dilakukan untuk menemukan akar masalah menggunakan perintah dasar pdb:

Menyisipkan Breakpoint: Menambahkan import pdb; pdb.set_trace() di dalam metode hitung_diskon.

Menjalankan Program: Mengeksekusi file debug.py di terminal.

Menelusuri Alur (n): Melangkah baris demi baris untuk memantau perubahan nilai variabel.

Bukti Penemuan Bug (Pemeriksaan Variabel)
Perintah p [nama_variabel] digunakan untuk membuktikan adanya perhitungan PPN ganda:

# Program berhenti di breakpoint
-> harga_setelah_diskon = harga_awal - jumlah_diskon

(Pdb) n
> debug.py(10)hitung_diskon()
-> harga_dengan_ppn_1 = harga_setelah_diskon * 1.1

(Pdb) n
> debug.py(12)hitung_diskon()
-> harga_akhir = harga_dengan_ppn_1 * 1.1

# PEMBUKTIAN VARIABEL
(Pdb) p harga_setelah_diskon
900.0  # Nilai ini sudah benar (1000 - 100) 

(Pdb) p harga_dengan_ppn_1
990.0  # PPN 10% pertama ditambahkan (900 * 1.1) 

(Pdb) n
(Pdb) p harga_akhir
1089.0 # AKAR MASALAH: PPN 10% ditambahkan kembali (990 * 1.1)


4. Akar Masalah (Root Cause)
Berdasarkan log di atas, bug disebabkan oleh redundansi logika pada baris harga_dengan_ppn_1 dan harga_akhir. Sistem melakukan perkalian dengan faktor 1.1 sebanyak dua kali secara beruntun, yang secara matematis mengakibatkan kenaikan harga total sebesar 21% dari harga setelah diskon.


5. Perbaikan
Sesuai dengan tujuan awal fungsi untuk menghitung diskon saja, baris yang mengandung pengali 1.1 harus dihapus, sehingga variabel harga_akhir langsung mengambil nilai dari harga_setelah_diskon.