from flask import render_template, url_for, flash, redirect, request, jsonify, session
from sqlalchemy.exc import SQLAlchemyError
from flaskblog import app, db, bcrypt, pipe_en_to_fi, pipe_fi_to_en, port_number
from flaskblog.form import RegistrationForm, LoginForm, TranslationForm
from flaskblog.models import User,Translation
from flask_login import login_user, logout_user, current_user, login_required
import requests, json


@app.route("/")
@app.route("/home", methods= ['GET', 'POST'])
def home():
    url = f'http://localhost:{port_number}/get_translation'
    form = TranslationForm()

    # Include user_id in the request data
    user_id = current_user.id if current_user.is_authenticated else None

    if form.validate_on_submit():    
        language = form.language.data
        submitted_content = form.content.data
        data = {"original_lan": language, "content": submitted_content, "user_id": user_id}
        # print(f'1. this is written in {language}. content to translate: {data["content"]}')
        translated_content_response = requests.post(url, json=data)
        # Deserialize the JSON response to access the content
        try:
            # Attempt to parse JSON from the response
            translated_content = translated_content_response.json()
        except json.decoder.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            return jsonify({"error": "Invalid translation response"})

        # print(f'4. result from request: {translated_content}')
        flash(f'{submitted_content}', 'dark')
        flash(f'{translated_content["translation_text"]}', 'secondary')

        return redirect(url_for('home'))
    return render_template('home.html', form=form)


@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
         print("/register: current user", current_user)
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
        print("/login: current user", current_user)
        return redirect(url_for('home'))
      
    form = LoginForm()
    if form.validate_on_submit():
            input_username = form.username.data.lower()
            username = User.query.filter_by(username = input_username).first()
            input_password = form.password.data
            if username and bcrypt.check_password_hash(username.password, input_password):
                login_user(username, remember=form.remember.data)
                session['user_id'] = current_user.id
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for('home'))
            else:
                flash('Login unsucessfull. Please check username or password', 'warning')
    return render_template('login.html', title= 'Login', form= form)

@app.route("/get_translation", methods=['GET', 'POST'])
def get_translation():
    url = f'http://localhost:{port_number}/get_translation_saved'

    # extracting the data from the request form from /home
    data = request.json
    original_lan = data["original_lan"]
    content = data["content"].strip()
    user_id = data["user_id"]
    # print(f'2. got from the incoming post request {data}')

    target_lan = None
    translated_text = None
    if (original_lan == "english"):
        translated_text = pipe_en_to_fi(content)
        target_lan = "finnish"
    elif (original_lan == "finnish"):
        translated_text = pipe_fi_to_en(content)
        target_lan = "english"

    # Load the user using the user_id
    if user_id:
        user = User.query.get(int(user_id))
        login_user(user)
        all_data = {"original_lan": original_lan, "content": content, "target_lan": target_lan, "translated_content":translated_text[0]['translation_text'], "user_id": user_id}
        translated_content_saved_db_response = requests.post(url, json=all_data)
        print("translated_content_saved_db_response: ",translated_content_saved_db_response)

    print("/get_translation: current user", current_user)

    # print(f'3. this is my dummy translation:{translated_text[0]["translation_text"]}')
    return jsonify(translated_text[0])

@app.route("/get_translation_saved", methods=['GET', 'POST'])
def get_translation_saved():

    data = request.json
    original_lan = data["original_lan"]
    content = data["content"]
    target_lan = data["target_lan"]
    translated_content = data["translated_content"]
    user_id = data["user_id"]
    # print("/get_translation_saved: the data to be saved is ", data)

    if not all([original_lan, content, target_lan, translated_content]):
        return jsonify({"error": "Invalid request data"}), 400

    try:
        new_translation = Translation(original_lan= original_lan, content= content, target_lan= target_lan, translated_content = translated_content, user_id = user_id)
        db.session.add(new_translation)
        db.session.commit()
        return jsonify({"message": "Translation saved successfully"})
    except SQLAlchemyError as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": "Failed to save translation"}), 500


@app.route("/translations")
@login_required
def translations():
    try:
        translations_history = Translation.query.filter_by(user_id=current_user.id).all()
        # This line filters translations by the current user's ID
    except Exception as e:
        translations_history = []
        print("Error occurred when retrieving translations from db:", str(e))
    return render_template('translations.html', translations_history = translations_history)

@app.route("/about")
def about():
    return render_template('about.html', title= 'About')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))