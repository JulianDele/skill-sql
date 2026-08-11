-- Casos que superficialmente parecen cumplir las reglas pero no lo hacen.
-- (Estos son los casos típicos de la fase de Red Team.)

-- Tiene WHERE, pero no filtra nada real:
DELETE FROM TA_USERS WHERE 1 = 1;

-- Tiene LIMIT, pero el valor es tan alto que no protege nada:
SELECT * FROM TA_USERS LIMIT 1000000000;

-- Tiene WHERE con LIKE, pero el patrón coincide con todo:
UPDATE TA_USERS SET FCROLE = 'ADMIN' WHERE FCEMAIL LIKE '%';

-- JOIN sin condición (cartesian product), sin que sea obvio a primera vista:
SELECT a.nombre, b.monto
FROM clientes a, pedidos b
WHERE a.activo = 1;

-- LIMIT correcto, pero WHERE con OR que amplía el filtro a casi todo:
SELECT * FROM pagos
WHERE monto > 0 OR estado <> 'inexistente'
LIMIT 50;
