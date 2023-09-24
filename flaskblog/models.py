from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    print("User id", user_id)
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(20), unique= True, nullable= False)
    password = db.Column(db.String(60), nullable= False)
    #In an user instance, we can access an user's Translations using user.Translations
    #In a Translation instance, we can access its author using Translation.author.
    Translations = db.relationship('Translation', backref='author', lazy=True)
    
    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"
    
class Translation(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(100), nullable= False)
    date_translated = db.Column(db.DateTime, nullable= False, default= datetime.utcnow)
    content = db.Column(db.Text, nullable= False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)

    def __repr__(self):
        return f"Translation('{self.id}', '{self.title}', '{self.date_translated}')"

