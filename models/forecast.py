from flask_analit.extensions import db

class Forecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    symbol = db.Column(db.String(50), nullable=False)
    predicted = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
