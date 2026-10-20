# Definición del Problema y Alcance del Proyecto CIMAT

**Subequipo responsable:** Equipo de Requerimientos (`Pau N.L.`, `Mariana M.R.`)  
**Fecha de actualización:** 19 de octubre de 2026  

---

## 1. Contexto del Problema Real

En México, la facturación de **operaciones inexistentes o simuladas** (regulada en el **Artículo 69-B del Código Fiscal de la Federación**) constituye uno de los principales mecanismos de evasión fiscal y lavado de activos. Este fenómeno involucra a dos figuras:

1. **EFOS (Empresas que Facturan Operaciones Simuladas):** Entidades constituidas legalmente en papel pero que carecen de activos, personal, infraestructura o capacidad material para producir o comercializar los bienes o servicios que facturan.
2. **EDOS (Empresas que Deducen Operaciones Simuladas):** Contribuyentes con actividad económica real que adquieren esos comprobantes fiscales para inflar deducciones y reducir su carga tributaria, o bien MIPYMES que contratan a proveedores fachada sin contar con controles internos de verificación (*debida diligencia*).

### ¿Por qué el fenómeno es un problema de redes y no de casos aislados?
La creación sistemática de empresas fachada requiere infraestructura legal, contable y notarial compartida. La evidencia empírica en México (Zumaya et al., 2021; Luna-Pla y Nicolás-Carlock, 2020–2023; Medina-Hernández et al., 2025) demuestra que estas entidades suelen reutilizar:
- Representantes legales, administradores únicos o comisarios.
- Socios o accionistas recurrentes.
- Domicilios fiscales compartidos.
- Notarías y fechas simultáneas de constitución.
- Patrones cíclicos de facturación cruzada.

---

## 2. Separación Estricta de las Piezas de Datos (Reencuadre Vigente)

| Dimensión | Pieza A: Diagnósticos de Compliance de PYMES | Pieza B: Listado Público Art. 69-B del SAT |
| :--- | :--- | :--- |
| **Naturaleza del dato** | Evaluaciones internas de madurez conforme al estándar **ISO 37301** (6 categorías fijas). | Padrón oficial publicado por el SAT de contribuyentes con operaciones presuntamente o definitivamente inexistentes. |
| **¿Qué mide?** | **Vulnerabilidad organizacional interna** (falta de controles, políticas o canales de denuncia). | **Casos señalados o confirmados por la autoridad fiscal** (*presuntos, definitivos, desvirtuados, sentencia favorable*). |
| **Restricción de privacidad** | **Alta:** Datos estrictamente anonimizados (`COS-BJ-01`, `PYME-001`, `CONS-SERV-01`). Prohibido exponer RFC, razón social o domicilio exacto. | **Datos públicos por mandato legal** (Art. 69-B del CFF y portal de Datos Abiertos del SAT). |
| **Uso en el proyecto (2026)** | Limpieza, homologación metodológica de escalas y análisis exploratorio (Frente 1). | Estructuración (Frente 2) y construcción/visualización de grafos societarios (Frente 3). |

> [!WARNING]
> **Límite interpretativo no negociable:** No existe ningún vínculo comprobado entre las PYMES evaluadas en la Pieza A y el listado 69-B de la Pieza B. Una calificación baja de *compliance* (nivel 1, *Inexistente*) indica vulnerabilidad e informalidad administrativa, **nunca** comisión de fraude fiscal.

---

## 3. Requerimientos Funcionales Verificables para Diciembre de 2026

1. **RF-01 (Frente 1 — Homologación y Calidad):** Automatizar la conversión de entregas `.xlsx` a `.csv` en codificación `UTF-8` estándar (sin BOM), auditar las 19 columnas y documentar la regla de equivalencia entre las tres escalas de riesgo empleadas por Derecho.
2. **RF-02 (Frente 1 — Protección de Datos):** Detectar y enmascarar cualquier cuasi-identificador residual en columnas abiertas (como municipios o plantillas exactas en `observaciones_calidad_dato`).
3. **RF-03 (Frente 2 — Dataset 69-B):** Construir un dataset estructurado y limpio a partir del listado oficial del **Art. 69-B del CFF** (descartando el listado del *Art. 69-B Bis* sobre pérdidas fiscales), preservando los estados procesales (*presunto, definitivo, desvirtuado, sentencia favorable*) bajo un esquema compatible con aprendizaje *Positive-Unlabeled (PU)*.
4. **RF-04 (Frente 3 — Grafos Societarios):** Construir y visualizar grafos exploratorios (`NetworkX` / `PyVis`) donde los nodos representen contribuyentes/personas y las aristas representen atributos societarios o geográficos compartidos, calculando métricas de grado, intermediación y comunidades.
5. **RF-05 (Frente 4 — Reproducibilidad para Supercómputo CIMAT):** Empaquetar el flujo completo sin impresiones en pantalla (`stdout`), escribiendo todas las salidas directamente a archivos y proporcionando scripts `sbatch` para que el Dr. Manuel Ledesma ejecute la corrida final en el clúster antes del **31 de diciembre de 2026**.
