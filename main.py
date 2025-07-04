from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
import json
import os
from models.favorit import Favorit, Fisikawan, Game, Film

app = Flask(__name__)

DATA_FILE = 'data/favorit.json'
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    favorit_data = load_data()
    return render_template('index.html', favorit=favorit_data)

@app.route('/cari')
def cari():
    q = request.args.get('q', '').lower()
    favorit_data = load_data()
    hasil = [f for f in favorit_data if q in f['nama'].lower()]
    return render_template('detail.html', favorit=hasil, judul=f"Hasil Pencarian: {q}")

@app.route('/kategori/<nama_kategori>')
def tampilkan_kategori(nama_kategori):
    favorit_data = load_data()
    hasil = [f for f in favorit_data if f['kategori'].lower() == nama_kategori.lower()]
    return render_template('detail.html', favorit=hasil, judul=f"Kategori: {nama_kategori}")

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        nama = request.form['nama']
        kategori = request.form['kategori']
        deskripsi = request.form['deskripsi']
        file = request.files['gambar']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # polimorfisme untuk menentukan class yang sesuai
            if kategori.lower() == 'fisikawan':
                favorit_obj = Fisikawan(kategori, nama, deskripsi, filename)
            elif kategori.lower() == 'game':
                favorit_obj = Game(kategori, nama, deskripsi, filename)
            elif kategori.lower() == 'film':
                favorit_obj = Film(kategori, nama, deskripsi, filename)
            else:
                favorit_obj = Favorit(kategori, nama, deskripsi, filename)

            data = load_data()
            data.append(favorit_obj.to_dict())
            save_data(data)

            return "Data berhasil ditambahkan. <a href='/'>Kembali</a>"

        return "Gagal upload gambar atau data tidak lengkap."

    return render_template('tambah.html')

if __name__ == '__main__':
    app.run(debug=True)
