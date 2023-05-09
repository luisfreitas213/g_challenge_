
#Create Transactions Table
use db_g;
CREATE TABLE db_g.Transactions (
	id int auto_increment,
    timestamp  timestamp NOT NULL,
    product_id  varchar(255) NOT NULL,
    product_name varchar(255) NOT NULL,
    product_price decimal(10,2) NOT NULL,
    cliente_id bigint NOT NULL,
    PRIMARY KEY (id)
);
