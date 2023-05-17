"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud 
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined 


@app.route('/') 
def create_homepage():

    return render_template('homepage.html')

@app.route('/movies')
def get_movies():
    all_movies = crud.get_movies()
    return render_template('all_movies.html', all_movies=all_movies)

@app.route('/movies/<movie_id>')
def get_movie_by_id(movie_id): 
    movie_dict = crud.get_movie_by_id(movie_id)
    user_logged_in = 'user_id' in session
    print(user_logged_in)

    return render_template('movie_details.html', movie_jinja=movie_dict, user_logged_in=user_logged_in)

@app.route('/users', methods=["POST"])
def create_an_account():
    email = request.form.get('email')
    password = request.form.get('password')

    if crud.get_user_by_email(email):
        flash('This email already exists!')
    else:
        new_user = crud.create_user(email, password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account successfully created! You can now log in.')
    
    return render_template('homepage.html')

@app.route('/login', methods = ['POST'])
def authenticate_user():
    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)
    if not user:
        flash("Please create an account!")
    elif user.password != password:
        flash("That's not the correct password! Try again!")
    else:
        session['user_id'] = user.user_id
        print(user.user_id)
        flash('You are now logged in.')

    return redirect('/')

@app.route('/rate_movie', methods = ['POST'])
def rate_movie():
    movie_rating = request.form.get('movie_rating')
    movie_id = request.form.get('movie_id')
    user_id = session['user_id']

    new_rating = crud.create_rating(movie_rating, movie_id, user_id) 
    db.session.add(new_rating)
    db.session.commit() 
    flash('Thank you for rating this movie!')

    return redirect(f'/movies/{movie_id}') 




if __name__ == "__main__":
    connect_to_db(app) 
    app.run(host="0.0.0.0", debug=True, port=5001)
