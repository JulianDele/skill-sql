# Security Rules

## SEC-01: DELETE/UPDATE sin WHERE
```
IF statement = DELETE OR UPDATE
AND WHERE clause is absent
THEN severity = CRITICAL
AND do not recommend executing the statement
```

## SEC-02: WHERE que no filtra realmente (tautología)
Un WHERE puede existir sintácticamente pero no cumplir su función. Se considera
tautológico si la condición es siempre verdadera para prácticamente cualquier fila.
```
IF statement = DELETE OR UPDATE
AND WHERE clause matches pattern: <col> = <col>, "1=1", "1" = "1",
    OR any condition using LIKE '%' alone, OR OR-chained conditions that
    cover the full domain of the column
THEN severity = CRITICAL
AND flag as "WHERE present but not restrictive"
AND do not recommend executing the statement
```
Justificación: el reto de Red Team del PDF usa exactamente `WHERE 1 = 1` y
`WHERE FCEMAIL LIKE '%'` — no basta con detectar "existe un WHERE", hay que evaluar
si restringe algo real.

## SEC-03: Concatenación de strings para construir SQL
```
IF query text shows string concatenation with a variable/placeholder
   (ej: "SELECT * FROM x WHERE id = '" + var + "'", o uso de %s / f-strings
   directamente en el cuerpo del SQL sin parámetros bindeados)
THEN severity = CRITICAL
AND recommend parameterized queries / prepared statements
```

## SEC-04: Permisos o roles otorgados de forma amplia
```
IF statement = UPDATE
AND SET clause modifies a role/permission/privilege column
AND WHERE clause is tautological (ver SEC-02) or absent
THEN severity = CRITICAL
AND flag as "privilege escalation risk"
```

## SEC-05: DROP / TRUNCATE sin confirmación explícita de intención
```
IF statement = DROP TABLE OR TRUNCATE
THEN severity = CRITICAL
AND require explicit user confirmation before recommending execution
```

## SEC-06: Falta de escape/validación en LIKE con input de usuario
```
IF LIKE clause embeds unescaped user input
THEN severity = HIGH
AND recommend input sanitization or parameter binding
```
