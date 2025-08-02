from flask_analit.extensions import db

class PortfolioHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    symbol = db.Column(db.String(50))
    quantity = db.Column(db.Float)
    buy_price = db.Column(db.Float)
    action = db.Column(db.String(20))  # add / edit / delete
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

def log_history(user_id, symbol, quantity, buy_price, action):
    record = PortfolioHistory(
        user_id=user_id,
        symbol=symbol,
        quantity=quantity,
        buy_price=buy_price,
        action=action
    )
    db.session.add(record)
    db.session.commit()
