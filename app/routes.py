from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, bcrypt
from app.models import User, Movie

@app.route('/')
def home():
    movies = Movie.query.all()
    return render_template('home.html', movies=movies)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    if current_user.role != 'moderator':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('home'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        movie = Movie(title=title, description=description, uploaded_by=current_user.id)
        db.session.add(movie)
        db.session.commit()
        flash('Movie added successfully', 'success')
        return redirect(url_for('home'))
    return render_template('add_movie.html')
