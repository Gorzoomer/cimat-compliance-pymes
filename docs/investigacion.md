# Resumen de Investigación Técnica y Literatura Relacionada

**Subequipo responsable:** Equipo de Arquitectura e Investigación (`Santiago A.H.`, `Alonzo H.S.`)  
**Referencias base:** `2026-09-28_referencias_literatura_relacionada_v1.md.docx`, `Manual de Acceso a Recursos-1.pdf` y `CIMAT.png` (Lámina 9).

---

## 1. Los 5 Conceptos Clave de la Investigación Relámpago (Lámina 9)

### 1.1. *Pipeline* de Datos: ¿Qué es y cómo se usa?
Un ***pipeline* de datos** es una secuencia automatizada y reproducible de etapas donde la salida de un proceso sirve como entrada validada del siguiente (`Ingesta → Validación/Limpieza → Estructuración → Modelado de Grafos → Visualización`). En este proyecto evita que la conversión de `.xlsx` a `.csv` o la homologación de escalas dependan de ediciones manuales en Excel propensas a error humano.

### 1.2. Grafos Societarios: ¿Cómo representan relaciones entre empresas y proveedores?
Un **grafo** $G = (V, E)$ modela entidades como **nodos** ($V$: empresas, socios, representantes legales, domicilios, notarios) y sus vínculos como **aristas** ($E$: compartir el mismo representante legal, el mismo domicilio fiscal o facturarse entre sí).
- **Precedente directo en México (Facturación):** **Zumaya et al. (2021)** (*"Identifying tax evasion in Mexico with tools from network science and machine learning"*) analizaron redes de facturación electrónica (2015–2018) junto con el listado oficial de EFOS del SAT, identificando ciclos de facturación sobrerrepresentados y alcanzando $>0.90$ de exactitud.
- **Precedentes en México (Redes Societarias):** **Luna-Pla y Nicolás-Carlock (2020, 2021, 2023)** modelaron redes de empresas fantasma mexicanas como **grafos bipartitos empresa–personal** (accionistas, representantes legales, administradores y fechas de creación), demostrando que las empresas fachada forman componentes altamente cohesionados alrededor de "nodos articuladores" (prestanombres o despachos).

### 1.3. Procesamiento de Lenguaje Natural (NLP): ¿Qué se puede extraer y cuáles son sus límites?
El **NLP** permite extraer automáticamente entidades nombradas (nombres de partes, fechas, montos, cláusulas de *compliance*) a partir de textos jurídicos o contratos.
- **Estado del arte y cautela metodológica:** Como documenta la revisión de literatura del proyecto (**Lopez-Gazpio et al., 2025**, *Knowledge-Based Systems*), el NLP aplicado a extracción de relaciones corporativas contra fraude fiscal es el eslabón menos consolidado en la literatura global. Además, dado que hoy no se cuenta con los textos íntegros de los contratos de las PYMES por protección de datos personales, en 2026 el análisis textual se acota a normalizar las descripciones de hallazgos y evidencias ya anonimizadas.

### 1.4. SLURM y Supercómputo en CIMAT: ¿Por qué una supercomputadora no se usa igual que una laptop?
El Laboratorio de Supercómputo del CIMAT (*Clúster El-Insurgente* y *Laboratorio de Supercómputo del Bajío*) opera bajo Ubuntu Linux Server y se accede por SSH hacia un nodo **Front-End**, el cual **jamás debe usarse para ejecutar cálculos** ([*Manual CIMAT*, 2025, p. 13]).
- **Nodos `p-0-1` y `p-0-2`:** Servidores de acceso libre por SSH + utilidad `screen` para pruebas cortas y depuración (12 núcleos, 24–48 GB RAM).
- **Nodos gestionados por SLURM (`c-0-X`, `c-1-X`, `c-2-X`, `g-0-X`):** No tienen acceso directo; las tareas se envían mediante scripts `sbatch` a particiones como `C1Mitad1` (40 nodos, 12 núcleos/nodo, límite de 8 nodos simultáneos por estudiante) o `C2` (15 nodos, 24 núcleos/nodo, 64 GB RAM). Los nodos **no se comparten simultáneamente entre distintos usuarios**, por lo que enviar un solo proceso secuencial desperdiciaría los demás núcleos del nodo ([*Manual CIMAT*, p. 22]).
- **Proyectos Tipo 1 (múltiples tareas secuenciales independientes):** Se agrupan en un archivo de tareas y se ejecutan en paralelo con `/opt/ClusterTools/MPI_Scheduler` y `slurm_script_Projects_Type1` ([*Manual CIMAT*, pp. 30–32]).
- **Regla técnica crítica de E/S:** Está prohibido imprimir a pantalla (`stdout`) o redirigir con `>`, ya que satura la red y las cachés de los discos distribuidos RAID; todo software debe abrir y escribir archivos directamente en disco ([*Manual CIMAT*, p. 18]).

### 1.5. *Data Validation* y Aprendizaje *Positive-Unlabeled (PU)*: ¿Cómo se asegura la calidad?
- **Validación de contrato de datos:** Antes de cualquier análisis, el código verifica tipos de datos, ausencia de caracteres corruptos (`\ufeff` BOM), completitud de las 6 dimensiones ISO 37301 por PYME y ausencia de datos personales identificables (PII).
- **Aprendizaje *Positive-Unlabeled (PU)* para el Listado 69-B:** **Medina-Hernández, Kertész y Fazekas (2025)** (*Scientific Reports*, con datos mexicanos), **Mittal et al. (2018)** y **Gao et al. (2021)** demuestran que los padrones fiscales oficiales solo contienen casos positivos confirmados (*definitivos*), casos en proceso (*presuntos*) y aclarados (*desvirtuados*), mientras que el resto del universo empresarial es **no etiquetado (*unlabeled*)**, no "negativo confirmado". Asimismo, **Barwahwala et al. (2024)** demuestran en campo que alta exactitud predictiva no equivale automáticamente a impacto recaudatorio, razón por la cual este proyecto mantiene en 2026 un alcance exploratorio honesto y riguroso.
