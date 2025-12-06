## 🔍 Analisis SOLID & Solusi Refactoring

Berikut adalah penjabaran detail mengenai pelanggaran prinsip SOLID dan bagaimana kode baru memperbaikinya:

### 1. Single Responsibility Principle (SRP)
> *"Sebuah kelas harus memiliki satu, dan hanya satu, alasan untuk berubah."*

| Sebelum (Violation) | Sesudah (Refactoring) |
| :--- | :--- |
| **Masalah:** Kelas `ValidatorManager` menangani validasi SKS, validasi Prasyarat, dan manajemen registrasi sekaligus. | **Solusi:** Tanggung jawab dipecah menjadi kelas-kelas kecil: <br> • `SksLimitRule`: Khusus validasi SKS. <br> • `PrerequisiteRule`: Khusus validasi mata kuliah. <br> • `RegistrationService`: Khusus koordinator alur registrasi. |

### 2. Open/Closed Principle (OCP)
> *"Kelas harus terbuka untuk ekstensi, tetapi tertutup untuk modifikasi."*

| Sebelum (Violation) | Sesudah (Refactoring) |
| :--- | :--- |
| **Masalah:** Untuk menambah aturan validasi baru (misal: Cek Jadwal), kita **harus mengedit** kode sumber `ValidatorManager` dan menambah blok `elif` baru. Ini berisiko merusak fitur lama. | **Solusi:** `RegistrationService` bersifat **tertutup** untuk modifikasi. Untuk menambah fitur, kita cukup membuat kelas baru (ekstensi) yang mewarisi `IValidationRule`. Tidak ada kode inti yang disentuh. |

### 3. Dependency Inversion Principle (DIP)
> *"Bergantunglah pada abstraksi, bukan pada implementasi konkrit."*

| Sebelum (Violation) | Sesudah (Refactoring) |
| :--- | :--- |
| **Masalah:** Modul tingkat tinggi bergantung langsung pada logika detail yang ditulis *hardcoded* di dalam fungsi. | **Solusi:** `RegistrationService` kini bergantung pada **Abstraksi** (Interface) bernama `IValidationRule`. Aturan validasi disuntikkan dari luar (*Dependency Injection*), membuat sistem lebih fleksibel. |