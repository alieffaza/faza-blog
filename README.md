# Faza Blog

Faza Blog adalah platform blog modern berbasis Django dengan fitur lengkap, tampilan profesional, dan integrasi berbagai layanan modern.

## Fitur Lengkap
- **Autentikasi**
  - Login/Logout dengan email-password (Django Auth)
  - Login/Logout dengan Auth0 (OAuth2, Social Login: Google, dsb)
- **Manajemen Artikel**
  - CRUD artikel (admin)
  - Daftar artikel dengan filter tag, pencarian (search), dan pagination
  - Detail artikel dengan navigasi next/prev
  - Tag artikel (filter dan tampilan konsisten)
  - Artikel terkait otomatis berdasarkan tag
  - Upload gambar judul artikel
- **Komentar**
  - Komentar via Disqus pada detail artikel
- **Galeri**
  - Galeri gambar dari artikel, dengan pagination
- **Dashboard**
  - Dashboard admin dan penulis untuk kelola artikel, user, kategori, tag
- **Tentang & Portofolio**
  - Halaman profil, portofolio, dan proyek
- **UI/UX**
  - Responsive dan konsisten
  - Navbar dengan dropdown user/admin
  - Footer dengan social media (Instagram, TikTok, GitHub)
  - Scroll to top button
- **Pencarian**
  - Search artikel berdasarkan judul
- **Bagikan ke Sosial Media**
  - Tombol share artikel ke WhatsApp, Twitter, Facebook
- **Admin Panel**
  - Kelola user, artikel, kategori, tag

## Library & API yang Digunakan
- **Django**: Framework utama backend dan ORM.
- **Django Auth**: Autentikasi user standar.
- **Auth0**: OAuth2, Social Login (Google, dsb), keamanan login modern.
- **Disqus**: Sistem komentar embed, mudah integrasi dan moderasi.
- **Bootstrap 4/5**: Framework UI responsif dan modern.
- **FontAwesome 5/6**: Ikon sosial media, UI, dsb.
- **jQuery**: Interaksi kecil pada UI (dropdown, dsb).
- **Pillow**: Pengelolaan gambar (upload gambar artikel).
- **CKEditor**: Rich text editor untuk isi artikel.
- **SQLite**: Database default (bisa diganti PostgreSQL/MySQL).

## Fitur Lain
- **Artikel Terkait**: Otomatis berdasarkan tag.
- **Artikel Populer**: Berdasarkan jumlah komentar.
- **Navigasi Artikel**: Next/Prev di detail artikel.
- **Galeri**: Kumpulan gambar dari artikel.
- **Portofolio**: Showcase project/skill penulis.
- **Komentar**: Disqus, dengan notifikasi dan moderasi.
- **Share ke Sosial Media**: WhatsApp, Twitter, Facebook.
- **Scroll to Top**: Tombol untuk kembali ke atas halaman.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- Alief Faza Rizqi Adi Jaya
