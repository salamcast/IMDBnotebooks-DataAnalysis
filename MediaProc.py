import os
import re
import pandas as pd
import numpy as np


# plot videos
def MovieAvgRating(DF, fig=(15, 10)):
    return DF.plot.line(
        x='primaryTitle',
        y=['averageRating', 'numVotes'],
        secondary_y='numVotes',
        #        stacked=True ,
        rot=90,
        figsize=fig,
        xticks=range(0, DF['primaryTitle'].count()),

    )


def MovieRuntime(DF, fig=(15, 10)):
    return DF.plot.line(
        x='primaryTitle',
        y=['minutes', 'averageRating'],
        secondary_y='averageRating',
        rot=90,
        figsize=fig,
        xticks=range(0, DF['primaryTitle'].count())
    )


def MovieHexBin(DF, fig=(15, 10), title="Movies hexbin"):
    DF.plot.hexbin(
        C='minutes',
        y='averageRating',
        x='numVotes',
        # reduce_C_function=np.sum,
        gridsize=10,
        cmap="viridis",
        title=title,
        figsize=fig
    )


# TV Shows
def group_tvshows(df):
    ep = df.groupby('TVShow').E.count()
    mins = df.groupby('TVShow').minutes.sum()
    rate = df.groupby('TVShow').averageRating.sum()
    votes = df.groupby('TVShow').numVotes.sum()
    enum = pd.DataFrame(ep)
    enum['minutes'] = mins
    enum['averageRating'] = rate / enum['E']
    enum['numVotes'] = votes
    enum = enum.sort_values(by="averageRating").reset_index()

    return enum
# TV Shows
def group_tvshows_season(df):
    ep = df.groupby('S').E.count()
    mins = df.groupby('S').minutes.sum()
    rate = df.groupby('S').averageRating.sum()
    votes = df.groupby('S').numVotes.sum()
    enum = pd.DataFrame(ep)
    enum['minutes'] = mins
    enum['averageRating'] = rate / enum['E']
    enum['numVotes'] = votes
    enum = enum.sort_values(by="averageRating").reset_index()

    return enum


def TVShowAvgRating(DF, fig=(15, 10), x='Episode'):
    return DF.plot.line(
        x=x,
        y=['averageRating', 'numVotes'],
        secondary_y='numVotes',
        #        stacked=True ,
        rot=90,
        figsize=fig,
        xticks=range(0, DF['E'].count()),
        fontsize=10.0,
        xlabel=x,
        #        ylabel=[ 'averageRating', 'numVotes' ]

    )


def TVShowRuntime(DF, fig=(15, 10), x='Episode'):
    return DF.plot.line(
        x=x,
        y=['minutes', 'averageRating'],
        secondary_y='averageRating',
        rot=90,
        figsize=fig,
        xticks=range(0, DF['E'].count()),
        fontsize=10.0,
        xlabel=x,
        #        ylabel='minutes'
    )


def TVShowHexBin(DF, fig=(15, 10), title="TVShow hexbin", c='minutes', y='averageRating', x='numVotes'):
    DF.plot.hexbin(
        C=c,
        y=y,
        x=x,
        reduce_C_function=np.sum,
        gridsize=10,
        cmap="viridis",
        title=title,
        figsize=fig,
        xlabel=x,
        ylabel=y,

    )


class IMDB:
    def __init__(self, tbasic, ratings):
        basics = pd.read_csv(tbasic, sep='\t', low_memory=False)
        ratings = pd.read_csv(ratings, sep='\t')
        self.tbasics = basics.join(ratings.set_index('tconst'), on="tconst").replace('\\N', np.nan)
        self.genres = []
        self.Videos = None
        self.TVShow = None

    def find_video(self, col, match):
        return self.Videos[col].str.contains(match).sum()

    def find_tv(self, col, match):
        return self.TVShow[col].str.contains(match).sum()

    def titleTypeCount(self):
        return self.tbasics.groupby(['titleType']).titleType.count()

    def genres_imdb(self):
        if self.TVShow is not None:
            return self.TVShow.groupby(['genres']).titleType.count()
        elif self.Videos is not None:
            return self.Videos.groupby(['genres']).titleType.count()
        else:
            return self.tbasics.groupby(['genres']).titleType.count()

    # returns a count of each genre found
    def set_genres(self):
        cg = {}
        # reset
        self.genres = []
        if self.TVShow is not None:
            data = self.TVShow.genres.dropna()
        elif self.Videos is not None:
            data = self.Videos.genres.dropna()
        else:
            data = self.tbasics.genres.dropna()
        for x in data:
            for g in self.process_genres(x):
                if g not in self.genres:
                    self.genres.append(g)
                    cg[g] = 1
                else:
                    cg[g] = cg[g] + 1
        return cg

    def process_genres(self, g):
        return str(g).split(',')

    # Filter out the TV shows and episodes.

    def filter_tv(self):
        self.Videos = self.tbasics.loc[
            (self.tbasics['titleType'] != "tvSeries") & (self.tbasics['titleType'] != "tvEpisode")
            ].rename(columns={
            "startYear": "year",
            "runtimeMinutes": "minutes"
        }).drop(["endYear"], axis=1)

    def set_tvshows(self, episodes):
        # set \\N to zero hear since some TV databases have shows with season 0 and episode 0 for some specials
        e = pd.read_csv(episodes, sep='\t').rename(columns={
            "seasonNumber": "S",
            "episodeNumber": "E"
        }).replace('\\N', 0)

        self.TVShow = e.join(self.tbasics.drop([
            'isAdult',
            'runtimeMinutes',
            'genres',
            'titleType',
            'averageRating',
            'numVotes'
        ], axis=1).rename(columns={
            "tconst": "parentTconst",
            "primaryTitle": "TVShow"
        }).set_index('parentTconst'), on="parentTconst").join(self.tbasics.drop([
            "endYear"
        ], axis=1).rename(columns={
            "primaryTitle": "episodeTitle",
            "originalTitle": "originalEpisode",
            "startYear": "year",
            "runtimeMinutes": "minutes"
        }).set_index('tconst'), on="tconst").drop([
            'parentTconst'
        ], axis=1)
        self.filter_tv()

    def search_video_df(self, search, ttype='movie', votes=100000):
        df = self.Videos.loc[
            self.Videos["primaryTitle"].str.contains(search) &
            (self.Videos['titleType'] == ttype) &
            (self.Videos['numVotes'] > votes)
            ].dropna().drop(columns=['titleType', 'originalTitle', 'isAdult']).sort_values(by='year')
        df['minutes'] = df['minutes'].astype('int64', errors='ignore')
        df['year'] = df['year'].astype('int64', errors='ignore')
        return df

    def search_tvshow_df(self, search, votes=100):
        df = self.TVShow.loc[
            (self.TVShow.numVotes > votes) &
            self.TVShow["TVShow"].str.contains(search, regex=True)
            ].drop(columns=[
            'titleType', 'originalTitle', 'isAdult',
            "year", "originalEpisode", "genres", "endYear"
        ]).sort_values(by='startYear').dropna()
        df['startYear'] = df['startYear'].astype('int64', errors='ignore')
        df['minutes'] = df['minutes'].astype('int64', errors='ignore')
        df['episodeTitle'] = df['S'].astype('str') + 'x' + df['E'].astype('str') + ' ' + df['episodeTitle']
        df['S'] = df['S'].astype('int64', errors='ignore')
        df['E'] = df['E'].astype('int64', errors='ignore')
        return df
