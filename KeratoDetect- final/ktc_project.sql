-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 08, 2021 at 07:28 AM
-- Server version: 10.4.8-MariaDB
-- PHP Version: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ktc_project`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(10) NOT NULL,
  `a_name` varchar(20) NOT NULL,
  `a_email` varchar(20) NOT NULL,
  `a_pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `a_name`, `a_email`, `a_pass`) VALUES
(1, 'Chetan', 'chetan@gmail.com', '123');

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE `patient` (
  `p_id` int(10) NOT NULL,
  `p_name` varchar(20) NOT NULL,
  `p_email` varchar(20) NOT NULL,
  `p_phone` int(10) NOT NULL,
  `p_age` int(3) NOT NULL,
  `p_gender` varchar(10) NOT NULL,
  `p_image` varchar(20) NOT NULL,
  `p_result` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`p_id`, `p_name`, `p_email`, `p_phone`, `p_age`, `p_gender`, `p_image`, `p_result`) VALUES
(10, 'Anil', 'ac@gmail.com', 2147483647, 25, 'Male', 'ktc_1224.jpg', 'Normal Eye'),
(14, 'raj', 'rsfg@email.com', 2147483647, 54, 'Male', 'nor_1271.jpg', 'Keratoconus Eye'),
(18, 'Chetan', 'chetan@gmail.com', 2147483647, 42, 'Male', 'eye.jpg', 'Keratoconus Eye'),
(19, 'Anil', 'vinay@gmail.com', 2147483647, 25, 'Male', 'eye-scan.jpg', 'Keratoconus Eye'),
(20, 'Anil', 'vinay@gmail.com', 2147483647, 25, 'Male', 'oc.jpg', 'Keratoconus Eye'),
(21, 'Anil', 'vinay@gmail.com', 2147483647, 25, 'Male', 'index.jpg', 'Keratoconus Eye'),
(22, 'Anil', 'vinay@gmail.com', 2147483647, 25, 'Male', 'cat.jpg', 'Keratoconus Eye');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(10) NOT NULL,
  `name` varchar(20) NOT NULL,
  `email` varchar(20) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `phone` int(15) NOT NULL,
  `dob` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `name`, `email`, `password`, `phone`, `dob`) VALUES
(100, 'abc', 'abc@gmail.com', '123', 1245368790, '12/05/1999'),
(102, 'Chetan', 'chetan@gmail.com', '12345', 2147483647, '1982-07-14'),
(109, 'Anil', 'anil@gmail.com', '123', 2147483647, '1987-09-09');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `patient`
--
ALTER TABLE `patient`
  ADD PRIMARY KEY (`p_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `patient`
--
ALTER TABLE `patient`
  MODIFY `p_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=110;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
