#! python3
# movies.py - PART2 Task4: Creates/updates movies.json following required list and format.

import sys, os, json, re
from main import Movie as Movie
from main import connect_db as connect_db

if __name__ == '__main__':
    conn, cursor = connect_db('movies.db')

    with conn:
        cursor.execute("SELECT DISTINCT movies.movie_title, movies.id FROM movies LEFT JOIN schedules ON movies.id = schedules.movie_id WHERE schedules.variant IS NOT NULL")
        variantlist = cursor.fetchall()        
        cursor.execute("SELECT DISTINCT movies.movie_title, movies.uuid, movies.rating, movies.cast, movies.image_url, movies.release_date, movies.synopsis, schedules.variant, movies.id FROM movies LEFT JOIN schedules ON movies.id = schedules.movie_id WHERE schedules.variant IS NULL")
        rows = cursor.fetchall()
    
    #There are 3 movie variants: regular(null), 3D/4DX, & ATMOS. Let's track 3D/4DX & ATMOS only.
    dx_variants = []
    atmos_variants = []    
    for eachvariant in variantlist:       
        dxvariant_regex = re.compile(r'(?<=\(3D/4DX\)\s).*')
        mo_dx = dxvariant_regex.search(eachvariant[0])
        dx_variants.append(None if mo_dx == None else mo_dx.group())
        mo_atmos = re.compile(r'(?<=\(ATMOS\)\s).*').search(eachvariant[0])
        atmos_variants.append(None if mo_atmos == None else mo_atmos.group())

    jsondict = {}
    jsondict['results']=[]   
    for row in rows:
        movie_db = Movie(row[1],row[2],row[5],row[3],row[6],row[0],row[4],row[8],row[7])
        mov_variant = []
        if movie_db.movie_title in dx_variants: mov_variant.append("3D/4DX")
        if movie_db.movie_title in atmos_variants: mov_variant.append("ATMOS")
        jsondict['results'].append({'id':movie_db.uuid,'movie':{'advisory_rating':movie_db.rating,'canonical_title':movie_db.movie_title,'cast':movie_db.cast,'poster_portrait':movie_db.image_url,'release_date':movie_db.release_date,'synopsis':movie_db.synopsis,'variants':mov_variant}})
     
    with open('movies.json', 'w') as f:
        json.dump(jsondict, f, indent=2)

    print("'movies.json' has been created/updated.")