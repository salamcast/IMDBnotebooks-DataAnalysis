CREATE DATABASE IF NOT EXISTS `IMDBmedia` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `IMDBmedia`;

DROP TABLE IF EXISTS `title.crew`;
CREATE TABLE `title.crew` (
  `tconst` varchar(12) NOT NULL,
  `directors` text,
  `writers` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `title.crew`
  ADD KEY `CrewID` (`tconst`);

load data infile '/data/title.crew.tsv' 
    into table `title.crew` 
    fields terminated by '\t' 
    lines terminated by '\n' 
    ignore 1 rows;