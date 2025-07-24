from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Investment, PortfolioHistory
from forms import AddInvestmentForm, EditInvestmentForm
from config.assets import AVAILABLE_ASSETS
from services.pricing import get_synced_price

portfolio_bp = Blueprint("portfolio", __name__)

def log_history(user_id, symbol, quantity, buy_price, action):
    db.session.add(PortfolioHistory(
        user_id=user_id, symbol=symbol, quantity=quantity,
        buy_price=buy_price, action=action
    ))
    db.session.commit()

@portfolio_bp.route("/portfolio", methods=["GET", "POST"])
@login_required
def view_portfolio():
    form = AddInvestmentForm()
    form.symbol.choices = AVAILABLE_ASSETS

    if form.validate_on_submit():
        name = dict(AVAILABLE_ASSETS).get(form.symbol.data, form.symbol.data.title())
        db.session.add(Investment(
            user_id=current_user.id, symbol=form.symbol.data,
            name=name, quantity=form.quantity.data, buy_price=form.buy_price.data
        ))
        db.session.commit()
        log_history(current_user.id, form.symbol.data, form.quantity.data, form.buy_price.data, "add")
        flash("✅ Актив добавлен", "success")
        return redirect(url_for("portfolio.view_portfolio"))

    investments = Investment.query.filter_by(user_id=current_user.id).all()
    enriched = []
    for inv in investments:
        current = get_synced_price(inv.symbol)
        if current <= 0:
            continue
        value_now = current * inv.quantity
        value_then = inv.buy_price * inv.quantity
        profit = value_now - value_then
        enriched.append({
            "id": inv.id, "name": inv.name, "symbol": inv.symbol,
            "quantity": inv.quantity, "buy": inv.buy_price,
            "current": current, "profit": profit
        })

    sort_by = request.args.get("sort")
    if sort_by == "profit":
        enriched.sort(key=lambda x: x["profit"], reverse=True)
    elif sort_by == "name":
        enriched.sort(key=lambda x: x["name"].lower())
    elif sort_by == "current":
        enriched.sort(key=lambda x: x["current"], reverse=True)

    return render_template("portfolio.html", form=form, investments=enriched)

@portfolio_bp.route("/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit_investment(item_id):
    inv = Investment.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    form = EditInvestmentForm(obj=inv)
    if form.validate_on_submit():
        inv.quantity = form.quantity.data
        inv.buy_price = form.buy_price.data
        db.session.commit()
        log_history(current_user.id, inv.symbol, form.quantity.data, form.buy_price.data, "edit")
        flash("✅ Изменения сохранены", "success")
        return redirect(url_for("portfolio.view_portfolio"))
    return render_template("edit_investment.html", form=form, investment=inv)

@portfolio_bp.route("/delete/<int:item_id>")
@login_required
def delete_investment(item_id):
    inv = Investment.query.filter_by(id=item_id, user_id=current_user.id).first()
    if inv:
        log_history(current_user.id, inv.symbol, inv.quantity, inv.buy_price, "delete")
        db.session.delete(inv)
        db.session.commit()
        flash("❌ Актив удалён", "info")
    else:
        flash("Актив не найден", "warning")
    return redirect(url_for("portfolio.view_portfolio"))
