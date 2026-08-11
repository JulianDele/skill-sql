SELECT id_usuario, nombre, email
FROM usuarios
WHERE estado = 'activo'
LIMIT 100;

SELECT id_usuario, nombre
FROM usuarios
WHERE id_usuario = 42;
