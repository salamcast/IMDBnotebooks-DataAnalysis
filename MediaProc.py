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

    def find_video_df(self, match):
        return None

    def find_tv_df(self, match):
        return None

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
            "runtimeMinutes":"minutes"
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




    # Get DataFrame filtered to titleType in the IMDB dataset
    # some videos/movies might have a title type you might not expect, like video instead of movie
    def get_tvMiniSeries(self):
        return self.tbasics.loc[(self.tbasics['titleType'] == "tvMiniSeries")]

    def get_tvSpecial(self):
        return self.tbasics.loc[(self.tbasics['titleType'] == "tvSpecial")]

    def get_tvPilot(self):
        return self.tbasics.loc[(self.tbasics['titleType'] == "tvPilot")]

    def get_video(self):
        return self.tbasics.loc[(self.tbasics['titleType'] == "video")]

    def get_tvPilot(self):
        return self.tbasics.loc[(self.tbasics['titleType'] == "videoGame")]

    # movies
    def get_tvMovie(self):
        return self.tbasics.loc[(self.tbasics['titleType'] == "tvMovie")]

    def get_movie(self):
        return self.tbasics.loc[(self.tbasics['titleType'] == "movie")]

    # shorts
    def get_tvShort(self):
        return self.tbasics.loc[(self.tbasics['titleType'] == "tvShort")]

    def get_short(self):
        return self.tbasics.loc[(self.tbasics['titleType'] == "short")]
