# For PPL340, Identify the years in which the number of readings is less than the average;
use db_g;
CREATE VIEW db_g.vw_count_less_avg_by_year_ppl340 as 
SELECT 
    YEAR AS year, 
    COUNT(1) AS num_readings,
    AVG(sensor_value) as avg_readings
FROM 
    Sensors s 
WHERE 
    sensor_name = 'PPL340'
GROUP BY 
    YEAR
HAVING 
    COUNT(1) <  AVG(sensor_value) ;