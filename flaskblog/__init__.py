from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from transformers import pipeline

app = Flask(__name__)

app.config['SECRET_KEY'] = '53926ed2fb071c29c11d17e16eb33f7b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
port_number = 5000

#creating a sqlite database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
pipe_en_to_fi = pipeline(
    "translation", model="Helsinki-NLP/opus-mt-en-fi",
    # not including the tensor representation in the output
    return_tensors=False, 
    # setting up the output to be already decoded text 
    return_text=True,
    # cleaning up extra spaces in the output text
    clean_up_tokenization_spaces=True,
)

pipe_fi_to_en = pipeline(
    "translation", model="Helsinki-NLP/opus-mt-fi-en",
    # not including the tensor representation in the output
    return_tensors=False, 
    # setting up the output to be already decoded text 
    return_text=True,
    # cleaning up extra spaces in the output text
    clean_up_tokenization_spaces=True,
)


from flaskblog import routes
