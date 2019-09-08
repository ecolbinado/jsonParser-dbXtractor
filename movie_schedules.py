#! python3
# movie_schedules.py - PART2 Task5: Creates/updates movies_schedules.json following required list and format. 
# Needs 2 arguments to run, 1st argument is the movie_id (not uuid), 2nd argument is the date (mm/dd/yyyy).
# For example; to run this script on your terminal, "python3 movie_schedules.py 8595 10/18/2017"

import sys, os, json, datetime
from main import Schedule as Schedule
from main import connect_db as connect_db

if __name__ == '__main__':
    conn, cursor = connect_db('movies.db')

    movie_id = sys.argv[1]
    showdate = sys.argv[2] #in 'mm/dd/yyyy' format

    jsondict = {}
    jsondict['results']=[]

    with conn:
        cursor.execute ("SELECT DISTINCT schedules.theater_code FROM schedules LEFT JOIN movies ON schedules.movie_id = movies.id WHERE movies.id = (?) AND schedules.screening LIKE (?)",(movie_id,'%'+showdate+'%'))
        rows = cursor.fetchall()
        theatrcodes = []
        for row in rows:
            theatrcodes.append(row[0])
        
        for code in theatrcodes:
            starttimes = []    
            cursor.execute ("SELECT schedules.uuid, schedules.cinema_code, movies.uuid, schedules.price, schedules.seat_type, schedules.screening, schedules.theater_code, schedules.variant FROM schedules LEFT JOIN movies ON schedules.movie_id = movies.id WHERE movies.id = (?) AND schedules.screening LIKE (?) AND schedules.theater_code = (?)",(movie_id,'%'+showdate+'%',code))
            rows = cursor.fetchall()
            for row in rows:
                starttimes.append(datetime.datetime.strptime(row[5],'%m/%d/%Y %I:%M:%S %p').strftime('%H:%M'))
            row = rows[0]
            startdate = datetime.datetime.strptime(row[5],'%m/%d/%Y %I:%M:%S %p').strftime('%d %b %Y')
            jsondict['results'].append({'id':row[0],'schedule':{'cinema':row[1],'movie':row[2],'price':row[3],'seating_type':row[4],'show_date':startdate,'start_times':starttimes,'theater':row[6],'variant':row[7]}})

    with open('movie_schedules.json', 'w') as f:
        json.dump(jsondict, f, indent=2)

    print("'movie_schedules.json' has been created/updated.")