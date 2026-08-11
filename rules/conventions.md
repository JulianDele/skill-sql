# Conventions Rules

## CONV-01: Nombres poco descriptivos
```
IF identifier (table/column alias) matches pattern of a single letter or
   generic name without domain meaning (ej: "t1", "x", "col1", "tmp")
THEN severity = LOW
AND recommend a descriptive name
```

## CONV-02: Uso incorrecto de NULL en comparaciones
```
IF WHERE clause compares a column to NULL using "=" or "!="
   (ej: "WHERE col = NULL")
THEN severity = MEDIUM
AND recommend using IS NULL / IS NOT NULL
```
Justificación técnica: `= NULL` nunca es verdadero en SQL estándar (NULL no es
igual a nada, ni siquiera a sí mismo), por lo que la condición silenciosamente
no filtra lo que el autor probablemente pretendía.

## CONV-03: Columnas NOT NULL sin default en ALTER/CREATE
```
IF statement = ALTER TABLE ... ADD COLUMN
AND column is NOT NULL
AND no DEFAULT value is specified
AND table may already contain rows
THEN severity = HIGH
AND flag as "will fail or require table rewrite on existing data"
```

## CONV-04: Tipo de dato inadecuado
```
IF column stores monetary values AND type = FLOAT/DOUBLE
THEN severity = MEDIUM
AND recommend DECIMAL/NUMERIC to avoid rounding errors

IF column stores dates/timestamps AND type = VARCHAR/STRING
THEN severity = MEDIUM
AND recommend a native DATE/DATETIME/TIMESTAMP type

IF column is boolean-like (0/1, 'S'/'N') AND type = VARCHAR without CHECK constraint
THEN severity = LOW
AND recommend BOOLEAN type or a CHECK constraint
```

## CONV-05: Falta de restricción NOT NULL en columnas claramente obligatorias
```
IF column name suggests a required field (ej: "email", "id", "fecha_creacion")
AND no NOT NULL constraint is defined
AND no context indicates it's intentionally optional
THEN severity = INFO [NEEDS CONTEXT]
AND recommend confirming whether the field should be mandatory
```

## CONV-06: Inconsistencia de convención de nombres dentro del mismo script
```
IF script mixes naming conventions (ej: snake_case y camelCase, o prefijos
   inconsistentes como FC/TA mezclados con nombres sin prefijo)
THEN severity = LOW
AND recommend unifying the naming convention
```
