from datetime import datetime, timedelta, timezone
from distutils.command.config import config
from flaskblog import db, login_manager
from flask_login import UserMixin
from flask import current_app
import jwt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) #define relationship with
    #the Post the class, that is why we need upper case Post
    
    def get_reset_token(self, expires_sec=60): #TODO change later
        reset_token = jwt.encode(
            {
                "user_id": self.id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_sec)
                #need to be .now() since we need to add it. utcnow is not allowed
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return reset_token
    
    @staticmethod
    def verify_reset_token(token):
        
        try:
            user_id = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=timedelta(seconds=10),
                algorithms=['HS256']
            )['user_id'] #TODO see if works, if not change it to get.('user_id')
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self): #magic printing mathod (same as << outload in C++?)
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    #int he db.ForeignKey we refer user.id with its column in the database, which the column namse
    #is automatically lower cased.
    
    def __repr__(self): #magic printing mathod (same as << outload in C++?)
        return f"Post('{self.title}','{self.date_posted}')"
    