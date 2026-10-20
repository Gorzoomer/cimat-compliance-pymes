"""Configuración central de rutas, constantes ISO 37301 y bitácora a disco (sin stdout).

Cumple con la directriz del Manual de Acceso a Recursos de Supercómputo del CIMAT (p. 18):
ningún proceso debe imprimir en pantalla (stdout) ni usar redirección '>'; toda salida
se escribe directamente en archivos mediante manejadores de disco.
"""

from __future__ import annotations

import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
LOG_FILE = PROCESSED_DIR / "pipeline_cimat.log"

EXPECTED_COLUMNS: list[str] = [
    "equipo",
    "id_pyme",
    "sector_economico",
    "forma_juridica",
    "antiguedad_rango",
    "tamano_empresa",
    "region_municipio",
    "categoria_riesgo_iso37301",
    "riesgo_identificado",
    "evidencia_disponible",
    "clausula_iso37301",
    "accion_recomendada",
    "tipo_escala_equipo",
    "valor_escala_original",
    "nivel_homologado_borrador",
    "etiqueta_homologada_borrador",
    "confianza_homologacion",
    "fuente_informacion",
    "observaciones_calidad_dato",
]

ISO_37301_CATEGORIES: dict[str, str] = {
    "Gobierno corporativo y contrapesos": "5.3",
    "Función de cumplimiento": "5.3",
    "Políticas y procedimientos documentados": "7.5",
    "Canal de denuncias e investigación interna": "8.3-8.4",
    "Gestión de riesgos y control interno": "8.1-8.2",
    "Gobernanza de datos e inteligencia artificial": "7.5 (analogía IA)",
}

VALID_HOMOLOGATED_LEVELS: dict[int, str] = {
    1: "Inexistente",
    2: "Ad hoc / informal",
    3: "Definido / documentado",
    4: "Consolidado",
}


def get_file_logger(name: str = "cimat_pipeline") -> logging.Logger:
    """Devuelve un logger que escribe exclusivamente a disco (sin StreamHandler/stdout)."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if not logger.handlers:
        handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
