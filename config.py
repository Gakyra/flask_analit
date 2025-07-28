# config.py
import os
from dotenv import load_dotenv


HF_TOKEN = os.getenv('HF_TOKEN')

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
