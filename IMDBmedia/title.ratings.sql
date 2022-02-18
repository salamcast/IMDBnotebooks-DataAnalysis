CREATE DATABASE IF NOT EXISTS `IMDBmedia` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `IMDBmedia`;

DROP TABLE IF EXISTS `title.ratings`;
CREATE TABLE `title.ratings` (
  `tconst` varchar(12) NOT NULL,
  `averageRating` float DEFAULT NULL,
  `numVotes` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE `title.ratings`
  ADD KEY `rateID` (`tconst`);


load data infile '/data/title.ratings.tsv' 
    into table `title.ratings` 
    fields terminated by '\t' 
    lines terminated by '\n' 
    ignore 1 rows;

