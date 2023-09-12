#!/usr/bin/python3

import mysql.connector
# widgets
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
# files
import os
import re

import shutil
import urllib.parse

global imdb 

global Root

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

def scan_dir(path, Dir):
    files = os.listdir(path)
    #base
    for n1 in files:
        if os.path.isdir(path + '/' + n1):
            Dir.append ( path + '/' + n1)
            Dir = scan_dir(path + '/' + n1, Dir)
    return Dir

def scan_files(path, Files):
    files = os.listdir(path)
    #base
    for n1 in files:
        if os.path.isfile(path + '/' + n1):
            Files.append (path + '/' + n1)
        elif os.path.isdir(path + '/' + n1):
            Files = scan_files(path + '/' + n1, Files)
    return Files


def search_db(sql, val = ()):
    mydb = mysql.connector.connect(host=imdb['host'], user=imdb['user'], password=imdb['pass'],database=imdb['dbname'])
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

def show_files(Dir, output=False):
    Files = []
    Files = scan_files(Dir, Files)
    Files.sort()
    Cast = {}
    for f in Files:

        show = get_show(Dir)
        year = get_year(Dir)
        fileBase=re.sub('\D*\([0-9]{4}\)', '', re.sub('.[mM][4Pp][4Vv]', '', os.path.basename(f)))
        E = re.findall(r'([1-9]|[1-9][0-9])', fileBase)
        key = E[0]+"x"+E[1]

        Cast[key] = {
            'show': show,
            'year': year,
            'S': E[0],
            'E': E[1],
            'file': f,
            'dir': Dir
        }
        if output:
            print(show + ", "+ year+ ", "+ E[0]+ ", "+ E[1]+", "+f+", "+Dir )
            #print(dirBase, ", ", E[0], ", ", E[1], ", ",  fileBase, ", ", f, ", ", Dir )
    return Cast

def scan_TV(TVCast):
    TV = []
    for t in TVCast:
        TV = scan_dir(t, TV)
    #TV.sort()
    return TV
    
def IMDBurl(ID):
    return "https://www.imdb.com/title/" + ID + "/"

def IMDBsearch_url(show):
    return "https://www.imdb.com/find?"+urllib.parse.urlencode({"q": show, "ref_":"nv_sr_sm" })

def IMDBname(ID):
    return "https://www.imdb.com/name/" + ID + "/"

def add_movie_match(ival):
    # insert row
    insert="""INSERT IGNORE INTO `movies_list` 
    ( `titleId`, `title`, `year`, `type`, `file`, `Dir`, `url` )
    VALUES (%s, %s, %s, %s, %s, %s, %s);
  """
    insert_db(insert, ival)

def install_movie_match(old, new, Dir):  
    os.makedirs(Dir, mode = 0o777, exist_ok = True)
    file = shutil.move(old,new)
    if file:
#        os.remove(old)
        return True

def check_imdb_man(show, year, file, MediaType):
    SDB=search_video_imdb(show, year, MediaType)
    PICK=[]
    for d in SDB:
        url = IMDBurl( d[0] )
        print("\n"+ d[0] +" "+ d[1] + " (" + str(d[2]) + ") - " + d[3] + "\n\t- " + url )
        val = "|".join(d)
        p = ( d[0], val+"|"+file )
        PICK.append(p)
    interact_manual(use_this_movie_match, match=PICK)


#match is a string, qurey + old file
# need to break with split
def use_this_movie_match(match):
    #print(match)
    d = match.split('|')
    url = IMDBurl(  d[0] )
    old = d[4]
    new = Root + "/" + d[3] + "/" + str(d[2]) + "/" + re.sub(':', ';', d[1]) + ".mp4"
    new_dir = Root + "/" + d[3] + "/" + str(d[2])
    ival=(d[0], d[1], d[2], d[3], new, new_dir, url)

    if install_movie_match(old, new, new_dir):
        add_movie_match(ival)
        #print("mkdir",new_dir)
        #print("mv",old,new)
        print("Added:",new)
        
def get_year(path):
    base = os.path.basename(path)
    S = re.split('\(', base)
    if len(S) > 1:
        year = re.sub(' ', '', re.sub('\)', '', re.sub('.[mM][Oo4Pp][4Vv]', '', S[1])))
        year = year.strip()
        return year
    return "1900"

def get_show(path):
    base = os.path.basename(path)
    S = re.split('\(', base)
    show = re.sub(';', ':', S[0], 1)
    show = show.strip()
    return show

        
def get_imdb_file_movie(Dir, MediaType):
    Files = []
    Files = scan_files(Dir, Files)
    Files.sort()
    Failed = []
    for x in Files:
        year = get_year(x)
        show = get_show(x)

        SDB=search_video_imdb(show, year, MediaType)
        records=len(SDB)
        #print(SDB,"\n",records,"\n",type(SDB))
        
        if records == 1:
            for d in SDB:
                url = IMDBurl( d[0] )
                print("\n"+d[1] + " (" + str(d[2]) + ") " + "\t-\t" + url + "\n")
                use_this_movie_match("|".join(d)+"|"+x)
                break
        elif records > 1:
            PICK=[]
            for d in SDB:
                url = IMDBurl( d[0] )
                print("\n"+ d[0] +" "+ d[1] + " (" + str(d[2]) + ") - " + d[3] + "\n\t- " + url )
                val = "|".join(d)
                p = ( d[0], val+"|"+x )
                PICK.append(p)
            interact_manual(use_this_movie_match, match=PICK)
        else:
            records = "0"
            
        if records == "0":
            Failed.append({'file': x, 'show' : show, 'year': year})

    for f in Failed:
        print(" => No record in the local Database")
        print("------------------------------------------------")
        print("Show:",f['show'],"\nYear:",f['year'])
        print(" -> skipped",f['file'],"\n - Check the IMDB query link bellow")
        print(IMDBsearch_url( f['show'] ) )
        LIST=media_type( 'list' )
        interact_manual(check_imdb_man, show=f['show'], year=f['year'], file=[ f['file'] ], MediaType=LIST)
        print("________________________________________________")
    
    
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



def search_title_basics(name, output=False):
    sql = "SELECT DISTINCT tconst, primaryTitle, startYear, originalTitle, titleType FROM `title.basics` WHERE (primaryTitle LIKE %s OR originalTitle LIKE %s);"
    val = (name, name)
    DATA=[]
    for x in search_db(sql, val):
        if output:
            print(x[1] + " (" + str(x[2]) + ") " + "\n\t - " + x[3] + "\n\t" + IMDBurl(x[0]) )
            print("\t"+x[4])

def search_title_basics_type(name, MediaType, output=False):
    sql = "SELECT DISTINCT tconst, primaryTitle, startYear, originalTitle, titleType FROM `title.basics` WHERE (primaryTitle LIKE %s OR originalTitle LIKE %s) AND titleType = %s;"
    val = (name, name, MediaType )
    DATA=[]
    for x in search_db(sql, val):
        if output:
            print(x[1] + " (" + str(x[2]) + ") " + "\n\t - " + x[3] + "\n\t" + IMDBurl(x[0]) + "\n")
        
        new = []
        new.append(x[0])
        new.append(x[1])
        new.append(x[2])
        new.append(x[3])
        DATA.append(new)
    return DATA            

def search_movie_year(name, year, MediaType, output=False):
    sql = "SELECT tconst, primaryTitle, startYear, originalTitle, titleType FROM `title.basics` WHERE (primaryTitle LIKE %s OR originalTitle LIKE %s) AND titleType = %s AND startYear = %s;"
    val = (name, name, MediaType, year)
    DATA=[]
    for x in search_db(sql, val):
        if output:
            print(x[1] + " (" + str(x[2]) + ") " + "\n\t - " + x[3] + "\n\t" + IMDBurl(x[0]) + "\n")
        
        new = []
        new.append(x[0])
        new.append(x[1])
        new.append(x[2])
        new.append(x[3])
        DATA.append(new)        
    
def get_imdb_dir_tv(Dir, output):

    show = get_show(Dir)
    year = get_year(Dir)
    DATA = {}

    sql ="""SELECT tconst, primaryTitle, startYear, originalTitle, titleType FROM `title.basics` 
                WHERE (primaryTitle LIKE %s OR originalTitle LIKE %s)
                AND (titleType = "tvSeries" OR titleType = "tvMiniSeries" OR titleType = "radioSeries")
                AND startYear = %s"""
    val=(show, show, year)
    SDB=search_db(sql, val)
    #print(SDB)
    
    for x in SDB:
        F = {}
        F['show'] = show
        F['year'] = year
        F['Dir'] = Dir
        if output:
            print(x[0] + " " + x[3] + " (" + str(x[4]) + ") " + "\n\t" + IMDBurl(x[0]) + "\n")
        else:
            F['ID'] = x[0]
            F['show'] = x[1]
            F['year'] = str(x[2])
            F['show_orig'] = x[3]
            F['url'] = IMDBurl(x[0])
            F['video_type'] = x[4]
        DATA[x[0]] = F 
            
    return DATA


# title.episode.tsv
# this table is basic, data only makes sence when joined with title.basic

def get_TV_name_year(name, year, MediaType, output=False):
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
    val=(name, name, MediaType, year)
    DATA={}
    for x in search_db(sql, val):
        key = str(x[1])+"x"+str(x[2])
        if output:
            print(key + " " + x[3] + " (" + str(x[4]) + ") " + "\n\t" + IMDBurl(x[0]) + "\n")

        new = { 
            'tconst': x[0],
            'S': x[1],
            'E': x[2],
            'title':x[3],
            'year': x[4],
            'minutes': x[5],
            'url': IMDBurl(x[0])
        }
        DATA[key] = new
    return DATA


def get_imdb_file_tv(Dir):
 
    show = get_show(Dir)
    year = get_year(Dir)
    F=show_files(Dir, False)
    
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
    SDB=search_db(sql, val)
    #print(SDB)
    for x in SDB:
        key = str(x[1])+"x"+str(x[2])
        #print(key + " " + x[3] + " (" + str(x[4]) + ") " + "\n\t" + IMDBurl(x[0]) + "\n")
        if len(F[key]) > 0:
            
            F[key]['ID'] = x[0]
            F[key]['Ep'] = x[3]
            F[key]['Ep_year'] = str(x[4])
            F[key]['Ep_orig'] = x[5]
            F[key]['Ep_min'] = x[6]
            F[key]['Ep_url'] = IMDBurl(x[0])
            F[key]['Ep_type'] = x[7]
            print(F[key])
