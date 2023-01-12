-- Creates a trigger that decreases the quantity of an item
-- after adding a new order.

DROP TRIGGER IF EXISTS trg_desc_qty;
delimiter //

CREATE TRIGGER trg_desc_qty
AFTER INSERT ON orders
FOR EACH ROW
	BEGIN
		UPDATE items
		SET quantity = quantity - NEW.number
		WHERE name = NEW.item_name;
	END
//
delimiter ;
		
