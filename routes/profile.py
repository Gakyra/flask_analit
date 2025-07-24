from flask import Blueprint, render_template
from flask_login import login_required, current_user

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/profile")
@login_required
def profile_view():
    return render_template("profile.html", user=current_user)
