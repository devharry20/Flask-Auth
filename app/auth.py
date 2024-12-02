from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from . import db


auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                
                return redirect(url_for("views.index"))
            else:
                flash("Incorrect email or password", category="error")
        else:
            flash("No account with this email found. Please create an account", category="error")
        
    return render_template("login.html", user=current_user)

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("There is already an account with this email. Please login", category="error")
        elif password1 != password2:
            flash("Passwords do not match", category="error")
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method="pbkdf2:sha256"))
            print(f"Created {email} {name}")
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")

            return redirect(url_for("views.index"))
            
    return render_template("register.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
