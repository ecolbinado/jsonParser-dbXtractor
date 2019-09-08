#! python3
# schedules.py - PART2 Task3: Parses schedules.json to movies.db

import sys, os, json, uuid
from main import Schedule as Schedule
from main import connect_db as connect_db
from main import create_sched_table as create_sched_table

pyPath = os.path.abspath(os.path.dirname(sys.argv[0]))
jsonSrc = os.path.join(pyPath, 'schedules.json')

if __name__ == '__main__':
    conn, cursor = connect_db('movies.db')

    create_sched_table(conn, cursor) #if not exists

    if os.path.exists(jsonSrc):
        with open(jsonSrc) as jsonFile:
            jsonData = json.load(jsonFile)

    for schedule in jsonData['result']:
        newsched = Schedule(str(uuid.uuid1()),schedule['cinema_code'],schedule['movie_id'],schedule['theater_code'],schedule['price'],None if schedule['variant']=='' else schedule['variant'],schedule['cinema_name'],schedule['movie_title'],schedule['screening'],schedule['seat_type'],schedule['id'])
        if newsched.check_sched_exists(conn, cursor):
            print(str(newsched) + " already exists in our database.")
        else:
            newsched.insert_schedule(conn, cursor)

    print("'schedules.json' has been parsed to 'schedules.db'")
    conn.close()