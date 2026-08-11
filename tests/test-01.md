# Test 01 — Happy Path

## Input
```sql
SELECT id_usuario, nombre, email
FROM usuarios
WHERE estado = 'activo'
LIMIT 100;
```

## Expected behavior
No debe generar hallazgos. La sentencia tiene columnas explícitas, WHERE
restrictivo real, y LIMIT razonable. La skill debe decir explícitamente que
no se detectaron violaciones, sin inventar problemas para "justificar" el análisis.

## Actual behavior
(Completar tras ejecutar la skill: pegar la salida real obtenida.)

## Pass / Fail
(Completar)

## Problem detected
(Completar — si la skill inventó un hallazgo falso, es un fallo grave)

## Modification made to the skill
(Completar si aplica)
