#!/usr/bin/python3
import pandas as pd
import mysql.connector

import urllib.parse

global imdb 

global DF

DF = False

imdb = {
    "host": False,
    "user": False,
    "pass": False,
    "dbname": False
} 


def media_type(Type):
    if Type == "movies":
        return ["movie", "video", "tvMovie", "tvSpecial" ]
    elif Type == "series":
        return [ "tvSeries", "tvMiniSeries", "radioSeries" ]
    return [ "ALL", "movie", "short", "video", "titleType", "tvMovie", "tvPilot", "tvShort", "tvSpecial","radioEpisode","radioSeries","tvEpisode", "tvMiniSeries","tvSeries", "videoGame" ]


def search_db(sql, val = ()):
    mydb = mysql.connector.connect(host=imdb['host'], user=imdb['user'], password=imdb['pass'],database=imdb['dbname'])
    if DF == True:
        result_dataFrame = pd.read_sql(sql,mydb,params=val)
        mydb.close()
        return result_dataFrame
    else:
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        return mycursor.fetchall()

def insert_db(sql, val = ()):
    mydb = mysql.connector.connect(host=imdb['host'], user=imdb['user'], password=imdb['pass'],database=imdb['dbname'])
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    return mycursor.rowcount
    
def IMDBurl(ID):
    return "https://www.imdb.com/title/" + ID + "/"

def IMDBsearch_url(show):
    return "https://www.imdb.com/find?"+urllib.parse.urlencode({"q": show, "ref_":"nv_sr_sm" })

def IMDBname(ID):
    return "https://www.imdb.com/name/" + ID + "/"
###########################################################
# Add movies_list
###########################################################
def add_movie_match(ival):
    # insert row
    insert="""INSERT IGNORE INTO `movies_list` 
    ( `titleId`, `title`, `year`, `type`, `file`, `Dir`, `url` )
    VALUES (%s, %s, %s, %s, %s, %s, %s);
  """
    return insert_db(insert, ival)
###########################################################
# Update movies_list
###########################################################
def update_movie_list(new_dir, new_file, old_file):
    update = """UPDATE movies_list SET 
        Dir = %s, file = %s
    WHERE file = %s"""
    uval = (new_dir, new_file, old_file)
    return insert_db(update, uval)
###########################################################
# movies_list
###########################################################
def search_movie_list_dir_type(Dir, MediaType):
    sql="""
SELECT file 
FROM movies_list ML
WHERE 
    ML.file Like %s AND
    ML.`type` = %s 
"""
    val=(Dir+'/%',MediaType)
    return search_db(sql, val)

##############################################################################################################
# basic.title.tsv SQL functions
##############################################################################################################

def search_video_imdb(show, year, MediaType):
    if MediaType == "ALL":
        sql ="""SELECT B.tconst as ID, 
            B.primaryTitle as title, B.startYear as year, B.titleType as video_type  
        FROM `title.basics` B 
        WHERE (primaryTitle LIKE %s OR originalTitle LIKE %s)
            AND ( titleType = "movie" OR  titleType = "tvMovie" 
                OR titleType = "tvPilot" OR titleType = "tvSpecial"
                OR titleType = "video"  
                OR titleType = "short" OR titleType = "tvShort"
                )
            AND startYear = %s ;"""
    elif MediaType == "tvEpisode":
        #tvEpisode
        sql ="""SELECT B.tconst as ID, 
            B.primaryTitle as title, B.startYear as year, B.titleType as video_type  
        FROM `title.basics` B 
        WHERE (primaryTitle LIKE %s OR originalTitle LIKE %s)
            AND startYear = %s 
            AND titleType = "tvEpisode" ;""" 
    else:
        sql ="""SELECT B.tconst as ID, 
            B.primaryTitle as title, B.startYear as year, B.titleType as video_type  
        FROM `title.basics` B 
        WHERE (primaryTitle LIKE %s OR originalTitle LIKE %s)
            AND startYear = %s 
            AND titleType = %s ;"""
    if MediaType == "ALL":
        val=(show, show, year)
    else:
        val=(show, show, year, MediaType)
    return search_db(sql, val)



def search_title_basics(name):
    sql = "SELECT DISTINCT tconst, primaryTitle, startYear, originalTitle, titleType FROM `title.basics` WHERE (primaryTitle LIKE %s OR originalTitle LIKE %s);"
    val = (name, name)
    return search_db(sql, val)

def search_title_basics_type(name, MediaType):
    sql = "SELECT DISTINCT tconst, primaryTitle, startYear, originalTitle, titleType FROM `title.basics` WHERE (primaryTitle LIKE %s OR originalTitle LIKE %s) AND titleType = %s;"
    val = (name, name, MediaType )
    return search_db(sql, val)

def search_movie_year(name, year, MediaType):
    sql = "SELECT tconst, primaryTitle, startYear, originalTitle, titleType FROM `title.basics` WHERE (primaryTitle LIKE %s OR originalTitle LIKE %s) AND titleType = %s AND startYear = %s;"
    val = (name, name, MediaType, year)
    return search_db(sql, val)

    
def get_imdb_dir_tv(show, year):
    sql ="""SELECT tconst, primaryTitle, startYear, originalTitle, titleType FROM `title.basics` 
                WHERE (primaryTitle LIKE %s OR originalTitle LIKE %s)
                AND (titleType = "tvSeries" OR titleType = "tvMiniSeries" OR titleType = "radioSeries")
                AND startYear = %s"""
    val=(show, show, year)
    return search_db(sql, val)


# title.episode.tsv
# this table is basic, data only makes sence when joined with title.basic

def get_tv_name_year_type(show, year, MediaType):
    sql ="""
    SELECT B.tconst as ID, E.seasonNumber as S, E.episodeNumber as Ep, B.primaryTitle as title, B.startYear as year, B.runtimeMinutes as minutes  
        FROM `title.basics` B, `title.episode` E 
        WHERE B.tconst = E.tconst 
            AND E.parentTconst IN (SELECT tconst FROM `title.basics` 
                WHERE (primaryTitle LIKE %s OR originalTitle LIKE %s)
                AND  titleType = %s 
                AND startYear = %s
            ) 
        Order by E.seasonNumber ASC, E.episodeNumber ASC;
"""
    val=(show, show, MediaType, year)
    return search_db(sql, val)


def get_tv_name_year(show, year):
    sql ="""SELECT B.tconst as ID, 
    E.seasonNumber as S, E.episodeNumber as Ep, 
    B.primaryTitle as title, B.startYear as year, B.originalTitle as org_title, 
    B.runtimeMinutes as minutes, B.titleType as video_type  
        FROM `title.basics` B, `title.episode` E 
        WHERE B.tconst = E.tconst 
            AND E.parentTconst IN (SELECT tconst FROM `title.basics` 
                WHERE (primaryTitle LIKE %s OR originalTitle LIKE %s)
                AND startYear = %s
            ) 
        Order by E.seasonNumber ASC, E.episodeNumber ASC;"""
    val=(show, show, year)
    return search_db(sql, val)

def get_tv_id(ID):
    sql ="""SELECT B.tconst as ID, 
    E.seasonNumber as S, E.episodeNumber as Ep, 
    B.primaryTitle as title, B.startYear as year, B.originalTitle as org_title, 
    B.runtimeMinutes as minutes, B.titleType as video_type, IMDBurl(B.tconst) as imdb_link
        FROM `title.basics` B, `title.episode` E 
        WHERE B.tconst = E.tconst AND E.parentTconst = %s
        Order by E.seasonNumber ASC, E.episodeNumber ASC;"""
    val=(ID,)
    return search_db(sql, val)
