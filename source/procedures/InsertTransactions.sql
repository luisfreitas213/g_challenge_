# Store Procedure to insert data in db_g.Transactions
#MySQL ELT() returns the string at the index number specified in the list of arguments. 
#The first argument indicates the index of the string to be retrieved from the list of arguments.
#MySQL MD5() Calculates an MD5 128-bit checksum for a string. 
#The value is returned as a binary string of 32 hex digits, or NULL if the argument was NULL. 
#The return value can, for example, be used as a hash key.

use db_g;
DELIMITER $$
CREATE PROCEDURE InsertTransactions(IN NumRows INT, IN MinVal INT, IN MaxVal INT)
    BEGIN
        DECLARE i INT;
       	DECLARE ProductName varchar(255);
        SET i = 1;
        START TRANSACTION;
        WHILE i <= NumRows DO
        	SET ProductName = elt(floor(rand() * 6 + 1), 'product_1', 'product_2', 'product_3','product_4','product_5','product_6');
            INSERT INTO db_g.Transactions (timestamp,product_id,product_name, product_price, cliente_id) VALUES (CURRENT_TIMESTAMP(),
           									MD5(ProductName),
           									ProductName,
           									MinVal + ROUND(RAND() * (MaxVal - MinVal),2),
           									elt(floor(rand() * 4 + 1), 1147483782, 1247583782, 1234583767,1234512345));
           									
            SET i = i + 1;
        END WHILE;
        COMMIT;
    END$$
DELIMITER ;

# CALL InsertTransactions(1000, 10, 1000);