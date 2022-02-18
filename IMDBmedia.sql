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

DROP TABLE IF EXISTS `name.basics`;
CREATE TABLE `name.basics` (
  `nconst` varchar(12) NOT NULL,
  `primaryName` text NOT NULL,
  `birthYear` varchar(4) DEFAULT NULL,
  `deathYear` varchar(4) DEFAULT '\\N',
  `primaryProfession` text,
  `knownForTitles` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `series_list`;
CREATE TABLE `series_list` (
  `titleId` varchar(12) NOT NULL,
  `show` text NOT NULL,
  `title` text NOT NULL,
  `year` varchar(4) DEFAULT NULL,
  `S` int(11) DEFAULT '0',
  `E` int(11) DEFAULT '0',
  `type` varchar(20) DEFAULT 'Video',
  `file` text NOT NULL,
  `Dir` text NOT NULL,
  `url` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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

DROP TABLE IF EXISTS `title.crew`;
CREATE TABLE `title.crew` (
  `tconst` varchar(12) NOT NULL,
  `directors` text,
  `writers` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `title.episode`;
CREATE TABLE `title.episode` (
  `tconst` varchar(12) NOT NULL,
  `parentTconst` varchar(12) DEFAULT NULL,
  `seasonNumber` int(11) DEFAULT '1',
  `episodeNumber` int(11) DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `title.principals`;
CREATE TABLE `title.principals` (
  `tconst` varchar(12) NOT NULL,
  `ordering` int(11) NOT NULL,
  `nconst` varchar(12) DEFAULT NULL,
  `category` varchar(256) DEFAULT NULL,
  `job` text,
  `characters` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `title.ratings`;
CREATE TABLE `title.ratings` (
  `tconst` varchar(12) NOT NULL,
  `averageRating` float DEFAULT NULL,
  `numVotes` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE `movies_list`
  ADD PRIMARY KEY (`titleId`),
  ADD KEY `MovieYear` (`year`),
  ADD KEY `VideoType` (`type`);
ALTER TABLE `movies_list` ADD FULLTEXT KEY `title` (`title`);
ALTER TABLE `movies_list` ADD FULLTEXT KEY `file` (`file`);
ALTER TABLE `movies_list` ADD FULLTEXT KEY `Dir` (`Dir`);
ALTER TABLE `movies_list` ADD FULLTEXT KEY `url` (`url`);

ALTER TABLE `name.basics`
  ADD PRIMARY KEY (`nconst`),
  ADD KEY `ActBirth` (`birthYear`);
ALTER TABLE `name.basics` ADD FULLTEXT KEY `primaryName` (`primaryName`);

ALTER TABLE `series_list`
  ADD PRIMARY KEY (`titleId`),
  ADD KEY `EpYear` (`year`),
  ADD KEY `SxEp` (`S`,`E`);
ALTER TABLE `series_list` ADD FULLTEXT KEY `show` (`show`);
ALTER TABLE `series_list` ADD FULLTEXT KEY `title` (`title`);
ALTER TABLE `series_list` ADD FULLTEXT KEY `file` (`file`);
ALTER TABLE `series_list` ADD FULLTEXT KEY `Dir` (`Dir`);
ALTER TABLE `series_list` ADD FULLTEXT KEY `url` (`url`);

ALTER TABLE `title.akas`
  ADD KEY `TitleIDakas` (`titleId`);
ALTER TABLE `title.akas` ADD FULLTEXT KEY `title` (`title`);

ALTER TABLE `title.basics`
  ADD PRIMARY KEY (`tconst`),
  ADD KEY `TitleYear` (`startYear`);
ALTER TABLE `title.basics` ADD FULLTEXT KEY `primaryTitle` (`primaryTitle`);
ALTER TABLE `title.basics` ADD FULLTEXT KEY `originalTitle` (`originalTitle`);

ALTER TABLE `title.crew`
  ADD KEY `CrewID` (`tconst`);

ALTER TABLE `title.episode`
  ADD KEY `TVEp` (`tconst`),
  ADD KEY `TVShow` (`parentTconst`),
  ADD KEY `SeasonEp` (`seasonNumber`,`episodeNumber`);

ALTER TABLE `title.principals`
  ADD KEY `TitleAct` (`tconst`,`nconst`),
  ADD KEY `PCategory` (`category`);

ALTER TABLE `title.ratings`
  ADD KEY `rateID` (`tconst`);

