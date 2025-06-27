# Faza Blog

Faza Blog adalah platform blog modern berbasis Django dengan fitur lengkap, tampilan profesional, dan integrasi berbagai layanan modern.

## Fitur Lengkap
- **Autentikasi**
  - Login/Logout dengan email-password (Django Auth)
  - Login/Logout dengan Auth0 (OAuth2, Social Login: Google, dsb)
- **Manajemen Artikel**
  - CRUD artikel (admin/penulis)
  - Daftar artikel dengan filter tag, pencarian (search), dan pagination
  - Detail artikel dengan navigasi next/prev
  - Tag artikel (filter dan tampilan konsisten)
  - Artikel terkait otomatis berdasarkan tag
  - Artikel populer berdasarkan komentar
  - Upload gambar judul artikel
- **Komentar**
  - Komentar via Disqus pada detail artikel
  - Komentar hanya untuk user login (opsional)
- **Galeri**
  - Galeri gambar dari artikel, dengan pagination
- **Dashboard**
  - Dashboard admin dan penulis untuk kelola artikel, user, kategori, komentar
- **Tentang & Portofolio**
  - Halaman profil, portofolio, dan proyek
- **UI/UX**
  - Responsive, dark mode, dan konsisten
  - Navbar dengan dropdown user/admin
  - Footer dengan social media (Instagram, TikTok, GitHub)
  - Scroll to top button
  - Progress bar membaca artikel (opsional)
- **Pencarian**
  - Search artikel berdasarkan judul/isi
- **Bagikan ke Sosial Media**
  - Tombol share artikel ke WhatsApp, Twitter, Facebook
- **Newsletter/Subscription**
  - Integrasi Mailchimp, user login bisa subscribe newsletter
- **Admin Panel**
  - Kelola user, artikel, kategori, komentar

## Library & API yang Digunakan
- **Django**: Framework utama backend dan ORM.
- **Django Auth**: Autentikasi user standar.
- **Auth0**: OAuth2, Social Login (Google, dsb), keamanan login modern.
- **Disqus**: Sistem komentar embed, mudah integrasi dan moderasi.
- **Mailchimp API**: Newsletter/Subscription, user bisa subscribe dengan email (hanya untuk user login).
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
- **Newsletter**: Integrasi Mailchimp, hanya untuk user login.
- **Dark Mode**: Tampilan gelap yang nyaman di mata.
- **Scroll to Top**: Tombol untuk kembali ke atas halaman.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- Alief Faza Rizqi Adi Jaya
