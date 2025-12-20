import unittest
from diskon_service import DiskonCalculator

class TestDiskonLanjut(unittest.TestCase):
    
    def setUp(self):
        """Arrange: Siapkan instance Calculator."""
        self.calc = DiskonCalculator()

    def test_diskon_float_33_persen(self):
        """Tes 5: Uji nilai float (diskon 33% pada 999)."""
        # Act: 999 - (33% * 999) = 999 - 329.67 = 669.33
        hasil = self.calc.hitung_diskon(999, 33)
        
        # Assert: Gunakan assertAlmostEqual untuk menangani presisi float
        self.assertAlmostEqual(hasil, 669.33, places=2)

    def test_harga_awal_nol(self):
        """Tes 6: Uji Edge Case (harga awal 0)."""
        # Act
        hasil = self.calc.hitung_diskon(0, 10)
        
        # Assert: Harga 0 dengan diskon apapun tetap 0
        self.assertEqual(hasil, 0.0)

if __name__ == '__main__':
    unittest.main()