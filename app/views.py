from flask import Blueprint, render_template
from flask_login import current_user
from flask_login import login_required

views = Blueprint("views", __name__)


@views.route("/")
def index():
    return render_template("index.html", user=current_user)

@login_required
@views.route("/account")
def account():
    return render_template("account.html", user=current_user)
