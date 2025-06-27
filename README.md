# Faza Blog

Faza Blog adalah platform blog modern berbasis Django dengan fitur lengkap dan tampilan profesional, siap untuk di-deploy di Railway.

## Fitur Utama
- **Autentikasi**: Login/Logout dengan email-password (Django) dan Auth0 (OAuth).
- **Artikel**:
  - CRUD artikel (admin/penulis)
  - Daftar artikel dengan filter tag, search, dan pagination (6 per halaman)
  - Detail artikel dengan navigasi next/prev
  - Tag artikel (filter dan tampilan konsisten)
  - Artikel terkait otomatis berdasarkan tag
- **Komentar**: Komentar via Disqus pada detail artikel
- **Galeri**: Galeri gambar dari artikel, dengan pagination
- **Dashboard**: Admin dan penulis dashboard
- **Tentang & Portofolio**: Halaman profil, portofolio, dan proyek
- **UI/UX**:
  - Responsive, dark mode, dan konsisten
  - Navbar dengan dropdown user/admin
  - Footer dengan social media (Instagram, TikTok, GitHub)
  - Scroll to top button
- **Pencarian**: Search artikel berdasarkan judul/isi
- **Pagination**: Pada daftar artikel dan galeri
- **Admin Panel**: Kelola user, artikel, kategori, komentar

## Library & API yang Digunakan
- **Django** (5.x)
- **Django Auth** (built-in)
- **Auth0** (OAuth2, Social Login)
- **Disqus** (embed komentar)
- **Bootstrap 4/5** (UI)
- **FontAwesome 5/6** (ikon)
- **jQuery** (untuk dropdown dan interaksi kecil)
- **Pillow** (image field)
- **CKEditor** (jika ada rich text editor)

## Cara Deploy di Railway
1. Pastikan sudah push semua kode ke GitHub.
2. Buat project baru di Railway, hubungkan ke repo ini.
3. Atur environment variable (jika perlu: DB, Auth0, Disqus, dsb).
4. Jalankan migrasi dan collectstatic.
5. Enjoy your blog!

---

**By Alief Faza Rizqi Adi Jaya**

## Features

- 🎨 Modern dark theme UI with Bootstrap
- 👤 User authentication (login/register)
- 📝 Article management system
- 🖼️ Gallery page for nature photos
- 💼 Portfolio page
- 📱 Fully responsive design
- 🔒 Secure user management
- 💬 Comments system

## Tech Stack

- Django
- Bootstrap
- SQLite
- HTML/CSS
- JavaScript

## Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/yourusername/faza-blog.git
cd faza-blog
```

2. Create and activate virtual environment
```bash
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

5. Create superuser (admin)
```bash
python manage.py createsuperuser
```

6. Run the development server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser to see the blog.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- Alief Faza Rizqi Adi Jaya 
