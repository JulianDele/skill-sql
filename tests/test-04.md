# Test 04 — Información insuficiente

## Input
```sql
SELECT * FROM logs WHERE tipo_evento = 'error';
```
(Sin contexto adicional sobre el tamaño de la tabla `logs` ni si tiene índice
en `tipo_evento`.)

## Expected behavior
- PERF-01 (SELECT *) → MEDIUM, esto sí se puede afirmar sin contexto.
- PERF-02 (sin LIMIT) → MEDIUM, también verificable sin contexto.
- PERF-04 (índice en `tipo_evento`) → la skill NO debe afirmar con certeza que
  falta un índice. Debe marcarlo como INFO [NEEDS CONTEXT] y pedir confirmar
  si la columna está indexada, en vez de inventar que sí o que no lo está.
- El tamaño real de `logs` (¿10 filas o 10 millones?) tampoco se puede asumir;
  la skill no debe decidir la severidad de PERF-02 basándose en un tamaño
  inventado, solo en la ausencia objetiva de LIMIT.

## Actual behavior
(Completar)

## Pass / Fail
(Completar — si la skill inventa que "la tabla es grande" o afirma con certeza
que falta un índice sin poder verificarlo, es un Fail)

## Problem detected
(Completar)

## Modification made to the skill
(Completar)

