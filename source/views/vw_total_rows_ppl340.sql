# Number of rows for the sensor PPL340;

use db_g;
CREATE VIEW db_g.vw_total_rows_ppl340 as 
Select COUNT(1) as total_rows_ppl340 from db_g.Sensors where sensor_name = 'PPL340';