from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from transformers import pipeline
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
port_number = 8000

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
genai.configure(api_key=os.environ["GEMINI_API_KEY"])


#creating a sqlite database
db = SQLAlchemy(app)
migrate = Migrate(app, db) 
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def pipe_en_to_fi(text):
    prompt = f"Käännä seuraava teksti suomeksi, vastauksessasi on oltava vain suomenkielinen käännös: {text}"
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

def pipe_fi_to_en(text):
    prompt = f"Translate the following text to English, your response must only be the translation in english: {text}"
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text


from flaskblog import routes
