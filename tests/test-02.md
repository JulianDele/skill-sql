# Test 02 — Error evidente

## Input
```sql
DELETE FROM usuarios;

SELECT * FROM t1;

UPDATE usuarios SET password = '12345' WHERE email = NULL;
```

## Expected behavior
- `DELETE FROM usuarios;` → CRITICAL (SEC-01, sin WHERE).
- `SELECT * FROM t1;` → MEDIUM (PERF-01 SELECT *) + LOW (CONV-01 nombre "t1"
  poco descriptivo) + MEDIUM (PERF-02 sin LIMIT).
- `UPDATE ... WHERE email = NULL` → CRITICAL (SEC-01, WHERE tautológicamente
  falso porque `= NULL` nunca es verdadero, equivale a no tener WHERE efectivo)
  + MEDIUM (CONV-02 uso incorrecto de NULL).
Todos los hallazgos deben citar la regla exacta que los generó.

## Actual behavior
(Completar)

## Pass / Fail
(Completar)

## Problem detected
(Completar)

## Modification made to the skill
(Completar)
