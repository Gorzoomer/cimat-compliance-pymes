# Informe Ejecutivo — Análisis del Problema y Viabilidad de Datos del Proyecto CIMAT

**Materia:** Programación Avanzada · Ingeniería en Ciencia de Datos (Tercer Semestre · Ago–Dic 2026)  
**Institución:** Universidad de Celaya en colaboración con el Área de Derecho y el CIMAT  
**Dirigido a:** Dr. Manuel Ledesma López (Investigador Principal del Proyecto) y Equipo de Derecho  
**Fecha:** 19 de octubre de 2026  

---

## Portada y Autoría por Sección

| Subequipo | Integrante (Nombre Completo) | Alias Git | Sección Redactada en este Informe |
| :--- | :--- | :--- | :--- |
| **Requerimientos** | Ana Paula Navarro López | `Pau N.L.` | **Sección 1.** Resumen ejecutivo y **Sección 2.** El problema en el mundo real |
| **Datos** | Santiago Alvarado Delgadillo | `Santiago A.D.` | **Sección 3.** ¿Qué es *compliance* y qué mide el dataset? |
| **Requerimientos** | Mariana Martínez Ruelas | `Mariana M.R.` | **Sección 4.** Alcance honesto del proyecto y **Sección 8.** Preguntas para el área de Derecho |
| **Datos** | Gerardo Jamaica Grande | `Gerardo J.M.` | **Sección 5 (Parte A).** Diagnóstico estructural del dataset, escalas, homologación y diferencias Excel vs. CSV |
| **Calidad** | Benny Joan Salvador Mosqueda Saldaña | `Benny M.S.` | **Sección 5 (Parte B).** Problemas y riesgos de calidad de datos identificados (10 hallazgos) |
| **Arquitectura** *(+ Investigación)* | Luis Alonzo Hernández Silva | `Alonzo H.S.` | **Sección 6.** Rol de cada área, flujo del *pipeline*, cuatro frentes y acceso al clúster |
| **Calidad** | Romina Centeno Gámez | `Romina C.G.` | **Sección 7.** Restricciones y reglas no negociables (anonimización, supercómputo y calendario) |
| **Arquitectura** *(+ Investigación)* | Santiago Aguilar Hernández | `Santiago A.H.` | **Sección 9.** Recomendación estratégica, sustento en literatura y siguientes pasos |

---

## 1. Resumen Ejecutivo

El **Proyecto CIMAT** aborda la vulnerabilidad de las micro, pequeñas y medianas empresas (MIPYMES) de Guanajuato frente a esquemas de facturación falsa u **operaciones simuladas**, reguladas en el **Artículo 69-B del Código Fiscal de la Federación (CFF)**. Mientras que en México existen empresas fachada que venden comprobantes fiscales sin actividad económica real y suelen operar en **redes societarias** interconectadas, muchas MIPYMES legítimas carecen de controles internos (*compliance*) que les impidan involucrarse accidentalmente con proveedores fraudulentos ([*Explicación sin tecnicismos*, 29-sep-2026, §1–2]).

Del análisis realizado sobre el dataset piloto entregado por Derecho ([`Dataset.csv`](../data/raw/Dataset.csv), con **18 registros** correspondientes a **3 PYMES** evaluadas en **6 categorías del estándar ISO 37301**), nuestro hallazgo principal es doble:
1. **No existe un vínculo directo entre la vulnerabilidad de una PYME (Pieza A) y la comisión confirmada de fraude fiscal (Pieza B — Listado 69-B)**; además, los tres equipos jurídicos emplearon escalas distintas (dos de madurez y una de riesgo probabilidad $\times$ impacto), por lo que **un tercio del dataset (6 de 18 filas) tiene confianza de homologación baja** y existen riesgos de re-identificación en notas textuales.
2. En el material de referencia del SAT se detectó que el enlace guardado apunta al **Art. 69-B Bis** (*transmisión indebida de pérdidas fiscales*, con solo 2 oficios en PDF), cuando el proyecto requiere el padrón público del **Art. 69-B** (*operaciones simuladas*, con miles de registros de presuntos, definitivos y desvirtuados).

**Recomendación del grupo:** Desacoplar el arranque en dos vías inmediatas que no sufren bloqueos externos ni requieren acceso directo al clúster: **(a) Frente 1**, estandarizar mediante código la limpieza, anonimización estricta y conversión de escalas del dataset de PYMES; y **(b) Frente 2**, construir el dataset público estructurado del **Art. 69-B** bajo un diseño de *aprendizaje con positivos y no etiquetados* (*Positive-Unlabeled*), insumo base para modelar los grafos societarios en noviembre y empaquetar las rutinas reproducibles que el Dr. Ledesma ejecutará en el clúster antes del **31 de diciembre de 2026** ([*Guion de primera sesión*, 28-sep-2026, Anexo]).

---

## 2. El Problema en el Mundo Real

En la economía real existen empresas creadas exclusivamente en papel: cuentan con acta constitutiva y registro fiscal, pero carecen de personal, activos o bodegas para producir bienes o prestar servicios. Su único giro consiste en emitir facturas por operaciones que jamás ocurrieron (**Empresas que Facturan Operaciones Simuladas, EFOS**). En el otro extremo, empresas con operaciones reales compran esas facturas para inflar artificialmente sus gastos deducibles y reducir el pago de impuestos (**Empresas que Deducen Operaciones Simuladas, EDOS**), o bien contratan de buena fe a proveedores fachada sin verificar su existencia material ([*Explicación sin tecnicismos*, 29-sep-2026, §1]).

Cuando el Servicio de Administración Tributaria (SAT) detecta que un contribuyente emite comprobantes sin contar con activos, personal o infraestructura, lo incorpora en el **Listado del Artículo 69-B del CFF**. Este padrón público constituye la única fuente oficial en México con casos verificados por la autoridad y clasifica a los contribuyentes en distintos estados procesales (**presuntos**, **definitivos**, **desvirtuados** y **con sentencia favorable**).

Estas empresas fachada rara vez actúan como casos aislados. Crear y operar una facturera exige costos legales, contables y financieros, por lo que quienes las articulan reutilizan los mismos **representantes legales, socios o accionistas, comisarios, notarios, domicilios fiscales o fechas simultáneas de constitución**, además de facturarse en círculos entre sí para aparentar actividad comercial ([*Referencias de literatura*, 28-sep-2026, §1–2: Zumaya et al., 2021; Luna-Pla y Nicolás-Carlock, 2020]). Al compartir personas y domicilios, dejan una huella colectiva: **forman redes societarias**, cuya estructura puede representarse y descubrirse mediante **análisis de grafos** (mapas matemáticos de puntos y conexiones).

---

## 3. ¿Qué es *Compliance* y Qué Mide el Dataset?

En términos prácticos, el ***compliance*** (cumplimiento normativo) mide qué tan preparada está una organización desde su interior para prevenir, detectar y corregir irregularidades legales, éticas o fiscales antes de que ocurran ([*Explicación sin tecnicismos*, 29-sep-2026, §2]). Una MIPYME sin controles internos no es automáticamente una empresa evasora, pero sí es altamente vulnerable a ser utilizada por un tercero, socio o proveedor fachada sin advertirlo a tiempo.

Los equipos de la materia de *Prácticas de Derecho Corporativo* diagnosticaron a un grupo piloto de MIPYMES de Guanajuato utilizando como referencia la norma internacional **ISO 37301** (*Sistemas de gestión de compliance*), estructurada en **6 categorías fijas de evaluación**:

| # | Categoría ISO 37301 en `Dataset.csv` | Cláusula ISO Ref. | ¿Qué evalúa en la práctica dentro de la PYME? |
| :-: | :--- | :---: | :--- |
| **1** | **Gobierno corporativo y contrapesos** | 5.3 | Existencia de órganos de decisión colegiados, actas formales y límites al poder de un solo socio o director. |
| **2** | **Función de cumplimiento** | 5.3 | Designación de un responsable o comité que supervise el cumplimiento regulatorio (fiscal, sanitario, laboral). |
| **3** | **Políticas y procedimientos documentados** | 7.5 | Existencia y vigencia de código de ética, políticas anticorrupción y reglamentos internos formalizados. |
| **4** | **Canal de denuncias e investigación interna** | 8.3 y 8.4 | Mecanismos confidenciales para reportar irregularidades sin represalias y protocolos para investigarlas. |
| **5** | **Gestión de riesgos y control interno** | 8.1 y 8.2 | Matrices de riesgo, auditoría interna y debida diligencia al contratar proveedores o firmar contratos. |
| **6** | **Gobernanza de datos e inteligencia artificial** | 7.5 *(analogía)* | Reglas de privacidad, resguardo de secretos comerciales y control sobre datos ingresados en herramientas de IA. |

**¿Qué representa una fila del dataset piloto?**  
Una fila de [`Dataset.csv`](../data/raw/Dataset.csv) **no representa a una empresa completa ni a un contrato individual**, sino la **evaluación de una categoría específica de la norma ISO 37301 aplicada a una PYME determinada** (unidad de observación: $\text{PYME} \times \text{Categoría ISO 37301}$). Dado que cada PYME se evalúa en las 6 categorías fijas, **cada empresa diagnosticada ocupa exactamente 6 filas consecutivas** en la tabla.

---

## 4. Alcance Honesto del Proyecto

Siguiendo el reencuadre metodológico establecido el 28 y 29 de septiembre de 2026, el proyecto distingue con rigor entre dos fuentes de datos independientes ([*Explicación sin tecnicismos*, 29-sep-2026, §3 y §5]):

* **Pieza A — Diagnósticos de *compliance* de PYMES ([`Dataset.csv`](../data/raw/Dataset.csv)):** Contiene evaluaciones internas de madurez organizacional levantadas por alumnos de Derecho. **Mide vulnerabilidad preventiva, no comisión de delitos.**
* **Pieza B — Listado público del Art. 69-B del SAT (por construir):** Contendrá los registros públicos de empresas confirmadas o señaladas por el SAT por operaciones simuladas, junto con datos societarios públicos.

**¿Por qué hoy NO es válido concluir que una PYME con baja calificación comete fraude fiscal?**
1. **Diferencia entre vulnerabilidad y conducta ilícita:** Que una microempresa familiar carezca de un comité de *compliance* o de un canal formal de denuncias (nivel 1, *Inexistente*) refleja informalidad administrativa típica de su tamaño, no emisión ni deducción de facturas falsas.
2. **Ausencia de vínculo empírico verificado:** No existe hoy ningún cruce ni variable de resultado que conecte a las 3 PYMES anonimizadas de la Pieza A con el listado 69-B de la Pieza B ([*Guion de primera sesión*, 28-sep-2026, §0:15–0:22]).
3. **Naturaleza de las etiquetas del 69-B en la literatura:** Como demuestran **Medina-Hernández et al. (2025)** y **Mittal et al. (2018)** ([*Referencias de literatura*, 28-sep-2026, §3]), el listado 69-B posee tres estados con distinto peso probatorio (*presuntos, definitivos, desvirtuados*) y las empresas no listadas no son "inocentes confirmadas", sino "no etiquetadas" (*Positive-Unlabeled*). Además, la evidencia de campo internacional (**Barwahwala et al., 2024**) advierte que ni siquiera un modelo predictivo con alta exactitud estadística garantiza impacto administrativo inmediato.

**Lo que el proyecto SÍ entregará al cierre de 2026 (y lo que queda para 2027):**  
En 2026 **no** se entregará un detector predictivo que dictamine si una PYME comete fraude. Se entregarán cuatro productos fundacionales verificables ([*Explicación sin tecnicismos*, 29-sep-2026, §5]):
1. **Un *pipeline* (flujo automatizado) de datos reproducible y documentado** (`limpieza → estructuración → grafos → visualización`).
2. **El primer dataset estructurado y limpio del listado público 69-B**, listo como base de referencia.
3. **Un prototipo exploratorio de modelado y visualización de grafos societarios**.
4. **Evidencia metodológica rigurosa** para sustentar publicaciones académicas y diseñar en **2027** un esquema formal de validación.

---

## 5. Diagnóstico de los Datos Disponibles

### 5.1. Radiografía Cuantitativa y Comparativa de Escalas
El archivo [`Dataset.csv`](../data/raw/Dataset.csv) consta de **18 registros** (filas de datos) y **19 columnas**, correspondientes a **3 PYMES** evaluadas por **3 equipos de Derecho** ($3\text{ PYMES} \times 6\text{ categorías ISO 37301} = 18\text{ filas}$). Los equipos utilizaron tres instrumentos de medición distintos que **no son directamente comparables entre sí**:

| Equipo de Derecho | ID PYME | Sector y Forma Jurídica | Escala Original Utilizada (`tipo_escala_equipo`) | Homologación en Borrador | Nivel de Confianza |
| :--- | :---: | :--- | :--- | :---: | :---: |
| `equiporisan` | `COS-BJ-01` | Cosméticos · S. de R.L. de C.V. (14 emp., 6 años) | **Escala de madurez 1–2** (`1=Inexistente`, `2=Ad hoc / informal`) | Niveles `1` (4 filas) y `2` (2 filas) | **Alta** *(6 filas)* |
| `equipoN` | `PYME-001` | Productos lácteos · S.A. de C.V. (Micro, 5–10 años) | **Escala de madurez 1–4 con semáforo** (`1=Inexistente` … `4=Consolidado`) | Nivel `1` en las 6 filas *(reclasificado de verde a rojo)* | **Alta** *(6 filas)* |
| `equipoJP` | `CONS-SERV-01` | Construcción · Persona física (Micro, >10 años) | **Matriz de riesgo Probabilidad × Impacto** (`bajo/medio/medio-alto/alto`) | Nivel `1` (5 filas) y Nivel `2` (1 fila) | **Baja** *(6 filas)* |

* **¿Por qué no son directamente comparables y cómo afecta la confianza?**  
  Mientras `equiporisan` y `equipoN` miden **madurez de controles internos** (aunque con distinto rango máximo: 1–2 frente a 1–4), `equipoJP` evaluó **exposición al riesgo (probabilidad $\times$ impacto)**. Medir "qué tan probable y grave es un daño" es un concepto distinto e inverso a medir "qué tan formalizado está un control". Por ello, al invertir manualmente `riesgo alto → madurez 1 (Inexistente)` y `riesgo medio-alto → madurez 2 (Ad hoc)`, quien consolidó la tabla etiquetó honestamente las 6 filas de `CONS-SERV-01` (**33.3% del dataset**) con **`confianza_homologacion = baja`**, frente al **66.7% (12 filas) con confianza `alta`**.
* **Diferencias entre la versión Excel (`18-sep-2026`) y la versión CSV (`29-sep-2026`):**  
  El archivo original `2026-09-18_dataset-consolidado-pymes-h1_v1.xlsx` ([*Guion de primera sesión*, 28-sep-2026, §0:05–0:15]) contenía los 18 registros en formato propietario de hoja de cálculo (`.xlsx`) y preservaba únicamente las calificaciones originales sin homologar. La versión evolucionada [`Dataset.csv`](../data/raw/Dataset.csv) ([*Explicación sin tecnicismos*, 29-sep-2026, §6]) migró a texto plano separado por comas e incorporó **6 columnas adicionales de auditoría y homologación en borrador** (`tipo_escala_equipo`, `valor_escala_original`, `nivel_homologado_borrador`, `etiqueta_homologada_borrador`, `confianza_homologacion` y `observaciones_calidad_dato`).

### 5.2. Diez Problemas y Riesgos de Calidad de Datos Identificados

| # | Problema / Riesgo Identificado | Evidencia Concreta en `Dataset.csv` / `Contexto` | Impacto Técnico o Jurídico |
| :-: | :--- | :--- | :--- |
| **1** | **Incompatibilidad de constructo en escalas (Riesgo vs. Madurez)** | Filas 14–19 (`equipoJP`): usa matriz *Probabilidad × Impacto* en vez de escala de madurez ISO 37301. | Sesgo metodológico al promediar o comparar puntuaciones de `CONS-SERV-01` con las demás PYMES. |
| **2** | **Fuga de cuasi-identificadores en notas de observaciones** | Filas 14–19 (`observaciones_calidad_dato`): revela que `CONS-SERV-01` tiene **11 años**, **4 personas**, giro de ingeniería civil y se ubica en **Villagrán, Gto.** | **Riesgo alto de re-identificación** de la PYME al cruzar municipio pequeño + giro + antigüedad exacta. |
| **3** | **Falta de anonimización a rangos/bandas en `COS-BJ-01`** | Filas 2–7 (`equiporisan`): `antiguedad_rango` dice `"6 años"` y `tamano_empresa` dice `"14 empleados"`, valores puntuales y no bandas. | Incumple el contrato de generalización a bandas y rebasa el umbral de $\le 10$ empleados de la lámina inicial. |
| **4** | **Pérdida total de granularidad por captura global duplicada** | Filas 8–13 (`equipoN`): repite idéntico texto en `riesgo_identificado`, `evidencia_disponible` y `accion_recomendada` para las 6 categorías. | Impide distinguir qué hallazgo o evidencia corresponde realmente a cada cláusula de ISO 37301. |
| **5** | **Contradicción lógica en fuente primaria (Semáforo vs. Nivel)** | Filas 8–13 (`equipoN`): reportó promedio de madurez `1 sobre 4` (Inexistente), pero asignó **semáforo verde** en su documento fuente. | Obligó a aplicar una regla correctiva manual a semáforo rojo durante la consolidación. |
| **6** | **Incoherencia jurídica entre forma legal y recomendación** | Fila 14 (`CONS-SERV-01`): es **Persona física con actividad empresarial**, pero `accion_recomendada` exige *"establecer un consejo de administración de al menos tres integrantes"*. | Una persona física no es una sociedad mercantil con estatuto social ni consejo de administración. |
| **7** | **Dimensiones no evaluadas en entrevista rellenadas por defecto** | Filas 3, 4 y 6 (`equiporisan`): no generaron hallazgo en entrevista y se registraron como "riesgo base" sin acción recomendada. | Mezcla ausencias reales de control con omisiones de levantamiento durante la entrevista. |
| **8** | **Falta de estandarización en cláusulas, IDs y valores nulos** | `clausula_iso37301` mezcla `"5.3 Roles..."`, `"5.3"` y `"No reportada en el archivo fuente"`; `region_municipio` usa `"No especificada en la fuente"`. | Textos libres en lugar de valores vacíos estándar (`NULL`/`NA`) dificultan el filtrado programático. |
| **9** | **Riesgo de transcripción manual y codificación `UTF-8 BOM`** | `equipoJP` entregó su matriz como **imagen incrustada en Word** (transcrita a mano); además, `Dataset.csv` inicia con el carácter invisible `\ufeff` (BOM). | El carácter `\ufeff` renombra la primera columna a `\ufeffequipo` si no se lee con codificación `utf-8-sig`. |
| **10** | **Desfase en la fuente del SAT (`Art. 69-B Bis` vs. `Art. 69-B`)** | El archivo `SAT listado del Art. 69-B del CFF.htm` descarga la página del **Art. 69-B Bis** (*transmisión indebida de pérdidas fiscales*, 2 oficios PDF). | El proyecto requiere el padrón de **EFOS del Art. 69-B** (operaciones simuladas), no el de pérdidas fiscales del 69-B Bis. |

---

## 6. Rol de Cada Área y Flujo de Trabajo

### 6.1. Articulación Interdisciplinaria y Organización Interna
* **Área de Derecho (Experto en la dimensión jurídica):** Define el problema normativo, realiza el levantamiento y curaduría de datos, anonimiza identificadores sensibles, parametriza las categorías ISO 37301 y valida la interpretación jurídica de los hallazgos ([*Lámina de arranque*, `CIMAT.png`, §4]).
* **Área de Ciencia de Datos (Experto en la dimensión computacional):** Estructurada en cuatro subequipos complementarios ([`Equipos.md`](../../Contexto/Equipos.md)): **Requerimientos** (`Pau N.L.`, `Mariana M.R.`), **Datos** (`Santiago A.D.`, `Gerardo J.M.`), **Calidad** (`Benny M.S.`, `Romina C.G.`) y **Arquitectura + Investigación** (`Alonzo H.S.`, `Santiago A.H.`). Se encarga de validar, limpiar, estructurar el dataset 69-B, construir los grafos y empaquetar el software reproducible.
* **CIMAT (Plataforma de cómputo de alto rendimiento):** Proporciona la infraestructura de supercómputo (*Clúster El-Insurgente* y *Laboratorio de Supercómputo del Bajío*) y el soporte técnico de ejecución ([*Manual de Acceso a Recursos*, 2025, §1 y §5]).

### 6.2. El *Pipeline* Propuesto y los Cuatro Frentes de Trabajo
Un ***pipeline* de datos** es una línea de ensamblaje automatizada donde cada etapa recibe datos crudos, les aplica reglas verificables y entrega un producto limpio a la siguiente etapa sin intervención manual:

1. **Etapa 1 — Limpieza (Frente 1: Limpieza y homologación del dataset de PYMES):** Lectura automática de entregas `.xlsx`/`.csv`, eliminación de marcas BOM, validación de anonimización, normalización de textos vacíos y evaluación metodológica de la conversión de las tres escalas de riesgo.
2. **Etapa 2 — Estructuración (Frente 2: Construcción del dataset público del Listado 69-B):** Descarga y transformación de los listados públicos del Art. 69-B del SAT (y fuentes registrales públicas como el RPPC) en una tabla limpia con RFC/identificador, razón social, domicilio, representante legal, fechas y estatus procesal (*presunto, definitivo, desvirtuado*). Es el activo de datos más importante del proyecto porque contiene casos confirmados ([*Explicación sin tecnicismos*, 29-sep-2026, §6]).
3. **Etapa 3 — Grafos (Frente 3: Modelado relacional societario):** Construcción de redes donde cada nodo es una empresa o persona asociada y cada arista representa un atributo compartido (representante legal, socio, domicilio fiscal), calculando métricas estructurales (grado de conexión, intermediación y comunidades mediante la librería `NetworkX` de Python).
4. **Etapa 4 — Visualización y Empaquetado para Supercómputo (Frente 4: Preparación para el clúster CIMAT):** Generación de mapas interactivos (`PyVis`) y empaquetado de scripts, bitácoras y lista de dependencias (`requirements.txt`).

**Restricción administrativa de acceso al clúster:** Conforme a la convocatoria firmada y al reglamento del laboratorio ([*Reglamento Lab. Supercómputo*, §Obligaciones; *Guion 28-sep-2026*, §0:23–0:40]), la cuenta de acceso (`proy_ai26_manuel.ledesma`) es personal e intransferible del solicitante. Por tanto, **los alumnos de Ciencia de Datos desarrollan y prueban todo el código en entorno local**, y **el Dr. Manuel Ledesma ejecuta las corridas finales en el clúster** una vez habilitado el enlace por soporte de CIMAT.

---

## 7. Restricciones y Reglas No Negociables

1. **Protección estricta de datos personales y anonimización:** Ningún nombre real, razón social, RFC ni domicilio exacto de las PYMES diagnosticadas por Derecho puede aparecer en el código, en el repositorio de GitHub ni en el clúster ([*Explicación sin tecnicismos*, 29-sep-2026, §7]). Es una obligación legal en materia de protección de datos personales y un compromiso ético con las empresas participantes. Además, debe depurarse cualquier dato en texto libre (como el municipio de Villagrán en `observaciones_calidad_dato`) que permita deducir la identidad de una PYME.
2. **Uso real y buenas prácticas del supercómputo con el volumen actual:** Con 18 registros en la Pieza A y algunos miles en el listado 69-B, **el proyecto hoy no requiere tarjetas gráficas (GPU) ni fuerza bruta masiva**; una computadora portátil procesa estos datos en segundos. El clúster del CIMAT se emplea para estandarizar el flujo reproducible hacia escalas mayores en 2027. Para cumplir estrictamente con el [*Manual de Acceso a Recursos del CIMAT* (2025, §5, §5.1, §5.2 y §6)]:
   * **Nunca ejecutar procesos en el servidor de entrada (*Front-End*)**; usar nodos de desarrollo (`p-0-1`, `p-0-2`) o nodos administrados por el gestor de colas **Slurm** (particiones CPU como `C1Mitad1` o `C2`).
   * **Prohibición de imprimir resultados en pantalla (`stdout` o redirección `>`):** En sistemas distribuidos, imprimir texto en consola degrada severamente el rendimiento de caché en disco ([*Manual CIMAT*, p. 18]). Todo nuestro software escribe resultados y bitácoras **directamente a archivos en disco**.
   * **Agrupación de tareas secuenciales (*Proyectos Tipo 1*):** Nunca reservar un nodo multicore completo para correr un solo proceso secuencial; deben agruparse mediante `/opt/ClusterTools/MPI_Scheduler` o scripts `sbatch` calibrados al número de núcleos del nodo ([*Manual CIMAT*, pp. 22 y 30–32]).
3. **Calendario y entregable obligatorio:** El proyecto semestral corre de agosto a diciembre de 2026 y tiene una fecha límite inamovible ante el CIMAT el **31 de diciembre de 2026** (además del reporte técnico de cierre de 2 a 4 páginas exigido por el Reglamento del Laboratorio).

---

## 8. Preguntas para el Área de Derecho (Indispensables Antes de Programar)

1. **Regla oficial de conversión entre escalas (Riesgo vs. Madurez):** Para el 33.3% de registros evaluados con matriz *Probabilidad × Impacto* (`equipoJP`), ¿validan jurídicamente la regla inversa `Riesgo Alto = Madurez 1 (Inexistente)` y `Riesgo Medio-Alto = Madurez 2 (Ad hoc)`, o qué correspondencia debemos programar para los equipos que faltan por entregar?
2. **Estandarización para las siguientes entregas de Derecho:** ¿Los nuevos equipos entregarán sus diagnósticos ya en una escala única (p. ej. madurez 1 a 4), o nuestro *pipeline* debe seguir recibiendo las tres escalas distintas?
3. **Depuración de cuasi-identificadores en `observaciones_calidad_dato`:** ¿Autorizan que el script de limpieza enmascare las menciones explícitas al municipio (*Villagrán*) y tamaño exacto (*4 personas, 11 años*) en `CONS-SERV-01`, y que homologue a bandas los valores exactos de `COS-BJ-01` (*6 años, 14 empleados*)?
4. **Criterio para dimensiones sin hallazgo en entrevista vs. captura global:** En `equiporisan`, 3 categorías sin hallazgo en entrevista se registraron con calificaciones `1` y `2` por defecto; en `equipoN`, se copió el mismo texto global en las 6 filas. ¿Debemos distinguir mediante una bandera de calidad (`hallazgo_directo = Sí/No`) las evaluaciones específicas de las globales o por defecto?
5. **Regla de aplicabilidad según forma jurídica (`Persona física` vs. `Sociedad mercantil`):** En `CONS-SERV-01` (persona física), se recomendó crear un *consejo de administración*. ¿Qué controles equivalentes de la cláusula 5.3 de ISO 37301 son jurídicamente exigibles a una persona física para no calificarla erróneamente?
6. **Confirmación de la fuente pública del SAT (`Art. 69-B` vs. `Art. 69-B Bis`):** Detectamos que el archivo HTML de referencia apunta al listado del **Art. 69-B Bis** (*transmisión indebida de pérdidas fiscales*). ¿Confirmamos que el Frente 2 debe construirse exclusivamente con el padrón de Datos Abiertos del **Art. 69-B** (*operaciones simuladas / EFOS*), y cómo debemos ponderar sus estados (*presunto, definitivo, desvirtuado, sentencia favorable*)?
7. **Fuentes públicas para enlaces societarios del grafo (Frente 3):** Dado que el CSV público del Art. 69-B del SAT publica RFC, razón social y fechas de oficios, pero no siempre incluye accionistas, representantes legales o domicilios completos, ¿qué fuentes públicas adicionales (RPPC, SIGER, Boletín Registral o contrataciones públicas) validará Derecho para extraer las conexiones (aristas) entre empresas?
8. **Naturaleza de las PYMES diagnosticadas y acuerdo de confidencialidad:** ¿Está confirmado que las PYMES de la Pieza A son empresas reales (pendiente señalado en el *Dictamen de Subsanación*, Hallazgo 2) y requieren los alumnos de Ciencia de Datos firmar una carta de confidencialidad equivalente a la de Derecho?

---

## 9. Recomendación y Siguientes Pasos

Para maximizar el avance real antes del cierre semestral y del entregable ante CIMAT del **31 de diciembre de 2026**, el grupo recomienda ejecutar un **plan incremental en cuatro bloques** que evita cualquier dependencia de los puntos hoy bloqueados (acceso directo al clúster y datos sensibles de PYMES):

| Periodo | Frente / Equipo Responsable | Entregable Técnico Concreto | Justificación de Viabilidad |
| :--- | :--- | :--- | :--- |
| **Semanas 1–2 (Octubre)** | **Frente 1** (`Datos` + `Calidad` + `Requerimientos`) | Script reproducible `.xlsx → .csv` (UTF-8 sin BOM), diccionario de datos, validador automático de las 19 columnas, anonimización de cuasi-identificadores y reporte exploratorio (EDA) de las PYMES. | Resuelve de inmediato los 10 problemas de calidad detectados en `Dataset.csv` sin depender del clúster. |
| **Semanas 3–4 (Noviembre)** | **Frente 2** (`Datos` + `Requerimientos`) | *Pipeline* de descarga y limpieza del padrón público del **Art. 69-B del SAT** (*presuntos, definitivos, desvirtuados*), estructurado para aprendizaje *Positive-Unlabeled (PU)* (Medina-Hernández et al., 2025). | Es información 100% pública y constituye la única fuente con casos confirmados para construir redes reales. |
| **Semanas 5–6 (Fin Nov.)** | **Frente 3** (`Arquitectura` + `Calidad`) | Construcción y visualización de grafos societarios preliminares (`NetworkX` y `PyVis`) y cálculo de métricas de centralidad y comunidades (Luna-Pla y Nicolás-Carlock, 2020–2023). | Corre localmente en segundos y cumple el hito de grafos preliminares a finales de noviembre. |
| **Semanas 7–8 (Mediados Dic.)** | **Frente 4** (`Arquitectura` + Todo el grupo) | Empaquetado final sin salida a pantalla (`stdout`), scripts `sbatch` para Slurm y entrega del repositorio listo para que el Dr. Ledesma ejecute la corrida oficial en CIMAT antes del 31-dic. | Garantiza reproducibilidad técnica y cumplimiento puntual del informe obligatorio ante el CIMAT. |

---

## Anexo A — Declaración de Uso de Herramientas de Inteligencia Artificial

En cumplimiento de las reglas de transparencia de la actividad ([*Actividad Informe ejecutivo*, Reglas importantes]):
* **Herramienta utilizada:** Asistente de codificación y análisis *Antigravity (Gemini)* como apoyo para la estructuración editorial, verificación cruzada de los archivos de la carpeta `Contexto`, perfilado programático de las 18 filas y 19 columnas de [`Dataset.csv`](../data/raw/Dataset.csv) y generación de plantillas de validación en Python.
* **Responsabilidad y autoría del grupo:** Todo diagnóstico, interpretación de inconsistencias entre versiones, formulación de preguntas para el área de Derecho y propuestas de arquitectura fueron revisados, validados y asumidos íntegramente por los 8 integrantes del grupo para su defensa oral ante el Dr. Manuel Ledesma López.

## Anexo B — Documentos del Proyecto Citados

1. **Ledesma López, M. (29 de septiembre de 2026).** *El Proyecto CIMAT, explicado sin tecnicismos legales. Documento de apoyo para la reunión con el equipo de Ciencia de Datos*. (`Explicación.docx`).
2. **Ledesma López, M. (28 de septiembre de 2026).** *Guion — Primera Sesión de Trabajo Conjunta, Ciencia de Datos × Proyecto CIMAT*. (`2026-09-28_guion_primera_sesion_trabajo_ciencia_datos_v1.md.docx`).
3. **Ledesma López, M. (28 de septiembre de 2026).** *Referencias de Literatura Relacionada — Modelado de Grafos y Analítica de Datos Masivos para la Detección Preventiva de Redes de Evasión Fiscal*. (`2026-09-28_referencias_literatura_relacionada_v1.md.docx`).
4. **Proyecto CIMAT–UDEC (septiembre de 2026).** *Dataset piloto consolidado de diagnósticos de madurez de compliance ISO 37301*. (`Dataset.csv` / `2026-09-18_dataset-consolidado-pymes-h1_v1.xlsx`).
5. **CIMAT (2025).** *Manual de Acceso a Recursos de Supercómputo del CIMAT: Guanajuato / Puerto Interior / Mérida*. (`Manual de Acceso a Recursos-1.pdf`).
6. **CONACYT – CIMAT (2019).** *Reglamento del Laboratorio de Supercómputo del Bajío, Versión 1 (08/01/19)*. (`Reglamento lab de supercomputo.pdf`).
7. **Universidad de Celaya (septiembre de 2026).** *Lámina resumen de la sesión de arranque: Proyecto CIMAT — Datos + Derecho + Tecnología para apoyar a las MIPYMES* y *Definición de Equipos*. (`CIMAT.png`, `Equipos.md`).
