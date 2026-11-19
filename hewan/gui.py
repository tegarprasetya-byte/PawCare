"""Tampilan GUI dengan tkinter."""
import tkinter as tk
from tkinter import ttk, messagebox

from .layanan import Katalog, KUNCI_URUT, hitung_status
from .model import JENIS_HEWAN, KELAMIN_HEWAN, STATUS_HEWAN


class FormHewan(tk.Toplevel):
    """Jendela form untuk tambah / ubah data hewan."""

    def __init__(self, induk, judul, hewan=None, saat_simpan=None):
        super().__init__(induk)
        self.title(judul)
        self.resizable(False, False)
        self.transient(induk)
        self.grab_set()
        self.saat_simpan = saat_simpan

        self.var = {
            "nama": tk.StringVar(),
            "jenis": tk.StringVar(value=JENIS_HEWAN[0]),
            "usia": tk.StringVar(),
            "kelamin": tk.StringVar(value=KELAMIN_HEWAN[0]),
            "kesehatan": tk.StringVar(),
            "deskripsi": tk.StringVar(),
            "status": tk.StringVar(value=STATUS_HEWAN[0]),
        }
        if hewan is not None:  # mode ubah: isi form dengan data lama
            for kunci, variabel in self.var.items():
                variabel.set(getattr(hewan, kunci))

        baris_form = [
            ("Nama", "nama", None),
            ("Jenis", "jenis", JENIS_HEWAN),
            ("Usia (tahun)", "usia", None),
            ("Jenis kelamin", "kelamin", KELAMIN_HEWAN),
            ("Kondisi kesehatan", "kesehatan", None),
            ("Deskripsi", "deskripsi", None),
            ("Status", "status", STATUS_HEWAN),
        ]
        for i, (label, kunci, pilihan) in enumerate(baris_form):
            ttk.Label(self, text=label).grid(
                row=i, column=0, sticky="w", padx=10, pady=4)
            if pilihan:
                widget = ttk.Combobox(self, textvariable=self.var[kunci],
                                      values=pilihan, state="readonly",
                                      width=28)
            else:
                widget = ttk.Entry(self, textvariable=self.var[kunci],
                                   width=31)
            widget.grid(row=i, column=1, padx=10, pady=4)

        frame = ttk.Frame(self)
        frame.grid(row=len(baris_form), column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Simpan", command=self.simpan).pack(
            side="left", padx=5)
        ttk.Button(frame, text="Batal", command=self.destroy).pack(
            side="left", padx=5)

    def simpan(self):
        data = {kunci: variabel.get() for kunci, variabel in self.var.items()}
        try:
            self.saat_simpan(**data)  # kirim sebagai keyword argument
        except ValueError as error:
            messagebox.showerror("Input tidak valid", str(error), parent=self)
            return
        self.destroy()


class AplikasiPawCare(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PawCare - Pengelolaan Hewan Terlantar")
        self.geometry("920x520")
        self.katalog = Katalog()

        self.buat_filter()
        self.buat_tabel()
        self.buat_tombol()
        self.muat_tabel()

    # ---------- Bagian tampilan ----------
    def buat_combobox(self, induk, label, variabel, nilai, lebar):
        ttk.Label(induk, text=label).pack(side="left", padx=(8, 2))
        kotak = ttk.Combobox(induk, textvariable=variabel, values=nilai,
                             state="readonly", width=lebar)
        kotak.pack(side="left")
        kotak.bind("<<ComboboxSelected>>", lambda e: self.muat_tabel())

    def buat_filter(self):
        self.var_cari = tk.StringVar()
        self.var_jenis = tk.StringVar(value="Semua")
        self.var_status = tk.StringVar(value="Semua")
        self.var_urut = tk.StringVar(value="ID")
        self.var_menurun = tk.BooleanVar(value=False)

        frame = ttk.Frame(self, padding=8)
        frame.pack(fill="x")
        ttk.Label(frame, text="Cari nama:").pack(side="left")
        ttk.Entry(frame, textvariable=self.var_cari, width=16).pack(
            side="left", padx=4)
        self.var_cari.trace_add("write", lambda *args: self.muat_tabel())

        self.buat_combobox(frame, "Jenis:", self.var_jenis,
                           ("Semua",) + JENIS_HEWAN, 9)
        self.buat_combobox(frame, "Status:", self.var_status,
                           ("Semua",) + STATUS_HEWAN, 10)
        self.buat_combobox(frame, "Urutkan:", self.var_urut,
                           tuple(KUNCI_URUT), 7)
        ttk.Checkbutton(frame, text="Menurun", variable=self.var_menurun,
                        command=self.muat_tabel).pack(side="left", padx=8)
        ttk.Button(frame, text="Reset", command=self.reset_filter).pack(
            side="left")

    def buat_tabel(self):
        kolom = ("id", "nama", "jenis", "usia", "kelamin", "kesehatan",
                 "status")
        judul = ("ID", "Nama", "Jenis", "Usia", "Kelamin", "Kesehatan",
                 "Status")
        lebar = (60, 110, 90, 60, 80, 220, 90)

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=8)
        self.tabel = ttk.Treeview(frame, columns=kolom, show="headings",
                                  selectmode="browse")
        for k, j, l in zip(kolom, judul, lebar):
            self.tabel.heading(k, text=j)
            self.tabel.column(k, width=l, anchor="w")
        scroll = ttk.Scrollbar(frame, orient="vertical",
                               command=self.tabel.yview)
        self.tabel.configure(yscrollcommand=scroll.set)
        self.tabel.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.tabel.bind("<Double-1>", lambda e: self.lihat_detail())

    def buat_tombol(self):
        frame = ttk.Frame(self, padding=8)
        frame.pack(fill="x")
        ttk.Button(frame, text="Tambah", command=self.tambah_hewan).pack(
            side="left", padx=3)
        ttk.Button(frame, text="Ubah", command=self.ubah_hewan).pack(
            side="left", padx=3)
        ttk.Button(frame, text="Hapus", command=self.hapus_hewan).pack(
            side="left", padx=3)
        ttk.Button(frame, text="Detail", command=self.lihat_detail).pack(
            side="left", padx=3)
        self.label_info = ttk.Label(frame, text="")
        self.label_info.pack(side="right")

    # ---------- Bagian logika tampilan ----------
    def muat_tabel(self):
        hasil = self.katalog.daftar_tampil(
            kata=self.var_cari.get().strip(),
            jenis=self.var_jenis.get(),
            status=self.var_status.get(),
            urut=self.var_urut.get(),
            menurun=self.var_menurun.get(),
        )
        for item in self.tabel.get_children():
            self.tabel.delete(item)
        for h in hasil:
            self.tabel.insert("", "end", iid=h.id, values=(
                h.id, h.nama, h.jenis, f"{h.usia} th", h.kelamin,
                h.kesehatan, h.status))

        total = len(self.katalog.data)
        tersedia = hitung_status(self.katalog.data, "Tersedia")
        self.label_info.config(
            text=f"Menampilkan {len(hasil)} dari {total} hewan | "
                 f"Tersedia: {tersedia}")

    def reset_filter(self):
        self.var_jenis.set("Semua")
        self.var_status.set("Semua")
        self.var_urut.set("ID")
        self.var_menurun.set(False)
        self.var_cari.set("")  # otomatis memanggil muat_tabel()
        self.muat_tabel()

    def hewan_terpilih(self):
        pilihan = self.tabel.selection()
        if not pilihan:
            messagebox.showwarning("Pilih data",
                                   "Pilih dulu satu hewan di tabel.")
            return None
        return self.katalog.cari_id(pilihan[0])

    def tambah_hewan(self):
        FormHewan(self, "Tambah Hewan", saat_simpan=self.simpan_baru)

    def simpan_baru(self, **data):
        self.katalog.tambah(**data)
        self.muat_tabel()

    def ubah_hewan(self):
        hewan = self.hewan_terpilih()
        if hewan is None:
            return
        FormHewan(self, "Ubah Hewan", hewan=hewan,
                  saat_simpan=lambda **data: self.simpan_ubah(hewan.id, **data))

    def simpan_ubah(self, id_hewan, **data):
        self.katalog.ubah(id_hewan, **data)
        self.muat_tabel()

    def hapus_hewan(self):
        hewan = self.hewan_terpilih()
        if hewan is None:
            return
        if messagebox.askyesno("Konfirmasi",
                               f"Yakin hapus {hewan.nama} ({hewan.id})?"):
            self.katalog.hapus(hewan.id)
            self.muat_tabel()

    def lihat_detail(self):
        hewan = self.hewan_terpilih()
        if hewan is None:
            return
        teks = (f"ID            : {hewan.id}\n"
                f"Nama          : {hewan.nama}\n"
                f"Jenis         : {hewan.jenis}\n"
                f"Usia          : {hewan.usia} tahun\n"
                f"Jenis kelamin : {hewan.kelamin}\n"
                f"Kesehatan     : {hewan.kesehatan}\n"
                f"Deskripsi     : {hewan.deskripsi}\n"
                f"Status        : {hewan.status}")
        messagebox.showinfo(f"Detail {hewan.nama}", teks)