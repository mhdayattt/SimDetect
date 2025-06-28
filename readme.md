# SIMDetect - Tools Informasi Nomor HP & SIM Akurat

[![Versi Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Lisensi: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sebuah tools berbasis command-line (CLI) yang berfokus pada penyediaan informasi akurat mengenai nomor telepon, termasuk validasi, tipe (seluler/telepon rumah/VOIP), operator, negara, dan zona waktu. Tools ini mengandalkan API pihak ketiga (Veriphone) dan pustaka `phonenumbers` untuk mendapatkan data.

## ✨ Fitur Utama

-   **Validasi Nomor Telepon:** Memeriksa apakah format nomor telepon valid secara struktural.
-   **Pencarian Data Akurat:** Memanfaatkan Veriphone API untuk detail presisi mengenai validitas nomor, tipe (misalnya, seluler, telepon rumah, VoIP), dan informasi operator.
-   **Cakupan Global:** Mendukung format nomor telepon internasional dari berbagai negara.
-   **Output Rinci:** Menyediakan nama operator, negara, kode negara, zona waktu, dan estimasi lokasi kota/area (dengan penjelasan keterbatasan).
-   **Mekanisme Fallback:** Jika Veriphone API gagal atau tidak tersedia, tools akan mencoba menampilkan informasi dasar dari pustaka `phonenumbers`.
-   **Antarmuka CLI yang Bersih & Menarik:** Dirancang dengan antarmuka terminal berwarna yang terinspirasi dari tools-tools di Kali Linux.

## ⚠️ Catatan Penting & Disclaimer

* **Membutuhkan API Key:** Tools ini sangat bergantung pada Veriphone API. API key yang valid sangat penting untuk mendapatkan informasi yang akurat dan lengkap. Anda bisa mendapatkan API key (biasanya ada tier gratis dengan batasan harian) dari [veriphone.io](https://veriphone.io/).
* **Privasi & Etika:** Harap gunakan tools ini secara bertanggung jawab dan etis. Mengumpulkan informasi pribadi tanpa persetujuan dapat melanggar hukum privasi data. Tools ini ditujukan untuk tujuan edukasi, investigasi yang sah, atau penggunaan pribadi pada nomor Anda sendiri.
* **Akurasi Lokasi (Nomor Seluler):** Perlu diperhatikan bahwa mendapatkan *kota spesifik* atau *lokasi geografis yang sangat akurat* untuk nomor telepon seluler adalah **sangat sulit, seringkali tidak tersedia untuk umum, dan umumnya tidak mungkin** menggunakan tools seperti ini karena alasan privasi dan sifat nomor seluler yang portabel. Output "Kota/Area (Estimasi)" didasarkan pada data alokasi regional awal nomor, bukan lokasi fisik pengguna saat ini. Harapkan informasi setingkat negara atau wilayah yang lebih luas, bukan akurasi jalan atau alamat.

## 🚀 Cara Menggunakan (Untuk Kali Linux)

Ikuti langkah-langkah mudah ini untuk menjalankan SIMDetect di sistem Kali Linux Anda:

1.  **Buka Terminal Anda di Kali Linux.**

2.  **Kloning repositori ini:**
    Perintah ini akan mengunduh semua file tools SIMDetect ke komputer Anda.
    ```bash
    git clone [https://github.com/mhdayattt/SIMDetect.git](https://github.com/mhdayattt/SIMDetect.git)
    ```

3.  **Masuk ke direktori tools:**
    ```bash
    cd SIMDetect
    ```

4.  **Instal semua dependensi yang diperlukan:**
    Perintah ini akan menginstal semua pustaka Python yang dibutuhkan tools agar bisa berjalan dengan baik. Pastikan Anda memiliki koneksi internet.
    ```bash
    sudo pip install -r requirements.txt
    ```
    *(Gunakan `sudo` karena Anda menginstal secara global ke sistem Kali Linux Anda.)*

5.  **Pengaturan API Key:**
    * Dapatkan API key (gratis atau berbayar) dari [veriphone.io](https://veriphone.io/).
    * Buka file `simdetect.py` menggunakan editor teks favorit Anda (misalnya `nano`):
        ```bash
        nano simdetect.py
        ```
    * Cari baris berikut (biasanya di dekat bagian atas file):
        ```python
        VERIPHONE_API_KEY = "3A99D5B325584F9F8D0624742239434B" # GANTI DENGAN API KEY ANDA
        ```
    * Ganti `"3A99D5B325584F9F8D0624742239434B"` dengan API Key Veriphone Anda yang sebenarnya.
    * Simpan perubahan file (di `nano`, tekan `Ctrl+O` lalu `Enter`, lalu `Ctrl+X`).

6.  **Jalankan tools:**
    Sekarang tools Anda siap untuk dijalankan!
    ```bash
    python3 simdetect.py
    ```

7.  Ikuti instruksi di layar. Anda akan diminta untuk memasukkan nomor telepon dalam format internasional (contoh: `+12025550123`, `+6281234567890`).
8.  Ketik `exit` untuk keluar dari tools kapan saja.

## 🙏 Kontributor

* Dibuat oleh [YatAja](https://github.com/mhdayattt)
* Terinspirasi dari tools informasi nomor telepon yang sudah ada.

## 📄 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT - lihat file [LICENSE](LICENSE) untuk detailnya.