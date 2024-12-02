# Flask-Auth
This is a boilerplate Python Flask app with basic user authentication, designed to be a starting point for building Flask-based applications with authentication functionaility.

### Features
-   User Registration
-   User Login
-   User Logout
-   Account info page
-   Password hashing for secure storage
-   Session management using Flask's built-in session handling

### Install dependencies
```pip install -r requirements.txt```

### Run the boilerplate
```python -m app```
Access the app on http://127.0.0.1:5000

### File structure
```plaintext
app/
├── __init__.py            # Main Flask application
├── __main__.py            # Package file
├── auth.py                # Authentication views
├── models.py              # Database models
├── views.py               # Non-protected views
├── pages/                 # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   └── account.html       # Account page
├── static/                # Static files (only css)
│   ├── base.css
│   ├── login.css
│   ├── register.css
├── requirements.txt       # Python dependencies
└── README.md              # Documentation
```
