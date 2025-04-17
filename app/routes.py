# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if User.query.filter_by(username=username).first():
            flash("User already exists!", "danger")
        else:
            new_user = User(username=username, password=generate_password_hash(password), role=role)
            db.session.add(new_user)
            db.session.commit()
            flash("Signup successful!", "success")
            return redirect(url_for('main.login'))

    return render_template('signup.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_role'] = user.role
            session['username'] = user.username
            flash("Login successful!", "success")
            return redirect(url_for('main.home'))
        else:
            flash("Invalid credentials!", "danger")

    return render_template('login.html')
