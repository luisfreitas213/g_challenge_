#Create Control Table
use db_g;
CREATE TABLE db_g.Control_ingestion (
	id int auto_increment,
    timestamp  timestamp NOT NULL,
    process_name varchar(150) NOT NULL,
    delta_execution varchar(150) NOT NULL,
    file_generated varchar(150) NOT NULL,
    PRIMARY KEY (id)
);