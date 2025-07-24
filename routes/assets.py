from flask import Blueprint, render_template
from config.assets import AVAILABLE_ASSETS
from services.pricing import get_synced_price

assets_bp = Blueprint("assets", __name__)

@assets_bp.route("/assets")
def asset_list():
    enriched = []
    for symbol, name in AVAILABLE_ASSETS:
        price = get_synced_price(symbol)
        if price > 0:
            enriched.append({"symbol": symbol, "name": name, "price": price})
    return render_template("asset_list.html", assets=enriched)
