CREATE DATABASE IF NOT EXISTS `IMDBmedia` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `IMDBmedia`;

DROP TABLE IF EXISTS `title.episode`;
CREATE TABLE `title.episode` (
  `tconst` varchar(12) NOT NULL,
  `parentTconst` varchar(12) DEFAULT NULL,
  `seasonNumber` int(11) DEFAULT '1',
  `episodeNumber` int(11) DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `title.episode`
  ADD KEY `TVEp` (`tconst`),
  ADD KEY `TVShow` (`parentTconst`),
  ADD KEY `SeasonEp` (`seasonNumber`,`episodeNumber`);
  


load data infile '/data/title.episode.tsv' 
    into table `title.episode` 
    fields terminated by '\t' 
    lines terminated by '\n' 
    ignore 1 rows;