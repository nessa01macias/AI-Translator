from flask import render_template, url_for, flash, redirect, request, jsonify, session
from sqlalchemy.exc import SQLAlchemyError
from flaskblog import app, db, bcrypt, pipe_en_to_fi, pipe_fi_to_en, port_number
from flaskblog.form import RegistrationForm, LoginForm, TranslationForm
from flaskblog.models import User,Translation
from flask_login import login_user, logout_user, current_user, login_required
import requests, json


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    form = TranslationForm()
    user_id = current_user.id if current_user.is_authenticated else None

    if form.validate_on_submit():
        # Get form data
        original_lan = form.language.data
        content = form.content.data

        # Call the translation logic directly 
        if original_lan == "english":
            translated_text = pipe_en_to_fi(content)
        elif original_lan == "finnish":
            translated_text = pipe_fi_to_en(content)
        else:
            flash("Unsupported language", "danger")
            return redirect(url_for("home"))

        # Save to database if the user is logged in
        if user_id:
            try:
                new_translation = Translation(
                    original_lan=original_lan,
                    target_lan="finnish" if original_lan == "english" else "english",
                    content=content,
                    translated_content=translated_text,
                    user_id=user_id,
                )
                db.session.add(new_translation)
                db.session.commit()
            except SQLAlchemyError as e:
                print(f"Database error: {e}")
                flash("Failed to save translation", "danger")

        # Flash messages for display
        flash(f"{content}", "dark")
        flash(f"{translated_text}", "secondary")

        return redirect(url_for("home"))

    return render_template("home.html", form=form)

@app.route("/translate", methods=["POST"])
def translate():
    # Extract data from the request
    data = request.json
    original_lan = data.get("original_lan")
    content = data.get("content", "").strip()
    user_id = data.get("user_id")

    # Validate input
    if not original_lan or not content:
        return jsonify({"error": "Invalid request data"}), 400

    # Determine translation direction
    if original_lan == "english":
        translated_text = pipe_en_to_fi(content)
        target_lan = "finnish"
    elif original_lan == "finnish":
        translated_text = pipe_fi_to_en(content)
        target_lan = "english"
    else:
        return jsonify({"error": "Unsupported language"}), 400

    # Prepare response
    response = {
        "original_lan": original_lan,
        "target_lan": target_lan,
        "content": content,
        "translated_content": translated_text,
    }

    # Save to database if user is logged in
    if user_id:
        try:
            user = User.query.get(int(user_id))
            if user:
                new_translation = Translation(
                    original_lan=original_lan,
                    target_lan=target_lan,
                    content=content,
                    translated_content=translated_text,
                    user_id=user_id,
                )
                db.session.add(new_translation)
                db.session.commit()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return jsonify({"error": "Failed to save translation"}), 500

    return jsonify(response)


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