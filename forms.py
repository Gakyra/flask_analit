from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")

class LoginForm(FlaskForm):
    email_or_username = StringField("Email или имя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")

class AddInvestmentForm(FlaskForm):
    symbol = SelectField("Актив", choices=[
        ("bitcoin", "Bitcoin (BTC)"),
        ("ethereum", "Ethereum (ETH)"),
        ("solana", "Solana (SOL)"),
        ("dogecoin", "Dogecoin (DOGE)"),
        ("binancecoin", "BNB"),
        ("cardano", "Cardano (ADA)")
    ], validators=[DataRequired()])
    quantity = FloatField("Количество", validators=[DataRequired()])
    buy_price = FloatField("Цена покупки (USD)", validators=[DataRequired()])
    submit = SubmitField("Добавить")

class EditInvestmentForm(FlaskForm):
    quantity = FloatField("Новое количество", validators=[DataRequired()])
    buy_price = FloatField("Новая цена покупки (USD)", validators=[DataRequired()])
    submit = SubmitField("Сохранить изменения")

class ForecastForm(FlaskForm):
    symbol = SelectField("Выберите актив", choices=[
        ("bitcoin", "Bitcoin"),
        ("ethereum", "Ethereum"),
        ("solana", "Solana"),
        ("dogecoin", "Dogecoin"),
        ("binancecoin", "BNB"),
        ("cardano", "Cardano")
    ], validators=[DataRequired()])
    submit = SubmitField("Прогнозировать")




