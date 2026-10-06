---
name: adr-mgat
description: >
  Úsalo cuando el usuario quiera crear, redactar, proponer o documentar un
  Architecture Decision Record (ADR) dentro del Marco de Gobierno de
  Arquitectura Tecnológica (MGAT). Aplica también cuando alguien diga "quiero
  registrar una decisión arquitectónica", "necesito un ADR para...", "voy a
  documentar por qué elegimos X", "tenemos que dejar constancia de esta
  decisión", "cómo documentamos esta elección de tecnología/patrón/enfoque",
  o cuando describa una decisión técnica que ya se tomó o se está evaluando
  y necesita trazabilidad formal. Produce un ADR completo, numerado,
  correctamente clasificado y listo para incorporarse al Nivel 4 del MGAT.
  IMPORTANTE: usa este skill siempre que el usuario mencione un ADR, una
  decisión arquitectónica, o quiera dejar evidencia formal de por qué se
  eligió algo en el contexto del ecosistema tecnológico institucional.
---

# Skill: Creación de ADR conforme al MGAT

## Propósito

Un ADR (Architecture Decision Record) es el instrumento de Nivel 4 del MGAT.
Su función es preservar la **memoria técnica** del ecosistema: documentar
*por qué* se tomó una decisión concreta, qué alternativas se evaluaron, y
cuáles son las consecuencias asumidas.

Un ADR no establece reglas generales (eso es AR, AT o ED). Documenta
**una elección puntual con contexto, alternativas y justificación**.

---

## Paso 1 — Verificar que el contenido pertenece a un ADR

Antes de redactar, confirma que el tema realmente corresponde al Nivel 4.
Usa el árbol de decisión del MGAT:

1. ¿Define la forma del ecosistema o una regla estructural? → **AR** (no ADR)
2. ¿Desarrolla a detalle un tema técnico especializado transversal? → **AT** (no ADR)
3. ¿Regula cómo trabajan los equipos en su día a día? → **ED** (no ADR)
4. ¿Documenta una **decisión concreta** entre alternativas, con contexto,
   justificación y consecuencias? → **ADR** ✓

Si el tema califica como ADR pero también requiere actualizar un AT o AR,
deberás señalarlo en la sección de consecuencias y crear el instrumento
correspondiente por separado.

**Si el tema no corresponde a un ADR, infórmalo claramente al usuario**
y sugiere el nivel documental correcto. No fuerces la creación de un ADR
para contenido que debería ir en otro instrumento.

---

## Paso 2 — Recopilar información

Antes de redactar, asegúrate de tener claridad sobre:

- **¿Cuál es la decisión?** (qué se está decidiendo o ya se decidió)
- **¿Cuál es el contexto?** (problema que motivó la decisión, restricciones técnicas o institucionales)
- **¿Qué alternativas se evaluaron?** (al menos dos opciones consideradas)
- **¿Por qué se eligió esta opción?** (razones técnicas, institucionales, de riesgo, costo, etc.)
- **¿Qué consecuencias genera?** (impactos en el ecosistema, deudas técnicas, restricciones futuras)
- **¿Afecta algún instrumento existente del MGAT?** (AR, AT o ED que deba actualizarse o sea referencia)
- **¿Cuáles son los sistemas o componentes afectados?**
- **¿Cuál es el estado de la decisión?** (Propuesta / Vigente / Deprecada / Sustituida)

### Información de licenciamiento y soporte técnico (obligatoria cuando la decisión involucra tecnología externa)

Cuando el ADR documenta la adopción, sustitución o rechazo de una tecnología
externa al ecosistema institucional (librería, framework, plataforma, protocolo,
herramienta o servicio), **siempre deberás recopilar y documentar** para cada
alternativa evaluada:

- **Licencia:** identificador SPDX (ej. `MIT`, `Apache-2.0`, `GPL-3.0`,
  `LGPL-2.1`, `Proprietary`). Si es propietaria, indicar el modelo
  (suscripción, perpetua, por núcleo, por usuario, etc.).
- **Tipo de soporte:** una de estas categorías:
  - `Comunidad` — mantenida por voluntarios; sin SLA ni garantía de respuesta.
  - `Comunidad + sponsor corporativo` — mantenida por comunidad pero con empresa
    patrocinadora activa (ej. Linux Foundation, Apache Software Foundation,
    CNCF). Mayor sostenibilidad que soporte puramente voluntario.
  - `Soporte comercial opcional` — versión open source con opción de contratar
    soporte de pago (ej. Redis, Elastic, RabbitMQ con VMware/Broadcom).
  - `Soporte comercial obligatorio` — requiere licencia comercial para uso
    en producción o para recibir soporte.
- **Estado del ciclo de vida:** versión activa, LTS, fin de soporte (EOL)
  y fecha si está declarada.
- **Riesgo de abandono o cambio de licencia:** historial relevante si existe
  (ej. cambios de licencia conocidos, fork de la comunidad, absorción por
  adquisición corporativa).

Esta información es obligatoria porque la institución asume un riesgo legal
y operativo concreto al adoptar una tecnología, independientemente de si la
decisión final es open source con soporte comunitario. Que quede formalmente
registrado que se eligió `X` con soporte `Comunidad` y licencia `MIT` —
sin garantía comercial, sin SLA — es exactamente el tipo de compromiso
que el ADR debe preservar para quien tome decisiones en el futuro.

Si el usuario no tiene la información de licencias a mano, ayúdalo a
identificarla. Para tecnologías conocidas puedes completar los campos con
los valores públicamente documentados e indicar la fuente.

Si el usuario no proporciona toda la información restante, pregunta solo lo
esencial antes de continuar. Prefiere preguntar una sola vez con todas las
dudas juntas en lugar de múltiples rondas de preguntas.

---

## Paso 3 — Asignar número y nombre de archivo

El formato de nombre de archivo del MGAT para ADRs es:

```
ADR-XXXX_<descripcion-kebab-case>.md
```

Donde `XXXX` es un número secuencial de 4 dígitos. Si el usuario no indica
el número, usa `ADR-NNNN` como placeholder e instrúyelo a asignar el siguiente
disponible en su repositorio.

El título del ADR debe ser una frase que describa la decisión concretamente,
por ejemplo: `ADR-0012_adopcion-contract-first-con-openapi.md`

---

## Paso 4 — Redactar el ADR

Usa la **plantilla maestra** ubicada en `assets/ADR_plantilla_maestra.md`.
Lee ese archivo antes de redactar. La plantilla define el formato exacto
requerido por el MGAT.

### Principios de redacción para ADRs de calidad

**Sobre el contexto:** Describe el problema con suficiente detalle para que
alguien que no vivió la decisión entienda por qué era necesaria. Incluye
restricciones técnicas, institucionales y de tiempo si son relevantes.

**Sobre las alternativas:** No liste opciones que no se evaluaron realmente.
Cada alternativa debe tener una descripción breve y sus ventajas/desventajas
honestas. Una tabla es el formato más legible. Cuando la decisión involucra
tecnología externa, la tabla debe incluir las columnas de licencia y soporte
técnico — ver plantilla maestra para el formato exacto.

**Sobre la justificación:** Explica *por qué* la opción elegida es superior
a las demás para *este* contexto específico. Evita justificaciones genéricas
del tipo "es la mejor práctica". Si la decisión involucra compromisos
(trade-offs), nómbralos explícitamente.

**Sobre las consecuencias:** Distingue entre consecuencias inmediatas,
a mediano plazo y a largo plazo. Incluye tanto impactos positivos como
deudas técnicas o restricciones que la decisión impone.

**Sobre la inmutabilidad:** Los ADRs vigentes no se modifican. Si la
decisión cambia, se registra un nuevo ADR que supersede al anterior.
El ADR original actualiza su estado a `Sustituido por ADR-XXXX`.

---

## Paso 5 — Verificar coherencia con el MGAT

Antes de dar por terminado el ADR, revisa:

- [ ] ¿La decisión documentada realmente era una elección entre alternativas?
- [ ] ¿El contenido no duplica ni contradice lo que debería estar en un AT o ED?
- [ ] ¿Si la decisión implica una excepción a un AT o ED vigente, está señalada explícitamente?
- [ ] ¿El estado del ADR (`Propuesta` / `Vigente` / etc.) es coherente con la situación actual?
- [ ] ¿Los sistemas y componentes afectados están identificados?
- [ ] ¿La relación con otros instrumentos del MGAT está documentada?
- [ ] Si la decisión involucra tecnología externa, ¿están documentados licencia (SPDX), tipo de soporte y estado del ciclo de vida para cada alternativa evaluada?

---

## Salida esperada

Produce el ADR completo en markdown, listo para guardarse en el directorio
`Nivel 4/` del repositorio MGAT. El documento debe ser autosuficiente:
alguien que lo lea sin conocer la historia del proyecto debe poder entender
el contexto, la decisión y sus implicaciones.

Si hay información que el usuario debe completar (números de ADR, referencias
a instrumentos específicos que desconoces), usa placeholders explícitos como
`[COMPLETAR: número del siguiente ADR disponible]` y explica al final qué
debe rellenarse antes de publicar el documento.
