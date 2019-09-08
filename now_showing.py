#! python3
# now_showing.py - PART2 Task1: Parses now_showing.json to movies.db

import sys, os, json, uuid
from main import Movie as Movie
from main import get_movie as get_movie
from main import connect_db as connect_db
from main import create_movie_table as create_movie_table

pyPath = os.path.abspath(os.path.dirname(sys.argv[0]))
jsonSrc = os.path.join(pyPath, 'now_showing.json')

if __name__ == '__main__':
    conn, cursor = connect_db('movies.db')

    create_movie_table(conn, cursor) #if not exists

    if os.path.exists(jsonSrc):
        with open(jsonSrc) as jsonFile:
            jsonData = json.load(jsonFile)

    for amovie in jsonData['results']:
        newmovie = Movie(str(uuid.uuid1()),amovie['rating'],amovie.get('release_date',"Now Showing"),str(amovie['cast']),amovie['synopsis'],amovie['movie_title'],amovie['image_url'],amovie['id'],None)
        if newmovie.check_movie_exists(conn, cursor):
            print(str(newmovie) + " already exists in our database.")
        else:
            newmovie.insert_movie(conn, cursor)

    print("'now_showing.json' has been parsed to 'movies.db'")

    conn.close()