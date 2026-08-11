
## Requisitos
- Python 3.9+

## Uso

Ejecuta el runner sobre un archivo SQL:

```powershell
python .\qa-runner\runner.py .\examples\valis.sql
```

O con un script de Windows:

```powershell
.\qa-runner\run.ps1 .\examples\valis.sql
```

## Salida
La herramienta devuelve un JSON con:
- `status`: `pass` o `fail`
- `summary`: resumen general
- `statements`: detalle por sentencia
- `findings`: lista de resultados detectados

## Ejemplos incluidos
- `qa-runner\samples\good.sql`
- `qa-runner\samples\bad.sql`

```powershell
python .\qa-runner\runner.py .\qa-runner\samples\good.sql
python .\qa-runner\runner.py .\qa-runner\samples\bad.sql
```
