import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server


os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read()) 

print(type(movie_data))

movie_objects = []
for m in movie_data:
    rel_date = datetime.strptime(m['release_date'], "%Y-%m-%d") 
    movie = crud.create_movie(m['title'], m['overview'], rel_date, m['poster_path'])
    movie_objects.append(movie)

model.db.session.add_all(movie_objects)
model.db.session.commit()