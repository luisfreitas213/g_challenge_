# The number of rows by year for the sensor PPL340;

use db_g;
CREATE VIEW db_g.vw_total_rows_ppl340_by_year as 
Select YEAR, COUNT(1) as total_rows_ppl340 from db_g.Sensors where sensor_name = 'PPL340' GROUP BY YEAR;