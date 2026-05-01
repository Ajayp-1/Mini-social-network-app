# Mini Social Network App

A complete Django-based social networking application with user authentication, posts, likes, comments, and analytics.

## Features

### 🔐 User Authentication
- User registration and login/logout
- Django's built-in User model
- Profile pages for each user

### 📝 Posts Management
- Create, edit, and delete posts
- Text content with optional image uploads
- Display author, timestamp, like count, and comments
- Image preview functionality

### ❤️ Likes System
- Like/unlike posts with AJAX
- Real-time like count updates
- Track which posts users have liked

### 💬 Comments
- Add comments to posts
- Display commenter name and timestamp
- Nested comment display under posts

### 📱 Feed & Navigation
- Homepage feed showing all posts (latest first)
- Bootstrap-based responsive UI
- Navigation bar with Home, Profile, Analytics, Login/Logout

### 👤 Profile Pages
- Individual user profiles
- Display user's posts and statistics
- Join date, post count, total likes received

### 📊 Analytics Dashboard
- Total posts, likes, comments, and users
- Top 3 most liked posts
- Top 5 users by post count (matplotlib chart)
- Platform activity metrics

### 🛠️ Admin Panel
- Django admin interface
- Manage users, posts, and comments
- Custom admin configurations with search and filters

## Technology Stack

- **Backend**: Django 5.2.6
- **Database**: SQLite3
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Image Processing**: Pillow
- **Data Visualization**: Matplotlib
- **Authentication**: Django's built-in auth system

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Project
```bash
# If you have the project files, navigate to the project directory
cd mini_social_network
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### Step 4: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account for accessing the Django admin panel.

### Step 6: Start Development Server
```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## Usage Guide

### 🏠 Homepage (Feed)
- Visit `http://127.0.0.1:8000/` to see all posts
- Posts are displayed in reverse chronological order
- Like posts by clicking the heart icon
- Add comments using the comment form

### 👤 User Registration & Login
- Register: `http://127.0.0.1:8000/signup/`
- Login: `http://127.0.0.1:8000/login/`
- Logout: Click "Logout" in the navigation bar

### ✍️ Creating Posts
- Click "Create Post" button on the homepage
- Add text content (required)
- Optionally upload an image
- Preview functionality available

### 📊 Analytics
- Visit `http://127.0.0.1:8000/analytics/`
- View platform statistics
- See top posts and users
- Interactive charts powered by matplotlib

### 👥 User Profiles
- Click on any username to view their profile
- See user's posts, join date, and statistics
- Edit/delete your own posts from your profile

### 🛠️ Admin Panel
- Visit `http://127.0.0.1:8000/admin/`
- Login with superuser credentials
- Manage users, posts, and comments
- Advanced filtering and search capabilities

## Project Structure

```
mini_social_network/
├── core/                          # Main Django app
│   ├── migrations/               # Database migrations
│   ├── templates/               # HTML templates
│   │   ├── core/               # App-specific templates
│   │   │   ├── analytics.html
│   │   │   ├── base.html
│   │   │   ├── create_post.html
│   │   │   ├── delete_post.html
│   │   │   ├── edit_post.html
│   │   │   ├── feed.html
│   │   │   └── profile.html
│   │   └── registration/       # Auth templates
│   │       ├── login.html
│   │       └── signup.html
│   ├── admin.py                # Admin configurations
│   ├── models.py               # Database models
│   ├── urls.py                 # App URL patterns
│   └── views.py                # View functions
├── socialmedia/                # Django project settings
│   ├── settings.py             # Project settings
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py                 # WSGI configuration
├── media/                      # User uploaded files
├── db.sqlite3                  # SQLite database
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Key Features Explained

### Models
- **Post**: Content, author, image, timestamps, like/comment counts
- **Like**: User-post relationship with uniqueness constraint
- **Comment**: User comments on posts with timestamps

### Views
- **Feed**: Paginated post display with like status
- **Authentication**: Signup, login, logout with Django auth
- **Post Management**: CRUD operations with ownership validation
- **Analytics**: Statistics and matplotlib chart generation
- **Profile**: User-specific post display and statistics

### Templates
- **Responsive Design**: Bootstrap-based mobile-friendly UI
- **AJAX Integration**: Real-time like functionality
- **Form Validation**: Client-side and server-side validation
- **Image Preview**: JavaScript-based image preview

## Customization

### Adding New Features
1. Create new models in `core/models.py`
2. Add corresponding views in `core/views.py`
3. Create templates in `core/templates/core/`
4. Update URL patterns in `core/urls.py`
5. Run migrations: `python manage.py makemigrations && python manage.py migrate`

### Styling
- Modify Bootstrap classes in templates
- Add custom CSS in template `<style>` sections
- Update navigation in `base.html`

### Database
- SQLite for development (included)
- For production, update `DATABASES` in `settings.py`

## Troubleshooting

### Common Issues

1. **Module not found errors**
   ```bash
   python -m pip install -r requirements.txt
   ```

2. **Database errors**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Static files not loading**
   ```bash
   python manage.py collectstatic
   ```

4. **Permission errors on uploads**
   - Ensure `media/` directory has write permissions

### Development Tips
- Use `python manage.py shell` for interactive Django shell
- Enable Django debug mode in `settings.py` for development
- Check `python manage.py check` for configuration issues

## Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Configure proper media file serving for production
- Use environment variables for sensitive settings

## License

This project is created for educational purposes. Feel free to modify and use as needed.

## Support

For issues or questions, please check the Django documentation at https://docs.djangoproject.com/