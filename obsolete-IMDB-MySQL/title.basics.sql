CREATE DATABASE IF NOT EXISTS `IMDBmedia` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `IMDBmedia`;

DROP TABLE IF EXISTS `title.basics`;
CREATE TABLE `title.basics` (
  `tconst` varchar(12) NOT NULL,
  `titleType` varchar(15) NOT NULL,
  `primaryTitle` text NOT NULL,
  `originalTitle` text,
  `isAdult` tinyint(1) DEFAULT '0',
  `startYear` varchar(4) DEFAULT NULL,
  `endYear` varchar(4) DEFAULT '\\N',
  `runtimeMinutes` int(11) DEFAULT '0',
  `genres` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `title.basics`
  ADD PRIMARY KEY (`tconst`),
  ADD KEY `TitleYear` (`startYear`);
ALTER TABLE `title.basics` ADD FULLTEXT KEY `primaryTitle` (`primaryTitle`);
ALTER TABLE `title.basics` ADD FULLTEXT KEY `originalTitle` (`originalTitle`);

load data infile '/data/title.basics.tsv' 
    into table `title.basics` 
    fields terminated by '\t' 
    lines terminated by '\n' 
    ignore 1 rows;
