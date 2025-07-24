from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Investment
from llm.advisor import generate_analysis
from services.pricing import get_synced_price

main_bp = Blueprint("main", __name__)

# Стартовая страница (до регистрации)
@main_bp.route("/")
def landing_page():
    return render_template("landing.html")

# Личный кабинет (после входа)
@main_bp.route("/dashboard")
@login_required
def dashboard_page():
    assets = Investment.query.filter_by(user_id=current_user.id).all()
    stats = {}
    for a in assets:
        current = get_synced_price(a.symbol)
        profit = current * a.quantity - a.buy_price * a.quantity
        stats[a.symbol] = {"quantity": a.quantity, "profit": round(profit, 2)}

    analysis = generate_analysis(stats) if stats else None
    return render_template("index.html", username=current_user.username, analysis=analysis)
