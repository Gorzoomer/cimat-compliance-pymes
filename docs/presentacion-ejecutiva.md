# Guía de Presentación Ejecutiva y Defensa Oral ante el Dr. Manuel Ledesma

**Duración de exposición:** 10 a 12 minutos (participan los 8 integrantes: ~1 min 20 seg por persona)  
**Sesión de preguntas:** 5 a 8 minutos (cualquier integrante puede ser cuestionado sobre cualquier sección)  
**Apoyo visual:** Máximo 6 diapositivas (o el propio informe proyectado)  
**Regla de oro:** Lenguaje claro y no técnico. Si se menciona un término de datos o programación (*pipeline*, *grafo*, *BOM*, *Slurm*), se explica de inmediato en una frase sencilla.

---

## Parte 1: Estructura de las 6 Diapositivas

### Diapositiva 1 — El Problema Real y el Propósito del Proyecto
* **Título:** Operaciones Simuladas (Art. 69-B), Redes Societarias y Vulnerabilidad en MIPYMES
* **Puntos clave en pantalla:**
  * **El fenómeno real:** Empresas fachada (EFOS) facturan operaciones inexistentes; empresas reales (EDOS) deducen esas facturas o contratan proveedores sin verificarlos.
  * **Fuente oficial confirmada:** Listado público del **Art. 69-B del SAT** (*presuntos, definitivos, desvirtuados*).
  * **¿Por qué forman redes?** Reutilizan representantes legales, socios, notarios y domicilios fiscales $\rightarrow$ dejan una huella conectada detectable mediante **grafos** (mapas de puntos y conexiones).
* **Exponen:** **Ana Paula Navarro López (`Pau N.L.`)** [Secciones 1 y 2]

---

### Diapositiva 2 — ¿Qué Mide el Dataset (ISO 37301) y Cuál es el Alcance Honesto 2026?
* **Título:** *Compliance* ISO 37301: Vulnerabilidad Interna $\neq$ Fraude Confirmado
* **Puntos clave en pantalla:**
  * **¿Qué es *compliance*?** Nivel de preparación interna de una PYME para prevenir irregularidades (**ISO 37301**: 6 categorías fijas).
  * **¿Qué es una fila de `Dataset.csv`?** La evaluación de **1 categoría ISO 37301 en 1 PYME** (6 filas = 1 PYME completa).
  * **Pieza A vs. Pieza B:** Pieza A (diagnósticos de PYMES, vulnerabilidad) $\neq$ Pieza B (Listado 69-B, fraude confirmado). Baja calificación en ISO 37301 **no** prueba delito fiscal.
  * **Entregables reales 2026:** (1) *Pipeline* reproducible, (2) Dataset 69-B estructurado, (3) Prototipo de grafos, (4) Base metodológica para validación 2027 (*Positive-Unlabeled*).
* **Exponen:** **Santiago Alvarado Delgadillo (`Santiago A.D.`)** [Sección 3] y **Mariana Martínez Ruelas (`Mariana M.R.`)** [Sección 4]

---

### Diapositiva 3 — Diagnóstico del Dataset Piloto y Comparativa de Escalas
* **Título:** Radiografía de `Dataset.csv`: 18 Registros, 3 PYMES y 3 Escalas Incompatibles
* **Puntos clave en pantalla:**
  * **Dimensiones:** 18 filas $\times$ 19 columnas (`COS-BJ-01`, `PYME-001`, `CONS-SERV-01`).
  * **Evolución `.xlsx` (18-sep) $\rightarrow$ `.csv` (29-sep):** Se agregaron 6 columnas de homologación en borrador y notas de calidad.
  * **Tres escalas distintas:**
    1. `equiporisan` (`COS-BJ-01`): Madurez 1–2 $\rightarrow$ Confianza **Alta**.
    2. `equipoN` (`PYME-001`): Madurez 1–4 con semáforo $\rightarrow$ Confianza **Alta** *(tras corregir semáforo verde a rojo)*.
    3. `equipoJP` (`CONS-SERV-01`): Matriz *Probabilidad $\times$ Impacto* (mide riesgo, no madurez) $\rightarrow$ Confianza **Baja** (**33.3% del dataset**).
* **Expone:** **Gerardo Jamaica Grande (`Gerardo J.M.`)** [Sección 5 — Parte A]

---

### Diapositiva 4 — Hallazgos Críticos de Calidad de Datos
* **Título:** 10 Riesgos de Calidad Detectados en los Datos y Fuentes
* **Puntos clave en pantalla:**
  * **Riesgo de re-identificación:** En `CONS-SERV-01`, la columna `observaciones_calidad_dato` revela municipio exacto (*Villagrán*), antigüedad (*11 años*) y tamaño (*4 personas*); en `COS-BJ-01` hay datos exactos (*6 años, 14 empleados*) sin agrupar en bandas.
  * **Pérdida de detalle e inconsistencias jurídicas:** `equipoN` copió el mismo texto global en las 6 categorías; `equipoJP` pide crear un *consejo de administración* a una **persona física**; `equiporisan` dejó 3 categorías sin hallazgo en entrevista.
  * **Hallazgo crítico en fuente del SAT:** El archivo HTML de referencia apunta al **Art. 69-B Bis** (*pérdidas fiscales*, 2 oficios PDF) en lugar del **Art. 69-B** (*operaciones simuladas / EFOS*).
* **Expone:** **Benny Joan Salvador Mosqueda Saldaña (`Benny M.S.`)** [Sección 5 — Parte B]

---

### Diapositiva 5 — Arquitectura del Flujo de Trabajo, 4 Frentes y Reglas No Negociables
* **Título:** Roles, *Pipeline* Técnico y Reglas de Operación en el CIMAT
* **Puntos clave en pantalla:**
  * **Flujo (*Pipeline*):** `1. Limpieza (Frente 1: PYMES)` $\rightarrow$ `2. Estructuración (Frente 2: SAT 69-B)` $\rightarrow$ `3. Grafos (Frente 3: NetworkX)` $\rightarrow$ `4. Visualización y Clúster (Frente 4: PyVis + Slurm)`.
  * **Reglas no negociables:**
    1. **Anonimización total:** Cero nombres, RFC o domicilios exactos (ni en texto libre).
    2. **Uso real del supercómputo:** Volumen actual corre en laptop sin GPU; el código se prepara sin impresiones en pantalla (escritura directa a archivo) para que el **Dr. Ledesma** ejecute la corrida oficial en su cuenta `proy_ai26_manuel.ledesma`.
    3. **Fecha límite obligatoria:** **31 de diciembre de 2026** ante CIMAT.
* **Exponen:** **Luis Alonzo Hernández Silva (`Alonzo H.S.`)** [Sección 6] y **Romina Centeno Gámez (`Romina C.G.`)** [Sección 7]

---

### Diapositiva 6 — Preguntas para Derecho y Plan de Acción (Oct–Dic 2026)
* **Título:** Decisiones Jurídicas Requeridas y Hoja de Ruta Semestral
* **Puntos clave en pantalla:**
  * **Preguntas clave para Derecho antes de programar:**
    1. ¿Validan la conversión `Riesgo Alto = Madurez 1` y habrá escala única para nuevas entregas?
    2. ¿Autorizan enmascarar menciones a municipios/tamaños exactos en `observaciones_calidad_dato`?
    3. ¿Cómo diferenciar controles exigibles a *Persona física* vs. *Sociedad mercantil*?
    4. Confirmación del padrón **Art. 69-B (EFOS)** y fuentes públicas societarias (RPPC/Boletín Registral) para las conexiones del grafo.
  * **Plan de ejecución (Oct–Dic 2026):** Arrancar de inmediato con **Frente 1** (limpieza automatizada) y **Frente 2** (dataset público 69-B), prototipar grafos en noviembre (**Frente 3**) y entregar paquete reproducible para Slurm a mediados de diciembre (**Frente 4**).
* **Exponen:** **Mariana Martínez Ruelas (`Mariana M.R.`)** [Sección 8] y **Santiago Aguilar Hernández (`Santiago A.H.`)** [Sección 9]

---

## Parte 2: Guion Cronometrado por Integrante (11 Minutos Totales)

### 1. Ana Paula Navarro López (`Pau N.L.`) — *Minuto 0:00 a 1:25 (Diapositiva 1)*
> "Buenas tardes, Dr. Ledesma y equipo de Derecho. Nuestro informe ejecutivo parte de una premisa: antes de programar, debemos comprender el fenómeno real y lo que nuestros datos realmente dicen.  
> En México existen empresas que solo existen en papel y emiten facturas de operaciones simuladas —conocidas como EFOS—, mientras otras empresas deducen esas facturas o las contratan sin saberlo. Cuando el SAT confirma esta práctica, publica a la empresa en el **Listado del Artículo 69-B**.  
> El punto clave para nosotros es que estas empresas fachada no operan aisladas: para reducir costos reutilizan representantes legales, socios, notarios y domicilios fiscales. Es decir, forman **redes societarias**. Nuestro hallazgo principal al revisar los datos del proyecto es que hoy tenemos dos piezas separadas —el diagnóstico interno de 3 PYMES y el listado público del 69-B— y nuestra recomendación es avanzar en paralelo limpiando el diagnóstico actual y construyendo la base pública del 69-B para modelar esas redes."

### 2. Santiago Alvarado Delgadillo (`Santiago A.D.`) — *Minuto 1:25 a 2:45 (Diapositiva 2, primera mitad)*
> "Para entender qué mide el dataset piloto que recibimos, partimos del concepto de ***compliance***: qué tan preparada está una PYME por dentro para prevenir irregularidades. Los equipos de Derecho evaluaron a las empresas con la norma internacional **ISO 37301**, que se divide en **6 categorías fijas**: gobierno corporativo, función de cumplimiento, políticas documentadas, canal de denuncias, gestión de riesgos y gobernanza de datos e inteligencia artificial.  
> En nuestra tabla de datos (`Dataset.csv`), **cada fila no es una empresa entera ni un contrato, sino la evaluación de una sola categoría de ISO 37301 para una PYME específica**. Por eso cada PYME evaluada ocupa exactamente 6 filas consecutivas."

### 3. Mariana Martínez Ruelas (`Mariana M.R.`) — *Minuto 2:45 a 4:05 (Diapositiva 2, segunda mitad)*
> "Esto nos lleva al alcance honesto del proyecto. Debemos distinguir entre la **Pieza A** —los diagnósticos de *compliance* de las PYMES— y la **Pieza B** —el listado público del Artículo 69-B del SAT—.  
> Hoy **no es válido concluir que una PYME con baja calificación de *compliance* comete fraude fiscal**. Tener nivel 1 (*Inexistente*) significa que la microempresa es informal y vulnerable, no que emita o compre facturas falsas; además, no existe ningún vínculo probado entre las PYMES evaluadas y el listado 69-B.  
> Por ello, en 2026 no prometemos un detector predictivo, sino cuatro entregables sólidos: (1) un flujo automatizado y reproducible de datos, (2) el primer dataset estructurado del listado 69-B, (3) un prototipo exploratorio de grafos de redes y (4) la base metodológica para que en 2027 se diseñe una validación rigurosa."

### 4. Gerardo Jamaica Grande (`Gerardo J.M.`) — *Minuto 4:05 a 5:30 (Diapositiva 3)*
> "Al analizar con detalle el archivo `Dataset.csv`, encontramos **18 registros y 19 columnas**, correspondientes a **3 PYMES** (`COS-BJ-01`, `PYME-001` y `CONS-SERV-01`) evaluadas por 3 equipos de Derecho.  
> Entre la versión en Excel del 18 de septiembre y la versión CSV del 29 de septiembre se añadieron 6 columnas nuevas para intentar empatar las calificaciones. Sin embargo, los tres equipos usaron reglas de medición distintas: `equiporisan` usó una escala de madurez de 1 a 2; `equipoN` usó una escala de 1 a 4 con semáforo; pero `equipoJP` usó una **matriz de probabilidad por impacto**.  
> Medir el *riesgo de un daño* no es lo mismo que medir la *madurez de un control*. Aunque en el borrador se invirtió el riesgo alto como madurez 1, esa conversión tiene **confianza baja en 6 de las 18 filas**, es decir, en una tercera parte del dataset."

### 5. Benny Joan Salvador Mosqueda Saldaña (`Benny M.S.`) — *Minuto 5:30 a 7:00 (Diapositiva 4)*
> "Como equipo de Calidad, identificamos **10 problemas concretos en los datos**, de los cuales destaco cinco críticos:  
> Primero, **fuga de datos que permiten identificar a la empresa**: en `CONS-SERV-01`, aunque se ocultó el municipio en su columna, la nota de observaciones revela que está en **Villagrán**, tiene **11 años** y **4 personas**; y en `COS-BJ-01` se dejaron números exactos (**6 años y 14 empleados**) en lugar de rangos.  
> Segundo, **pérdida de detalle por captura global**: `equipoN` repitió exactamente el mismo texto en las 6 categorías, y en su documento original puso calificación 1 sobre 4 con semáforo verde.  
> Tercero, **incoherencia jurídica**: a `CONS-SERV-01`, que es una **persona física**, se le recomienda crear un *consejo de administración de tres integrantes*, figura propia de sociedades mercantiles.  
> Cuarto, un detalle técnico: el archivo CSV tiene un carácter invisible al inicio (llamado BOM) que altera el nombre de la primera columna si no se limpia.  
> Y quinto, un hallazgo clave en la carpeta del proyecto: el archivo web del SAT guardado apunta al **Artículo 69-B Bis** (*transmisión indebida de pérdidas fiscales*, con solo 2 oficios), cuando nosotros necesitamos el padrón del **Artículo 69-B** sobre *operaciones simuladas*."

### 6. Luis Alonzo Hernández Silva (`Alonzo H.S.`) — *Minuto 7:00 a 8:20 (Diapositiva 5, primera mitad)*
> "Para resolver esto ordenadamente, articulamos las tres áreas: Derecho aporta la curaduría legal y anonimización; CIMAT aporta la infraestructura de supercómputo; y Ciencia de Datos —dividida en nuestros subequipos de Requerimientos, Datos, Calidad y Arquitectura— construye el ***pipeline***, que es una cadena automatizada de cuatro pasos: **limpieza, estructuración, construcción de grafos y visualización**.  
> Esto se traduce en **cuatro frentes de trabajo**: Frente 1, limpiar y homologar el dataset de PYMES; Frente 2, estructurar el listado público del 69-B; Frente 3, armar y visualizar los grafos de empresas conectadas; y Frente 4, dejar el paquete de código listo para el clúster, considerando que por regla de la convocatoria del CIMAT solo el Dr. Ledesma tiene acceso de ejecución al servidor."

### 7. Romina Centeno Gámez (`Romina C.G.`) — *Minuto 8:20 a 9:35 (Diapositiva 5, segunda mitad)*
> "En esa ejecución respetamos tres **reglas no negociables**:  
> La primera es la **protección absoluta de datos personales**: ningún nombre, RFC ni domicilio exacto —tampoco pistas en las notas de observaciones— puede subir a GitHub ni al clúster.  
> La segunda es el **uso realista y correcto del supercómputo**: con 18 filas hoy no necesitamos tarjetas gráficas (GPU) ni fuerza bruta; usamos el clúster para dejar estandarizado el entorno hacia 2027. Además, siguiendo el Manual del CIMAT, nuestro programa nunca corre en el servidor de entrada ni imprime texto en pantalla, sino que guarda todo directamente en archivos para no saturar los discos del laboratorio.  
> Y la tercera es el **calendario**: todo debe estar probado y ejecutado antes del entregable obligatorio ante el CIMAT el **31 de diciembre de 2026**."

### 8. Mariana Martínez Ruelas (`Mariana M.R.`) y Santiago Aguilar Hernández (`Santiago A.H.`) — *Minuto 9:35 a 11:00 (Diapositiva 6)*
> **Mariana M.R. (Preguntas a Derecho):** "Antes de fijar las reglas en código, necesitamos que Derecho nos confirme: (1) si validan la equivalencia entre la matriz de riesgo y la escala de madurez y si fijarán una escala única para los equipos restantes; (2) si autorizan recortar los datos de Villagrán y tamaños exactos en las notas de calidad; (3) cómo evaluar la cláusula 5.3 cuando la PYME es persona física; y (4) qué fuentes públicas adicionales al 69-B (como el Registro Público de Comercio) usaremos para trazar representantes legales y domicilios compartidos."  
> **Santiago A.H. (Recomendación y Cierre):** "Con base en la literatura —como Zumaya et al. (2021) y Medina-Hernández et al. (2025) en México—, sabemos que el listado 69-B debe tratarse como casos positivos frente a casos aún no etiquetados (*Positive-Unlabeled*). Por eso recomendamos arrancar esta misma semana con los **Frentes 1 y 2**, que usan datos ya disponibles o 100% públicos y no dependen del clúster; construir los grafos preliminares en noviembre (**Frente 3**); y entregarle al Dr. Ledesma los scripts listos para **Slurm** a mediados de diciembre (**Frente 4**). Muchas gracias; quedamos abiertos a sus preguntas."

---

## Parte 3: Guía de Defensa Oral (Preguntas que Puede Hacer el Dr. Ledesma y Cómo Responderlas)

> [!IMPORTANT]
> **Recuerden:** El Dr. Ledesma puede preguntarle a **cualquier integrante sobre cualquier sección**. Todos deben dominar estas 8 respuestas clave.

1. **"¿Qué representa exactamente una fila de `Dataset.csv` y cuántas empresas hay?"**
   * **Respuesta corta:** Cada fila representa la evaluación de **una de las 6 categorías de la norma ISO 37301 para una PYME específica**. Como hay 18 filas y cada PYME tiene 6 categorías, el dataset contiene exactamente **3 PYMES** (`COS-BJ-01`, `PYME-001` y `CONS-SERV-01`), evaluadas por 3 equipos distintos.
2. **"¿Por qué dicen que no podemos concluir que `PYME-001` o `CONS-SERV-01` cometen fraude fiscal si salieron con nivel 1 (el más bajo)?"**
   * **Respuesta corta:** Porque la Pieza A solo mide **madurez de controles internos (*compliance*)**, es decir, qué tan vulnerable o informal es la empresa por dentro. No mide si emitió o compró facturas falsas, ni existe hoy ningún cruce con el listado 69-B del SAT. Confundir informalidad administrativa con delito fiscal sería metodológica y jurídicamente incorrecto.
3. **"¿Por qué el 33.3% del dataset tiene confianza de homologación 'baja'?"**
   * **Respuesta corta:** Porque el `equipoJP` (6 de las 18 filas, `CONS-SERV-01`) no usó una escala de madurez de *compliance*, sino una **matriz de riesgo de Probabilidad $\times$ Impacto** entregada como imagen en Word. Convertir "riesgo alto" en "madurez 1 (inexistente)" invierte dos conceptos distintos, por lo que solo puede tomarse como borrador de confianza baja hasta que Derecho valide la regla.
4. **"Mencionaron un error entre el Artículo 69-B y el 69-B Bis en los archivos del proyecto. ¿Cuál es la diferencia?"**
   * **Respuesta corta:** El **Artículo 69-B** regula las **operaciones simuladas o inexistentes (empresas factureras / EFOS)** y su padrón tiene miles de registros con estados de *presunto, definitivo y desvirtuado*. En cambio, la página web guardada en la carpeta (`SAT listado del Art. 69-B del CFF.htm`) corresponde al **Artículo 69-B Bis**, que trata sobre la **transmisión indebida de pérdidas fiscales** y solo tiene 2 oficios en PDF. Nuestro proyecto requiere el padrón del **69-B**, no del **69-B Bis**.
5. **"En la literatura se habla de aprendizaje *Positive-Unlabeled (PU)*. ¿Qué significa eso en palabras simples y por qué importa para el listado 69-B?"**
   * **Respuesta corta:** En un problema normal tenemos casos "positivos confirmados" y casos "negativos confirmados". Pero en evasión fiscal (Medina-Hernández et al., 2025; Mittal et al., 2018), el listado 69-B solo nos da **positivos confirmados (definitivos)**, **positivos en proceso (presuntos)** y **aclarados (desvirtuados)**. Una empresa que **no** está en el listado 69-B no está "confirmada como honesta", simplemente **no ha sido revisada o etiquetada todavía**. Tratar a todas las demás empresas como "negativos limpios" sesgaría cualquier análisis futuro.
6. **"Si el volumen actual es de 18 filas, ¿para qué queremos la supercomputadora del CIMAT?"**
   * **Respuesta corta:** Hoy 18 filas corren en milisegundos en cualquier laptop y no requieren tarjetas gráficas (GPU). El valor de preparar el código para el clúster del CIMAT hoy es **estandarizar la arquitectura reproducible** (usando el gestor de tareas *Slurm* y escribiendo directo a archivo sin imprimir en pantalla) para cuando el dataset del 69-B y los grafos de redes crezcan a decenas de miles de registros en 2027.
7. **"¿Dónde encontraron una falla de anonimización dentro del dataset si ya se habían quitado los nombres y el RFC?"**
   * **Respuesta corta:** En dos puntos: primero, en la columna `observaciones_calidad_dato` de `CONS-SERV-01` se dejó escrito que la empresa está en el municipio de **Villagrán**, tiene **11 años** y **4 empleados** en ingeniería civil (datos que combinados permiten adivinar qué empresa es); y segundo, en `COS-BJ-01` se dejaron valores exactos (**6 años** y **14 empleados**) en vez de rangos.
8. **"¿Por qué una recomendación del `equipoJP` tiene un problema jurídico en la fila 14?"**
   * **Respuesta corta:** Porque `CONS-SERV-01` está registrada como **Persona física con actividad empresarial**, y la acción recomendada le pide *"formalizar los órganos de gobierno y establecer un consejo de administración de al menos tres integrantes"*, lo cual solo aplica a personas morales (sociedades mercantiles), no a una persona física.
