import json
from statistics import mean, stdev
from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from models import db, Forecast
from forms import ForecastForm
from config.assets import AVAILABLE_ASSETS
from services.pricing import get_synced_price, get_historical_prices

forecast_bp = Blueprint("forecast", __name__)

@forecast_bp.route("/forecast", methods=["GET", "POST"])
@login_required
def forecast_view():
    form = ForecastForm()
    form.symbol.choices = AVAILABLE_ASSETS
    forecast_data = []
    symbol_name = None

    if form.validate_on_submit():
        symbol = form.symbol.data
        symbol_name = dict(AVAILABLE_ASSETS).get(symbol, symbol.title())

        # ⛔ Если валидной цены нет — не строим
        base = get_synced_price(symbol)
        if base <= 0:
            flash(f"⚠️ Нет актуальной цены для {symbol_name}. Прогноз невозможен.", "danger")
            return render_template("forecast_result.html", form=form)

        # 📈 Грузим историю
        history = get_historical_prices(symbol)
        if len(history) < 5:
            flash("📭 Истории недостаточно. Построен fallback‑прогноз.", "warning")

        # 🎯 Первый день — строго current price
        forecast_data.append(round(base, 2))

        # 🔬 Волатильность
        volatility = stdev(history[-5:]) / base if len(history) >= 5 else 0.03

        # 🧠 Генерация прогноза
        for i in range(1, 10):
            recent = history[-5:] if len(history) >= 5 else [base] * 5
            avg = mean(recent)
            next_price = avg + avg * volatility
            forecast_data.append(round(next_price, 2))
            history.append(next_price)

        db.session.add(Forecast(
            user_id=current_user.id,
            symbol=symbol,
            predicted=json.dumps(forecast_data)
        ))
        db.session.commit()

        flash(f"📊 Прогноз на 10 дней построен для {symbol_name}", "success")

    return render_template("forecast_result.html", form=form, symbol=symbol_name, data=forecast_data)
