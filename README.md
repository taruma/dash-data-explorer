# DASHBOARD BMKG DATA EXPLORER

![Web capture_5-5-2022_143748_127 0 0 1](https://user-images.githubusercontent.com/1007910/166880494-376eadf7-6892-4a64-874f-0b85bf9d1d25.jpeg)

Cara menjalankan Dashboard:

- Buat _virtual environment_ menggunakan `environment.yml` (untuk conda) atau `requirements.txt` (untuk venv).
- Lakukan [konfigurasi config.ini](#konfigurasi-configini).
- Jalankan `app.py` di terminal.
- Buka alamat `http://127.0.0.1:8050/` di browser.

## KONFIGURASI `config.ini`

Konfigurasi yang harus diisi adalah:

- Pada bagian `[PATH BMKG DATABASE]` seluruh _key_ harus diisi:
    - `FOLDER_BMKG`: Lokasi direktori/folder dataset
    - `FILE_NAME_BMKG`: Nama file HDF5 (.h5) yang berisikan dataset BMKG. Strukturnya mengikuti [panduan disini](https://github.com/taruma/dataset/tree/main/bmkg#struktur-file).
    - `FILE_NAME_BMKG_COMPLETENESS`: Nama file HDF5 (.h5) yang berisikan informasi nilai kelengkapan dataset BMKG.
- Sisanya opsional. 

## Catatan

- Disini saya tidak akan menyediakan datasetnya, silakan cari sendiri atau melakukan kompilasi sendiri dari situs BMKG Online. Script untuk kompilasi data direncanakan saya publish juga, jadi bisa buat sendiri, baik untuk BMKG Online ataupun data sendiri.
- Untuk dataset persen kelengkapan data (`_BMKG_COMPLETENESS`), itu hasil olahan dari dataset BMKG yang saya simpan dalam bentuk HDF5 juga. Jadi, sebenarnya informasi kelengkapan data bmkg itu hasil olahan dari dataset utama. 
