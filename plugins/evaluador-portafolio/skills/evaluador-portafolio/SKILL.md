---
name: evaluador-portafolio
description: |
  Ejecuta la evaluación semestral de portafolio tecnológico de un equipo de desarrollo.
  
  Úsalo cuando el usuario quiera:
  - Evaluar el desempeño del equipo al cierre de un semestre
  - Calcular calificaciones de productos con criterios ponderados (Resultado, Arquitectura, Estándares, Innovación, Colaboración)
  - Generar el reporte ejecutivo de portafolio (semáforo, ranking, análisis por responsable, patrones, backlog)
  - Crear fichas individuales de retroalimentación para compartir con cada integrante
  - Hacer cualquier parte del flujo: solo scoring, solo reporte, solo fichas, o todo completo
  
  Aplica cuando el usuario diga: "evalúa el semestre", "genera el reporte de evaluación", 
  "califica los productos del equipo", "crea las fichas", "procesa la evaluación", 
  "quiero el reporte semestral", o cuando proporcione archivos con criterios de evaluación 
  por persona. Usa este skill también para evaluaciones parciales o actualizaciones 
  intermedias del portafolio durante el semestre.
---

# Evaluador de Portafolio Tecnológico

## Qué produce este skill

A partir de archivos de entrada por persona, genera dos tipos de entregables:

1. **`reporte-evaluacion-semestral.md`** — Reporte ejecutivo del portafolio completo con semáforo, ranking, análisis por responsable, patrones recurrentes, radar de madurez y backlog institucional.

2. **`ficha-[nombre-apellido].md`** por cada integrante — Documento en primera persona con sus scores, fortalezas, áreas de mejora, citas de la sesión y plan de desarrollo para el siguiente semestre.

---

## Formato de entrada

Antes de comenzar, verifica que el usuario haya proporcionado información para cada persona. El formato mínimo esperado por persona:

```markdown
# [Nombre Apellido] — Promedio: [XX] ([Nivel])

## Período: [1er/2do Semestre YYYY]

| # | Producto | R | A | E | I | C | Observaciones |
|---|---|---|---|---|---|---|---|
| 1 | Nombre del producto | 25 | 20 | NA | 15 | 10 | Descripción del resultado logrado |
| 2 | Otro producto       | 25 | NA | 20 | NA | NA | Descripción del resultado |

## Evidencia oral (Sesión de Avances)
Citas textuales o paráfrasis de lo que dijo la persona durante la presentación.

## Calificación como responsable: [XX] ([Nivel])
[Narrativa de evaluación del responsable — opcional, puedes generarla]
```

**Columnas de criterios:**
- `R` = Resultado (peso base 25)
- `A` = Arquitectura (peso base 25)
- `E` = Estándares (peso base 20)
- `I` = Innovación (peso base 15)
- `C` = Colaboración (peso base 15)

**Valores posibles en la tabla:**
- Número ≤ peso base: logro efectivo (igual al base = completo; menor = parcial)
- `0`: criterio aplica pero no se logró
- `NA`: criterio no aplicable a este producto (excluido del cálculo)

Si los archivos no tienen todo, pregunta al usuario lo que falta antes de proceder. Lee `references/plantilla-entrada.md` para ver el formato completo con ejemplos.

---

## Flujo de trabajo

### Paso 1 — Leer y validar entradas

Lee todos los archivos proporcionados. Para cada persona verifica:
- Lista de productos con tabla de criterios
- Al menos observaciones básicas por producto
- Evidencia oral (si no existe, puedes omitir esa sección en las fichas o pedirla al usuario)

Si hay ambigüedad en los valores de la tabla (por ejemplo, una columna desplazada), pregunta antes de calcular.

### Paso 2 — Calcular scores por producto

Lee `references/metodologia.md` antes de calcular. El resumen:

```
Score = Σ(valor_criterio) / Σ(peso_base_criterio_aplicable) × 100
```

Ejemplo: producto con R=25, A=20, E=NA, I=NA, C=0
→ Numerador: 25 + 20 + 0 = 45
→ Denominador: 25 + 25 + 15 = 65  (R+A+C, porque E e I son NA)
→ Score: 45/65 × 100 = 69.2 → 69 (Aceptable 🟠)

**Escala de niveles:**
| Rango | Nivel | Semáforo |
|---|---|---|
| 97–100 | Sobresaliente | 🟢 |
| 92–96 | Excelente | 🟢 |
| 85–91 | Muy Bueno | 🟢 |
| 75–84 | Bueno | 🟡 |
| 65–74 | Aceptable | 🟠 |
| 50–64 | Requiere Mejora | 🔴 |
| 0–49 | Crítico | 🔴 |

### Paso 3 — Calcular promedios y calificación como responsable

**Promedio del portafolio individual:** media aritmética de todos los scores de los productos del responsable.

**Calificación como responsable:** puede ajustar ±5 puntos del promedio considerando:
- Patrón de colaboración y transferencia de conocimiento (si es bajo, reduce)
- Riesgo de concentración de conocimiento (si es alto, puede reducir)
- Ejecución ante bloqueos (si escaló a tiempo, mantiene; si no, puede reducir)
- Calidad de la reflexión y madurez profesional (si es alta, puede subir)

Si no tienes criterio suficiente para ajustar, usa el promedio directamente.

### Paso 4 — Generar el reporte ejecutivo

Produce `reporte-evaluacion-semestral.md`. Lee `references/estructura-reporte.md` para la estructura completa con plantillas de cada sección.

El reporte tiene estas secciones en orden:
1. Resumen Ejecutivo
2. Índice de Carga por Responsable
3. Metodología de Evaluación
4. Evaluación por Responsable
5. Análisis del Portafolio
6. Radar de Madurez del Portafolio
7. Semáforo Consolidado
8. Ranking
9. Patrones y Recomendaciones
10. Backlog Institucional
11. Modalidad de Trabajo
12. Compromisos y Plan Siguiente Semestre

### Paso 5 — Generar fichas individuales

Produce `ficha-[nombre-apellido].md` por cada persona. Lee `references/estructura-ficha.md` para el template con ejemplos.

**Características clave de las fichas:**
- **Tono:** primera persona, directo ("tu portafolio", "lo que necesitas trabajar")
- **Fortalezas:** reconocimiento genuino, con evidencia específica
- **Áreas de mejora:** nombra el patrón, no solo el síntoma
- **Plan de desarrollo:** compromisos con métrica y plazo, no genéricos
- **Citas:** usa las citas textuales de la evidencia oral cuando estén disponibles

### Paso 6 — Verificar consistencia antes de entregar

- Que el total de productos en el resumen ejecutivo cuadre con la suma por responsable
- Que la distribución de semáforos en el resumen coincida con el semáforo consolidado
- Que los promedios individuales coincidan con los datos del índice de carga
- Que productos compartidos entre responsables aparezcan en ambas tablas

---

## Notas para el evaluador

**Scoring es evaluativo, no automático.** Los valores en la tabla de criterios son el juicio del evaluador sobre el logro en cada dimensión. La fórmula mecaniza el cálculo, pero el input viene de una valoración experta. Si el usuario te proporciona los valores, aplica la fórmula. Si te pide que valores tú, basa tu juicio en las observaciones y evidencia disponibles.

**NA ≠ 0.** NA significa que el criterio no aplica (no penaliza). 0 significa que aplica pero no se logró (sí penaliza). La diferencia cambia significativamente el score.

**Las fichas no son reportes de RH.** Son documentos de desarrollo profesional. El plan de cada ficha debe tener compromisos específicos y medibles, no frases genéricas. Evita "mejorar la comunicación" — escribe "establecer revisión quincenal de avances con el líder antes de julio 2026".

**Productos críticos jalan el promedio.** Un responsable con muchos productos puede tener buen promedio general y aún así tener un producto crítico que requiere acción. El semáforo individual por producto es más importante que el promedio para identificar riesgos.
