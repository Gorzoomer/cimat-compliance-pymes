"""Módulo de construcción y análisis de grafos societarios (Frente 3).

Responsables: Equipo de Arquitectura e Investigación (Santiago A.H., Alonzo H.S.).
Implementa la red bipartita empresa-atributo y su proyección unimodal empresa-empresa
siguiendo la metodología de Luna-Pla y Nicolás-Carlock (2020-2023), guardando métricas
directamente a disco sin usar stdout.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import networkx as nx

from src.config import PROCESSED_DIR, get_file_logger
from src.sat_69b_etl import generate_synthetic_69b_network_dataset

SHARED_ATTRIBUTES = [
    ("id_representante_legal", "Representante_Legal"),
    ("id_socio_accionista", "Socio_Accionista"),
    ("id_domicilio_fiscal", "Domicilio_Fiscal"),
    ("id_notaria_constitucion", "Notaria_Constitucion"),
]


def build_corporate_graphs(input_csv: Path | None = None) -> tuple[nx.Graph, nx.Graph]:
    """Construye el grafo bipartito (empresa-atributo) y el grafo proyectado (empresa-empresa)."""
    csv_path = input_csv or generate_synthetic_69b_network_dataset()
    with csv_path.open("r", encoding="utf-8", newline="") as fp:
        rows = list(csv.DictReader(fp))

    bipartite_g = nx.Graph()
    company_nodes: list[str] = []

    for row in rows:
        comp_id = row["id_empresa"]
        company_nodes.append(comp_id)
        bipartite_g.add_node(
            comp_id,
            bipartite=0,
            tipo_nodo="Empresa",
            estatus_69b=row["estatus_69b"],
            clase_pu=row["clase_pu"],
            peso_evidencia=float(row["peso_evidencia"]),
        )
        for col, attr_type in SHARED_ATTRIBUTES:
            attr_val = row.get(col, "NA")
            if attr_val and attr_val != "NA":
                bipartite_g.add_node(attr_val, bipartite=1, tipo_nodo=attr_type)
                bipartite_g.add_edge(comp_id, attr_val, tipo_relacion=attr_type)

    # Proyección unimodal: arista entre dos empresas si comparten >= 1 atributo societario
    projected_g = nx.Graph()
    for comp in company_nodes:
        projected_g.add_node(comp, **bipartite_g.nodes[comp])

    for i, u in enumerate(company_nodes):
        u_neighbors = set(bipartite_g.neighbors(u))
        for v in company_nodes[i + 1 :]:
            shared = sorted(u_neighbors.intersection(bipartite_g.neighbors(v)))
            if shared:
                projected_g.add_edge(
                    u,
                    v,
                    weight=len(shared),
                    atributos_compartidos=";".join(shared),
                )

    return bipartite_g, projected_g


def run_frente3_graph_pipeline(input_csv: Path | None = None) -> dict[str, Any]:
    """Calcula métricas estructurales de red y las guarda directamente en data/processed/."""
    logger = get_file_logger("frente3_grafos")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    bipartite_g, projected_g = build_corporate_graphs(input_csv)
    degree_cent = nx.degree_centrality(projected_g)
    betweenness_cent = nx.betweenness_centrality(projected_g, weight="weight")
    clustering_coef = nx.clustering(projected_g, weight="weight")
    components = list(nx.connected_components(projected_g))

    metrics_rows: list[dict[str, Any]] = []
    for node, data in projected_g.nodes(data=True):
        metrics_rows.append(
            {
                "id_empresa": node,
                "estatus_69b": data["estatus_69b"],
                "clase_pu": data["clase_pu"],
                "grado_empresas_conectadas": projected_g.degree(node),
                "centralidad_grado": round(degree_cent[node], 4),
                "centralidad_intermediacion": round(betweenness_cent[node], 4),
                "coeficiente_agrupamiento": round(clustering_coef[node], 4),
            }
        )

    out_metrics_csv = PROCESSED_DIR / "grafo_metricas_nodos.csv"
    with out_metrics_csv.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(metrics_rows[0].keys()))
        writer.writeheader()
        writer.writerows(metrics_rows)

    summary = {
        "grafo_bipartito": {
            "total_nodos": bipartite_g.number_of_nodes(),
            "total_aristas": bipartite_g.number_of_edges(),
        },
        "grafo_proyectado_empresas": {
            "total_empresas": projected_g.number_of_nodes(),
            "total_conexiones_societarias": projected_g.number_of_edges(),
            "componentes_conexas": len(components),
            "tamano_mayor_componente": max((len(c) for c in components), default=0),
        },
        "nodos_metricas": metrics_rows,
    }

    out_summary_json = PROCESSED_DIR / "resumen_grafo_societario.json"
    with out_summary_json.open("w", encoding="utf-8") as fp:
        json.dump(summary, fp, ensure_ascii=False, indent=2)

    logger.info("Frente 3 completado. Métricas de grafo guardadas en: %s", out_metrics_csv.name)
    return summary


if __name__ == "__main__":
    run_frente3_graph_pipeline()
