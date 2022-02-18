# IMDB Data Set structre: 

https://www.imdb.com/interfaces/

I wasn't able too import the gz file in mysql, i had to uncompress them first.  

### some files get very big!

* 1.4G	title.akas.tsv
* 676M	title.basics.tsv
* 256M	title.crew.tsv
* 150M	title.episode.tsv
* 2.0G	title.principals.tsv
* 20M	title.ratings.tsv
* 640M	name.basics.tsv

#### enable file import in my.cnf

This will solve the **“MySQL server is running with the –secure-file-priv”** Error

```
[mysqld]
secure-file-priv = ""
```

#### info on enabling file import on mysql server when you get errors: 

https://computingforgeeks.com/how-to-solve-mysql-server-is-running-with-the-secure-file-priv-error/

#### Info on importing CSV,TSV files into mysql tables

https://phoenixnap.com/kb/import-csv-file-into-mysql


# TV Series, mini Series and Radio Series

### Widget examples with year and media type

```
def search_tv_year(name, year, MediaType):
    sql = "SELECT tconst, primaryTitle, startYear, runtimeMinutes FROM `title.basics` WHERE primaryTitle LIKE '" + name + "' AND startYear = '" + str(year) + "' AND titleType = '" +  MediaType + "' ;"
    for x in search_db(sql):
        print(x)

print ("Search for TV Shows with start Year:")
interact_manual(search_tv_year, name='Blindspot%', year=widgets.IntSlider(min=1900, max=2022, step=1, value=2015), MediaType=[ "tvSeries", "tvMiniSeries", "radioSeries" ]);
```


### Search for Season and Episode numbers

#### Fields
* tconst, parentTconst, seasonNumber, episodeNumber

to query all the season and episode numbers for a TV Show, like bellow using the **tconst** id from the query above to pull the episode and season numbers using the **parentTconst**

```
SELECT * FROM `title.episode` WHERE parentTconst = 'tt4474344'
```

### Search for Episode Name and details

#### Fields
* tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres 

```
SELECT tconst, primaryTitle, startYear, runtimeMinutes FROM `title.basics` WHERE tconst = 'tt4843812' AND titleType = 'tvEpisode';
```

### Self Join Example widget of a list of TV Show Episodes

This gives a nice clean list of episode names with season and episode numbers in order.  I'm using aliases for the tables to it's less typing (and typos)

```
def get_TV_2Q(name, year):
    ID = 0
    sql ="SELECT tconst, primaryTitle FROM `title.basics` WHERE primaryTitle LIKE '" + name + "' AND ( titleType = 'tvSeries' OR titleType = 'tvMiniSeries' ) AND startYear = '" + str(year) + "';"
    for x in search_db(sql):
        ID=str(x[0])
        title=x[1]
        break
    if ID == 0:
        print( "Not found!")
    else:
        sql ="""
        SELECT B.tconst as ID, E.seasonNumber as S, E.episodeNumber as Ep, B.primaryTitle as title, B.startYear as year, B.runtimeMinutes as minutes  
            FROM `title.basics` B, `title.episode` E 
            WHERE B.tconst = E.tconst 
                AND B.titleType = 'tvEpisode' 
                AND E.parentTconst = '""" + ID + """' 
            Order by E.seasonNumber ASC, E.episodeNumber ASC;
"""
        print(title + " (" + str(year) + ")")
        for x in search_db(sql):
            print(x)

print ("Search for TV Show Episode List (2 queries):")

interact_manual(get_TV_2Q, name='Blindspot%', year=widgets.IntSlider(min=1900, max=2022, step=1, value=2015));        

```
