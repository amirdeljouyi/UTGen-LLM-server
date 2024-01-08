INSERT INTO persons (first_name, last_name) SELECT 'james', 'carter' WHERE NOT EXISTS (SELECT * FROM persons WHERE id=1);
INSERT INTO persons (first_name, last_name) SELECT 'helen', 'leary' WHERE NOT EXISTS (SELECT * FROM persons WHERE id=2);
INSERT INTO persons (first_name, last_name) SELECT 'peter', 'pan' WHERE NOT EXISTS (SELECT * FROM persons WHERE id=3);