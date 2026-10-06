# Estructura de Fichas Individuales

Cada ficha se guarda como `ficha-[nombre-apellido].md` (todo en minúsculas, sin acentos, guiones en lugar de espacios).

Ejemplos: `ficha-carlos-morales.md`, `ficha-efren-prado.md`

---

## Template completo

```markdown
# Evaluación Semestral · [Nombre Apellido]
**Período:** [1er/2do] Semestre [YYYY] | **Fecha:** [YYYY-MM-DD]
**Evaluador:** [Nombre o rol del evaluador] | **Calificación como responsable: [XX] ([Nivel])**

---

## Tu portafolio del semestre

| # | Producto | Cal. | Nivel | Riesgo |
|---|---|---|---|---|
| 1 | Nombre del producto | XX | Nivel | Alto/Medio/Bajo |
| ... | | | | |

**Promedio del semestre: [XX] ([Nivel])**

🟢 Muy Bueno (85+): [lista de productos o "—"]
🟡 Bueno (75–84): [lista de productos o "—"]
🟠 Aceptable (65–74): [lista de productos o "—"]
🔴 Requiere Mejora / Crítico (0–64): [lista de productos o "—"]

---

## Cómo te fue

[2-4 párrafos en segunda persona. Incluir:
- Contexto de carga y cobertura del semestre
- Logro principal del semestre (no solo "cumpliste X")
- Diagnóstico del riesgo central (técnico u organizacional)
- Si aplica: contexto que explica un resultado bajo sin minimizarlo]

| Dimensión | Nivel |
|---|---|
| [Dimensión relevante] | [Nivel] |
| ... | ... |

[1 párrafo conectando las dimensiones con el diagnóstico central]

---

## Lo que reconocemos de tu trabajo

[Lista de 3-5 bullets. Cada uno debe ser específico y basado en evidencia:
- Nombrar el producto o situación concreta
- Decir qué fue lo que se hizo bien
- Si hay cita oral relevante, puede ir aquí]

---

## Lo que necesitas trabajar

[2-4 secciones en negrita, una por área de mejora. Cada sección:
- Nombre el patrón, no solo el síntoma
- Explica por qué importa (consecuencias concretas)
- Puede mencionar el producto donde se evidenció]

**[Área de mejora 1].** [Descripción del patrón + consecuencia + evidencia]

**[Área de mejora 2].** [Descripción del patrón + consecuencia + evidencia]

---

## Lo que dijiste en la sesión de avances

[Párrafo o sección con citas textuales de la sesión. Si hay varias citas, puede estructurarse por producto.
Formato: *"cita textual entre comillas"*
Agregar contexto breve antes o después de cada cita para que tenga sentido.
Si no hay evidencia oral disponible, omitir esta sección o escribir "[Sesión de avances pendiente]"]

---

## Plan de desarrollo — [1er/2do] Semestre [YYYY]

[Una tabla con compromisos específicos:]

| Compromiso | Métrica | Plazo |
|---|---|---|
| [Acción específica y observable] | [Cómo se mide] | [Mes año] |
| ... | ... | ... |

---

> Esta ficha es parte de la Evaluación Semestral de Portafolio Tecnológico · [Período].
> Es un documento de retroalimentación directa. Su propósito es orientar tu desarrollo, no catalogarte.
```

---

## Guía de tono y redacción

### Segunda persona directa
Siempre "tú", no "usted" ni tercera persona. La ficha es un documento que la persona lee directamente.
- ✅ "Tu portafolio", "lo que necesitas trabajar", "lo que dijiste"
- ❌ "El responsable", "se recomienda que", "debería considerar"

### Reconocimientos genuinos
Los reconocimientos deben ser específicos y basados en evidencia, no genéricos.
- ✅ "Entregaste SIM General con DevOps completo (app+BD), que es referencia de implementación para el equipo."
- ❌ "Tienes buena capacidad técnica."

### Áreas de mejora: el patrón, no el síntoma
Nombrar el patrón subyacente es más útil que describir el síntoma.
- ✅ "El patrón de no escalar bloqueos hasta que se vuelven incumplimientos es la causa directa de SDMX Migración. No es un problema de capacidad — es de proceso."
- ❌ "SDMX Migración no avanzó suficientemente."

### Plan de desarrollo: compromisos medibles
Cada compromiso debe tener una métrica observable y un plazo real.
- ✅ "Capacitar a una segunda persona en Arquitectura — métrica: puede explicar los anexos técnicos sin apoyo — plazo: agosto 2026"
- ❌ "Mejorar la transferencia de conocimiento."

### Citas orales
Si el usuario proporcionó evidencia oral, úsala. Las citas textuales dan credibilidad a la retroalimentación.
- Formato: *"cita entre comillas"*
- Incluye el contexto justo antes o después para que la cita tenga sentido sin saber toda la sesión

### Sobre el plan de desarrollo para personas con evaluación crítica
Para personas con promedio bajo o patrón de incumplimiento, el plan debe ser más directivo:
- Incluir revisiones intermedias con fecha
- Los compromisos deben ser mínimos no opcionales (no "oportunidades")
- Puede incluir una nota sobre el carácter de intervención del plan

---

## Ejemplo de ficha abreviada (referencia de tono)

```markdown
# Evaluación Semestral · Cristian Galván
**Período:** 1er Semestre 2026 | **Calificación como responsable: 82 (Bueno)**

## Tu portafolio del semestre

| # | Producto | Cal. | Nivel | Riesgo |
|---|---|---|---|---|
| 1 | SIM APM (Continuidad Operativa) | 77 | Bueno | Bajo |
| 2 | SIM APM (Desarrollo) | 81 | Bueno | Bajo |
| 3 | SIM APM (Refactorización) | 85 | Muy Bueno | Bajo |
| 4 | CIP | 79 | Bueno | Bajo |

**Promedio: 81 (Bueno)**
> Sin riesgos identificados en ningún producto. Único integrante del portafolio con esta distinción.

## Cómo te fue

Eres el caso de mayor mejora demostrada del semestre. El reporte documenta que tuviste un 
inicio difícil y que las intervenciones aplicadas funcionaron. El resultado lo respalda: 
4 de 4 objetivos cumplidos, incluyendo una refactorización al 100% (34/34 servicios).

## Lo que reconocemos de tu trabajo

- Refactorización SIM APM: 34/34 servicios (100%), 92.8% de cumplimiento de reglas DCM TIC.
- Eres el único integrante sin ningún riesgo identificado en ningún producto.

## Lo que puedes llevar más lejos

**Formalizar la transferencia de conocimiento.** El proceso de refactorización SIM APM tiene 
valor para el equipo. Documentarlo convierte tu trabajo en capital institucional.

## Plan de desarrollo — 2do Semestre 2026

| Compromiso | Métrica | Plazo |
|---|---|---|
| Documentar proceso de refactorización SIM APM | README técnico publicado en GitLab | Agosto 2026 |
| Mentorear activamente a nuevo integrante | Objetivo definido + revisión mensual | Julio 2026 |
```
