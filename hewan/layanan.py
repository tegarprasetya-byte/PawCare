"""Logika utama: validasi, searching, sorting, rekursi, dan class Katalog."""
from .model import (Hewan, JENIS_HEWAN, KELAMIN_HEWAN, STATUS_HEWAN,
                    USIA_MIN, USIA_MAX, PEMISAH)
from .penyimpanan import NAMA_FILE, muat_semua, simpan_semua


def nomor_id(id_hewan):
    """'A003' -> 3"""
    return int(id_hewan[1:])


# Lambda sebagai kunci pengurutan
KUNCI_URUT = {
    "ID": lambda h: nomor_id(h.id),
    "Nama": lambda h: h.nama.lower(),
    "Usia": lambda h: h.usia,
}


def buat_data_dummy():
    return [
        Hewan("A001", "Mochi", "Kucing", 2, "Betina", "Sehat",
              "Kucing manis, jinak, suka bermain bola", "Tersedia"),
        Hewan("A002", "Bruno", "Anjing", 3, "Jantan", "Sehat",
              "Anjing aktif, sudah terlatih duduk dan salam", "Tersedia"),
        Hewan("A003", "Luna", "Kucing", 1, "Betina", "Butuh vaksin",
              "Anak kucing pemalu, cocok untuk rumah tenang", "Tersedia"),
        Hewan("A004", "Snowy", "Kelinci", 1, "Jantan", "Sehat",
              "Kelinci putih, suka makan wortel", "Diproses"),
        Hewan("A005", "Rocky", "Anjing", 5, "Jantan", "Luka ringan di kaki",
              "Anjing setia, butuh perawatan luka ringan", "Tersedia"),
        Hewan("A006", "Oyen", "Kucing", 4, "Jantan", "Sehat",
              "Kucing oranye yang ramah", "Teradopsi"),
    ]


# ================= VALIDASI =================
def bersihkan_teks(teks):
    return str(teks).strip().replace(PEMISAH, "/")


def validasi(nama, jenis, usia, kelamin, kesehatan, deskripsi,
             status="Tersedia"):
    """Periksa input. Jika salah -> raise ValueError. Jika benar -> dict bersih."""
    nama = bersihkan_teks(nama)
    kesehatan = bersihkan_teks(kesehatan)
    deskripsi = bersihkan_teks(deskripsi)

    if not nama:
        raise ValueError("Nama tidak boleh kosong.")
    if not kesehatan:
        raise ValueError("Kondisi kesehatan tidak boleh kosong.")
    if not deskripsi:
        raise ValueError("Deskripsi tidak boleh kosong.")
    if jenis not in JENIS_HEWAN:
        raise ValueError("Jenis hewan tidak valid.")
    if kelamin not in KELAMIN_HEWAN:
        raise ValueError("Jenis kelamin tidak valid.")
    if status not in STATUS_HEWAN:
        raise ValueError("Status tidak valid.")
    try:
        usia = int(usia)
    except (TypeError, ValueError):
        raise ValueError("Usia harus berupa angka.")
    if not USIA_MIN <= usia <= USIA_MAX:
        raise ValueError(f"Usia harus antara {USIA_MIN} - {USIA_MAX} tahun.")

    return {"nama": nama, "jenis": jenis, "usia": usia, "kelamin": kelamin,
            "kesehatan": kesehatan, "deskripsi": deskripsi, "status": status}


# ================= SEARCHING =================
def linear_search_nama(daftar, kata):
    """Linear Search: cek satu per satu, kumpulkan yang namanya cocok."""
    hasil = []
    for hewan in daftar:
        if kata.lower() in hewan.nama.lower():
            hasil.append(hewan)
    return hasil


def binary_search_id(daftar, id_cari):
    """Binary Search berdasarkan ID. Data harus terurut menurut ID."""
    target = nomor_id(id_cari)
    awal, akhir = 0, len(daftar) - 1
    while awal <= akhir:
        tengah = (awal + akhir) // 2
        nilai = nomor_id(daftar[tengah].id)
        if nilai == target:
            return tengah
        elif nilai < target:
            awal = tengah + 1
        else:
            akhir = tengah - 1
    return -1


# ================= SORTING =================
def insertion_sort(daftar, kunci, menurun=False):
    """Insertion Sort. Mengembalikan list baru, list asli tidak berubah."""
    hasil = list(daftar)
    for i in range(1, len(hasil)):
        sisip = hasil[i]
        j = i - 1
        while j >= 0 and kunci(hasil[j]) > kunci(sisip):
            hasil[j + 1] = hasil[j]
            j -= 1
        hasil[j + 1] = sisip
    if menurun:
        hasil.reverse()
    return hasil


# ================= REKURSI =================
def hitung_status(daftar, status, indeks=0):
    """Hitung jumlah hewan dengan status tertentu secara rekursif."""
    if indeks >= len(daftar):  # base case
        return 0
    cocok = 1 if daftar[indeks].status == status else 0
    return cocok + hitung_status(daftar, status, indeks + 1)  # recursive case


# ================= KATALOG =================
class Katalog:
    def __init__(self, nama_file=NAMA_FILE):
        self.nama_file = nama_file
        data = muat_semua(nama_file)
        if data is None:  # file belum ada -> pakai dummy data
            data = buat_data_dummy()
            simpan_semua(data, nama_file)
        self.data = data  # selalu terurut menurut ID

    def simpan(self):
        simpan_semua(self.data, self.nama_file)

    def id_baru(self):
        terbesar = 0
        for hewan in self.data:
            terbesar = max(terbesar, nomor_id(hewan.id))
        return f"A{terbesar + 1:03d}"

    def cari_id(self, id_hewan):
        indeks = binary_search_id(self.data, id_hewan)
        return self.data[indeks] if indeks != -1 else None

    def tambah(self, **data):
        bersih = validasi(**data)
        hewan = Hewan(self.id_baru(), **bersih)
        self.data.append(hewan)
        self.simpan()
        return hewan

    def ubah(self, id_hewan, **data):
        hewan = self.cari_id(id_hewan)
        if hewan is None:
            raise ValueError("Hewan tidak ditemukan.")
        bersih = validasi(**data)
        for atribut, nilai in bersih.items():
            setattr(hewan, atribut, nilai)
        self.simpan()

    def hapus(self, id_hewan):
        hewan = self.cari_id(id_hewan)
        if hewan is None:
            raise ValueError("Hewan tidak ditemukan.")
        self.data.remove(hewan)
        self.simpan()

    def daftar_tampil(self, kata="", jenis="Semua", status="Semua",
                      urut="ID", menurun=False):
        hasil = self.data
        if kata:
            hasil = linear_search_nama(hasil, kata)
        if jenis != "Semua":
            hasil = [h for h in hasil if h.jenis == jenis]
        if status != "Semua":
            hasil = [h for h in hasil if h.status == status]
        return insertion_sort(hasil, KUNCI_URUT[urut], menurun)