## PERF-01: SELECT *
```
IF statement = SELECT
AND column list = "*"
THEN severity = MEDIUM
AND recommend listing explicit columns
```

## PERF-02: Ausencia de LIMIT en SELECT potencialmente masivo
```
IF statement = SELECT
AND no LIMIT clause present
AND no aggregate function (COUNT/SUM/AVG/etc.) makes result inherently small
THEN severity = MEDIUM
AND recommend adding LIMIT or pagination
```

## PERF-03: LIMIT que no protege realmente
```
IF statement = SELECT
AND LIMIT value >= a threshold that defeats its purpose (ej: LIMIT 1000000000)
THEN severity = MEDIUM
AND flag as "LIMIT present but not effectively restrictive"
```
Justificación: el caso de Red Team `SELECT * FROM TA_USERS LIMIT 1000000000` cumple
"tiene LIMIT" superficialmente pero no protege el rendimiento real.

## PERF-04: Índice potencialmente faltante
```
IF WHERE clause or JOIN condition filters/joins on a column
AND no context confirms that column is indexed
THEN severity = INFO [NEEDS CONTEXT]
AND recommend verifying/creating an index on that column
```
No se debe afirmar con certeza que falta un índice sin poder inspeccionar el
esquema real — por eso es INFO y no MEDIUM/HIGH, salvo que el usuario confirme
que no existe.

## PERF-05: JOIN sin condición
```
IF statement contains JOIN
AND no ON/USING clause is present
THEN severity = HIGH
AND flag as "cartesian product risk"
```

## PERF-06: Funciones aplicadas sobre columnas indexadas en WHERE
```
IF WHERE clause applies a function to a column (ej: UPPER(col), YEAR(fecha))
THEN severity = LOW
AND recommend rewriting to avoid disabling index usage (ej: rango de fechas
    en vez de YEAR(fecha) = X)
```

## PERF-07: Subconsultas correlacionadas evitables
```
IF a correlated subquery could be rewritten as a JOIN
THEN severity = LOW
AND recommend evaluating a JOIN rewrite
