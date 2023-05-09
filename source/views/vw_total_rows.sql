# Total number of rows;

use db_g;
CREATE VIEW db_g.vw_total_rows as 
Select count(1) as total_rows from db_g.Sensors;