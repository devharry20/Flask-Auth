import json

import requests
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from .models import User
from . import get_google_provider_cfg, client, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, db
from .helpers import create_user


auth = Blueprint("auth", __name__)


@auth.route("/google/auth")
def google_auth():
    """A view which allows the user to login using Google"""
    global google_provider_cfg
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri = request.url_root.rstrip("/") + "/callback",
        scope=["openid", "email", "profile"],
    )

    return redirect(request_uri)

@auth.route("/callback")
def google_callback():
    """A view which is called once a Google user is authenticated"""
    code = request.args.get("code")
    
    if not code:
        return redirect(url_for("views.index"))

    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        users_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
        
        user = User.query.filter_by(email=users_email).first()
        if user:
            if users_id == user.user_auth:
                if user.user_auth:
                    login_user(user)
                    return redirect(url_for("views.index"))
                else:
                    flash("Your account was not created using a Google account, please login with your email and password")
            else:
                flash("Authentication error, please login using the approriate method")

            return redirect(url_for("auth.login"))
        
        session["email"] = users_email
        session["name"] = users_name
        session["id"] = userinfo_response.json()["sub"]
        
        return redirect(url_for("auth.set_password"))
    else:
        return "User email not available or not verified by Google.", 400

@auth.route("/set-password", methods=["GET", "POST"])
def set_password():
    """A view which allows the user to set their account password, only used for Google registrations"""
    set_reset = request.args.get("type", "set")

    if request.method == "POST":
        users_name = session.get("name")
        users_email = session.get("email")
        user_id = session.get("id")
        password1 = request.form.get("password2")
        password2 = request.form.get("password2")
        set_password = request.form.get("type")

        if password1 != password2:
            flash("Passwords do not match")
        else:
            if set_password == "reset":
                user = current_user
                if user is None:
                    flash("You need to be logged in to change your account password!")
                    return redirect(url_for("auth.login"))
            
                new_password = generate_password_hash(password1, method="pbkdf2:sha256")
                user.password = new_password
                db.session.commit()

                logout_user()

                flash("Password successfully changed. Please login")
                return redirect(url_for("auth.login"))

            user = User.query.filter_by(email=users_email).first()
            if user:
                return redirect(url_for("auth.login"))
            
            new_user = create_user(users_email, users_name, password1, user_type="google", user_auth=user_id)
            login_user(new_user, remember=True)

            return redirect(url_for("views.index"))
        
    return render_template("set_password.html", user=current_user, type=set_reset)

@auth.route("/login", methods=["GET", "POST"])
def login():
    """A view to log a user into the session"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if user.user_auth:
                return redirect(url_for("auth.google_auth"))
            
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                
                return redirect(url_for("views.index"))
            else:
                flash("Incorrect email or password")
        else:
            flash("No account with this email found. Please create an account")
        
    return render_template("login.html", user=current_user)

@auth.route("/register", methods=["GET", "POST"])
def register():
    """A view to register a users account"""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("There is already an account with this email. Please login")
        elif password1 != password2:
            flash("Passwords do not match")
        else:
            new_user = create_user(email, name, password1, user_type="local")
            login_user(new_user, remember=True)
            print(f"Created {email} {name}")
            flash("Account created!", category="success")

            return redirect(url_for("views.index"))
            
    return render_template("register.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    """A view to log a user out of their session"""
    logout_user()
    return redirect(url_for("auth.login"))
