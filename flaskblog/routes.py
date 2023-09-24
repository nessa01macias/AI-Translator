from flask import render_template, url_for, flash, redirect, request, jsonify
from flaskblog import app, db, bcrypt, pipe_en_to_fi, pipe_fi_to_en, port_number
from flaskblog.form import RegistrationForm, LoginForm, TranslationForm
from flaskblog.models import User,Translation
from flask_login import login_user, logout_user, current_user, login_required
import requests

dummy_translations = [
    {
        'autor': 'Corey Schafor',
        'title' : 'Blog post 1',
        'content': 'first post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'autor': 'Corey Schafor',
        'title' : 'Blog post 2',
        'content': 'second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home", methods= ['GET', 'POST'])
def home():
    url = f'http://localhost:{port_number}/get_translation'
    form = TranslationForm()
    submitted_content = None
    if form.validate_on_submit():    
        language = form.language.data
        submitted_content = form.content.data
        data = {"original_lan": language, "content": submitted_content}

        print(f'1. this is written in {language}. content to translate: {data["content"]}')
        translated_content_response = requests.post(url, json=data)
        # Deserialize the JSON response to access the content
        translated_content = translated_content_response.json()
        print(f'4. result from request: {translated_content}')

        flash(f'{submitted_content}', 'dark')
        flash(f'{translated_content["translation_text"]}', 'secondary')

        return redirect(url_for('home'))
    return render_template('home.html', form=form, submitted_content = submitted_content)

@app.route("/get_translation", methods=['GET', 'POST'])
def get_translation():
    data = request.json
    original_lan = data["original_lan"]
    content = data["content"]
    print(f'2. got from the incoming post request {data}')
    translated_text = None
    if (original_lan == "english"):
        translated_text = pipe_en_to_fi(content)
        print(f'3. this is my dummy translation:{translated_text[0]["translation_text"]}')
    elif (original_lan == "finnish"):
        translated_text = pipe_fi_to_en(content)

    return jsonify(translated_text[0])


@app.route("/translations")
@login_required
def translations():
    return render_template('translations.html', dummy_translations=dummy_translations)

@app.route("/about")
def about():
    return render_template('about.html', title= 'About')


@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    form = RegistrationForm()
    # form fullfills the requisits in the validations rules
    if form.validate_on_submit():
        password_hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        username = form.username.data.lower()
        new_user = User(username=username, password= password_hashed)
        db.session.add(new_user)
        db.session.commit()
        flash('You account has been created successfully!', 'sucess')
        return redirect(url_for('login'))
    
    return render_template('register.html', title= 'Register', form= form)


@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
      
    form = LoginForm()
    if form.validate_on_submit():
            input_username = form.username.data.lower()
            username = User.query.filter_by(username = input_username).first()
            input_password = form.password.data
            if username and bcrypt.check_password_hash(username.password, input_password):
                login_user(username, remember=form.remember.data)
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for('home'))
            else:
                flash('Login unsucessfull. Please check username or password', 'warning')
    return render_template('login.html', title= 'Login', form= form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
