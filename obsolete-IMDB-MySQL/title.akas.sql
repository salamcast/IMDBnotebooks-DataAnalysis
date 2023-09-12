CREATE DATABASE IF NOT EXISTS `IMDBmedia` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `IMDBmedia`;

DROP TABLE IF EXISTS `title.akas`;
CREATE TABLE `title.akas` (
  `titleId` varchar(12) NOT NULL,
  `ordering` int(11) NOT NULL,
  `title` text NOT NULL,
  `region` varchar(4) DEFAULT NULL,
  `language` varchar(4) DEFAULT NULL,
  `types` varchar(45) DEFAULT NULL,
  `attributes` varchar(128) DEFAULT NULL,
  `isOriginalTitle` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `title.akas`
  ADD KEY `TitleIDakas` (`titleId`);
ALTER TABLE `title.akas` ADD FULLTEXT KEY `title` (`title`);

load data infile '/data/title.akas.tsv' 
    into table `title.akas` 
    fields terminated by '\t' 
    lines terminated by '\n' 
    ignore 1 rows;