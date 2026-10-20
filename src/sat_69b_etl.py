"""Módulo ETL para estructurar el listado público del Art. 69-B del CFF (Frente 2).

Responsables: Equipo de Datos (Gerardo J.M.) y Requerimientos (Mariana M.R.).
Incluye validación para rechazar archivos del Art. 69-B Bis (transmisión indebida de pérdidas
fiscales) y esquema de etiquetado Positive-Unlabeled (PU) conforme a Medina-Hernández et al. (2025).
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from src.config import PROCESSED_DIR, get_file_logger

# Mapeo de estatus procesal del Art. 69-B bajo enfoque Positive-Unlabeled (PU)
STATUS_PU_MAPPING: dict[str, dict[str, Any]] = {
    "Definitivo": {"etiqueta_pu": 1, "clase_pu": "Positivo_Confirmado", "peso_evidencia": 1.0},
    "Presunto": {"etiqueta_pu": 1, "clase_pu": "Positivo_Presunto", "peso_evidencia": 0.6},
    "Desvirtuado": {"etiqueta_pu": 0, "clase_pu": "Aclarado_Desvirtuado", "peso_evidencia": 0.2},
    "Sentencia Favorable": {"etiqueta_pu": 0, "clase_pu": "Aclarado_Sentencia", "peso_evidencia": 0.1},
    "No_Listado": {"etiqueta_pu": -1, "clase_pu": "Unlabeled_No_Identificado", "peso_evidencia": 0.0},
}


def verify_not_69b_bis_html(html_path: Path) -> dict[str, Any]:
    """Verifica si un archivo HTML corresponde por error al Art. 69-B Bis en vez del Art. 69-B."""
    content = html_path.read_text(encoding="utf-8", errors="replace")
    is_bis = "69-B Bis" in content or "69-b-bis" in content.lower()
    return {
        "archivo": html_path.name,
        "es_articulo_69b_bis_perdidas_fiscales": is_bis,
        "valido_para_frente_2_efos": not is_bis,
        "mensaje": (
            "ALERTA: El archivo corresponde al Art. 69-B Bis (transmisión indebida de pérdidas fiscales), "
            "no al padrón de operaciones simuladas (EFOS) del Art. 69-B."
            if is_bis
            else "Archivo correspondiente al Art. 69-B (operaciones simuladas)."
        ),
    }


def generate_synthetic_69b_network_dataset(output_csv: Path | None = None) -> Path:
    """Genera un dataset estructurado prototipo (100% sintético/público) con el esquema del Frente 2."""
    logger = get_file_logger("frente2_sat69b")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = output_csv or (PROCESSED_DIR / "sat_69b_estructurado_prototipo.csv")

    records = [
        {
            "id_empresa": "EFOS-GTO-001",
            "estatus_69b": "Definitivo",
            "fecha_publicacion_dof": "2024-07-05",
            "municipio_fiscal": "León, Gto.",
            "id_representante_legal": "REP-101",
            "id_socio_accionista": "SOC-201",
            "id_domicilio_fiscal": "DOM-301",
            "id_notaria_constitucion": "NOT-401",
        },
        {
            "id_empresa": "EFOS-GTO-002",
            "estatus_69b": "Definitivo",
            "fecha_publicacion_dof": "2024-07-05",
            "municipio_fiscal": "León, Gto.",
            "id_representante_legal": "REP-101",
            "id_socio_accionista": "SOC-202",
            "id_domicilio_fiscal": "DOM-301",
            "id_notaria_constitucion": "NOT-401",
        },
        {
            "id_empresa": "EFOS-GTO-003",
            "estatus_69b": "Presunto",
            "fecha_publicacion_dof": "2025-05-30",
            "municipio_fiscal": "Celaya, Gto.",
            "id_representante_legal": "REP-102",
            "id_socio_accionista": "SOC-201",
            "id_domicilio_fiscal": "DOM-301",
            "id_notaria_constitucion": "NOT-402",
        },
        {
            "id_empresa": "EFOS-GTO-004",
            "estatus_69b": "Presunto",
            "fecha_publicacion_dof": "2025-05-30",
            "municipio_fiscal": "Irapuato, Gto.",
            "id_representante_legal": "REP-102",
            "id_socio_accionista": "SOC-203",
            "id_domicilio_fiscal": "DOM-302",
            "id_notaria_constitucion": "NOT-401",
        },
        {
            "id_empresa": "EMP-GTO-005",
            "estatus_69b": "Desvirtuado",
            "fecha_publicacion_dof": "2026-06-05",
            "municipio_fiscal": "Salamanca, Gto.",
            "id_representante_legal": "REP-103",
            "id_socio_accionista": "SOC-203",
            "id_domicilio_fiscal": "DOM-303",
            "id_notaria_constitucion": "NOT-403",
        },
        {
            "id_empresa": "EMP-GTO-006",
            "estatus_69b": "No_Listado",
            "fecha_publicacion_dof": "NA",
            "municipio_fiscal": "Guanajuato, Gto.",
            "id_representante_legal": "REP-104",
            "id_socio_accionista": "SOC-204",
            "id_domicilio_fiscal": "DOM-304",
            "id_notaria_constitucion": "NOT-404",
        },
    ]

    enriched: list[dict[str, Any]] = []
    for rec in records:
        pu_info = STATUS_PU_MAPPING[rec["estatus_69b"]]
        row = dict(rec)
        row.update(pu_info)
        enriched.append(row)

    fieldnames = list(enriched[0].keys())
    with out_path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enriched)

    logger.info("Dataset prototipo 69-B estructurado escrito en: %s", out_path.name)
    return out_path
