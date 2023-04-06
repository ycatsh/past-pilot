from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request
from past_pilot.forms import SignInForm, SignUpForm, QuestionForm
from past_pilot.similarity import calculate_similarity
from past_pilot.pdf_converter import converter
from past_pilot.key import generate_key
from past_pilot import app, db, bcrypt
from past_pilot.models import User


@app.route('/question')
def index():
    form = QuestionForm()
    return render_template('index.html', form=form)


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/resources')
def resources():
    return render_template('resources.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignUpForm()
    key = generate_key()
    
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, key=form.key.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')

        return redirect(url_for('signin'))


    return render_template('signup.html', title='Sign Up', form=form, key=key)


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignInForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('signin.html', title='Sign In', form=form)


@app.route("/signout")
def signout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html')




