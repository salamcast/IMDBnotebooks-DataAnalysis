CREATE DATABASE IF NOT EXISTS `IMDBmedia` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `IMDBmedia`;

DROP TABLE IF EXISTS `series_list`;
CREATE TABLE `series_list` (
  `titleId` varchar(12) NOT NULL,
  `showId` VARCHAR(12) NOT NULL,
  `show` text NOT NULL,
  `title` text NOT NULL,
  `year` varchar(4) DEFAULT NULL,
  `showYear` VARCHAR(4) DEFAULT NULL,
  `S` int(11) DEFAULT '0',
  `E` int(11) DEFAULT '0',
  `type` varchar(20) DEFAULT 'Video',
  `showType` VARCHAR(20) DEFAULT 'tvSeries',
  `file` text NOT NULL,
  `Dir` text NOT NULL,
  `url` text NOT NULL,
  `showUrl` TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `series_list`
  ADD PRIMARY KEY (`titleId`),
  ADD KEY `EpYear` (`year`),
  ADD KEY `SxEp` (`S`,`E`),
  ADD KEY `showId` (`showId`),
  ADD KEY `showYear` (`showYear`);

ALTER TABLE `series_list` ADD FULLTEXT KEY `show` (`show`);
ALTER TABLE `series_list` ADD FULLTEXT KEY `title` (`title`);
ALTER TABLE `series_list` ADD FULLTEXT KEY `file` (`file`);
ALTER TABLE `series_list` ADD FULLTEXT KEY `Dir` (`Dir`);
ALTER TABLE `series_list` ADD FULLTEXT KEY `url` (`url`);
ALTER TABLE `series_list` ADD FULLTEXT KEY `showUrl` (`showUrl`) ;

-- add import CSV after adding records --



