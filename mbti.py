import tkinter as tk
from tkinter import ttk, messagebox
from pyswip import Prolog

# Inisialisasi Prolog
prolog = Prolog()
prolog.consult("mbti.pl")

sifat_list = []
jawaban_positif = []
index_sifat = -1
current_sifat = ""
import random

# Fungsi untuk memulai tes MBTI
def mulai_diagnosa():
    global sifat_list, index_sifat

    # Reset state
    prolog.retractall("sifat_pos(_)") 
    prolog.retractall("sifat_neg(_)")

    start_btn.configure(state=tk.DISABLED)
    yes_btn.configure(state=tk.NORMAL)
    no_btn.configure(state=tk.NORMAL)

    # Ambil semua sifat dan acak
    sifat_set = list(prolog.query("pertanyaan(X, _)"))
    sifat_list = [g["X"] for g in sifat_set]
    random.shuffle(sifat_list)

    index_sifat = -1
    pertanyaan_selanjutnya()

# Tampilkan pertanyaan selanjutnya
def pertanyaan_selanjutnya():
    global index_sifat, current_sifat

    index_sifat += 1

    if index_sifat >= len(sifat_list):
        hasil_diagnosa()
        return

    current_sifat = sifat_list[index_sifat]

    if list(prolog.query(f"sifat_pos({current_sifat})")) or \
       list(prolog.query(f"sifat_neg({current_sifat})")):
        pertanyaan_selanjutnya()
        return

    pertanyaan = list(prolog.query(f"pertanyaan({current_sifat}, Y)"))[0]["Y"].decode()
    tampilkan_pertanyaan(pertanyaan)

# Tampilkan pertanyaan ke kotak teks
def tampilkan_pertanyaan(pertanyaan):
    kotak_pertanyaan.configure(state=tk.NORMAL)
    kotak_pertanyaan.delete(1.0, tk.END)
    kotak_pertanyaan.insert(tk.END, pertanyaan)
    kotak_pertanyaan.configure(state=tk.DISABLED)

# Simpan jawaban pengguna
def jawaban(jwb):
    if jwb:
        prolog.assertz(f"sifat_pos({current_sifat})")
    else:
        prolog.assertz(f"sifat_neg({current_sifat})")
    pertanyaan_selanjutnya()

# Logika menghitung hasil MBTI
def hasil_diagnosa():
    dimensi = {
        "I": 0, "E": 0,
        "N": 0, "S": 0,
        "T": 0, "F": 0,
        "P": 0, "J": 0
    }

    # mapping prefix ke dimensi MBTI
    mapping = {
        "introvert": "I", "ekstrovert": "E",
        "intuitif": "N", "sensing": "S",
        "thinking": "T", "feeling": "F",
        "perceiving": "P", "judging": "J"
    }

    # Ambil semua jawaban positif
    jawaban_ya = list(prolog.query("sifat_pos(X)"))

    for j in jawaban_ya:
        nama = j["X"].decode() if isinstance(j["X"], bytes) else j["X"]

        # Ambil prefix sebelum "_"
        prefix = nama.split("_")[0]
        if prefix in mapping:
            dimensi[mapping[prefix]] += 1

    # Hitung MBTI berdasarkan skor
    hasil = ""
    hasil += "I" if dimensi["I"] >= dimensi["E"] else "E"
    hasil += "N" if dimensi["N"] >= dimensi["S"] else "S"
    hasil += "T" if dimensi["T"] >= dimensi["F"] else "F"
    hasil += "P" if dimensi["P"] >= dimensi["J"] else "J"

    messagebox.showinfo("Hasil MBTI Anda", f"Tipe Kepribadian Anda: {hasil}")
    yes_btn.configure(state=tk.DISABLED)
    no_btn.configure(state=tk.DISABLED)
    start_btn.configure(state=tk.NORMAL)


# Setup utama GUI
root = tk.Tk()
root.title("Tes Kepribadian MBTI")
root.geometry("500x380")
root.configure(bg="#f2f2f2")  # latar belakang lembut
root.resizable(False, False)

# Style modern
style = ttk.Style()
style.theme_use("clam")  # tampilan modern
style.configure("TFrame", background="#f2f2f2")
style.configure("TLabel", background="#f2f2f2", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
style.map("TButton",
          background=[('active', '#d9d9d9')],
          foreground=[('disabled', 'gray')])

# Main frame
mainframe = ttk.Frame(root, padding="20 15 20 15", style="TFrame")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

# Judul
judul = ttk.Label(mainframe, text="Tes Kepribadian MBTI", font=("Segoe UI", 18, "bold"), anchor="center")
judul.grid(column=0, row=0, columnspan=3, pady=(0, 10))

# Label pertanyaan
label_pertanyaan = ttk.Label(mainframe, text="Pertanyaan:")
label_pertanyaan.grid(column=0, row=1, columnspan=3, sticky=tk.W)

# Kotak pertanyaan
kotak_pertanyaan = tk.Text(mainframe, height=4, width=50, wrap=tk.WORD, state=tk.DISABLED,
                           font=("Segoe UI", 10), bg="#ffffff", relief=tk.SOLID, bd=1)
kotak_pertanyaan.grid(column=0, row=2, columnspan=3, pady=10)

# Tombol Ya
yes_btn = ttk.Button(mainframe, text="✅ Ya", command=lambda: jawaban(True), state=tk.DISABLED)
yes_btn.grid(column=1, row=3, padx=10, pady=10, sticky=tk.E)

# Tombol Tidak
no_btn = ttk.Button(mainframe, text="❌ Tidak", command=lambda: jawaban(False), state=tk.DISABLED)
no_btn.grid(column=2, row=3, padx=10, pady=10, sticky=tk.W)

# Tombol Mulai
start_btn = ttk.Button(mainframe, text="▶ Mulai Tes MBTI", command=mulai_diagnosa)
start_btn.grid(column=0, row=4, columnspan=3, pady=15)

# Spasi dan padding antar widget
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()