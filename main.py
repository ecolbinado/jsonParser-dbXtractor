#! python3
# Main.py

import sys, os, json, sqlite3

class Movie:

    def __init__(self, uuid, rating, release_date, cast, synopsis, movie_title, image_url, id, variant):
        self.uuid = uuid
        self.rating = rating
        self.release_date = release_date
        self.cast = cast
        self.synopsis = synopsis
        self.movie_title = movie_title
        self.image_url = image_url
        self.id = id
        self.variant = variant
        self.entities = (uuid, rating, release_date, cast, synopsis, movie_title, image_url, id, variant)
    
    def __str__(self):
        return self.id + ': ' + self.movie_title

    def insert_movie(self, conn, cursor):
        with conn:
            cursor.execute("""INSERT INTO movies(uuid, rating, release_date, cast, synopsis, movie_title, image_url, id, variant) VALUES(?,?,?,?,?,?,?,?,?)""",(self.entities))


    def check_movie_exists(self, conn, cursor):
        with conn:
            cursor.execute("SELECT id FROM movies WHERE id = (?)",(self.id,))
        rows = cursor.fetchall()
        if len(rows):
            return True
        else:
            return False 

    def update_release_date(self, conn, cursor):
        with conn:
            cursor.execute("UPDATE movies SET release_date = (?) WHERE id = (?)",(self.release_date, self.id))

    def update_movie():
        pass

    def remove_movie():
        pass

class Schedule:

    def __init__(self, uuid, cinema_code, movie_id, theater_code, price, variant, cinema_name, movie_title, screening, seat_type, id):
        self.uuid = uuid
        self.cinema_code = cinema_code
        self.movie_id = movie_id
        self.theater_code = theater_code
        self.price = price
        self.variant = variant
        self.cinema_name = cinema_name
        self.movie_title = movie_title
        self.screening = screening
        self.seat_type = seat_type
        self.id = id
        self.entities = (uuid, cinema_code, movie_id, theater_code, price, variant, cinema_name, movie_title, screening, seat_type, id)
    
    def __str__(self):
        return self.id + ': ' + self.movie_title + 'screening at ' + self.screening 

    def check_sched_exists(self, conn, cursor):
        with conn:
            cursor.execute("SELECT id FROM schedules WHERE id = (?)",(self.id,))
        rows = cursor.fetchall()
        if len(rows):
            return True
        else:
            return False 
    
    def insert_schedule(self, conn, cursor):
        with conn:
            cursor.execute("""INSERT INTO schedules(uuid, cinema_code, movie_id, theater_code, price, variant, cinema_name, movie_title, screening, seat_type, id) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",(self.entities))
    
# Functions        
def get_movie(conn, cursor):
    with conn:
        cursor.execute("SELECT * FROM movies")
    rows = cursor.fetchall()
    for row in rows:
        movie_db = Movie(*row)
        print(movie_db.entities)

def connect_db(database):
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as error:
        print("Error in connecting to sqlite3", error)

def create_movie_table(conn, cursor):
    cursor.execute("""CREATE TABLE if not exists movies (
                    uuid text PRIMARY KEY,
                    rating text,
                    release_date text,
                    cast blob,
                    synopsis text,
                    movie_title text,
                    image_url text,
                    id integer,
                    variant text
                    )""")
    conn.commit()

def create_sched_table(conn, cursor):
    cursor.execute("""CREATE TABLE if not exists schedules (
                    uuid text PRIMARY KEY,
                    cinema_code text,
                    movie_id text,
                    theater_code text,
                    price text,
                    variant text,
                    cinema_name text,
                    movie_title text,
                    screening text,
                    seat_type text,
                    id text
                    )""")
    conn.commit()