CREATE DATABASE IF NOT EXISTS `IMDBmedia` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `IMDBmedia`;

DROP TABLE IF EXISTS `movies_list`;
CREATE TABLE `movies_list` (
  `titleId` varchar(12) NOT NULL,
  `title` text NOT NULL,
  `year` varchar(4) DEFAULT NULL,
  `type` varchar(20) DEFAULT 'Video',
  `file` text NOT NULL,
  `Dir` text NOT NULL,
  `url` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `movies_list`
  ADD PRIMARY KEY (`titleId`),
  ADD KEY `MovieYear` (`year`),
  ADD KEY `VideoType` (`type`);
ALTER TABLE `movies_list` ADD FULLTEXT KEY `title` (`title`);
ALTER TABLE `movies_list` ADD FULLTEXT KEY `file` (`file`);
ALTER TABLE `movies_list` ADD FULLTEXT KEY `Dir` (`Dir`);
ALTER TABLE `movies_list` ADD FULLTEXT KEY `url` (`url`);

--- custom tables ---
load data infile '/export/obsolete-IMDB-MySQL/movies_list.csv'
    into table `movies_list` 
    fields terminated by ',' 
    optionally enclosed by '"'
    escaped by '"'
    lines terminated by '\n' 
    ignore 1 rows;

--- Make views ---

-- Rating based views --
-- Bad Movies --
CREATE VIEW bad_movies_list
AS 
SELECT titleId, title, averageRating, numVotes, `year`, file 
FROM  movies_list ML, `title.ratings` R 
WHERE R.tconst = ML.titleId AND R.averageRating < 5
Order by R.averageRating;

-- Average Movies --

CREATE VIEW average_movies_list
AS 
SELECT titleId, title, averageRating, numVotes, `year`, file 
FROM  movies_list ML, `title.ratings` R 
WHERE R.tconst = ML.titleId 
    AND R.averageRating >= 5 AND R.averageRating < 7.0
Order by R.averageRating;

-- Above Average Movies --

CREATE VIEW good_movies_list
AS 
SELECT titleId, title, averageRating, numVotes, `year`, file 
FROM  movies_list ML, `title.ratings` R 
WHERE R.tconst = ML.titleId 
    AND R.averageRating >= 7 AND R.averageRating < 8.0
Order by R.averageRating;

-- Great Movies --

CREATE VIEW great_movies_list
AS 
SELECT titleId, title, averageRating, numVotes, `year`, file 
FROM  movies_list ML, `title.ratings` R 
WHERE R.tconst = ML.titleId 
    AND R.averageRating >= 8
Order by R.averageRating;


--- Custom Functions ---
CREATE FUNCTION `IMDBurl` (
    tconst VARCHAR(12)
)
RETURNS TEXT
BEGIN
    DECLARE url TEXT;
    SET url = concat("https://www.imdb.com/title/", tconst, "/");
RETURN url;
END

CREATE FUNCTION `IMDBname` (
    nconst VARCHAR(12)
)
RETURNS TEXT
BEGIN
    DECLARE url TEXT;
    SET url = concat("https://www.imdb.com/name/", nconst, "/");
RETURN url;
END
