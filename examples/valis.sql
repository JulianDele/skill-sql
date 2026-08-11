SELECT id_usuario, nombre, email, fecha_creacion
FROM usuarios
WHERE estado = 'activo'
  AND fecha_creacion >= '2026-01-01'
ORDER BY fecha_creacion DESC
LIMIT 100;

UPDATE usuarios
SET ultimo_login = NOW()
WHERE id_usuario = 45231;

DELETE FROM sesiones_expiradas
WHERE fecha_expiracion < '2026-01-01'
  AND id_sesion IN (SELECT id_sesion FROM sesiones_a_purgar);

ALTER TABLE pedidos
ADD COLUMN monto_total DECIMAL(10,2) NOT NULL DEFAULT 0.00;
