# Test 03 — Edge case

## Input
```sql
DELETE FROM TA_USERS WHERE 1 = 1;
```

## Expected behavior
No basta con detectar "existe un WHERE". Debe aplicarse SEC-02: el WHERE es
tautológico (1=1 es siempre verdadero), por lo tanto equivale a un DELETE sin
condición real. Severidad = CRITICAL, con el hallazgo explícitamente etiquetado
como "WHERE present but not restrictive", no como "no problem found".

## Actual behavior
(Completar)

## Pass / Fail
(Completar — si la skill solo valida "existe WHERE" y no evalúa si restringe
algo, este test debe marcarse Fail)

## Problem detected
(Completar)

## Modification made to the skill
(Completar)

