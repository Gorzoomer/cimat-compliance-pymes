"""Módulo de validación de contrato de datos y detección de riesgos de calidad (Frente 1).

Responsables: Equipo de Calidad (Benny M.S., Romina C.G.) y Equipo de Datos (Santiago A.D.).
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from src.config import (
    EXPECTED_COLUMNS,
    ISO_37301_CATEGORIES,
    VALID_HOMOLOGATED_LEVELS,
)

RFC_REGEX = re.compile(r"\b[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}\b")
QUASI_ID_PATTERNS = [
    re.compile(r"\bVillagr[aá]n\b", re.IGNORECASE),
    re.compile(r"\b11\s*a[ñn]os\b", re.IGNORECASE),
    re.compile(r"\b4\s*personas\b", re.IGNORECASE),
]


def inspect_csv_bom(csv_path: Path) -> bool:
    """Detecta si el archivo CSV inicia con la marca de orden de bytes UTF-8 BOM (\\ufeff)."""
    raw_bytes = csv_path.read_bytes()
    return raw_bytes.startswith(b"\xef\xbb\xbf")


def load_raw_dataset(csv_path: Path) -> list[dict[str, str]]:
    """Carga el archivo CSV removiendo de forma segura el BOM si existe."""
    with csv_path.open("r", encoding="utf-8-sig", newline="") as fp:
        reader = csv.DictReader(fp)
        return list(reader)


def validate_dataset(csv_path: Path) -> dict[str, Any]:
    """Ejecuta las reglas de validación del contrato de datos sobre el dataset piloto."""
    has_bom = inspect_csv_bom(csv_path)
    rows = load_raw_dataset(csv_path)

    issues: list[dict[str, str]] = []
    if has_bom:
        issues.append(
            {
                "codigo": "RQ-09",
                "severidad": "media",
                "detalle": "El archivo inicia con marca UTF-8 BOM (\\ufeff) en el encabezado 'equipo'.",
            }
        )

    actual_columns = list(rows[0].keys()) if rows else []
    missing_cols = [c for c in EXPECTED_COLUMNS if c not in actual_columns]
    extra_cols = [c for c in actual_columns if c not in EXPECTED_COLUMNS]

    rows_by_pyme: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        rows_by_pyme[row["id_pyme"]].append(row)

    for id_pyme, pyme_rows in rows_by_pyme.items():
        cats = [r["categoria_riesgo_iso37301"] for r in pyme_rows]
        if set(cats) != set(ISO_37301_CATEGORIES.keys()) or len(pyme_rows) != 6:
            issues.append(
                {
                    "codigo": "ESTRUCTURA-ISO",
                    "severidad": "alta",
                    "detalle": f"La PYME {id_pyme} no contiene exactamente las 6 categorías ISO 37301.",
                }
            )

        # RQ-04: Detección de captura global idéntica en las 6 dimensiones
        unique_risks = {r["riesgo_identificado"].strip() for r in pyme_rows}
        if len(unique_risks) == 1:
            issues.append(
                {
                    "codigo": "RQ-04",
                    "severidad": "alta",
                    "id_pyme": id_pyme,
                    "detalle": f"{id_pyme} presenta el mismo texto de riesgo repetido en las 6 categorías ISO 37301.",
                }
            )

    for idx, row in enumerate(rows, start=2):
        id_pyme = row["id_pyme"]

        # RQ-01: Escala de riesgo (probabilidad x impacto) vs madurez
        if "probabilidad" in row["tipo_escala_equipo"].lower():
            issues.append(
                {
                    "codigo": "RQ-01",
                    "severidad": "alta",
                    "fila": str(idx),
                    "id_pyme": id_pyme,
                    "detalle": "Instrumento original es Matriz Probabilidad x Impacto, no escala de madurez.",
                }
            )

        # RQ-02: Fuga de cuasi-identificadores en observaciones_calidad_dato
        obs = row["observaciones_calidad_dato"]
        if any(pat.search(obs) for pat in QUASI_ID_PATTERNS):
            issues.append(
                {
                    "codigo": "RQ-02",
                    "severidad": "critica",
                    "fila": str(idx),
                    "id_pyme": id_pyme,
                    "detalle": "Fuga de cuasi-identificadores (municipio Villagrán / años / personas exactas) en observaciones.",
                }
            )

        # RQ-03: Valores exactos sin generalizar a bandas en antiguedad_rango o tamano_empresa
        if re.fullmatch(r"\d+\s*a[ñn]os", row["antiguedad_rango"].strip(), re.IGNORECASE) or re.fullmatch(
            r"\d+\s*empleados", row["tamano_empresa"].strip(), re.IGNORECASE
        ):
            issues.append(
                {
                    "codigo": "RQ-03",
                    "severidad": "alta",
                    "fila": str(idx),
                    "id_pyme": id_pyme,
                    "detalle": f"Valores puntuales sin agrupar en banda: '{row['antiguedad_rango']}', '{row['tamano_empresa']}'.",
                }
            )

        # RQ-06: Incoherencia entre Persona física y consejo de administración
        if "persona física" in row["forma_juridica"].lower() and "consejo de administración" in row[
            "accion_recomendada"
        ].lower():
            issues.append(
                {
                    "codigo": "RQ-06",
                    "severidad": "media",
                    "fila": str(idx),
                    "id_pyme": id_pyme,
                    "detalle": "Se recomienda crear un consejo de administración a una Persona física.",
                }
            )

        # Validación de dominio de nivel_homologado_borrador
        try:
            lvl = int(row["nivel_homologado_borrador"])
            expected_label = VALID_HOMOLOGATED_LEVELS.get(lvl)
            if expected_label != row["etiqueta_homologada_borrador"]:
                issues.append(
                    {
                        "codigo": "DOMINIO-ESCALA",
                        "severidad": "alta",
                        "fila": str(idx),
                        "id_pyme": id_pyme,
                        "detalle": "Discrepancia entre nivel numérico y etiqueta homologada.",
                    }
                )
        except ValueError:
            issues.append(
                {
                    "codigo": "DOMINIO-ESCALA",
                    "severidad": "alta",
                    "fila": str(idx),
                    "id_pyme": id_pyme,
                    "detalle": "nivel_homologado_borrador no es un entero válido.",
                }
            )

    return {
        "archivo": str(csv_path.name),
        "total_registros": len(rows),
        "total_columnas": len(actual_columns),
        "total_pymes": len(rows_by_pyme),
        "pymes_identificadas": list(rows_by_pyme.keys()),
        "tiene_utf8_bom": has_bom,
        "columnas_faltantes": missing_cols,
        "columnas_extra": extra_cols,
        "total_hallazgos_calidad": len(issues),
        "codigos_detectados": sorted({i["codigo"] for i in issues}),
        "hallazgos": issues,
    }
