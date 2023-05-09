# Number of distinct sensors present on the database;;

use db_g;
CREATE VIEW db_g.vw_distinct_sensors as 
Select COUNT(DISTINCT sensor_name) as number_distinct_sensors from db_g.Sensors;