# 📝 Personal Blog Project

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

A full-featured blogging platform built with Django, featuring user authentication, post creation, and social interactions.

## 🌟 Features

### 📚 Core Functionality
- User registration/login with profile management
- CRUD operations for blog posts
- Rich text editor for post content
- Image uploads for posts and profiles

### 💬 Social Features
- Post liking/bookmarking system
- User following functionality
- Real-time notifications
- Comment system with replies

### 🛠️ Technical Highlights
- Responsive Bootstrap 5 design
- AJAX-powered interactions
- Paginated post listings
- Custom template tags

## 🚀 Deployment

### PythonAnywhere Setup
```bash
# Clone repository
git clone https://github.com/yourusername/personal-blog.git

# Set up virtual environment
mkvirtualenv --python=python3.8 blog-venv

# Install dependencies
pip install -r requirements.txt

# Configure database
python manage.py migrate
python manage.py createsuperuser

Environment Variables
Create .env file:
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourusername.pythonanywhere.com

🏗️ Project Structure
personal-blog/
├── blog/                      # Main app
│   ├── migrations/            # Database migrations
│   ├── templates/             # HTML templates
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   └── ...
├── blog_project/              # Project config
├── manage.py                  # Django CLI
└── requirements.txt           # Dependencies

🔧 Development Setup
1.Clone repository:
  git clone https://github.com/yourusername/personal-blog.git
  cd personal-blog
2.Create virtual environment:
  python -m venv venv
  .\venv\Scripts\activate
3.Install dependencies:
  pip install -r requirements.txt
4.Run migrations:
  python manage.py migrate
5.Create superuser:
  python manage.py createsuperuser
6.Run development server:
  python manage.py runserver

🌐 Live Demo
Access the deployed version at:
🔗 yourusername.pythonanywhere.com

📜 License
MIT License - See LICENSE for details.

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first.

💡 Tip: Remember to set DEBUG=False in production and configure proper ALLOWED_HOSTS!
### Key Features of This README:
1. **Visual Badges** - Shows tech stack at a glance
2. **Structured Sections** - Clear separation of features, setup, and deployment
3. **PowerShell Friendly** - Includes PowerShell commands specifically for Windows users
4. **Emoji Visual Cues** - Makes sections easier to scan
5. **Production Notes** - Highlights important security considerations
