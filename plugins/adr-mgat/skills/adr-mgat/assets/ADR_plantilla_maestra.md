---
número: "ADR-NNNN"
título: "[Título conciso de la decisión — qué se decidió]"
estado: "Propuesta"           # Propuesta | Vigente | Deprecada | Sustituida
fecha: "YYYY-MM-DD"
autor: "[Nombre o equipo]"
revisores: []                 # Lista de revisores (opcional)
sistemas-afectados:
  - "[Sistema o componente 1]"
  - "[Sistema o componente 2]"
instrumentos-mgat-relacionados:
  - tipo: "[AR | AT | ED | ADR]"
    referencia: "[Código o nombre del instrumento]"
    relación: "[referencia | excepción | actualiza | sustituye]"
sustituye: ""                 # Completar si este ADR reemplaza a otro: "ADR-XXXX"
sustituido-por: ""            # Completar si este ADR fue reemplazado: "ADR-XXXX"
# Completar si la decisión involucra tecnología externa (librería, framework,
# plataforma, protocolo, herramienta o servicio). Omitir si no aplica.
tecnologia-externa:
  aplica: false               # true si la decisión involucra tecnología externa
  tecnologia-adoptada:
    nombre: ""
    version: ""
    licencia-spdx: ""         # Ej: MIT, Apache-2.0, GPL-3.0, Proprietary
    tipo-soporte: ""          # Comunidad | Comunidad + sponsor corporativo | Soporte comercial opcional | Soporte comercial obligatorio
    estado-ciclo-vida: ""     # Activa | LTS | EOL
    eol-fecha: ""             # Fecha de fin de soporte declarada, si existe
    url-licencia: ""
    notas-licencia: ""        # Restricciones relevantes, cambios de licencia históricos, etc.
---

# ADR-NNNN — [Título conciso de la decisión]

## 1. Contexto

<!--
Describe el problema o situación que motivó esta decisión.
Incluye:
- El estado actual del sistema o del ecosistema relevante
- Las restricciones técnicas, institucionales o de tiempo que condicionaron la decisión
- Qué pasaría si no se toma ninguna decisión (status quo)
- Referencias a principios o directrices del MGAT que aplican

Este bloque debe ser comprensible para alguien que no vivió la situación.
-->

## 2. Decisión

<!--
Una o dos oraciones que enuncien claramente qué se decidió.
Debe ser directa y específica, no ambigua.

Ejemplo: "Se adopta el enfoque contract-first con OpenAPI 3.1 como estándar
para la definición de contratos de API en todos los módulos del ecosistema."
-->

## 3. Alternativas evaluadas

<!--
Lista las opciones que se consideraron seriamente.
No incluyas alternativas que no se evaluaron realmente.
Una tabla es el formato recomendado.

Si la decisión involucra tecnología externa, usa la tabla extendida con
columnas de Licencia y Soporte técnico. Estas columnas son obligatorias
en ese caso: el ADR debe registrar formalmente bajo qué términos legales
y con qué garantía de mantenimiento se adopta cada opción, incluyendo la
elegida. "Comunidad sin garantía comercial" es una decisión consciente que
debe quedar escrita.

Para decisiones que no involucran tecnología externa (p. ej. patrones
arquitectónicos, excepciones a reglas del MGAT), usa la tabla básica.
-->

### Tabla básica (decisiones sin tecnología externa)

| Alternativa | Descripción breve | Ventajas | Desventajas |
|-------------|-------------------|----------|-------------|
| **[Opción A — la elegida]** | | | |
| **[Opción B]** | | | |
| **[Opción C]** | | | |

### Tabla extendida (cuando la decisión involucra tecnología externa)

<!--
Licencia: identificador SPDX (MIT, Apache-2.0, GPL-3.0, LGPL-2.1, Proprietary, etc.)
Soporte: Comunidad | Comunidad + sponsor corporativo | Soporte comercial opcional | Soporte comercial obligatorio
Ciclo de vida: versión activa | LTS hasta YYYY | EOL desde YYYY
-->

| Alternativa | Descripción breve | Licencia | Soporte técnico | Ciclo de vida | Ventajas | Desventajas |
|-------------|-------------------|----------|-----------------|---------------|----------|-------------|
| **[Opción A — la elegida]** | | | | | | |
| **[Opción B]** | | | | | | |
| **[Opción C]** | | | | | | |

## 4. Justificación

<!--
Explica por qué la opción elegida es la más adecuada para este contexto.
- Argumenta con base en los criterios relevantes: riesgo técnico, alineación
  con la AR, costo de implementación, reversibilidad, madurez, etc.
- Si la decisión involucra trade-offs explícitos (sacrificar X para ganar Y),
  nómbralos con honestidad.
- Evita justificaciones genéricas. "Es la mejor práctica" no es una
  justificación: explica por qué es la mejor práctica *en este contexto*.
-->

## 5. Consecuencias

### 5.1 Impactos positivos

<!--
Qué mejora, se simplifica o se habilita gracias a esta decisión.
-->

- 

### 5.2 Riesgos y compromisos asumidos

<!--
Qué se sacrifica, complica o restringe como resultado de esta decisión.
Incluye deudas técnicas conocidas o riesgos que deberán gestionarse.

Si la decisión involucra tecnología externa, incluye aquí los riesgos de
licenciamiento y soporte: ¿qué implica operar con soporte comunitario sin
SLA? ¿hay riesgo de cambio de licencia (ej. BSL, SSPL)? ¿qué pasa si la
comunidad abandona el proyecto o si el sponsor corporativo cambia su política?
Nombrar estos riesgos es tan importante como nombrar los riesgos técnicos.
-->

- 

### 5.3 Impacto en el ecosistema

<!--
Cómo afecta esta decisión a los sistemas, módulos o componentes identificados.
¿Requiere cambios en otros componentes? ¿Genera dependencias nuevas?
-->

- 

### 5.4 Evolución futura

<!--
¿Cuándo debería revisarse esta decisión?
¿Qué condiciones harían obsoleto este ADR?
¿Existe una hoja de ruta hacia una solución más definitiva?
-->

- 

## 6. Relación con el MGAT

<!--
Documenta explícitamente cómo este ADR se relaciona con otros instrumentos.
-->

| Instrumento | Código / Referencia | Tipo de relación |
|-------------|---------------------|------------------|
| | | Referencia normativa |
| | | Excepción documentada |
| | | Requiere actualización |

> **Nota sobre excepciones:** Si este ADR establece una excepción a una
> regla de un AT o ED vigente, esa excepción es válida **solo para el
> contexto descrito en este ADR** y **no modifica el instrumento de referencia**.
> Para que la excepción sea permanente, el AT o ED debe actualizarse formalmente.

## 7. Estado y trazabilidad

| Campo | Valor |
|-------|-------|
| Estado actual | `Propuesta` |
| Fecha de propuesta | YYYY-MM-DD |
| Fecha de aprobación | — |
| Aprobado por | — |
| Sustituye a | — |
| Sustituido por | — |

---

*Este ADR es un instrumento de Nivel 4 del Marco de Gobierno de Arquitectura
Tecnológica (MGAT). Una vez aprobado y marcado como `Vigente`, es inmutable.
Si la decisión cambia, registrar un nuevo ADR que lo sustituya y actualizar
el campo `Sustituido por` de este documento.*
