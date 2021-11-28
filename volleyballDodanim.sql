-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 28, 2021 at 06:08 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `volleyball`
--

-- --------------------------------------------------------

--
-- Table structure for table `match`
--

CREATE TABLE `match` (
  `id` int(11) NOT NULL,
  `tournament_id` int(11) DEFAULT NULL,
  `team1_id` int(11) DEFAULT NULL,
  `team2_id` int(11) DEFAULT NULL,
  `points_team1` int(11) DEFAULT NULL,
  `points_team2` int(11) DEFAULT NULL,
  `sets_team1` int(11) DEFAULT NULL,
  `sets_team2` int(11) DEFAULT NULL,
  `winner_id` int(11) DEFAULT NULL,
  `looser_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `match`
--

INSERT INTO `match` (`id`, `tournament_id`, `team1_id`, `team2_id`, `points_team1`, `points_team2`, `sets_team1`, `sets_team2`, `winner_id`, `looser_id`) VALUES
(1, 3, 1, 2, 73, 68, 2, 1, 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `player`
--

CREATE TABLE `player` (
  `id` int(11) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `player`
--

INSERT INTO `player` (`id`, `name`, `team_id`) VALUES
(2, 'Juan Carlos', 1),
(3, 'Shoy', 1),
(4, 'Kageyama', 1),
(5, 'Tsuki', 2),
(6, 'Kiki', 2),
(7, 'Jeremy', 2),
(8, 'Pablo feliz', 3),
(9, 'Izumi', 3),
(10, 'Jose', 4),
(11, 'Junior', 4);

-- --------------------------------------------------------

--
-- Table structure for table `team`
--

CREATE TABLE `team` (
  `id` int(11) NOT NULL,
  `name` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `team`
--

INSERT INTO `team` (`id`, `name`) VALUES
(1, 'Karasuno'),
(2, 'Shiratorizawa'),
(3, 'Dateko'),
(4, 'Aoba Yoshai');

-- --------------------------------------------------------

--
-- Table structure for table `team_tournament`
--

CREATE TABLE `team_tournament` (
  `id` int(11) NOT NULL,
  `team_id` int(11) DEFAULT NULL,
  `tournament_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `team_tournament`
--

INSERT INTO `team_tournament` (`id`, `team_id`, `tournament_id`) VALUES
(1, 1, 3),
(2, 2, 3),
(3, 3, 3),
(4, 4, 3);

-- --------------------------------------------------------

--
-- Table structure for table `tournament`
--

CREATE TABLE `tournament` (
  `id` int(11) NOT NULL,
  `name` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tournament`
--

INSERT INTO `tournament` (`id`, `name`) VALUES
(2, 'ChampionsUnadeca'),
(3, 'ChampionsUnadeca');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `user` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `rol` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `user`, `password`, `rol`) VALUES
(1, 'admin', '123', 'admin'),
(2, 'contador', '1234', 'usuario'),
(3, 'juez', '12345', 'Usuario');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `match`
--
ALTER TABLE `match`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tournament_id` (`tournament_id`),
  ADD KEY `team1_id` (`team1_id`),
  ADD KEY `team2_id` (`team2_id`),
  ADD KEY `winner_id` (`winner_id`),
  ADD KEY `looser_id` (`looser_id`);

--
-- Indexes for table `player`
--
ALTER TABLE `player`
  ADD PRIMARY KEY (`id`),
  ADD KEY `team_id` (`team_id`);

--
-- Indexes for table `team`
--
ALTER TABLE `team`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `team_tournament`
--
ALTER TABLE `team_tournament`
  ADD PRIMARY KEY (`id`),
  ADD KEY `team_id` (`team_id`),
  ADD KEY `tournament_id` (`tournament_id`);

--
-- Indexes for table `tournament`
--
ALTER TABLE `tournament`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `match`
--
ALTER TABLE `match`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `player`
--
ALTER TABLE `player`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `team`
--
ALTER TABLE `team`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `team_tournament`
--
ALTER TABLE `team_tournament`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `tournament`
--
ALTER TABLE `tournament`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `match`
--
ALTER TABLE `match`
  ADD CONSTRAINT `match_ibfk_1` FOREIGN KEY (`tournament_id`) REFERENCES `tournament` (`id`),
  ADD CONSTRAINT `match_ibfk_2` FOREIGN KEY (`team1_id`) REFERENCES `team` (`id`),
  ADD CONSTRAINT `match_ibfk_3` FOREIGN KEY (`team2_id`) REFERENCES `team` (`id`),
  ADD CONSTRAINT `match_ibfk_4` FOREIGN KEY (`winner_id`) REFERENCES `team` (`id`),
  ADD CONSTRAINT `match_ibfk_5` FOREIGN KEY (`looser_id`) REFERENCES `team` (`id`);

--
-- Constraints for table `player`
--
ALTER TABLE `player`
  ADD CONSTRAINT `player_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`);

--
-- Constraints for table `team_tournament`
--
ALTER TABLE `team_tournament`
  ADD CONSTRAINT `team_tournament_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`),
  ADD CONSTRAINT `team_tournament_ibfk_2` FOREIGN KEY (`tournament_id`) REFERENCES `tournament` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
