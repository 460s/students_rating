ALTER TABLE task ADD pass_from INTEGER;
ALTER TABLE task ADD pass_to INTEGER;

UPDATE task SET pass_from = 1542805200, pass_to = 1543222800 WHERE id = 1;
UPDATE task SET pass_from = 1543237200, pass_to = 1543395600 WHERE id = 2;
UPDATE task SET pass_from = 1543410000, pass_to = 1543827600 WHERE id = 3;
UPDATE task SET pass_from = 1543842000, pass_to = 1544000400 WHERE id = 4;
UPDATE task SET pass_from = 1544014800, pass_to = 1544432400 WHERE id = 5;
UPDATE task SET pass_from = 1544446800, pass_to = 1544605200 WHERE id = 6;
UPDATE task SET pass_from = 1544619600, pass_to = 1545037200 WHERE id = 7;