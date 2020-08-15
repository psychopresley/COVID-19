CREATE DEFINER=`root`@`localhost` FUNCTION `total_confirmed`(country_name VARCHAR(255)) RETURNS int
    DETERMINISTIC
BEGIN

DECLARE total_confirmed INTEGER;

SET total_confirmed = (SELECT 
	MAX(Confirmed)
FROM `covid19`.`country_report`
WHERE `Country/Region` = country_name);

RETURN total_confirmed;
END