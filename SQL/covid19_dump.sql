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
-- Temporary view structure for view `average_rate`
--

DROP TABLE IF EXISTS `average_rate`;
/*!50001 DROP VIEW IF EXISTS `average_rate`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `average_rate` AS SELECT 
 1 AS `country`,
 1 AS `days`,
 1 AS `confirmed_cases_per_day`,
 1 AS `average_deaths_per_day`,
 1 AS `average_recovered_per_day`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `case_share`
--

DROP TABLE IF EXISTS `case_share`;
/*!50001 DROP VIEW IF EXISTS `case_share`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `case_share` AS SELECT 
 1 AS `Country`,
 1 AS `total_confirmed`,
 1 AS `active`,
 1 AS `pct_active`,
 1 AS `total_recovered`,
 1 AS `pct_recovered`,
 1 AS `total_deaths`,
 1 AS `pct_deaths`*/;
SET character_set_client = @saved_cs_client;

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

--
-- Temporary view structure for view `most_recently_affected_countries`
--

DROP TABLE IF EXISTS `most_recently_affected_countries`;
/*!50001 DROP VIEW IF EXISTS `most_recently_affected_countries`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `most_recently_affected_countries` AS SELECT 
 1 AS `country`,
 1 AS `date_of_first_case`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `outbreak_evolution`
--

DROP TABLE IF EXISTS `outbreak_evolution`;
/*!50001 DROP VIEW IF EXISTS `outbreak_evolution`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `outbreak_evolution` AS SELECT 
 1 AS `week`,
 1 AS `begin_week`,
 1 AS `end_week`,
 1 AS `countries_with_cases_reported`,
 1 AS `confirmed_cases`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `raw_data`
--

DROP TABLE IF EXISTS `raw_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `raw_data` (
  `Active` double DEFAULT NULL,
  `Confirmed` double DEFAULT NULL,
  `Country/Region` text,
  `Date` text,
  `Deaths` double DEFAULT NULL,
  `Latitude` double DEFAULT NULL,
  `Longitude` double DEFAULT NULL,
  `Province/State` text,
  `Recovered` double DEFAULT NULL,
  `Mortality rate in %` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'covid19'
--

--
-- Dumping routines for database 'covid19'
--
/*!50003 DROP FUNCTION IF EXISTS `total_confirmed` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `total_confirmed`(country_name VARCHAR(255)) RETURNS int
    DETERMINISTIC
BEGIN

DECLARE total_confirmed INTEGER;

SET total_confirmed = (SELECT 
	MAX(Confirmed)
FROM `covid19`.`country_report`
WHERE `Country/Region` = country_name);

RETURN total_confirmed;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `active_cases_by_time_period` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `active_cases_by_time_period`(
IN country_name VARCHAR(255),
IN time_var VARCHAR(255)
)
BEGIN
SELECT `Country/Region` AS country,
       MIN(date) AS begin_week,
       MAX(date) AS end_week,
       IF(time_var='week',WEEK(Date),MONTH(Date)) AS time_period,
       (MAX(confirmed) - MAX(recovered) - MAX(deaths)) AS active
FROM country_report
WHERE `Country/Region` = country_name
GROUP BY time_period
ORDER BY time_period;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `countries_in_confirmed_range` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `countries_in_confirmed_range`(
IN min_cases INT,
IN max_cases INT
)
BEGIN
SELECT `Country/Region`,
MAX(Confirmed) AS 'total confirmed cases'
FROM covid19.`country_report`
GROUP BY `Country/Region`
HAVING MAX(Confirmed) BETWEEN min_cases AND max_cases;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `countries_with_higher_confirmed_cases_after_X_days` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `countries_with_higher_confirmed_cases_after_X_days`(IN days_from_1st_case INT)
BEGIN
SELECT `Country/Region` AS country,
       MAX(confirmed) AS total_confirmed
FROM country_report
WHERE days_since_1st_case = days_from_1st_case
GROUP BY Country
ORDER BY total_confirmed DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `countries_with_higher_death_rate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `countries_with_higher_death_rate`(IN minimum_confirmed INT)
BEGIN
SELECT `Country/Region` AS Country,
       MAX(deaths)/MAX(confirmed)*100 AS pct_deaths
FROM country_report
GROUP BY Country
HAVING MAX(confirmed) > minimum_confirmed
ORDER BY pct_deaths DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `countries_with_higher_recovered_rate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `countries_with_higher_recovered_rate`(IN minimum_confirmed INT)
BEGIN
SELECT `Country/Region` AS Country,
       MAX(Recovered)/MAX(confirmed)*100 AS pct_recovered
FROM country_report
GROUP BY Country
HAVING MAX(confirmed) > minimum_confirmed
ORDER BY pct_recovered DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `country_summary` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `country_summary`(
IN country_name VARCHAR(255),
IN time_var VARCHAR(255)
)
BEGIN
SELECT 
    `Country/Region` AS country,
    IF(time_var='week',WEEK(Date),MONTH(Date)) AS time_period,
    MAX(Confirmed) AS total_confirmed,
    MAX(Recovered) AS total_recovered,
    MAX(Deaths) AS total_deaths,
    MAX(Confirmed) - MAX(Deaths) - MAX(Recovered) AS active_cases
FROM
    `covid19`.`country_report`
WHERE
    `Country/Region` = country_name
GROUP BY time_period;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `count_countries` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `count_countries`(
IN min_confirmed INT,
IN max_confirmed INT
)
BEGIN
WITH country_table AS (
SELECT 
`Country/Region` AS countries,
MAX(Confirmed) AS total_confirmed_cases
FROM covid19.`country_report`
GROUP BY `Country/Region`
HAVING MAX(Confirmed) BETWEEN min_confirmed AND max_confirmed
)

SELECT
COUNT(DISTINCT countries) AS total_of_countries
FROM country_table;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `days_since_Xpct` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `days_since_Xpct`(
IN country_name VARCHAR(30),
IN percentage DECIMAL(6,2)
)
BEGIN
SELECT 
    `Country/Region` AS country,
    Date,
    Days_since_1st_case AS days,
    Confirmed,
    (SELECT TOTAL_CONFIRMED(country_name)) AS `Total confirmed cases`,
    100 * Confirmed / (SELECT TOTAL_CONFIRMED(country_name)) AS pct_confirmed
FROM
    `covid19`.`country_report`
WHERE
    `Country/Region` = country_name
HAVING 100 * Confirmed / (SELECT TOTAL_CONFIRMED(country_name)) >= percentage;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `info` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `info`()
BEGIN
SELECT 
    MAX(`country_report`.`Date`) AS `last_update`,
    COUNT(DISTINCT `country_report`.`Country/Region`) AS `countries`
FROM
    `country_report`;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `average_rate`
--

/*!50001 DROP VIEW IF EXISTS `average_rate`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `average_rate` AS select `country_report`.`Country/Region` AS `country`,max(`country_report`.`Days_since_1st_case`) AS `days`,(max(`country_report`.`Confirmed`) / max(`country_report`.`Days_since_1st_case`)) AS `confirmed_cases_per_day`,(max(`country_report`.`Deaths`) / max(`country_report`.`Days_since_1st_case`)) AS `average_deaths_per_day`,(max(`country_report`.`Recovered`) / max(`country_report`.`Days_since_1st_case`)) AS `average_recovered_per_day` from `country_report` group by `country` having (max(`country_report`.`Days_since_1st_case`) > 0) order by `confirmed_cases_per_day` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `case_share`
--

/*!50001 DROP VIEW IF EXISTS `case_share`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `case_share` AS select `country_report`.`Country/Region` AS `Country`,max(`country_report`.`Confirmed`) AS `total_confirmed`,((max(`country_report`.`Confirmed`) - max(`country_report`.`Recovered`)) - max(`country_report`.`Deaths`)) AS `active`,(100 - (((max(`country_report`.`Recovered`) + max(`country_report`.`Deaths`)) / max(`country_report`.`Confirmed`)) * 100)) AS `pct_active`,max(`country_report`.`Recovered`) AS `total_recovered`,((max(`country_report`.`Recovered`) / max(`country_report`.`Confirmed`)) * 100) AS `pct_recovered`,max(`country_report`.`Deaths`) AS `total_deaths`,((max(`country_report`.`Deaths`) / max(`country_report`.`Confirmed`)) * 100) AS `pct_deaths` from `country_report` group by `Country` having (max(`country_report`.`Confirmed`) > 1000) order by `Country` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `most_recently_affected_countries`
--

/*!50001 DROP VIEW IF EXISTS `most_recently_affected_countries`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `most_recently_affected_countries` AS select `country_report`.`Country/Region` AS `country`,min(`country_report`.`Date`) AS `date_of_first_case` from `country_report` group by `country_report`.`Country/Region` order by `date_of_first_case` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `outbreak_evolution`
--

/*!50001 DROP VIEW IF EXISTS `outbreak_evolution`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `outbreak_evolution` AS select week(`country_report`.`Date`,0) AS `week`,min(`country_report`.`Date`) AS `begin_week`,max(`country_report`.`Date`) AS `end_week`,count(distinct `country_report`.`Country/Region`) AS `countries_with_cases_reported`,sum(`country_report`.`Confirmed`) AS `confirmed_cases` from `country_report` group by `week` having (max(`country_report`.`Confirmed`) > 0) order by `week` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-08 17:42:40
