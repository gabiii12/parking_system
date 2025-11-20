-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 20, 2025 at 04:44 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `parking_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `employee_vehicle`
--

CREATE TABLE `employee_vehicle` (
  `id` int(11) NOT NULL,
  `card_uid` varchar(50) DEFAULT NULL,
  `employee_name` varchar(50) DEFAULT NULL,
  `vehicle_plate` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee_vehicle`
--

INSERT INTO `employee_vehicle` (`id`, `card_uid`, `employee_name`, `vehicle_plate`) VALUES
(1, '47364B63', 'TRINIDAD, ALFONZO GABRYL DOMINGO', 'NEU6791'),
(2, '47725963', 'GALON, GESSA MARIZ CASTRO', 'WOW9021');

-- --------------------------------------------------------

--
-- Table structure for table `parking_logs`
--

CREATE TABLE `parking_logs` (
  `id` int(11) NOT NULL,
  `card_uid` varchar(50) DEFAULT NULL,
  `employee_name` varchar(100) DEFAULT NULL,
  `vehicle_plate` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `last_action` enum('ENTRY','EXIT') DEFAULT 'ENTRY',
  `time` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `parking_logs`
--

INSERT INTO `parking_logs` (`id`, `card_uid`, `employee_name`, `vehicle_plate`, `status`, `last_action`, `time`) VALUES
(1, '47725963', 'GALON, GESSA MARIZ CASTRO', 'WOW9021', NULL, 'ENTRY', '2025-11-01 22:00:41'),
(2, '47364B63', 'TRINIDAD, ALFONZO GABRYL DOMINGO', 'NEU6791', NULL, 'ENTRY', '2025-11-01 22:00:50'),
(3, '47725963', 'GALON, GESSA MARIZ CASTRO', 'WOW9021', NULL, 'EXIT', '2025-11-01 22:02:56'),
(4, '47364B63', 'TRINIDAD, ALFONZO GABRYL DOMINGO', 'NEU6791', NULL, 'EXIT', '2025-11-01 22:06:21'),
(5, '47725963', 'GALON, GESSA MARIZ CASTRO', 'WOW9021', NULL, 'ENTRY', '2025-11-01 22:06:28'),
(6, '47364B63', 'TRINIDAD, ALFONZO GABRYL DOMINGO', 'NEU6791', NULL, 'ENTRY', '2025-11-01 22:07:56'),
(7, '47725963', 'GALON, GESSA MARIZ CASTRO', 'WOW9021', NULL, 'EXIT', '2025-11-01 22:08:02'),
(8, '47364B63', 'TRINIDAD, ALFONZO GABRYL DOMINGO', 'NEU6791', NULL, 'EXIT', '2025-11-02 00:49:51'),
(9, '47725963', 'GALON, GESSA MARIZ CASTRO', 'WOW9021', NULL, 'ENTRY', '2025-11-02 00:49:57'),
(10, '47364B63', 'TRINIDAD, ALFONZO GABRYL DOMINGO', 'NEU6791', NULL, 'ENTRY', '2025-11-02 00:50:05'),
(11, '47725963', 'GALON, GESSA MARIZ CASTRO', 'WOW9021', NULL, 'EXIT', '2025-11-02 00:50:12'),
(12, '47725963', 'GALON, GESSA MARIZ CASTRO', 'WOW9021', NULL, 'ENTRY', '2025-11-02 00:50:21'),
(13, '47364B63', 'TRINIDAD, ALFONZO GABRYL DOMINGO', 'NEU6791', NULL, 'EXIT', '2025-11-02 00:50:30');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `employee_vehicle`
--
ALTER TABLE `employee_vehicle`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `parking_logs`
--
ALTER TABLE `parking_logs`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `employee_vehicle`
--
ALTER TABLE `employee_vehicle`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `parking_logs`
--
ALTER TABLE `parking_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
