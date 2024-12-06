# Flask-Auth

This is a boilerplate Python Flask app with user authentication, including Google OAuth, designed to be a starting point for building Flask-based applications with authentication functionaility using SQLite.

### Features

-   User registration
-   User registration using Google OAuth
-   User login
-   User logout
-   Account info page
-   Password hashing for secure storage
-   Session management using Flask's built-in session handling

### Install dependencies

`pip install -r requirements.txt`

### Gather Google developer credentials

In order to run this app you will need to [register a Google application](https://console.developers.google.com/apis/credentials) to get your client
secret and ID.\
In a development environment, set the authorized javascript origins to http://127.0.0.1:5000 and authorized redirect uris to http://127.0.0.1:5000/callback\
In a production environment, these IPs will need to be modified accordingly\
\
You will then need to create a `.env` file in the root directory of the project, including your

```
GOOGLE_CLIENT_ID = "ID"
GOOGLE_CLIENT_SECRET = "SECRET
```

### Run the boilerplate

`python -m app`
Access the app on http://127.0.0.1:5000

### File structure

```plaintext
app/
├── __init__.py            # Main Flask application
├── __main__.py            # Package file
├── auth.py                # Authentication views
├── models.py              # Database models
├── views.py               # Non-protected views
├── helpers.py             # Helper / regular functions
├── pages/                 # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── login.html         # Login page
│   └── set_password.html  # Set password page
│   ├── register.html      # Registration page
│   └── account.html       # Account page
├── static/                # Static files (only css)
│   ├── base.css
│   ├── login.css
│   ├── register.css
├── requirements.txt       # Python dependencies
└── README.md              # Documentation
```
