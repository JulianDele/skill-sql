---
name: sql-reviewer
description: Revisa sentencias o scripts SQL como un revisor técnico de base de datos. Detecta problemas de seguridad, rendimiento, convenciones y uso incorrecto de NULL/tipos de datos, clasificando cada hallazgo con una severidad (CRITICAL/HIGH/MEDIUM/LOW/INFO). Úsala siempre que el usuario pegue código SQL y pida revisión, análisis, opinión, "¿está bien esto?", o antes de aprobar/ejecutar un script SQL.
---

# SQL Reviewer

## Purpose
Actuar como revisor técnico de bases de datos: analizar sentencias o scripts SQL
y producir una lista de hallazgos objetivos, clasificados por severidad, siguiendo
reglas deterministas definidas en `rules/`. No es un generador de opiniones libres;
es un procedimiento reproducible.

## When to activate
- El usuario pega una o más sentencias SQL (SELECT, INSERT, UPDATE, DELETE, DDL) y pide
  revisión, feedback, aprobación, o "¿esto está bien?".
- El usuario pide explícitamente un code review de un script `.sql`.
- El usuario pide validar un cambio antes de ejecutarlo en producción.

## When NOT to activate
- No hay SQL real en el mensaje (solo se habla de bases de datos en general).
- El usuario pide que la sentencia SEA EJECUTADA, no revisada (esta skill no ejecuta SQL).
- El usuario pide que se "arregle" el SQL sin pedir revisión — en ese caso, primero
  revisar y mostrar hallazgos; solo reescribir si el usuario lo confirma después del reporte.
- El SQL es pseudocódigo o está incompleto a propósito (ej: fragmentos de documentación),
  y el usuario no busca una revisión real.

## Inputs
- Una o más sentencias SQL (texto plano o archivo `.sql`).
- Opcional: contexto de la tabla (tamaño esperado, si es producción, motor de BD).
  Si no se provee, ver sección **Failure handling**.

## Procedure
1. Separar el input en sentencias individuales (por `;`).
2. Para cada sentencia, identificar el tipo (SELECT, INSERT, UPDATE, DELETE, DDL, otro).
3. Aplicar, en orden, las reglas de `rules/security.md`, luego `rules/performance.md`,
   luego `rules/conventions.md`.
4. Para cada regla que aplique, generar un hallazgo con: severidad, descripción,
   línea/fragmento afectado, y recomendación concreta.
5. Si dos reglas entran en conflicto (ver **Rule conflicts**), aplicar la de mayor severidad
   y anotar explícitamente que hubo conflicto y por qué se resolvió así.
6. Si falta contexto necesario para decidir una severidad (ver **Failure handling**),
   marcar el hallazgo como `INFO` con la etiqueta `[NEEDS CONTEXT]` en vez de asumir.
7. Ordenar los hallazgos de mayor a menor severidad.
8. Producir la salida en el formato de **Expected output**.
9. Nunca ejecutar el SQL ni asumir que se ejecutó.

## Rules
Las reglas completas y sus condiciones exactas viven en:
- `rules/security.md` — SQL injection, DELETE/UPDATE sin WHERE seguro, permisos.
- `rules/performance.md` — SELECT *, LIMIT ausente, índices, rendimiento general.
- `rules/conventions.md` — nombres, tipos de datos, uso de NULL.

Ejemplo de formato de regla (todas las reglas siguen esta estructura):
```
IF statement = DELETE
AND WHERE is absent
THEN severity = CRITICAL
AND do not recommend executing the statement
```

### Rule conflicts
Si una sentencia dispara dos reglas con distinta severidad (ej: `SELECT *` [MEDIUM]
sobre una tabla sin `LIMIT` [MEDIUM] pero además con filtro por `LIKE '%'` que anula
el WHERE [CRITICAL, ver security.md]), se reporta CADA hallazgo por separado, pero el
resumen ejecutivo usa la severidad más alta como severidad global de la sentencia.
Nunca se "promedian" severidades ni se ocultan hallazgos de menor severidad.

## Severity levels
- **CRITICAL**: riesgo real de pérdida de datos irreversible o brecha de seguridad
  explotable (DELETE/UPDATE sin WHERE seguro, SQL injection evidente).
- **HIGH**: riesgo serio pero no necesariamente irreversible (WHERE que técnicamente
  existe pero no filtra nada real, ej. `WHERE 1=1` o `LIKE '%'`, permisos excesivos).
- **MEDIUM**: impacto de rendimiento o mantenibilidad significativo pero no destructivo
  (SELECT * en tabla grande, ausencia de LIMIT, índice probablemente faltante).
- **LOW**: problemas de estilo/convención con impacto operativo bajo (nombres poco
  descriptivos, tipos de datos subóptimos pero funcionales).
- **INFO**: sugerencias, o hallazgos que requieren contexto adicional para confirmarse.

## Expected output
Para cada sentencia analizada:
```
### Statement N: <tipo> <resumen breve>
- [SEVERITY] <descripción del problema> — Recomendación: <acción concreta>
- [SEVERITY] ...

Resumen: <severidad más alta encontrada> — <se recomienda / no se recomienda ejecutar>
```
Si NO se encuentra ningún problema, decirlo explícitamente: "No se detectaron
violaciones a las reglas definidas." No inventar hallazgos para justificar el análisis.

## Validation
Antes de entregar el resultado, verificar:
- Cada hallazgo cita la regla exacta de `rules/` que lo generó.
- No hay hallazgos duplicados para el mismo fragmento.
- Toda sentencia DELETE/UPDATE fue evaluada explícitamente contra `security.md`.
- El resumen final no contradice los hallazgos individuales.

## Failure handling
La skill NO debe inventar contexto para completar un análisis. Casos y su manejo:
- **No se sabe el tamaño de la tabla**: no asumir que es pequeña ni grande. Marcar
  reglas de rendimiento como `[INFO][NEEDS CONTEXT]` y pedir el dato si es relevante
  para la severidad (ej. SELECT * en tabla de 10 filas vs. de 10M).
- **No se sabe si es producción**: tratar toda sentencia destructiva (DELETE/UPDATE/DROP)
  con el mismo rigor que si fuera producción — nunca bajar la severidad por asumir
  que es un entorno de pruebas.
- **Motor de BD no especificado**: aplicar reglas agnósticas de motor; si una regla
  depende del motor (ej. sintaxis de índices), indicarlo y no asumir un motor específico.
- **SQL incompleto o truncado**: reportarlo como tal, no completar la sentencia
  adivinando la intención del autor.
