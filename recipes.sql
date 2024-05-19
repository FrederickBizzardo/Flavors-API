CREATE TABLE recipes (
            rep_id INT PRIMARY KEY NOT NULL,
            title VARCHAR(155) NOT NULL,
            ingredients VARCHAR(155),
            servings VARCHAR(20), 
            instructions VARCHAR(255)
        );

INSERT INTO recipes VALUES(2,'Beef Stew','Chicken, tomatoes, onions','4','Cut the chicken');