from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from models import Investment
from llm.advisor import generate_analysis

llm_bp = Blueprint("llm", __name__)

@llm_bp.route("/advisor")
@login_required
def advisor_view():
    assets = Investment.query.filter_by(user_id=current_user.id).all()
    stats = {}
    for inv in assets:
        stats[inv.symbol] = {
            "quantity": inv.quantity,
            "profit": (getattr(inv, "current_price", 0) * inv.quantity) - (inv.buy_price * inv.quantity)
        }
    try:
        advice = generate_analysis(stats)
        flash("🧠 Анализ успешно получен", "success")
    except Exception as e:
        advice = f"⚠️ Ошибка при запросе анализа: {e}"
        flash("LLM анализ временно недоступен", "danger")
    return render_template("advisor.html", text=advice)
