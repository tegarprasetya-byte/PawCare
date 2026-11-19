import os
import tempfile
import unittest

from hewan.layanan import (Katalog, binary_search_id, insertion_sort,
                           hitung_status)


class TestKatalog(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.file = os.path.join(self.folder.name, "tes.txt")
        self.katalog = Katalog(self.file)

    def tearDown(self):
        self.folder.cleanup()

    def data_valid(self, **tambahan):
        data = dict(nama="Milo", jenis="Kucing", usia=2, kelamin="Jantan",
                    kesehatan="Sehat", deskripsi="Aktif")
        data.update(tambahan)
        return data

    def test_dummy_terisi(self):
        self.assertEqual(len(self.katalog.data), 6)

    def test_tambah_id_unik(self):
        hewan = self.katalog.tambah(**self.data_valid())
        self.assertEqual(hewan.id, "A007")
        self.assertEqual(len(self.katalog.data), 7)

    def test_usia_tidak_valid(self):
        with self.assertRaises(ValueError):
            self.katalog.tambah(**self.data_valid(usia=99))
        with self.assertRaises(ValueError):
            self.katalog.tambah(**self.data_valid(usia="abc"))

    def test_nama_kosong(self):
        with self.assertRaises(ValueError):
            self.katalog.tambah(**self.data_valid(nama="   "))

    def test_ubah(self):
        self.katalog.ubah("A001", **self.data_valid(nama="Mochi Baru"))
        self.assertEqual(self.katalog.cari_id("A001").nama, "Mochi Baru")

    def test_hapus(self):
        self.katalog.hapus("A002")
        self.assertIsNone(self.katalog.cari_id("A002"))

    def test_binary_search(self):
        self.assertEqual(binary_search_id(self.katalog.data, "A003"), 2)
        self.assertEqual(binary_search_id(self.katalog.data, "A999"), -1)

    def test_insertion_sort_usia(self):
        hasil = insertion_sort(self.katalog.data, lambda h: h.usia)
        usia = [h.usia for h in hasil]
        self.assertEqual(usia, sorted(usia))

    def test_hitung_status_rekursif(self):
        self.assertEqual(hitung_status(self.katalog.data, "Tersedia"), 4)
        self.assertEqual(hitung_status(self.katalog.data, "Diproses"), 1)

    def test_simpan_dan_muat_file(self):
        self.katalog.tambah(**self.data_valid())
        katalog_baru = Katalog(self.file)
        self.assertEqual(len(katalog_baru.data), 7)

    def test_filter_dan_cari(self):
        hasil = self.katalog.daftar_tampil(kata="lu", jenis="Kucing")
        self.assertEqual([h.nama for h in hasil], ["Luna"])


if __name__ == "__main__":
    unittest.main()