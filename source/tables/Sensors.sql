
#Create Sensors Table
use db_g;
CREATE TABLE db_g.Sensors (
	id int auto_increment,
    sensor_name varchar(255) COMMENT "Sensor name",
    sensor_value decimal(10,2) COMMENT "Sensor value",
    timestamp timestamp COMMENT "Event timestamp",
    year Int  COMMENT "Sensor reading year",
    month Int  COMMENT " Sensor reading month",
    day int  COMMENT "Sensor reading day",
    PRIMARY KEY (id)
);
