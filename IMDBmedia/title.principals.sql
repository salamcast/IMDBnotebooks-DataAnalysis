CREATE DATABASE IF NOT EXISTS `IMDBmedia` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `IMDBmedia`;

DROP TABLE IF EXISTS `title.principals`;
CREATE TABLE `title.principals` (
  `tconst` varchar(12) NOT NULL,
  `ordering` int(11) NOT NULL,
  `nconst` varchar(12) DEFAULT NULL,
  `category` varchar(256) DEFAULT NULL,
  `job` text,
  `characters` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE `title.principals`
  ADD KEY `TitleAct` (`tconst`,`nconst`),
  ADD KEY `PCategory` (`category`);


load data infile '/data/title.principals.tsv' 
    into table `title.principals` 
    fields terminated by '\t' 
    lines terminated by '\n' 
    ignore 1 rows;
