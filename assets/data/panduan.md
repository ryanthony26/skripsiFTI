

## 🏠 Beranda
Halaman ini merupakan halaman utama yang berfungsi sebagai titik awal penggunaan aplikasi. 
Pada halaman ini disajikan penjelasan ringkas mengenai tujuan aplikasi, metode analisis yang digunakan, 
serta tombol untuk memulai proses pengujian data secara langsung.

> **Catatan:** Tekan tombol **"Mulai Uji Sekarang"** untuk memulai proses pemodelan dari tahap awal.

---

## 📂 Data
Modul ini digunakan untuk mengunggah dan memvalidasi dataset cuaca yang akan dianalisis menggunakan aplikasi ini.

### Prosedur Pengunggahan Data
1. Siapkan dataset dalam format **`.csv`** atau **`.xlsx`**.
2. Pastikan dataset telah memuat kolom-kolom yang dibutuhkan sesuai ketentuan sistem.
3. Unggah dataset melalui komponen unggah berkas (file uploader) pada halaman ini.
4. Periksa dan pastikan format data telah sesuai sebelum melanjutkan ke tahap pemrosesan.

> **Informasi Tambahan:** Aplikasi menyediakan _template dataset_ yang dapat diunduh apabila pengguna belum memiliki data dengan format yang sesuai.

---

## 📊 Hasil & Analisis
Halaman ini menampilkan **hasil klasifikasi** serta **analisis performa model** dengan membandingkan dua pendekatan:

- **PCA + LDA (Principal Component Analysis + Linear Discriminant Analysis)**
- **LDA tanpa reduksi dimensi**

### Visualisasi yang Ditampilkan
- Confusion Matrix
- Nilai Akurasi Model
- Perbandingan Akurasi Antar Metode

Analisis ini bertujuan untuk mengevaluasi pengaruh proses reduksi dimensi terhadap kualitas hasil klasifikasi.

---

## 🧪 Uji
Modul ini digunakan untuk melakukan pengujian terhadap model yang telah dihasilkan.

### Langkah Pengujian
1. Masukkan data baru atau pilih data yang tersedia.
2. Klik tombol **"Klasifikasi"** untuk memproses data.
3. Hasil klasifikasi dan tingkat akurasi akan ditampilkan pada layar.

Modul uji ini membantu pengguna memahami performa model dalam kondisi aktual.

---

## 📘 Panduan Teknis
Halaman ini menyediakan instruksi penggunaan aplikasi agar pengguna dapat menjalankan setiap modul dengan baik.

### Materi yang Dibahas
- Alur penggunaan aplikasi
- Format data yang diterima sistem
- Penjelasan langkah pemrosesan model
- Interpretasi hasil keluaran model

Panduan ini dirancang agar mudah dipahami baik oleh pengguna pemula maupun berpengalaman.

---

## ℹ️ Tentang Aplikasi
Halaman ini memuat informasi mengenai tujuan pengembangan aplikasi serta identitas pengembang.

### Tujuan Pengembangan
Aplikasi ini dikembangkan untuk mendukung analisis prediksi cuaca ekstrem berbasis pembelajaran mesin, 
sehingga proses pengambilan keputusan dapat dilakukan secara lebih cepat dan terukur.
