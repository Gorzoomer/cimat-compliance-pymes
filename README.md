# cimat-compliance-pymes

**Proyecto CIMAT × Universidad de Celaya (Ingeniería en Ciencia de Datos & Derecho)**  
*Evaluación Exploratoria de Madurez de Compliance (ISO 37301) en MIPYMES y Modelado Relacional de Redes Societarias (Art. 69-B del CFF)*

---

## Propósito del Repositorio

Este repositorio contiene el análisis del problema, los contratos y diccionarios de datos, las reglas de control de calidad, la arquitectura modular y el prototipo reproducible en Python preparados por el equipo de **Ingeniería en Ciencia de Datos** (*Programación Avanzada*, Ago–Dic 2026) en colaboración con el área de **Derecho** y bajo la dirección del **Dr. Manuel Ledesma López** (investigador responsable ante el Laboratorio de Supercómputo del CIMAT).

> **Alcance honesto 2026:** Estudio exploratorio de evaluación de madurez de *compliance* (ISO 37301) y modelado relacional preliminar mediante grafos sobre datos públicos del listado del Art. 69-B del SAT, situado en la literatura existente (Zumaya et al., 2021; Luna-Pla y Nicolás-Carlock, 2020–2023; Medina-Hernández et al., 2025). No constituye todavía un modelo predictivo validado ni emite dictámenes acusatorios sobre PYMES individuales.

---

## Estructura del Repositorio

```text
cimat-compliance-pymes/
├── README.md                           # Documentación general y guía de ejecución
├── requirements.txt                    # Dependencias reproducibles (locales y clúster CIMAT)
├── .gitignore                          # Protección contra subida de datos sensibles o temporales
├── docs/
│   ├── informe-ejecutivo.md            # Entregable oficial: Informe Ejecutivo para el Dr. Ledesma
│   ├── presentacion-ejecutiva.md       # 6 diapositivas + Guion oral (10-12 min) + Defensa Q&A
│   ├── problema.md                     # Contexto jurídico-fiscal y separación Pieza A vs. Pieza B
│   ├── diccionario-datos.md            # Contrato de datos de las 19 columnas de Dataset.csv
│   ├── preguntas-derecho.md            # Cuestionario técnico-jurídico previo a programación
│   ├── riesgos-calidad.md              # Diagnóstico de los 10 problemas de calidad identificados
│   ├── arquitectura-inicial.md         # Diseño modular de los 4 frentes y acople con Slurm
│   ├── decisiones.md                   # Registro de decisiones de arquitectura y datos (ADRs)
│   └── investigacion.md                # Investigación: Pipelines, Grafos, NLP, Slurm y PU Learning
├── data/
│   ├── raw/
│   │   └── Dataset.csv                 # Dataset piloto anonimizado (18 registros x 19 columnas)
│   └── processed/                      # Salidas limpias sin BOM, reportes de auditoría y grafos
├── src/
│   ├── __init__.py
│   ├── config.py                       # Configuración de rutas y logging directo a archivo (sin stdout)
│   ├── validation.py                   # Validador de esquema, anonimización y calidad (Frente 1)
│   ├── homologacion.py                 # Conversión .xlsx->.csv sin BOM y homologación (Frente 1)
│   ├── sat_69b_etl.py                  # Estructuración pública del Listado Art. 69-B SAT (Frente 2)
│   └── graph_builder.py                # Construcción de grafos societarios y métricas (Frente 3)
├── scripts/
│   └── slurm/
│       └── slurm_cimat_pipeline.sh     # Script sbatch para ejecución en clúster CIMAT (Frente 4)
├── tests/
│   └── test_validation.py              # Pruebas automatizadas de calidad y anonimización
└── notebooks/                          # Cuadernos de exploración local
```

---

## Equipos de Trabajo y Convención de Autoría

| Equipo | Integrante | Alias Git | Responsabilidad Principal |
| :--- | :--- | :--- | :--- |
| **Arquitectura** *(+ Investigación)* | Luis Alonzo Hernández Silva | `Alonzo H.S.` | Estructura del sistema, decisiones técnicas, seguridad, despliegue en Slurm y experimentos de grafos/NLP. |
| **Arquitectura** *(+ Investigación)* | Santiago Aguilar Hernández | `Santiago A.H.` | Investigación de literatura (grafos, aprendizaje PU), modelado relacional y visualización. |
| **Calidad** | Benny Joan Salvador Mosqueda Saldaña | `Benny M.S.` | Reglas de validación, detección de anomalías de datos y auditoría de fuentes (69-B vs. 69-B Bis). |
| **Calidad** | Romina Centeno Gámez | `Romina C.G.` | Pruebas unitarias, métricas de calidad, criterios de aceptación y cumplimiento de anonimización. |
| **Requerimientos** | Ana Paula Navarro López | `Pau N.L.` | Alcance, contexto del problema real, requisitos verificables y aceptación funcional. |
| **Requerimientos** | Mariana Martínez Ruelas | `Mariana M.R.` | Coordinación de decisiones jurídicas con Derecho y deslinde entre Pieza A y Pieza B. |
| **Datos** | Santiago Alvarado Delgadillo | `Santiago A.D.` | Perfilado, diccionario y contrato de datos bajo ISO 37301. |
| **Datos** | Gerardo Jamaica Grande | `Gerardo J.M.` | Normalización de escalas, linaje Excel/CSV y estructuración de conjuntos derivados. |

### Ramas de Trabajo (`Git Flow`)
- `feature/analisis-dataset` — Equipo de Datos (`Santiago A.D.`, `Gerardo J.M.`)
- `feature/requerimientos` — Equipo de Requerimientos (`Pau N.L.`, `Mariana M.R.`)
- `feature/calidad-datos` — Equipo de Calidad (`Benny M.S.`, `Romina C.G.`)
- `feature/arquitectura` — Equipo de Arquitectura (`Alonzo H.S.`, `Santiago A.H.`)
- `feature/investigacion` — Equipo de Arquitectura / Investigación (`Santiago A.H.`, `Alonzo H.S.`)

### Formato de Commits
- **Individual**: `<Alias>: <acción en imperativo>` (ej. `Santiago A.D.: documenta el contrato de datos`).
- **De equipo**: `Equipo de <nombre>: <acción en imperativo>` (ej. `Equipo de Calidad: agrega reglas de validación del dataset piloto`).

---

## Ejecución Rápida (Entorno Local y Clúster CIMAT)

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecutar el pipeline de validación, limpieza sin BOM, EDA y prototipo de grafos (escribe resultados y bitácoras directamente a disco en `data/processed/`, sin imprimir en pantalla conforme al Manual de Supercómputo del CIMAT):
   ```bash
   python -m src.homologacion
   python -m src.graph_builder
   ```
3. Ejecutar la suite de pruebas de calidad y no-regresión:
   ```bash
   pytest -q
   ```
