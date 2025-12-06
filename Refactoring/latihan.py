from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
import logging

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)

# === 0. DATA MODEL ===
@dataclass
class Mahasiswa:
    nama: str
    sks_diambil: int
    mata_kuliah_lulus: List[str]
    jadwal_krs: List[str]  # Format: "Senin-08:00"

# === 1. ABSTRAKSI (Langkah 2: Implementasi DIP/OCP) ===
class IValidationRule(ABC):
    """Interface untuk aturan validasi registrasi mahasiswa.

    Kontrak: Semua aturan validasi harus mengimplementasikan method validate
    yang menerima data mahasiswa dan mengembalikan boolean.

    Example:
        >>> class CustomRule(IValidationRule):
        ...     def validate(self, mhs: Mahasiswa) -> bool:
        ...         return True
    """

    @abstractmethod
    def validate(self, mhs: Mahasiswa) -> bool:
        """Memvalidasi data mahasiswa berdasarkan aturan tertentu.

        Args:
            mhs: Objek Mahasiswa yang akan divalidasi.

        Returns:
            True jika validasi berhasil/lolos, False jika gagal.
        """
        pass

# === 2. IMPLEMENTASI KONKRIT (Langkah 2) ===

class SksLimitRule(IValidationRule):
    """Aturan 1: Mengecek batas maksimal SKS (Maks 24 SKS)"""
    def validate(self, mhs: Mahasiswa) -> bool:
        MAX_SKS = 24
        if mhs.sks_diambil > MAX_SKS:
            LOGGER.warning(f"[GAGAL] {mhs.nama} mengambil {mhs.sks_diambil} SKS (Maks: {MAX_SKS}).")
            return False
        LOGGER.info(f"[OK] SKS {mhs.sks_diambil} aman.")
        return True

class PrerequisiteRule(IValidationRule):
    """Aturan 2: Mengecek apakah prasyarat 'Dasar Pemrograman' sudah lulus"""
    def validate(self, mhs: Mahasiswa) -> bool:
        PRASYARAT = "Dasar Pemrograman"
        if PRASYARAT not in mhs.mata_kuliah_lulus:
            LOGGER.warning(f"[GAGAL] {mhs.nama} belum lulus {PRASYARAT}.")
            return False
        LOGGER.info(f"[OK] Prasyarat {PRASYARAT} terpenuhi.")
        return True

# === 3. KELAS KOORDINATOR (Langkah 3: Implementasi SRP & DI) ===

class RegistrationService:
    """Layanan koordinasi validasi registrasi mahasiswa.

    Service ini bertanggung jawab mengkoordinasi proses validasi
    menggunakan aturan-aturan yang disuntikkan (Dependency Injection).
    Mengikuti prinsip SRP dengan hanya fokus pada koordinasi validasi.

    Attributes:
        rules: Daftar aturan validasi yang akan dijalankan.

    Example:
        >>> rules = [SksLimitRule(), PrerequisiteRule()]
        >>> service = RegistrationService(rules=rules)
        >>> service.register_student(mahasiswa)
    """

    def __init__(self, rules: List[IValidationRule]):
        """Inisialisasi RegistrationService dengan daftar aturan validasi.

        Args:
            rules: Daftar implementasi IValidationRule yang akan digunakan
                untuk memvalidasi registrasi mahasiswa.
        """
        self.rules = rules

    def register_student(self, mhs: Mahasiswa) -> bool:
        """Menjalankan proses registrasi mahasiswa.

        Memvalidasi data mahasiswa menggunakan semua aturan yang telah
        dikonfigurasi. Proses berhenti pada aturan pertama yang gagal.

        Args:
            mhs: Objek Mahasiswa yang akan diregistrasi.

        Returns:
            True jika semua validasi berhasil dan registrasi disetujui,
            False jika ada validasi yang gagal.
        """
        LOGGER.info(f"Memulai Validasi Registrasi untuk: {mhs.nama}")
        
        # Loop semua aturan yang disuntikkan
        for rule in self.rules:
            is_valid = rule.validate(mhs)
            if not is_valid:
                LOGGER.warning("Status: REGISTRASI DITOLAK.")
                return False
        
        LOGGER.info("Status: REGISTRASI BERHASIL DISETUJUI.")
        return True

# === 4. CHALLENGE: PEMBUKTIAN OCP (Langkah 4) ===
# Kita membuat aturan baru TANPA mengubah RegistrationService

class JadwalBentrokRule(IValidationRule):
    """
    Aturan Tambahan: Mengecek jadwal bentrok.
    (Simulasi sederhana: Cek duplikasi string di list jadwal)
    """
    def validate(self, mhs: Mahasiswa) -> bool:
        if len(mhs.jadwal_krs) != len(set(mhs.jadwal_krs)):
            LOGGER.warning(f"[GAGAL] Terdeteksi jadwal bentrok pada KRS {mhs.nama}.")
            return False
        LOGGER.info(f"[OK] Tidak ada jadwal bentrok.")
        return True


# === PROGRAM UTAMA (Main Execution) ===

if __name__ == "__main__":
    # A. Setup Data Mahasiswa
    # Kasus 1: Mahasiswa Pintar (Lulus semua syarat)
    mhs_bagus = Mahasiswa(
        nama="Budi", 
        sks_diambil=20, 
        mata_kuliah_lulus=["Dasar Pemrograman", "Logika"],
        jadwal_krs=["Senin-08:00", "Selasa-10:00"]
    )

    # Kasus 2: Mahasiswa Bermasalah (SKS Over & Jadwal Bentrok)
    mhs_kacau = Mahasiswa(
        nama="Siti", 
        sks_diambil=26, 
        mata_kuliah_lulus=["Logika"], # Belum lulus Daspro
        jadwal_krs=["Senin-08:00", "Senin-08:00"] # Bentrok
    )

    # B. Konfigurasi Dependency Injection
    # Kita bisa memilih aturan mana yang mau dipakai secara fleksibel
    
    # Skenario Awal: Hanya Cek SKS dan Prasyarat
    print("=== SKENARIO 1: Validasi Standar (SKS & Prasyarat) ===")
    basic_rules = [SksLimitRule(), PrerequisiteRule()]
    service_standard = RegistrationService(rules=basic_rules)
    
    service_standard.register_student(mhs_bagus)
    
    # Skenario Challenge: Menambah Cek Jadwal Bentrok
    # Perhatikan: Kita TIDAK mengubah kode RegistrationService, hanya list rules-nya.
    print("\n=== SKENARIO 2 (Challenge): Menambah Aturan Jadwal Bentrok ===")
    
    complete_rules = [
        SksLimitRule(), 
        PrerequisiteRule(), 
        JadwalBentrokRule() # Inject aturan baru di sini
    ]
    service_complete = RegistrationService(rules=complete_rules)
    
    service_complete.register_student(mhs_bagus) # Budi lulus semua
    service_complete.register_student(mhs_kacau) # Siti akan gagal di validasi pertama