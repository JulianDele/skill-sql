#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


def normalize_sql(text: str) -> str:
    return text.strip()


def split_statements(text: str):
    raw_statements = re.split(r";\s*(?=\S)", text, flags=re.DOTALL)
    statements = [part.strip() for part in raw_statements if part and part.strip()]
    return statements if statements else ([text.strip()] if text.strip() else [])


def detect_findings(sql_text: str):
    lower = sql_text.lower()
    findings = []

    if re.search(r"\bdelete\s+from\b", lower) and not re.search(r"\bwhere\b", lower):
        findings.append({
            "severity": "CRITICAL",
            "rule": "security.md::SEC-01",
            "message": "DELETE sin WHERE: riesgo de borrado masivo irreversible.",
            "recommendation": "Agregar un WHERE específico o ejecutar un backup antes de confirmar."
        })

    if re.search(r"\bupdate\b", lower) and not re.search(r"\bwhere\b", lower):
        findings.append({
            "severity": "CRITICAL",
            "rule": "security.md::SEC-01",
            "message": "UPDATE sin WHERE: la sentencia puede afectar todas las filas.",
            "recommendation": "Añadir un filtro preciso y validar el impacto antes de ejecutar."
        })

    if "select *" in lower:
        findings.append({
            "severity": "MEDIUM",
            "rule": "performance.md::PERF-01",
            "message": "SELECT * recupera columnas no necesarias.",
            "recommendation": "Especificar columnas explícitas para reducir lectura y costo."
        })

    if re.search(r"\bselect\b", lower) and "limit" not in lower and not re.search(r"\b(count|sum|avg|min|max)\s*\(", lower):
        findings.append({
            "severity": "MEDIUM",
            "rule": "performance.md::PERF-02",
            "message": "SELECT sin LIMIT puede devolver un volumen muy grande.",
            "recommendation": "Agregar paginación o un límite adecuado."
        })

    if "where 1=1" in lower or "like '%'" in lower or 'like "%"' in lower:
        findings.append({
            "severity": "HIGH",
            "rule": "security.md::SEC-02",
            "message": "WHERE tautológico o no restrictivo: no filtra realmente la información.",
            "recommendation": "Reemplazarlo por condiciones concretas y verificables."
        })

    if re.search(r"\+\s*['\"]|['\"]\s*\+\s*\w+|%s|f[\"'].*\{", lower):
        findings.append({
            "severity": "CRITICAL",
            "rule": "security.md::SEC-03",
            "message": "Se detectó concatenación de SQL con entrada variable.",
            "recommendation": "Usar consultas parametrizadas o prepared statements."
        })

    if re.search(r"\bwhere\b.*=\s*null|\bwhere\b.*!=\s*null", lower):
        findings.append({
            "severity": "MEDIUM",
            "rule": "conventions.md::CONV-02",
            "message": "Se compara una columna con NULL usando = o != .",
            "recommendation": "Usar IS NULL o IS NOT NULL."
        })

    if re.search(r"alter\s+table\s+.+\s+add\s+column\s+.+\bnot\s+null\b", lower) and "default" not in lower:
        findings.append({
            "severity": "HIGH",
            "rule": "conventions.md::CONV-03",
            "message": "Se agrega una columna NOT NULL sin default y puede romper datos existentes.",
            "recommendation": "Definir un valor por defecto o migrar datos antes del cambio."
        })

    if re.search(r"\b[a-z_]+\s*=\s*['\"][^'\"]*['\"]\s*\+\s*\w+", lower):
        findings.append({
            "severity": "CRITICAL",
            "rule": "security.md::SEC-03",
            "message": "Se detectó construcción dinámica de la sentencia SQL.",
            "recommendation": "No concatenar entrada del usuario en el SQL final."
        })

    return findings


def analyze_file(path: Path):
    text = path.read_text(encoding="utf-8")
    statements = split_statements(text)
    result_statements = []
    all_findings = []

    for index, statement in enumerate(statements, start=1):
        findings = detect_findings(statement)
        if findings:
            highest = max(["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"].index(item["severity"]) for item in findings)
            max_severity = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"][highest]
        else:
            max_severity = "PASS"

        result_statements.append({
            "statement_number": index,
            "sql": statement,
            "severity": max_severity,
            "findings": findings,
        })
        all_findings.extend(findings)

    status = "fail" if all_findings else "pass"
    summary = (
        "No se detectaron violaciones relevantes."
        if not all_findings
        else f"Se detectaron {len(all_findings)} hallazgos en {len(statements)} sentencia(s)."
    )

    return {
        "status": status,
        "summary": summary,
        "statements": result_statements,
        "findings": all_findings,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "fail",
            "summary": "Debe indicar la ruta del archivo SQL a revisar.",
            "findings": []
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    path = Path(sys.argv[1]).resolve()
    if not path.exists():
        print(json.dumps({
            "status": "fail",
            "summary": f"No existe el archivo: {path}",
            "findings": []
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    try:
        result = analyze_file(path)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["status"] == "pass" else 1)
    except Exception as exc:  # pragma: no cover
        print(json.dumps({
            "status": "fail",
            "summary": f"Error al analizar el SQL: {exc}",
            "findings": []
        }, ensure_ascii=False, indent=2))
        sys.exit(2)
