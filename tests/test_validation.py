"""Pruebas unitarias automatizadas para validar el contrato de datos y el pipeline.

Responsables: Equipo de Calidad (Romina C.G., Benny M.S.).
"""

from __future__ import annotations

from pathlib import Path

from src.config import PROCESSED_DIR, RAW_DIR
from src.graph_builder import run_frente3_graph_pipeline
from src.homologacion import run_frente1_pipeline
from src.sat_69b_etl import verify_not_69b_bis_html
from src.validation import inspect_csv_bom, validate_dataset


def test_raw_dataset_dimensions_and_quality_detection() -> None:
    """Verifica que Dataset.csv tenga 18 filas, 19 columnas y detecte los hallazgos clave."""
    raw_csv = RAW_DIR / "Dataset.csv"
    report = validate_dataset(raw_csv)

    assert report["total_registros"] == 18
    assert report["total_columnas"] == 19
    assert report["total_pymes"] == 3
    assert set(report["pymes_identificadas"]) == {"COS-BJ-01", "PYME-001", "CONS-SERV-01"}
    assert report["tiene_utf8_bom"] is True
    for expected_code in ("RQ-01", "RQ-02", "RQ-03", "RQ-04", "RQ-06", "RQ-09"):
        assert expected_code in report["codigos_detectados"]


def test_frente1_cleaning_removes_bom_and_quasi_identifiers() -> None:
    """Verifica que el archivo procesado no tenga BOM y haya sanitizado 'Villagrán'."""
    eda = run_frente1_pipeline()
    cleaned_csv = PROCESSED_DIR / "dataset_pymes_homologado_limpio.csv"

    assert cleaned_csv.exists()
    assert inspect_csv_bom(cleaned_csv) is False

    content = cleaned_csv.read_text(encoding="utf-8")
    assert "Villagrán" not in content
    assert "[MUNICIPIO_RESERVADO]" in content
    assert eda["resumen_general"]["distribucion_confianza_homologacion"] == {"alta": 12, "baja": 6}


def test_frente2_detects_69b_bis_mismatch() -> None:
    """Verifica que el detector identifique que el HTML en Contexto es Art. 69-B Bis y no 69-B."""
    context_htm = Path(__file__).resolve().parent.parent.parent / "Contexto" / "SAT listado del Art. 69-B del CFF.htm"
    if context_htm.exists():
        res = verify_not_69b_bis_html(context_htm)
        assert res["es_articulo_69b_bis_perdidas_fiscales"] is True
        assert res["valido_para_frente_2_efos"] is False


def test_frente3_graph_builder_creates_projected_network() -> None:
    """Verifica la construcción del grafo bipartito y proyectado en NetworkX."""
    summary = run_frente3_graph_pipeline()
    assert summary["grafo_proyectado_empresas"]["total_empresas"] == 6
    assert summary["grafo_proyectado_empresas"]["total_conexiones_societarias"] >= 4
    assert (PROCESSED_DIR / "grafo_metricas_nodos.csv").exists()
