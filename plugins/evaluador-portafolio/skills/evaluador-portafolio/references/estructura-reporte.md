# Estructura del Reporte Ejecutivo

El reporte se genera como `reporte-evaluacion-semestral.md`. A continuación la plantilla de cada sección.

---

## Sección 1: Resumen Ejecutivo

```markdown
# Reporte Evaluación Semestral de Portafolio Tecnológico
**Período:** [1er/2do] Semestre [YYYY] | **Fecha:** [YYYY-MM-DD]
**Responsable de Evaluación:** [Nombre del evaluador]

---

## 1. Resumen Ejecutivo

El portafolio tecnológico del semestre registró **[N] productos activos** distribuidos entre **[N] responsables**.
El promedio general del portafolio fue **[XX] ([Nivel])**.

| Indicador | Valor |
|---|---|
| Total de productos evaluados | N |
| Promedio general del portafolio | XX (Nivel) |
| Productos en nivel Muy Bueno o superior (🟢) | N (XX%) |
| Productos en nivel Bueno (🟡) | N (XX%) |
| Productos En Riesgo (🟠) | N (XX%) |
| Productos Críticos (🔴) | N (XX%) |
| Responsable con mayor promedio | Nombre (XX) |
| Responsable con mayor número de productos | Nombre (N productos) |

**Hallazgos principales:**
[3-5 bullets con los hallazgos más relevantes del portafolio. Incluir la brecha más importante y al menos un punto positivo.]
```

---

## Sección 2: Índice de Carga por Responsable

```markdown
## 2. Índice de Carga por Responsable

| Responsable | Productos | % del portafolio | Promedio | Semáforo |
|---|---|---|---|---|
| [Nombre] | N | XX% | XX (Nivel) | 🟢/🟡/🟠/🔴 |
| ... | | | | |
| **Total** | **N** | **100%** | **XX** | |
```

---

## Sección 3: Metodología de Evaluación

```markdown
## 3. Metodología de Evaluación

### Modelo: Evaluador de Productos Tecnológicos v2.0

La evaluación aplica el método de criterios ponderados con 4 niveles de análisis:
- **Nivel 1:** Producto (score individual por producto)
- **Nivel 2:** Responsable (calificación como responsable)
- **Nivel 3:** Portafolio (análisis cruzado de patrones)
- **Nivel 4:** Estratégico (alineación con objetivos institucionales)

### Criterios y pesos base

| Criterio | Código | Peso Base |
|---|---|---|
| Resultado | R | 25 |
| Arquitectura | A | 25 |
| Estándares | E | 20 |
| Innovación | I | 15 |
| Colaboración | C | 15 |
| **Total** | | **100** |

### Fórmula
Score = Σ(valor_criterio) / Σ(peso_base_aplicable) × 100

Los criterios marcados como NA se excluyen del denominador. Los valores por debajo del peso base indican logro parcial.

### Escala
[Insertar la tabla de escala de niveles de metodologia.md]

### Criterios por producto
[Incluir la tabla de criterios efectivos por producto para el(los) responsable(s) principales, si está disponible]
```

---

## Sección 4: Evaluación por Responsable

Una subsección por persona. Estructura de cada subsección:

```markdown
### [Nombre Apellido]

**Calificación como responsable: [XX] ([Nivel])**

[2-3 párrafos de evaluación narrativa. Incluir:
- Fortaleza técnica y cobertura
- Patrón de colaboración / transferencia
- Riesgo principal identificado
- Contexto de cualquier producto no cumplido]

| Dimensión | Nivel |
|---|---|
| Capacidad técnica | [nivel] |
| ... | ... |

**Áreas de mejora:** [2-3 áreas específicas]

**Evidencia oral — Sesión de Avances ([YYYY-HN]):** [Párrafo con las citas más relevantes de la presentación. Usa comillas para citas textuales. Nombrar los patrones observados.]

---
```

---

## Sección 5: Análisis del Portafolio

```markdown
## 5. Análisis del Portafolio (Nivel 3)

### Productos similares y duplicados
[Análisis de productos que comparten tecnología o dominio entre varios responsables. Identificar si hay coordinación o silos.]

### Dependencias identificadas
[Lista de dependencias críticas: productos que dependen de personas externas al equipo, productos que bloquean a otros, etc.]

### Patrones problemáticos recurrentes
[Patrones que aparecen en más de un responsable. Numerados. Por ejemplo:
1. "Si [nombre] no está, no hay soporte" — aplica a N productos
2. "No pide apoyo aunque lo necesita" — patrón de comunicación en X personas
3. etc.]
```

---

## Sección 6: Radar de Madurez

```markdown
## 6. Radar de Madurez del Portafolio

| Dimensión | Calificación (0–10) | Nivel |
|---|---|---|
| Arquitectura | X.X | [Nivel] |
| Calidad | X.X | [Nivel] |
| Innovación | X.X | [Nivel] |
| Colaboración | X.X | [Nivel] |
| Automatización | X.X | [Nivel] |
| DevOps | X.X | [Nivel] |
| Operación | X.X | [Nivel] |
| Continuidad | X.X | [Nivel] |
| Documentación | X.X | [Nivel] |
| Seguridad | X.X | [Nivel] |

> [Observación sobre la brecha más significativa del portafolio en 1-2 líneas]
```

Para calcular las dimensiones del radar, promediar el desempeño observado en los productos de cada área. Continuidad y Colaboración suelen ser las más bajas en equipos con el patrón "islitas".

---

## Sección 7: Semáforo Consolidado

```markdown
## 7. Semáforo

### 🟢 Consolidados (85–100)
| Producto | Responsable | Calificación |
|---|---|---|
| ... | ... | ... |

### 🟡 En Evolución (75–84)
| Producto | Responsable | Calificación |
|---|---|---|
| ... | ... | ... |

### 🟠 En Riesgo (65–74)
| Producto | Responsable | Calificación | Riesgo Principal |
|---|---|---|---|
| ... | ... | ... | ... |

### 🔴 Críticos (0–64)
| Producto | Responsable | Calificación | Acción Requerida |
|---|---|---|---|
| ... | ... | ... | ... |
```

---

## Sección 8: Ranking

```markdown
## 8. Ranking

### Top 5 Productos por Calificación
| # | Producto | Responsable | Calificación |
|---|---|---|---|

### Top 5 Innovaciones del Semestre
| # | Innovación | Responsable | Impacto |
|---|---|---|---|

### Productos con Mayor Impacto Institucional
| # | Producto | Motivo |
|---|---|---|

### Productos con Mayor Riesgo
| # | Producto | Calificación | Riesgo |
|---|---|---|---|
```

---

## Sección 9: Patrones y Recomendaciones

```markdown
## 9. Patrones y Recomendaciones Estratégicas

### Patrón 1: [Nombre del patrón]
**Prevalencia:** N de N responsables
**Evidencia:** [productos/situaciones donde se observó]
**Recomendación:** [acción específica]

### [Repetir para cada patrón identificado]

### Recomendación general de arquitectura de equipo
[Si aplica: recomendación sobre redistribución de productos, roles, o mecanismos de coordinación]
```

---

## Sección 10: Backlog Institucional

```markdown
## 10. Backlog Institucional

### Deuda técnica identificada
| Producto | Deuda | Impacto | Responsable |
|---|---|---|---|

### Riesgos de continuidad abiertos
| Producto | Riesgo | Estado | Responsable |
|---|---|---|---|

### Iniciativas propuestas para el siguiente semestre
| Iniciativa | Origen | Prioridad |
|---|---|---|
```

---

## Sección 11: Modalidad de Trabajo

```markdown
## 11. Modalidad de Trabajo

| Integrante | Modalidad actual | Recomendación | Fundamento |
|---|---|---|---|
| [Nombre] | [4x1 / 5x5 / Remoto / etc.] | [Mantener / Cambiar] | [razón basada en patrones de colaboración] |

> Nota: La modalidad presencial no garantiza colaboración activa. Los datos del portafolio muestran [X] integrantes con modalidad presencial que presentan el mismo patrón de aislamiento que integrantes en modalidad híbrida.
```

---

## Sección 12: Compromisos y Plan Siguiente Semestre

```markdown
## 12. Compromisos y Plan [1er/2do] Semestre [YYYY]

### Compromisos institucionales
[2-3 acciones que el equipo como unidad debe ejecutar, con dueño y fecha]

### Por responsable
| Responsable | Compromiso principal | Plazo |
|---|---|---|
| [Nombre] | [acción específica] | [mes año] |

### Productos en observación
[Lista de productos críticos o en riesgo que requieren revisión a mitad del siguiente semestre]
```
