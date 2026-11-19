"""File handling: simpan dan muat data hewan dari file teks."""
import os

from .model import Hewan

# File data disimpan di folder utama project
NAMA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data_hewan.txt",
)


def simpan_semua(daftar, nama_file=NAMA_FILE):
    """Tulis seluruh data ke file (mode 'w' = timpa isi lama)."""
    with open(nama_file, "w", encoding="utf-8") as file:
        for hewan in daftar:
            file.write(hewan.ke_baris() + "\n")


def muat_semua(nama_file=NAMA_FILE):
    """Baca data dari file (mode 'r'). Return None jika file belum ada."""
    daftar = []
    try:
        with open(nama_file, "r", encoding="utf-8") as file:
            for baris in file:
                if not baris.strip():
                    continue
                try:
                    daftar.append(Hewan.dari_baris(baris))
                except ValueError:
                    print("[PERINGATAN] Baris dilewati:", baris.strip())
    except FileNotFoundError:
        return None
    return daftar