import os
from flask import Flask
from dotenv import load_dotenv

from extensions import db, migrate, login_manager
from models import User
from routes.auth import auth_bp
from routes.main import main_bp
from routes.assets import assets_bp
from routes.portfolio import portfolio_bp
from routes.forecast import forecast_bp
from routes.profile import profile_bp
from routes.llm import llm_bp
from routes.admin import admin_bp, ensure_superadmin

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "super-secret-key")

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 📦 Регистрируем маршруты
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(assets_bp)
app.register_blueprint(portfolio_bp)
app.register_blueprint(forecast_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(llm_bp)
app.register_blueprint(admin_bp)

# 🛡️ Создаём супер-админа
with app.app_context():
    ensure_superadmin()
