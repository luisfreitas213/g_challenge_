# Average number of readings by year for the sensor PPL340;

use db_g;
CREATE VIEW db_g.vw_average_ppl340_by_year as 
Select YEAR, AVG(sensor_value) as avg_ppl340 from db_g.Sensors where sensor_name = 'PPL340' GROUP BY YEAR;