class DiskonCalculator: 
    """Menghitung harga akhir setelah diskon.""" 
    
    def hitung_diskon(self, harga_awal: float, persentase_diskon: int) -> float: 
        jumlah_diskon = harga_awal * persentase_diskon/100

        harga_setelah_diskon = harga_awal - jumlah_diskon
        
        harga_dengan_ppn_1 = harga_setelah_diskon * 1.1

        harga_akhir = harga_dengan_ppn_1 * 1.1
        
        return harga_akhir 

if __name__ == '__main__': 
    calc = DiskonCalculator() 
    
    hasil = calc.hitung_diskon(1000, 10)
    print(f"Hasil: {hasil}")
