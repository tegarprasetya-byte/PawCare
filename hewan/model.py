"""Model data dan konstanta PawHaven."""

JENIS_HEWAN = ("Kucing", "Anjing", "Kelinci", "Lainnya")
KELAMIN_HEWAN = ("Jantan", "Betina")
STATUS_HEWAN = ("Tersedia", "Diproses", "Teradopsi")
USIA_MIN = 0
USIA_MAX = 30
PEMISAH = "|"  # pemisah kolom di file teks


class Hewan:
    def __init__(self, id_hewan, nama, jenis, usia, kelamin,
                 kesehatan, deskripsi, status="Tersedia"):
        self.id = id_hewan
        self.nama = nama
        self.jenis = jenis
        self.usia = int(usia)
        self.kelamin = kelamin
        self.kesehatan = kesehatan
        self.deskripsi = deskripsi
        self.status = status

    def ke_baris(self):
        """Ubah objek menjadi satu baris teks untuk disimpan ke file."""
        kolom = [self.id, self.nama, self.jenis, self.usia, self.kelamin,
                 self.kesehatan, self.deskripsi, self.status]
        return PEMISAH.join(str(k) for k in kolom)

    @staticmethod
    def dari_baris(baris):
        """Ubah satu baris teks dari file menjadi objek Hewan."""
        kolom = baris.strip().split(PEMISAH)
        if len(kolom) != 8:
            raise ValueError("Format baris tidak valid")
        return Hewan(*kolom)