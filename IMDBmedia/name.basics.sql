CREATE DATABASE IF NOT EXISTS `IMDBmedia` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `IMDBmedia`;

DROP TABLE IF EXISTS `name.basics`;
CREATE TABLE `name.basics` (
  `nconst` varchar(12) NOT NULL,
  `primaryName` text NOT NULL,
  `birthYear` varchar(4) DEFAULT NULL,
  `deathYear` varchar(4) DEFAULT '\\N',
  `primaryProfession` text,
  `knownForTitles` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE `name.basics`
  ADD PRIMARY KEY (`nconst`),
  ADD KEY `ActBirth` (`birthYear`);
ALTER TABLE `name.basics` ADD FULLTEXT KEY `primaryName` (`primaryName`);

load data infile '/data/name.basics.tsv' 
    into table `name.basics` 
    fields terminated by '\t' 
    lines terminated by '\n' 
    ignore 1 rows;

