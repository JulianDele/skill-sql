-- Ejemplo con múltiples violaciones claras (para test de "error evidente").

SELECT * FROM t1;

DELETE FROM usuarios;

UPDATE usuarios SET password = '12345' WHERE email = NULL;

SELECT * FROM pedidos WHERE id_cliente = '" + userInput + "';

ALTER TABLE pedidos ADD COLUMN activo VARCHAR(1);
