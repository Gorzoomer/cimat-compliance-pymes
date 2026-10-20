# Cuestionario Técnico-Jurídico para el Área de Derecho

**Subequipo responsable:** Equipo de Requerimientos (`Mariana M.R.`, `Pau N.L.`) en coordinación con Datos y Calidad  
**Propósito:** Resolver las definiciones jurídicas y de negocio indispensables antes de congelar las reglas de programación de los Frentes 1, 2 y 3.

---

## Preguntas Prioritarias Antes de Programar

### Bloque A — Sobre el Dataset de PYMES (Pieza A, Frente 1)

1. **Regla de conversión entre Riesgo (Probabilidad $\times$ Impacto) y Madurez ISO 37301:**
   - *Contexto:* El `equipoJP` (`CONS-SERV-01`) evaluó probabilidad e impacto del riesgo en lugar de madurez de controles internos, por lo que sus 6 filas tienen `confianza_homologacion = baja`.
   - *Pregunta:* ¿Validan jurídicamente como regla definitiva la inversión `Riesgo Alto -> Nivel 1 (Inexistente)` y `Riesgo Medio-Alto -> Nivel 2 (Ad hoc / informal)`, o desean que tratemos a `CONS-SERV-01` en una escala separada?

2. **Estándar único para los equipos de Derecho pendientes de entregar:**
   - *Contexto:* En el primer corte convivieron tres escalas distintas (1–2, 1–4 con semáforo y matriz de riesgo) y una tabla pegada como imagen en Word.
   - *Pregunta:* Para los equipos que faltan por entregar en el semestre, ¿se les exigirá entregar en una plantilla única de Excel/CSV con **escala de madurez 1 a 4**, o debemos programar reglas de conversión para múltiples escalas?

3. **Autorización para sanitizar cuasi-identificadores en `observaciones_calidad_dato` y valores puntuales:**
   - *Contexto:* En `CONS-SERV-01`, la columna `observaciones_calidad_dato` menciona explícitamente el municipio de **Villagrán**, **11 años de antigüedad** y **4 personas**; y en `COS-BJ-01` se dejaron `"6 años"` y `"14 empleados"` sin agrupar en bandas.
   - *Pregunta:* ¿Autorizan que nuestro script de limpieza reemplace esos datos exactos por sus bandas correspondientes (`5 a 10 años`, `Pequeña (11-50 empleados)`) y elimine el nombre del municipio en las notas de observaciones para evitar la re-identificación de las PYMES?

4. **Tratamiento de dimensiones sin hallazgo en entrevista vs. reportes globales:**
   - *Contexto:* En `COS-BJ-01`, tres categorías no tuvieron hallazgo durante la entrevista y se rellenaron como "riesgo base" sin acción recomendada; en `PYME-001` (`equipoN`), se copió el mismo párrafo global en las 6 categorías.
   - *Pregunta:* ¿Una categoría no abordada en la entrevista debe codificarse realmente como `Nivel 1 (Inexistente)` o como `No evaluada (NA)` para no castigar artificialmente el promedio de madurez de la PYME?

5. **Adecuación de controles ISO 37301 para Personas Físicas con Actividad Empresarial:**
   - *Contexto:* `CONS-SERV-01` es una **Persona física con actividad empresarial**, pero se le recomendó establecer un *consejo de administración de tres integrantes* (propio de sociedades mercantiles).
   - *Pregunta:* Bajo la cláusula 5.3 de ISO 37301 (*Gobierno corporativo y contrapesos*), ¿qué control equivalente es exigible a una persona física (p. ej. segregación de funciones operativas/contables o carta de poderes) para validar correctamente esa fila?

---

### Bloque B — Sobre el Listado 69-B y el Modelado de Redes (Pieza B, Frentes 2 y 3)

6. **Confirmación de la fuente oficial del SAT (`Art. 69-B` vs. `Art. 69-B Bis`):**
   - *Contexto:* El archivo HTML incluido en el material de apoyo apunta al listado del **Artículo 69-B Bis** (*transmisión indebida del derecho a disminuir pérdidas fiscales*, que contiene únicamente 2 oficios en PDF), mientras que el protocolo del proyecto estudia las **operaciones simuladas (EFOS)** reguladas en el **Artículo 69-B**.
   - *Pregunta:* ¿Confirmamos que debemos construir el Frente 2 exclusivamente con el padrón de Datos Abiertos del **Artículo 69-B** (EFOS) y qué peso probatorio debemos asignar a cada uno de sus cuatro estatus (*Definitivo, Presunto, Desvirtuado, Sentencia Favorable*)?

7. **Fuentes públicas autorizadas para extraer relaciones societarias (aristas del grafo):**
   - *Contexto:* El listado público del Art. 69-B del SAT proporciona RFC, razón social, estatus y fechas de publicación en el SAT/DOF, pero no desglosa por sí solo quiénes son los socios, representantes legales, comisarios o notarios.
   - *Pregunta:* ¿De qué fuentes públicas específicas (Registro Público de la Propiedad y el Comercio / SIGER, Boletín Registral, compranet / contrataciones públicas o acervos ya recopilados por Derecho) obtendremos los nombres de representantes legales y domicilios para conectar los nodos del grafo en el Frente 3?

8. **Estatus jurídico de las fuentes de la Pieza A y convenio de confidencialidad:**
   - *Contexto:* En el guion de trabajo del 28 de septiembre se mencionó como pendiente confirmar si la totalidad de los diagnósticos de la materia de Derecho provienen de empresas reales o de casos simulados, así como la posible firma de un acuerdo de confidencialidad.
   - *Pregunta:* ¿Los alumnos de Ciencia de Datos debemos firmar un documento de confidencialidad adicional antes de recibir los diagnósticos de los equipos restantes de Derecho?
