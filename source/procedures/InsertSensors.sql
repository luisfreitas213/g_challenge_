# Store Procedure to insert data in db_g.Sensors
#MySQL ELT() returns the string at the index number specified in the list of arguments. 
#The first argument indicates the index of the string to be retrieved from the list of arguments.
#MySQL MD5() Calculates an MD5 128-bit checksum for a string. 
#The value is returned as a binary string of 32 hex digits, or NULL if the argument was NULL. 
#The return value can, for example, be used as a hash key.

use db_g;
DELIMITER $$
CREATE PROCEDURE InsertSensors(IN NumRows INT, IN MinVal INT, IN MaxVal INT)
    BEGIN
        DECLARE i INT;
       	DECLARE SensorName varchar(255);
        SET i = 1;
        START TRANSACTION;
        WHILE i <= NumRows DO
        	SET SensorName = elt(floor(rand() * 6 + 1), 'PPL340', 'PPL341', 'PPL342','PPL343','PPL344','PPL345');
            INSERT INTO db_g.Sensors (sensor_name,sensor_value,timestamp, year, month,day) VALUES (SensorName, 
                                            MinVal + ROUND(RAND() * (MaxVal - MinVal),2),
                                            CURRENT_TIMESTAMP(),
                                            YEAR(CURRENT_TIMESTAMP()),
                                            MONTH(CURRENT_TIMESTAMP()),
                                            DAY(CURRENT_TIMESTAMP()));
           									
            SET i = i + 1;
        END WHILE;
        COMMIT;
    END$$
DELIMITER ;

# CALL InsertSensors(1000, 10, 1000);