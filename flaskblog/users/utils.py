import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flaskblog import mail
from flask_mail import Message

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) #get a random name for user uploaded pictures
    _ , f_ext = os.path.splitext(form_picture.filename) #we don't need f_name, so ignore it with _
    picture_fn = random_hex + f_ext #Assign picture filename
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    
    #resize profile image for website performance
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='Flaskblog.meier@gmail.com',
        recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)} 
    
    If you did not make this requestion then simply ignore this emial and no changes with be made.
    '''
    mail.send(msg)