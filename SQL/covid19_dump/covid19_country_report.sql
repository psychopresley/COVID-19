CREATE DATABASE  IF NOT EXISTS `covid19` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `covid19`;
-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: covid19
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `country_report`
--

DROP TABLE IF EXISTS `country_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `country_report` (
  `Country/Region` text,
  `Date` text,
  `Active` int DEFAULT NULL,
  `Confirmed` int DEFAULT NULL,
  `Deaths` int DEFAULT NULL,
  `Latitude` double DEFAULT NULL,
  `Longitude` double DEFAULT NULL,
  `Recovered` int DEFAULT NULL,
  `Mortality rate in %` double DEFAULT NULL,
  `Days_since_1st_case` int DEFAULT NULL,
  `Active_new_cases` int DEFAULT NULL,
  `Active_daily_%inc_by_country` double DEFAULT NULL,
  `Active_new_cases_inc_rate` int DEFAULT NULL,
  `Active_new_cases_inc_rate_speed` int DEFAULT NULL,
  `Confirmed_new_cases` int DEFAULT NULL,
  `Confirmed_daily_%inc_by_country` double DEFAULT NULL,
  `Confirmed_new_cases_inc_rate` int DEFAULT NULL,
  `Confirmed_new_cases_inc_rate_speed` int DEFAULT NULL,
  `Deaths_new_cases` int DEFAULT NULL,
  `Deaths_daily_%inc_by_country` double DEFAULT NULL,
  `Deaths_new_cases_inc_rate` int DEFAULT NULL,
  `Deaths_new_cases_inc_rate_speed` int DEFAULT NULL,
  `Recovered_new_cases` int DEFAULT NULL,
  `Recovered_daily_%inc_by_country` double DEFAULT NULL,
  `Recovered_new_cases_inc_rate` int DEFAULT NULL,
  `Recovered_new_cases_inc_rate_speed` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-07 16:41:50
