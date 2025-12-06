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

## 📝 Penambahan Docstring (Google Style)

Docstring ditambahkan pada semua class dan method utama menggunakan format **Google Style** untuk meningkatkan dokumentasi dan keterbacaan kode.

### Format Google Style Docstring:
```python
def function_name(param1: Type, param2: Type) -> ReturnType:
    """Deskripsi singkat fungsi.

    Deskripsi lebih detail jika diperlukan.

    Args:
        param1: Penjelasan parameter pertama.
        param2: Penjelasan parameter kedua.

    Returns:
        Penjelasan nilai yang dikembalikan.

    Raises:
        ExceptionType: Penjelasan kapan exception dilempar.

    Example:
        >>> contoh_penggunaan()
    """
```

### Contoh Implementasi pada Kode:

| Class/Method | Docstring yang Ditambahkan |
| :--- | :--- |
| `IValidationRule` | Deskripsi interface, kontrak yang harus dipenuhi, dan contoh penggunaan. |
| `IValidationRule.validate()` | Args (parameter `mhs`) dan Returns (boolean). |
| `RegistrationService` | Deskripsi layanan, Attributes (`rules`), dan Example penggunaan. |
| `RegistrationService.__init__()` | Args untuk dependency injection. |
| `RegistrationService.register_student()` | Deskripsi proses, Args, dan Returns. |

### Manfaat Docstring:
- ✅ **Dokumentasi Otomatis**: Tools seperti Sphinx dapat generate dokumentasi dari docstring.
- ✅ **IDE Support**: Tooltip dan autocomplete di IDE menampilkan informasi dari docstring.
- ✅ **Maintainability**: Developer baru lebih mudah memahami kode.
- ✅ **Testing**: Doctest dapat menjalankan contoh di docstring sebagai unit test.

---

## 📊 Penambahan Logging

Mengganti `print()` dengan modul `logging` untuk mencatat event sistem secara profesional.

### Konfigurasi Logging:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
```

### Penggunaan Level Logging:

| Level | Penggunaan | Contoh |
| :--- | :--- | :--- |
| `LOGGER.info()` | Event normal/sukses | `[OK] SKS 20 aman.` |
| `LOGGER.warning()` | Validasi gagal (bukan error sistem) | `[GAGAL] Siti mengambil 26 SKS (Maks: 24).` |
| `LOGGER.error()` | Error yang perlu ditangani | Exception handling |
| `LOGGER.debug()` | Informasi debugging | Detail proses internal |

### Perubahan pada Kode:

| Class | Sebelum | Sesudah |
| :--- | :--- | :--- |
| `SksLimitRule` | `print(f"[GAGAL]...")` | `LOGGER.warning(f"[GAGAL]...")` |
| `SksLimitRule` | `print(f"[OK]...")` | `LOGGER.info(f"[OK]...")` |
| `PrerequisiteRule` | `print(f"[GAGAL]...")` | `LOGGER.warning(f"[GAGAL]...")` |
| `PrerequisiteRule` | `print(f"[OK]...")` | `LOGGER.info(f"[OK]...")` |
| `JadwalBentrokRule` | `print(f"[GAGAL]...")` | `LOGGER.warning(f"[GAGAL]...")` |
| `JadwalBentrokRule` | `print(f"[OK]...")` | `LOGGER.info(f"[OK]...")` |
| `RegistrationService` | `print("Status: DITOLAK")` | `LOGGER.warning("Status: DITOLAK")` |
| `RegistrationService` | `print("Status: BERHASIL")` | `LOGGER.info("Status: BERHASIL")` |

### Manfaat Logging vs Print:
- ✅ **Level Control**: Bisa filter pesan berdasarkan level (DEBUG, INFO, WARNING, ERROR).
- ✅ **Timestamp**: Otomatis mencatat waktu event terjadi.
- ✅ **Output Fleksibel**: Bisa diarahkan ke file, console, atau external service.
- ✅ **Production Ready**: `print()` tidak cocok untuk production, logging adalah standar industri.
- ✅ **Performance**: Logging bisa dimatikan tanpa menghapus kode.