class Favorit:
    def __init__(self, kategori, nama, deskripsi, gambar):
        self.kategori = kategori
        self.nama = nama
        self.deskripsi = deskripsi
        self.gambar = gambar

    def to_dict(self):
        return {
            "kategori": self.kategori,
            "nama": self.nama,
            "deskripsi": self.deskripsi,
            "gambar": self.gambar
        }

    def get_info(self):
        return f"{self.nama} adalah favorit dalam kategori {self.kategori}."

class Fisikawan(Favorit):
    def get_info(self):
        return f"Fisikawan hebat: {self.nama} — {self.deskripsi}"

class Game(Favorit):
    def get_info(self):
        return f"Game favorit: {self.nama} - {self.deskripsi}"

class Film(Favorit):
    def get_info(self):
        return f"Film menarik: {self.nama} - {self.deskripsi}"
