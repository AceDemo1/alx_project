from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note
from . import db
from flask_bcrypt import Bcrypt
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usr = request.form.get('username')
        passwd = request.form.get('password')

        user = User.query.filter_by(username=usr).first()
        if user:
            if bcrypt.check_password_hash(user.password, passwd):
                flash('Login successsfull', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Username does not exit', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        passwd = request.form.get('password')
        passwd2 = request.form.get('confirm_password')
        usr = request.form.get('username')

        user = User.query.filter_by(username=usr).first()
        user_email = User.query.filter_by(email=email).first()
        if user:
            flash('Username already exists.', category='error')
        elif user_email:
            flash('Email already exists.', category='error')
        elif not email:
            flash('Email is required.', category='error')
        elif not usr:
            flash('Username is required.', category='error')
        elif not passwd:
            flash('Password is required.', category='error')
        elif not passwd2:
            flash('Please confirm your password.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category = 'error')
        elif len(usr) < 2:
            flash('Username must be greater than 2 characters.', category = 'error')
        elif len(passwd) < 7:
            flash('Password must be at least 7 characters.', category = 'error')
        elif passwd != passwd2:
            flash("Passwords don't match", category = 'error')
        else:
            hashed = bcrypt.generate_password_hash(passwd).decode('utf-8')

            new_usr = User(email=email, username=usr, password=hashed)
            db.session.add(new_usr)
            db.session.commit()
            login_user(new_usr)         
            flash('Account created', category='success')
            return redirect(url_for('views.home'))
    
    return render_template('signup.html', user=current_user)