# Registro de Decisiones de Arquitectura y Datos (ADR)

**Subequipo responsable:** Equipo de Arquitectura (`Alonzo H.S.`, `Santiago A.H.`) y Requerimientos (`Pau N.L.`, `Mariana M.R.`)  

---

## ADR-001: Separación de Flujos entre Pieza A (Compliance PYMES) y Pieza B (Listado 69-B)
- **Estado:** Aceptada (29 de septiembre de 2026).
- **Contexto:** El dataset piloto de Derecho (`Dataset.csv`) evalúa vulnerabilidad interna de *compliance* ISO 37301 en 3 PYMES anonimizadas, sin variable de resultado fiscal ni detalles de proveedores/contratos.
- **Decisión:** Mantener dos *pipelines* desacoplados: el Frente 1 procesa la Pieza A para diagnóstico de madurez, mientras que los Frentes 2 y 3 construyen y modelan los grafos societarios sobre datos públicos confirmados del Listado 69-B del SAT (Pieza B).
- **Consecuencia:** Se evita incurrir en inferencias inválidas (baja madurez $\neq$ fraude fiscal) y se desbloquea el modelado de grafos con datos 100% públicos.

---

## ADR-002: Adopción del Marco *Positive-Unlabeled (PU) Learning* para el Listado 69-B
- **Estado:** Aceptada (28 de septiembre de 2026).
- **Contexto:** El listado del Art. 69-B contiene tres estados procesales principales (*presuntos, definitivos, desvirtuados*), y los contribuyentes no listados no son "negativos confirmados (legítimos)", sino "no etiquetados todavía".
- **Decisión:** Estructurar el dataset del Frente 2 distinguiendo explícitamente el estado procesal y diseñando el esquema de etiquetas para aprendizaje *Positive-Unlabeled (PU)* conforme a Medina-Hernández et al. (2025), Mittal et al. (2018) y Gao et al. (2021).
- **Consecuencia:** Se previene el sesgo metodológico de tratar empresas no auditadas como ejemplos negativos limpios.

---

## ADR-003: Descarte del Enlace Art. 69-B Bis y Uso Exclusivo del Padrón Art. 69-B (EFOS)
- **Estado:** Aceptada (19 de octubre de 2026).
- **Contexto:** La auditoría del archivo `SAT listado del Art. 69-B del CFF.htm` reveló que apunta a la página del **Art. 69-B Bis** (*transmisión indebida de pérdidas fiscales*, con solo 2 oficios en PDF), mientras que el objeto de estudio son las **operaciones simuladas (EFOS)** del **Art. 69-B**.
- **Decisión:** Configurar el módulo `src/sat_69b_etl.py` para ingerir el padrón público del **Art. 69-B** (EFOS) desde Datos Abiertos del SAT y notificar al área de Derecho en la sesión de presentación.

---

## ADR-004: Escritura Directa a Disco (Cero `stdout`) y Empaquetado para Slurm
- **Estado:** Aceptada (19 de octubre de 2026).
- **Contexto:** El *Manual de Acceso a Recursos de Supercómputo del CIMAT* (2025, p. 18) establece que los programas ejecutados en el clúster **no deben imprimir nada en pantalla** ni usar el operador de redirección `>`, pues ello degrada las cachés de los discos distribuidos. Además, solo el Dr. Manuel Ledesma tiene cuenta de acceso (`proy_ai26_manuel.ledesma`).
- **Decisión:** Todos los módulos de `src/` utilizan manejadores de archivo (`open(..., encoding='utf-8')` y `logging.FileHandler`) para volcar resultados y bitácoras directamente a `data/processed/`, entregando scripts `sbatch` listos para que el investigador principal los ejecute en el clúster.
