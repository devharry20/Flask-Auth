from flask import Blueprint, render_template
from flask_login import current_user
from flask_login import login_required

views = Blueprint("views", __name__)


@views.route("/")
def index():
    """A view to render the home page"""
    return render_template("index.html", user=current_user)

@views.route("/account")
@login_required
def account():
    """A protected view to show users account data"""
    return render_template("account.html", user=current_user)
