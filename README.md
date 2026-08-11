# sql-reviewer

Skill para IA que actúa como revisor técnico de sentencias SQL: detecta
problemas de seguridad, rendimiento y convenciones, y clasifica cada hallazgo
en CRITICAL / HIGH / MEDIUM / LOW / INFO.

## Estructura

```
sql-reviewer-skill/
├── SKILL.md              # Definición completa de la skill (leer primero)
├── rules/
│   ├── security.md        # Reglas SEC-01 a SEC-06
│   ├── performance.md     # Reglas PERF-01 a PERF-07
│   └── conventions.md     # Reglas CONV-01 a CONV-06
├── examples/
│   ├── valid.sql
│   ├── invalid.sql
│   └── edge-cases.sql
└── tests/
    ├── test-01.md          # happy path
    ├── test-02.md          # error evidente
    ├── test-03.md          # edge case
    ├── test-04.md          # información insuficiente
    └── test-05.md          # adversarial
```

## Cómo usarla
Pegar el contenido de `SKILL.md` (y las reglas referenciadas) como contexto/skill
de un modelo de IA, junto con el SQL a revisar. El modelo debe seguir el
`Procedure` de `SKILL.md` paso a paso y producir la salida en el formato de
`Expected output`.

## Estado de las pruebas
Completar cada archivo en `tests/` con el resultado real obtenido al ejecutar
la skill (secciones "Actual behavior", "Pass/Fail", "Problem detected" y
"Modification made to the skill"). Este repositorio se entrega con las
secciones "Expected behavior" ya definidas; el equipo debe correr las pruebas
y documentar lo que realmente ocurrió, incluyendo cualquier ajuste hecho a
`SKILL.md` o a las reglas como consecuencia.

## Decisiones técnicas a poder justificar en la defensa
- Por qué `WHERE 1=1` y `LIKE '%'` se tratan como "sin WHERE efectivo" (SEC-02)
  en vez de solo verificar la presencia sintáctica de la cláusula.
- Por qué la falta de índice es INFO y no HIGH (no se puede confirmar sin
  inspeccionar el esquema real — ver `SKILL.md → Failure handling`).
- Cómo se resuelven conflictos entre reglas (`SKILL.md → Rule conflicts`).
- Qué partes son deterministas (las reglas IF/THEN) y cuáles dependen del
  razonamiento del modelo (identificar patrones de tautología, interpretar
  intención de nombres de columnas, etc.).
