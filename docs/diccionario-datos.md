# Diccionario y Contrato de Datos (`Dataset.csv`)

**Subequipo responsable:** Equipo de Datos (`Santiago A.D.`, `Gerardo J.M.`)  
**Archivo perfilado:** `data/raw/Dataset.csv` (evolución de `2026-09-18_dataset-consolidado-pymes-h1_v1.xlsx`)  
**Dimensiones actuales:** 18 registros (filas) $\times$ 19 columnas  
**Unidad de observación (Granularidad):** Cada fila representa la evaluación de **una categoría de la norma ISO 37301 para una PYME específica** ($\text{PYME} \times \text{Categoría ISO 37301}$). Cada PYME consta exactamente de 6 filas.

---

## 1. Especificación de las 19 Columnas

| # | Nombre de Columna | Tipo de Dato | ¿Acepta Nulos? | Valores Válidos / Dominio Esperado | ¿Sensible / Cuasi-ID? | Regla de Validación del Contrato |
| :-: | :--- | :---: | :---: | :--- | :---: | :--- |
| **1** | `equipo` | `string` (categórico) | No | Identificador del equipo evaluador de Derecho (`equiporisan`, `equipoN`, `equipoJP`). | No | No vacío; eliminar prefijo invisible `\ufeff` (UTF-8 BOM) al ingerir. |
| **2** | `id_pyme` | `string` (clave) | No | Clave anonimizada de la PYME. Actuales: `COS-BJ-01`, `PYME-001`, `CONS-SERV-01`. | **Clave anónima** | Formato recomendado: `[SECTOR]-[NUM]`; exactamente 6 filas por `id_pyme`. Prohibido incluir RFC o razón social. |
| **3** | `sector_economico` | `string` | No | Giro general de actividad económica (ej. *Comercialización y distribución de cosméticos...*). | Cuasi-ID (si es muy específico) | Texto descriptivo general sin marcas comerciales ni nombres propios. |
| **4** | `forma_juridica` | `string` (categórico) | No | Régimen societario o fiscal: `Sociedad de Responsabilidad Limitada de Capital Variable`, `Sociedad Anónima de Capital Variable`, `Persona física con actividad empresarial`. | No | Debe pertenecer al catálogo oficial de figuras jurídicas mexicanas; condiciona las recomendaciones válidas de la cláusula 5.3. |
| **5** | `antiguedad_rango` | `string` (ordinal) | No | Banda de antigüedad (`1 a 5 años`, `5 a 10 años`, `Más de 10 años`). *(Anomalía actual: `6 años` en `COS-BJ-01`)*. | **Sí (Cuasi-ID si es exacto)** | **Prohibido usar años exactos**; transformar todo entero puntual $x$ a su banda correspondiente. |
| **6** | `tamano_empresa` | `string` (ordinal) | No | Categoría por número de empleados: `Micro (1-10 empleados)`, `Pequeña (11-50 empleados)`. *(Anomalía actual: `14 empleados`, `Microempresa`)*. | **Sí (Cuasi-ID si es exacto)** | **Prohibido usar conteos exactos de empleados**; homologar al catálogo estratificado de INEGI/Secretaría de Economía. |
| **7** | `region_municipio` | `string` | Sí (`NA`) | Región o municipio anonimizado según regla jurídica. *(Actuales: `Guanajuato, Guanajuato`, `No especificada en la fuente`, `Región del Bajío, Guanajuato`)*. | **Sí (Cuasi-ID en municipios pequeños)** | Reemplazar textos como `"No especificada en la fuente"` por valor nulo estándar (`NA`) o etiqueta controlada `SIN_DATO`. |
| **8** | `categoria_riesgo_iso37301` | `string` (categórico fijo) | No | Exactamente una de las **6 categorías ISO 37301**:<br>1. `Gobierno corporativo y contrapesos`<br>2. `Función de cumplimiento`<br>3. `Políticas y procedimientos documentados`<br>4. `Canal de denuncias e investigación interna`<br>5. `Gestión de riesgos y control interno`<br>6. `Gobernanza de datos e inteligencia artificial` | No | Para cada `id_pyme` deben existir las 6 categorías sin omisiones ni duplicados (biyección 1 a 1 por empresa). |
| **9** | `riesgo_identificado` | `string` (texto libre) | No | Descripción del riesgo o vulnerabilidad observada en la categoría evaluada. | Revisar texto libre | No debe ser idéntico en las 6 filas de una misma PYME (alerta de captura global como en `equipoN`) ni contener nombres propios. |
| **10** | `evidencia_disponible` | `string` (texto libre) | No | Evidencia documental o testimonial recabada durante el diagnóstico. | Revisar texto libre | No debe incluir números de escritura pública, folios mercantiles, nombres de socios ni RFC. |
| **11** | `clausula_iso37301` | `string` (código) | Sí (`NA`) | Cláusula normativa ISO 37301: `5.3`, `7.5`, `8.1-8.2`, `8.3-8.4`, `7.5 (analogía IA)`. | No | Normalizar a código numérico estándar (`5.3`, `7.5`, `8.1-8.2`, `8.3-8.4`) separando el título descriptivo. |
| **12** | `accion_recomendada` | `string` (texto libre) | Sí (`NA`) | Medida de mitigación o remediación propuesta por el equipo de Derecho. | No | Validar coherencia con `forma_juridica` (ej. no exigir *consejo de administración* a una *Persona física*). |
| **13** | `tipo_escala_equipo` | `string` (categórico) | No | Instrumento original usado por el equipo:<br>- `Escala de madurez 1-2`<br>- `Escala de madurez 1-4 con semáforo`<br>- `Matriz de riesgo probabilidad × impacto` | No | Columna de trazabilidad agregada en la consolidación del 29-sep-2026. |
| **14** | `valor_escala_original` | `string` | No | Valor textual literal reportado por el equipo en su entrega primaria. | No | Preservar intacto sin modificación para auditoría de linaje. |
| **15** | `nivel_homologado_borrador` | `integer` (ordinal) | No | Entero en el rango `{1, 2, 3, 4}` (actualmente solo aparecen `1` y `2` en los 18 registros). | No | Tipo entero estricto $\in \{1, 2, 3, 4\}$. |
| **16** | `etiqueta_homologada_borrador` | `string` (ordinal) | No | Etiqueta asociada al nivel homologado: `1 -> Inexistente`, `2 -> Ad hoc / informal`, `3 -> Definido / documentado`, `4 -> Consolidado`. | No | Correspondencia biunívoca estricta con `nivel_homologado_borrador`. |
| **17** | `confianza_homologacion` | `string` (categórico) | No | Nivel de certeza metodológica de la conversión: `alta`, `media`, `baja`. | No | `baja` cuando `tipo_escala_equipo` mide riesgo (probabilidad $\times$ impacto) en lugar de madurez. |
| **18** | `fuente_informacion` | `string` | No | Referencia a la entrega académica de origen (`Diagnóstico de Madurez de Compliance — Entrega 1 (equipo ...)`). | No | No vacío; trazabilidad interna. |
| **19** | `observaciones_calidad_dato` | `string` (texto libre) | Sí | Notas de auditoría sobre reclasificaciones, omisiones o generalizaciones aplicadas al consolidar. | **Alerta Crítica (Fuga de Cuasi-ID)** | **Regla de sanitización obligatoria:** Prohibido conservar en esta columna los valores exactos originales (municipio, años o empleados exactos) que fueron anonimizados en las columnas 5, 6 y 7. |

---

## 2. Resumen de Distribución Actual en `Dataset.csv`

- **Registros totales:** 18 filas.
- **Empresas (`id_pyme`):** 3 (`COS-BJ-01` = 6 filas, `PYME-001` = 6 filas, `CONS-SERV-01` = 6 filas).
- **Distribución de `nivel_homologado_borrador`:**
  - Nivel `1` (*Inexistente*): **15 registros (83.3%)** — 4 de `COS-BJ-01`, 6 de `PYME-001` y 5 de `CONS-SERV-01`.
  - Nivel `2` (*Ad hoc / informal*): **3 registros (16.7%)** — 2 de `COS-BJ-01` y 1 de `CONS-SERV-01`.
  - Niveles `3` y `4`: **0 registros (0.0%)**.
- **Distribución de `confianza_homologacion`:**
  - `alta`: **12 registros (66.7%)** (`equiporisan` y `equipoN`).
  - `baja`: **6 registros (33.3%)** (`equipoJP`).
