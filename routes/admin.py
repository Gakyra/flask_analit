from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from models import User, Forecast, db
from werkzeug.security import generate_password_hash

admin_bp = Blueprint("admin", __name__)

def admin_required(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return login_required(wrapper)

def ensure_superadmin():
    if not User.query.filter_by(email="admin@site.com").first():
        admin = User(
            username="admin",
            email="admin@site.com",
            password=generate_password_hash("supersecure123"),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("[🛡️] Супер-админ создан: admin@site.com / supersecure123")

@admin_bp.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    users = User.query.all()
    forecasts = Forecast.query.all()
    return render_template("admin_dashboard.html", users=users, forecasts=forecasts)
