# DASHBOARD ~BMKG~ 🛖 DATA EXPLORER

![Web capture_6-5-2022_195257_app-bmkg-exp herokuapp com](https://user-images.githubusercontent.com/1007910/167135166-ebb956ef-a80d-4cfe-a840-5d1d4156e7a5.jpeg)

Cara menjalankan Dashboard:

- Buat _virtual environment_ menggunakan `environment.yml` (untuk conda) atau `requirements.txt` (untuk venv).
- Lakukan [konfigurasi config.ini](#konfigurasi-configini).
- Jalankan `app.py` di terminal.
- Buka alamat `http://127.0.0.1:8050/` di browser.

## KONFIGURASI `config.ini`

Konfigurasi yang harus diisi adalah:

- Pada bagian `[PATH BMKG DATABASE]` seluruh _key_ harus diisi (secara default akan menggunakan dummy data):
    - `FOLDER_BMKG`: Lokasi direktori/folder dataset
    - `FILE_NAME_BMKG`: Nama file HDF5 (.h5) yang berisikan dataset BMKG. Strukturnya mengikuti [panduan disini](https://github.com/taruma/dataset/tree/main/bmkg#struktur-file).
    - `FILE_NAME_BMKG_COMPLETENESS`: Nama file HDF5 (.h5) yang berisikan informasi nilai kelengkapan dataset BMKG.
- Sisanya opsional. 

## Catatan

- Disini saya tidak akan menyediakan datasetnya, silakan cari sendiri atau melakukan kompilasi sendiri dari situs BMKG Online. Untuk sekarang sudah saya sediakan dummy data.
- Untuk dataset persen kelengkapan data (`_BMKG_COMPLETENESS`), itu hasil olahan dari dataset BMKG yang saya simpan dalam bentuk HDF5 juga. Jadi, sebenarnya informasi kelengkapan data bmkg itu hasil olahan dari dataset utama.
- Source code repo ini tidak jauh berbeda dengan situs https://app-bmkg-exp.herokuapp.com/. Repo ini dirancang untuk penggunaan lokal (aplikasi web lokal). 
- Silakan buat isu kalau ada pertanyaan/komentar/kritik/dll atau pull request kalo pengen utak-atik dan sharing modifikasinya. Didukung kalau mau _fork_ repo ini. hehe. :)
