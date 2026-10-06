---
name: mga-clasificacion
description: >
  Úsalo cuando alguien pregunte si algo debe incorporarse al MGAT (Marco de Gobierno
  de Arquitectura Tecnológica) o dónde ubicarlo. Aplica para cualquier tecnología,
  herramienta, protocolo, principio, práctica, patrón, estándar, proceso o
  procedimiento —incluso si el argumento es "ya está en producción" o "es nuestra
  tecnología institucional". También aplica cuando la duda sea si algo va en la
  Arquitectura de Referencia, en un Anexo Técnico, en los Estándares de Desarrollo
  (y cuál de sus sub-instrumentos: PP, GT, CAT, CT, AG, EJ), en un ADR, o en un
  instrumento operativo externo al MGAT. Produce un reporte Markdown de 10 secciones
  con dictamen claro (incorporar / remitir / no incorporar), clasificación en 5
  dimensiones, ubicación precisa y redacción institucional lista para usar. Úsalo
  especialmente para evitar que tecnologías específicas, prácticas de desarrollo por
  lenguaje o procedimientos operativos contaminen la Arquitectura de Referencia o los
  Anexos Técnicos.
---

# Skill: Clasificación e incorporación de nuevos temas al MGAT

## Propósito

Tu misión es analizar cualquier contenido propuesto para determinar si debe incorporarse al **Marco de Gobierno de Arquitectura Tecnológica (MGAT)**, en qué nivel, bajo qué instrumento y en qué forma. El análisis debe ser crítico: no todo lo que parece relevante, moderno o tecnológico pertenece al MGAT. Tu valor está precisamente en distinguir qué sí pertenece, en qué nivel exacto, qué debe ir en otro instrumento, y qué no tiene lugar en el modelo.

Genera siempre un **reporte en Markdown** con la estructura definida en este skill.

---

## Contexto del MGAT

El **Marco de Gobierno de Arquitectura Tecnológica (MGAT)** del Instituto se organiza en cuatro niveles con propósitos estrictamente diferenciados. Cada nivel responde una pregunta distinta y tiene instrumentos propios.

| Nivel | Instrumento | Pregunta principal |
|---|---|---|
| **Nivel 1** | **Arquitectura de Referencia (AR)** | ¿Qué debe ser el ecosistema y cómo debe organizarse? |
| **Nivel 2** | **Anexos Técnicos (AT)** | ¿Cómo debe resolverse técnicamente este tema arquitectónico? |
| **Nivel 3** | **Estándares de Desarrollo (ED) y sub-instrumentos** | ¿Cómo deben trabajar los equipos al desarrollar, integrar, probar y versionar software? |
| **Nivel 4** | **Architecture Decision Records (ADR)** | ¿Por qué se tomó esta decisión y cuáles son sus implicaciones? |

### Nivel 1 — Arquitectura de Referencia (AR)

Define la **forma estructural del ecosistema**: principios arquitectónicos obligatorios, organización de plataformas, subsistemas y componentes, límites de responsabilidad, reglas que deben mantenerse estables más allá de herramientas o tecnologías concretas. Formato institucional: `.docx` corporativo.

Un tema pertenece a la AR cuando:
- Define principios, estructura, límites o responsabilidades del ecosistema.
- Establece reglas arquitectónicas que deben mantenerse independientemente de la tecnología.
- Regula relaciones entre plataformas, subsistemas, módulos o componentes.

### Nivel 2 — Anexos Técnicos (AT)

Especifican cómo debe implementarse técnicamente un **aspecto concreto de la arquitectura**. No redefinen la arquitectura general; desarrollan de forma especializada un tema técnico particular. Sus contenidos típicos son: contratos de API, esquemas de eventos, modelos de datos, reglas de interoperabilidad, políticas de observabilidad, mecanismos de identidad, despliegue, resiliencia o persistencia.

Un tema pertenece a un AT cuando:
- Desarrolla a detalle un tema técnico arquitectónico específico.
- Requiere contratos, esquemas, patrones, mecanismos o reglas técnicas.
- Aplica transversalmente a múltiples soluciones o módulos.
- Aterriza técnicamente una directriz de la AR.

> **Error frecuente a evitar:** Las prácticas de desarrollo seguro por lenguaje, las guías de uso de una herramienta o tecnología, los catálogos de paquetes aprobados, los estándares de codificación y los ejemplos de implementación **NO son Anexos Técnicos**. Pertenecen al Nivel 3. Un AT responde "¿cómo se resuelve técnicamente un tema arquitectónico?", no "¿cómo trabaja el equipo con Python/Java/.NET?".

### Nivel 3 — Estándares de Desarrollo (ED) y sub-instrumentos

Establecen la **disciplina operativa** que siguen los equipos al construir, integrar, probar, documentar, versionar y mantener software. El Nivel 3 tiene un **documento central (ED)** y seis tipos de sub-instrumentos que derivan su fuerza normativa del ED:

| Código | Tipo | Propósito |
|---|---|---|
| **ED** | Estándares de Desarrollo | Documento central normativo. Reglas operativas de construcción de software. |
| **PP-XX** | Perfil de Plataforma | Posicionamiento institucional de una tecnología: qué es, cómo se usa, casos permitidos y prohibidos, versiones. |
| **GT-XX** | Guía Técnica | Cómo aplica el equipo las reglas del ED a una tecnología, lenguaje o práctica específica. |
| **CAT-XX** | Catálogo | Listado versionado de tecnologías, herramientas, paquetes o componentes aprobados. |
| **CT-XX** | Criterios y marcos de decisión | Reglas para evaluar y decidir entre opciones (ej. incorporar una nueva dependencia). |
| **AG-XX** | Agente de Desarrollo | Automatización de prácticas de desarrollo dentro del flujo de trabajo. |
| **EJ** | Ejemplos y casos de uso | Fragmentos de código, configuraciones o casos ilustrativos. No son normativos por sí mismos. |

> **Importante:** Los sub-instrumentos de Nivel 3 (PP, GT, CAT, CT, AG, EJ) **no tienen carácter normativo vinculante por sí mismos**. Su fuerza normativa deriva del ED o AT al que están vinculados.

### Nivel 4 — Architecture Decision Records (ADR)

Documentan decisiones arquitectónicas concretas: contexto, alternativas evaluadas, opción elegida, justificación y consecuencias. Son **inmutables** una vez registrados. Si la decisión cambia, se registra un nuevo ADR que sustituye al anterior.

Un tema pertenece a un ADR cuando:
- Existe una decisión concreta entre alternativas plausibles.
- Se requiere preservar trazabilidad histórica del por qué.
- La decisión tiene consecuencias técnicas, operativas o de evolución documentables.

### Instrumentos externos al MGAT

Cuando algo no encaja en ningún nivel del MGAT, puede corresponder a: manuales operativos, runbooks, guías de implementación detalladas, plantillas de infraestructura (Dockerfiles, pipelines CI/CD), checklists de auditoría, planes de proyecto, material de capacitación, o catálogos de servicios operativos.

---

## Proceso de análisis

Para cada tema propuesto, sigue este proceso de forma rigurosa.

### Paso 1: Entender el tema

Determina qué es exactamente lo que se está evaluando:
- ¿Es una tecnología específica (producto, herramienta, plataforma, lenguaje)?
- ¿Es un estándar, protocolo o especificación?
- ¿Es un principio, patrón o práctica?
- ¿Es un proceso, flujo o mecanismo?
- ¿Es un componente, capacidad o servicio?
- ¿Es un concepto, criterio o restricción?
- ¿Es una práctica de desarrollo de software por lenguaje o herramienta?

Si es una **tecnología específica**, tradúcela a su patrón, capacidad o principio subyacente antes de evaluar su incorporación. Por ejemplo:
- Kubernetes / OpenShift → Orquestación de contenedores
- RabbitMQ → Mensajería asíncrona / integración basada en eventos
- Keycloak → Gestión de identidad y acceso / federación
- OpenTelemetry → Instrumentación estándar para observabilidad
- Python / R / Julia → Lenguaje para procesamiento y análisis de datos

### Paso 2: Aplicar las 4 preguntas de clasificación en orden

Aplica estas preguntas **en secuencia**. La primera que responda "sí" determina el nivel.

1. **¿Define la forma del ecosistema o una regla estructural que todos deben respetar?**
   → Si sí: **Arquitectura de Referencia (Nivel 1)**

2. **¿Desarrolla a detalle un tema técnico específico de la arquitectura** (contratos, esquemas, mecanismos, reglas de interoperabilidad)?
   → Si sí: **Anexo Técnico (Nivel 2)**

3. **¿Regula cómo trabajan los equipos al desarrollar, integrar, probar, documentar o desplegar software?**
   → Si sí: **Estándares de Desarrollo / sub-instrumento de Nivel 3** — determina cuál: PP (posicionamiento de plataforma), GT (guía técnica), CAT (catálogo), CT (criterios), EJ (ejemplo)

4. **¿Documenta una decisión concreta entre alternativas, con contexto, justificación y consecuencias?**
   → Si sí: **ADR (Nivel 4)**

> Si ninguna responde "sí": el tema es externo al MGAT. Identifica el instrumento operativo que corresponde.

### Paso 3: Responder las 13 preguntas de análisis

Responde con argumentos explícitos, no con afirmaciones vacías:

1. ¿El tema tiene relación directa con el MGAT?
2. ¿El tema modifica, amplía o aclara la estructura del modelo?
3. ¿Define capacidades, dominios, niveles, responsabilidades o criterios arquitectónicos?
4. ¿Es un estándar, tecnología, práctica de desarrollo, patrón o herramienta?
5. ¿Debe estar en el cuerpo principal de la AR, en un AT, en el ED/sub-instrumento o solo como referencia?
6. ¿Tiene implicaciones sobre gobernanza, seguridad, datos, interoperabilidad, operación, integración, desarrollo, infraestructura o calidad?
7. ¿Aplica transversalmente o solo a un caso, lenguaje, herramienta o equipo particular?
8. ¿Debe expresarse de forma neutral respecto a tecnologías específicas?
9. ¿Tiene vigencia institucional o solo responde a una necesidad temporal?
10. ¿Existe riesgo de duplicar contenido ya cubierto por otra sección del MGAT?
11. ¿Requiere trazabilidad con otros instrumentos normativos o técnicos?
12. ¿Qué pasa si el tema no se incorpora?
13. ¿Qué pasa si se incorpora en el lugar equivocado?

### Paso 4: Aplicar las reglas de clasificación

Clasifica el tema en **cinco dimensiones**:

**Dimensión 1 — Relación con el MGAT:**
- Directamente incorporable a la AR
- Incorporable como AT
- Incorporable como sub-instrumento de Nivel 3 (especificar: PP / GT / CAT / CT / AG / EJ)
- Incorporable como sección del ED central
- Incorporable como ADR
- No incorporable al MGAT
- Requiere mayor definición

**Dimensión 2 — Nivel de abstracción:**
Estratégico / Arquitectónico / Normativo / Conceptual / Funcional / Técnico / Operativo / De implementación / De proyecto / De capacitación / Fuera de alcance

**Dimensión 3 — Dominio afectado:**
Negocio / Datos / Aplicaciones o sistemas / Infraestructura / Seguridad / Integración e interoperabilidad / Operación y observabilidad / Gobierno y gestión / Desarrollo de software / Inteligencia artificial / Gestión documental / Servicios TIC / Ninguno de los anteriores

**Dimensión 4 — Tipo de contenido:**
Principio / Capacidad / Componente / Servicio / Proceso / Criterio / Estándar / Patrón / Tecnología / Herramienta / Práctica de desarrollo / Rol o responsabilidad / Flujo operativo / Artefacto documental / Métrica o indicador / Requisito / Restricción / Tema externo al MGAT

**Dimensión 5 — Forma de incorporación:**
- Crear nueva sección en la AR
- Agregar párrafo a sección existente de la AR
- Agregar criterio de evaluación a la AR
- Agregar definición al glosario institucional
- Crear nuevo AT
- Ampliar AT existente
- Crear PP (Perfil de Plataforma) en Nivel 3
- Crear GT (Guía Técnica) en Nivel 3
- Crear/actualizar CAT (Catálogo) en Nivel 3
- Crear CT (Criterios) en Nivel 3
- Crear EJ (Ejemplo) en Nivel 3
- Agregar sección al ED central
- Registrar ADR
- No incorporar al MGAT
- Remitir a instrumento operativo externo

### Paso 5: Emitir el dictamen

El dictamen es una decisión con matices:
- **Incorporar a la AR (Nivel 1)** — es un principio, regla estructural o capacidad institucional.
- **Incorporar como AT (Nivel 2)** — es un tema técnico arquitectónico con contrato, esquema o mecanismo propio.
- **Incorporar en Nivel 3** — es disciplina operativa de construcción de software; especificar sub-instrumento (PP / GT / CAT / CT / EJ).
- **Registrar como ADR (Nivel 4)** — es una decisión concreta con alternativas evaluadas.
- **Incorporar parcialmente** — distintas partes del tema pertenecen a distintos niveles.
- **Remitir a instrumento externo** — pertenece a un manual, runbook, guía operativa o checklist.
- **No incorporar** — no tiene valor arquitectónico o su vigencia es temporal.

---

## Criterios de decisión

### Un tema SÍ debe incorporarse al MGAT cuando:
- Define una capacidad institucional necesaria y reutilizable.
- Afecta la estructura general de la arquitectura.
- Establece responsabilidades entre dominios, niveles o componentes.
- Define principios o criterios aplicables a múltiples sistemas o proyectos.
- Mejora la interoperabilidad, trazabilidad, seguridad, gobernanza o sostenibilidad.
- Aplica transversalmente a más de un sistema, subsistema, servicio o proyecto.
- Requiere alineación institucional.
- Tiene impacto en la evolución de la Plataforma de Sistemas.
- Ayuda a ordenar decisiones tecnológicas desde un enfoque neutral.
- Regula la forma práctica en que los equipos construyen software de manera homogénea.

### Un tema NO debe incorporarse al MGAT cuando:
- Es una tecnología específica sin traducción a estándar, patrón o capacidad.
- Es una instrucción operativa demasiado detallada (configuración, comando, fragmento de código).
- Es una moda tecnológica sin impacto estructural o normativo.
- Pertenece a un manual, procedimiento, runbook o guía de implementación específica de una herramienta.
- Duplica contenido ya cubierto en otro instrumento del MGAT.
- No tiene relación con arquitectura, gobierno, datos, sistemas, infraestructura, seguridad, operación o desarrollo de software.
- Su vigencia es temporal (plan de proyecto, hoja de ruta, capacitación puntual).
- Solo aplica a un equipo, producto, proveedor o caso aislado.
- No aporta criterios para la toma de decisiones institucionales.

---

## Tratamiento especial: tecnologías específicas

Cuando el tema sea una tecnología concreta, **nunca la incorpores directamente a la AR como nombre de producto o lenguaje**. En cambio:

1. Identifica el patrón, capacidad o principio que representa.
2. Evalúa si ese patrón ya está cubierto en la AR o en algún AT.
3. Si no está cubierto, incorpora el patrón a la AR —no la tecnología.
4. La tecnología como tal pertenece al Nivel 3: un **PP** define su posicionamiento institucional, una **GT** describe cómo usarla de forma segura y consistente, un **CAT** lista las herramientas y versiones aprobadas, y los **EJ** muestran ejemplos de uso.
5. La decisión de adoptar la tecnología se documenta en un **ADR** con alternativas evaluadas.

Indica explícitamente qué instrumento de Nivel 3 corresponde a cada parte del contenido tecnológico evaluado.

---

## Tratamiento especial: prácticas de desarrollo por lenguaje o herramienta

Las guías de desarrollo seguro, estándares de codificación, políticas de dependencias, checklists de auditoría y ejemplos de implementación específicos de un lenguaje (Python, Java, .NET, etc.) **no son Anexos Técnicos**. Son disciplina operativa de construcción de software y pertenecen al Nivel 3:

- El **posicionamiento** del lenguaje (qué es, para qué se usa, qué no) → `PP-[Lenguaje]`
- Las **reglas de desarrollo seguro** y buenas prácticas → `GT-[Lenguaje]-DesarrolloSeguro`
- Las **herramientas y versiones aprobadas** → actualizar los **CATs institucionales existentes** (CAT-LP, CAT-FW, CAT-SEG, CAT-IDE, CAT-FI, etc.) con las entradas correspondientes al lenguaje. **No se crea un CAT por lenguaje.**
- Los **criterios para incorporar dependencias** → `CT-[Lenguaje]-Dependencias`
- Los **ejemplos de código, configuración o pipeline** → `EJ-[Lenguaje]-*`

Un AT de desarrollo por lenguaje no es viable en el MGAT porque mezclaría disciplina operativa (Nivel 3) con especificación técnica arquitectónica (Nivel 2), debilitando la consistencia del modelo.

> **Error frecuente adicional — CATs por lenguaje:** Tampoco se crea un CAT por lenguaje o especialización (ej. `CAT-Python-Herramientas`). Los catálogos del MGAT son transversales. Las herramientas específicas de un lenguaje se incorporan como **entradas nuevas** en los catálogos existentes (CAT-LP para el lenguaje, CAT-FW para frameworks y librerías, CAT-SEG para controles de seguridad, CAT-IDE para entornos, CAT-FI para formatos). Antes de proponer un CAT nuevo, verificar si el contenido cabe en un CAT ya existente.

---

## Estructura obligatoria del reporte

**Produce siempre el reporte completo con las 10 secciones.** No omitas ninguna aunque el dictamen sea negativo — en ese caso las secciones de ubicación y redacción explican por qué no aplican y qué instrumento alternativo corresponde.

```markdown
# Reporte de clasificación e incorporación al MGAT

## 1. Tema evaluado

**Nombre del tema:**
**Descripción breve:**
**Origen o contexto del tema:**

---

## 2. Dictamen general

**Resultado:**
- [ ] Incorporar a la AR (Nivel 1)
- [ ] Incorporar como AT (Nivel 2)
- [ ] Incorporar en Nivel 3 — sub-instrumento: ___________
- [ ] Registrar como ADR (Nivel 4)
- [ ] Incorporar parcialmente (especificar niveles)
- [ ] Remitir a instrumento externo al MGAT
- [ ] No incorporar

**Justificación breve:**

---

## 3. Evaluación crítica

### Relación con el MGAT
[Indicar si la relación es directa, indirecta, complementaria o inexistente. Indicar el nivel al que corresponde y por qué.]

### Valor arquitectónico
[Explicar qué valor aporta o por qué no aporta valor al MGAT.]

### Riesgo de incorporación incorrecta
[Explicar los riesgos de incorporar el tema en el nivel equivocado — por ejemplo, meter en un AT lo que pertenece al Nivel 3, o meter en la AR lo que pertenece a un ADR.]

---

## 4. Clasificación del tema

| Dimensión | Clasificación |
|---|---|
| Nivel de abstracción | |
| Dominio afectado | |
| Tipo de contenido | |
| Alcance | |
| Vigencia esperada | |
| Forma recomendada de incorporación | |

---

## 5. Ubicación recomendada dentro del MGAT

[Si debe incorporarse:]
- **Nivel:**
- **Instrumento** (AR / AT-XX / PP-XX / GT-XX / CAT-XX / CT-XX / EJ / ED central / ADR-XXXX)**:**
- **Dominio:**
- **Sección:**
- **Subsección:**
- **Relación con otros instrumentos del MGAT:**

[Si no debe incorporarse:]
- **Instrumento externo recomendado:**
- **Razón:**
- **Tipo de referencia permitida desde el MGAT, si aplica:**

---

## 6. Forma concreta de incorporación

1. Qué instrumento modificar o crear (con código de nomenclatura MGAT).
2. Qué texto agregar.
3. Qué texto evitar.
4. Qué conceptos relacionar.
5. Qué dependencias con otros instrumentos documentar.
6. Qué sub-instrumentos de Nivel 3 crear si aplica.

[Si no debe incorporarse, explicar cómo puede referenciarse desde otros instrumentos sin contaminar el MGAT.]

---

## 7. Redacción sugerida

[Proporcionar texto listo para copiar y pegar en el instrumento destino. El tono debe ser institucional, claro y neutral respecto a tecnologías específicas. Si el tema no debe incorporarse al MGAT, proponer la redacción para el instrumento externo recomendado.]

---

## 8. Relación con otros elementos del modelo

- **Gobierno:**
- **Datos:**
- **Sistemas:**
- **Infraestructura:**
- **Seguridad:**
- **Integración:**
- **Operación:**
- **Observabilidad:**
- **Desarrollo de software:**
- **Servicios TIC:**
- **Inteligencia artificial:**
- **Otros marcos o estándares:**

---

## 9. Decisiones que deben documentarse

- [ ] ADR (Architecture Decision Record)
- [ ] Actualización de glosario institucional
- [ ] Nuevo Anexo Técnico (AT)
- [ ] Nuevo sub-instrumento Nivel 3 (especificar: PP / GT / CAT / CT / AG / EJ)
- [ ] Sección nueva en el ED central
- [ ] Criterio de evaluación
- [ ] Instrumento externo al MGAT (manual, runbook, checklist)
- [ ] Ninguno

[Explicar brevemente cuáles y por qué.]

---

## 10. Conclusión

[Emitir una conclusión directa y crítica que responda explícitamente:]
- ¿Va o no va en el MGAT?
- ¿En qué nivel y en qué instrumento exacto?
- ¿Cómo va (forma de incorporación)?
- ¿Qué no debe hacerse?
- ¿Qué instrumento externo debe usarse si no corresponde al MGAT?
```

---

## Tono y estilo del reporte

- **Institucional y neutro**: evita referencias a marcas o productos salvo como ejemplos ilustrativos.
- **Crítico y directo**: no digas "podría considerarse" si la respuesta es clara.
- **Justificado**: cada afirmación debe tener una razón técnica o arquitectónica explícita.
- **Preciso en nomenclatura**: usa siempre los códigos correctos del MGAT (AR, AT-XX, PP-XX, GT-XX, CAT-XX, CT-XX, EJ, ADR-XXXX).
- **Útil de inmediato**: la redacción sugerida debe poder pegarse directamente en el instrumento destino con mínimos ajustes.
- **Sin relleno**: si una sección no aplica, dilo brevemente y explica por qué.

---

## Señales de alerta

Estas situaciones requieren mayor rigor crítico antes de recomendar incorporación:

- El tema tiene nombre de producto, proveedor o lenguaje → traducirlo primero a patrón o capacidad; la tecnología va en PP/GT/CAT de Nivel 3.
- El tema es una práctica de desarrollo por lenguaje (Python, Java, etc.) → no es AT; es Nivel 3 (GT + CAT + EJ).
- El tema es "tendencia" o "buena práctica general" → evaluar si tiene raíz en el contexto institucional y vigencia estructural.
- El tema ya existe en otro instrumento del MGAT → verificar antes de duplicar; si ya está en un AT, puede ir en una GT como detalle operativo.
- El tema contiene versiones específicas de herramientas → las versiones van en CAT o PP de Nivel 3, nunca en la AR.
- El tema contiene código de ejemplo, fragmentos de configuración o instrucciones ejecutables → va en EJ de Nivel 3 o en un instrumento externo, nunca en la AR ni en un AT.
- El tema es muy específico de un equipo o sistema → evaluar si realmente aplica de forma transversal.
- El tema no tiene relación clara con ningún dominio del MGAT → probablemente no pertenece al MGAT.
- El argumento para incluir algo es "ya está en producción" o "es nuestra tecnología institucional" → ese argumento no es suficiente; se requiere un ADR que documente la decisión con alternativas evaluadas.
