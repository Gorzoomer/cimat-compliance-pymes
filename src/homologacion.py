"""Módulo de limpieza, sanitización de cuasi-identificadores y homologación (Frente 1).

Responsables: Equipo de Datos (Santiago A.D., Gerardo J.M.) y Calidad (Benny M.S., Romina C.G.).
Escribe salidas directamente a data/processed/ sin imprimir en stdout.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from src.config import (
    ISO_37301_CATEGORIES,
    PROCESSED_DIR,
    RAW_DIR,
    get_file_logger,
)
from src.validation import load_raw_dataset, validate_dataset


def normalize_antiguedad(val: str) -> str:
    """Generaliza valores puntuales de antigüedad a bandas estándar."""
    v = val.strip()
    m = re.fullmatch(r"(\d+)\s*a[ñn]os", v, re.IGNORECASE)
    if m:
        years = int(m.group(1))
        if years < 5:
            return "Menos de 5 años"
        if years <= 10:
            return "5 a 10 años"
        return "Más de 10 años"
    return v


def normalize_tamano(val: str) -> str:
    """Generaliza conteos exactos de empleados a estratos MIPYME."""
    v = val.strip()
    m = re.fullmatch(r"(\d+)\s*empleados", v, re.IGNORECASE)
    if m:
        emp = int(m.group(1))
        if emp <= 10:
            return "Micro (1-10 empleados)"
        if emp <= 50:
            return "Pequeña (11-50 empleados)"
        return "Mediana (51-250 empleados)"
    if v.lower() == "microempresa":
        return "Micro (1-10 empleados)"
    return v


def sanitize_observations(text: str) -> str:
    """Enmascara cuasi-identificadores residuales (municipios, años o empleados exactos)."""
    sanitized = re.sub(r"\(\s*\d+\s*a[ñn]os\s*\)", "([ANTIGUEDAD_RESERVADA])", text, flags=re.IGNORECASE)
    sanitized = re.sub(r"\(\s*\d+\s*personas\s*\)", "([TAMANO_RESERVADO])", sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r"\bVillagr[aá]n\b", "[MUNICIPIO_RESERVADO]", sanitized, flags=re.IGNORECASE)
    return sanitized


def run_frente1_pipeline(
    input_csv: Path | None = None,
    output_csv: Path | None = None,
    output_eda_json: Path | None = None,
) -> dict[str, Any]:
    """Ejecuta la limpieza, sanitización y EDA del Frente 1 volcando todo a disco."""
    logger = get_file_logger("frente1_homologacion")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    in_path = input_csv or (RAW_DIR / "Dataset.csv")
    out_csv_path = output_csv or (PROCESSED_DIR / "dataset_pymes_homologado_limpio.csv")
    out_json_path = output_eda_json or (PROCESSED_DIR / "reporte_eda_calidad.json")

    logger.info("Iniciando validación y limpieza del dataset: %s", in_path.name)
    validation_report = validate_dataset(in_path)
    raw_rows = load_raw_dataset(in_path)

    # Identificar PYMES con texto global duplicado en las 6 dimensiones
    risks_by_pyme: dict[str, set[str]] = defaultdict(set)
    for r in raw_rows:
        risks_by_pyme[r["id_pyme"]].add(r["riesgo_identificado"].strip())

    cleaned_rows: list[dict[str, str]] = []
    level_counts: Counter[int] = Counter()
    confidence_counts: Counter[str] = Counter()
    category_level_sum: dict[str, list[int]] = defaultdict(list)

    for row in raw_rows:
        new_row = dict(row)
        id_pyme = new_row["id_pyme"]
        cat = new_row["categoria_riesgo_iso37301"]

        new_row["antiguedad_rango"] = normalize_antiguedad(new_row["antiguedad_rango"])
        new_row["tamano_empresa"] = normalize_tamano(new_row["tamano_empresa"])
        if new_row["region_municipio"].strip().lower().startswith("no especificada"):
            new_row["region_municipio"] = "NA"

        new_row["clausula_iso37301_normalizada"] = ISO_37301_CATEGORIES.get(cat, "NA")
        new_row["observaciones_calidad_dato"] = sanitize_observations(new_row["observaciones_calidad_dato"])

        # Banderas de auditoría derivadas para análisis estadístico seguro
        new_row["es_reporte_global"] = "Si" if len(risks_by_pyme[id_pyme]) == 1 else "No"
        new_row["hallazgo_entrevista_directo"] = (
            "No"
            if "no se generó un hallazgo formal independiente" in new_row["riesgo_identificado"].lower()
            else "Si"
        )
        new_row["alerta_forma_juridica"] = (
            "Si"
            if (
                "persona física" in new_row["forma_juridica"].lower()
                and "consejo de administración" in new_row["accion_recomendada"].lower()
            )
            else "No"
        )

        lvl = int(new_row["nivel_homologado_borrador"])
        level_counts[lvl] += 1
        confidence_counts[new_row["confianza_homologacion"]] += 1
        category_level_sum[cat].append(lvl)
        cleaned_rows.append(new_row)

    fieldnames = list(cleaned_rows[0].keys()) if cleaned_rows else []
    with out_csv_path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    eda_summary: dict[str, Any] = {
        "resumen_general": {
            "total_registros": len(cleaned_rows),
            "total_pymes": len(risks_by_pyme),
            "codificacion_salida": "UTF-8 sin BOM",
            "distribucion_nivel_homologado": {str(k): v for k, v in sorted(level_counts.items())},
            "distribucion_confianza_homologacion": dict(confidence_counts),
            "promedio_madurez_por_categoria_iso37301": {
                cat: round(sum(vals) / len(vals), 2) for cat, vals in category_level_sum.items()
            },
        },
        "auditoria_calidad_entrada": validation_report,
    }

    with out_json_path.open("w", encoding="utf-8") as fp:
        json.dump(eda_summary, fp, ensure_ascii=False, indent=2)

    logger.info("Frente 1 completado. CSV limpio escrito en: %s", out_csv_path.name)
    return eda_summary


if __name__ == "__main__":
    run_frente1_pipeline()
