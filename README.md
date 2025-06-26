# Faza Blog

A modern blog platform built with Django and featuring a beautiful dark theme UI. This blog system includes user management, article publishing, gallery features, and a responsive design.

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