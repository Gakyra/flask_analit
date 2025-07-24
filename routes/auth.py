from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_

from models import db, User
from forms import RegisterForm, LoginForm

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            or_(User.email == form.email.data.strip(), User.username == form.username.data.strip())
        ).first()
        if existing_user:
            flash("Пользователь с таким email или именем уже существует", "warning")
            return redirect(url_for("auth.register"))
        new_user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip(),
            password=generate_password_hash(form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Вы успешно зарегистрированы!", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.email_or_username.data.strip()
        password = form.password.data

        user = User.query.filter(
            or_(User.email == identifier, User.username == identifier)
        ).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f"Добро пожаловать, {user.username}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.dashboard_page"))  # ✅ исправлено
        else:
            flash("Неверные данные для входа", "danger")
    return render_template("login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "info")
    return redirect(url_for("main.landing_page"))  # ✅ уже верно
