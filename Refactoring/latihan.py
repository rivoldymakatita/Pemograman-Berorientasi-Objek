from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

# === 0. DATA MODEL ===
@dataclass
class Mahasiswa:
    nama: str
    sks_diambil: int
    mata_kuliah_lulus: List[str]
    jadwal_krs: List[str]  # Format: "Senin-08:00"

# === 1. ABSTRAKSI (Langkah 2: Implementasi DIP/OCP) ===
class IValidationRule(ABC):
    """
    Kontrak: Semua aturan validasi harus memiliki method validate
    yang menerima data mahasiswa dan mengembalikan boolean.
    """
    @abstractmethod
    def validate(self, mhs: Mahasiswa) -> bool:
        pass

# === 2. IMPLEMENTASI KONKRIT (Langkah 2) ===

class SksLimitRule(IValidationRule):
    """Aturan 1: Mengecek batas maksimal SKS (Maks 24 SKS)"""
    def validate(self, mhs: Mahasiswa) -> bool:
        MAX_SKS = 24
        if mhs.sks_diambil > MAX_SKS:
            print(f"[GAGAL] {mhs.nama} mengambil {mhs.sks_diambil} SKS (Maks: {MAX_SKS}).")
            return False
        print(f"[OK] SKS {mhs.sks_diambil} aman.")
        return True

class PrerequisiteRule(IValidationRule):
    """Aturan 2: Mengecek apakah prasyarat 'Dasar Pemrograman' sudah lulus"""
    def validate(self, mhs: Mahasiswa) -> bool:
        PRASYARAT = "Dasar Pemrograman"
        if PRASYARAT not in mhs.mata_kuliah_lulus:
            print(f"[GAGAL] {mhs.nama} belum lulus {PRASYARAT}.")
            return False
        print(f"[OK] Prasyarat {PRASYARAT} terpenuhi.")
        return True

# === 3. KELAS KOORDINATOR (Langkah 3: Implementasi SRP & DI) ===

class RegistrationService:
    """
    Service ini hanya bertugas mengkoordinasi validasi.
    Ia tidak tahu aturan apa saja yang dijalankan, ia hanya tahu
    daftar aturan yang diberikan (Dependency Injection).
    """
    def __init__(self, rules: List[IValidationRule]):
        # Dependency Injection: Menerima daftar aturan via constructor
        self.rules = rules

    def register_student(self, mhs: Mahasiswa):
        print(f"\n--- Memulai Validasi Registrasi untuk: {mhs.nama} ---")
        
        # Loop semua aturan yang disuntikkan
        for rule in self.rules:
            is_valid = rule.validate(mhs)
            if not is_valid:
                print("Status: REGISTRASI DITOLAK.")
                return False
        
        print("Status: REGISTRASI BERHASIL DISETUJUI.")
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
            print(f"[GAGAL] Terdeteksi jadwal bentrok pada KRS {mhs.nama}.")
            return False
        print(f"[OK] Tidak ada jadwal bentrok.")
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