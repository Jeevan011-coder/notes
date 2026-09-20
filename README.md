# Notes App

A Django web app for creating and managing notes, with user registration, login and profile pictures.

## Features
- User registration, login and profile page
- Create, view and manage notes (with tags and file attachments)
- Landing page and responsive styling

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create the database
python manage.py migrate

# 4. (Optional) create an admin user
python manage.py createsuperuser

# 5. Run the server
python manage.py runserver
```

Then open http://127.0.0.1:8000/ in your browser.

## Project structure
- `book/` – notes app (models, views, forms)
- `user/` – registration, login, profiles
- `note/` – project settings and URLs
- `template/`, `static/` – HTML templates and CSS/images
