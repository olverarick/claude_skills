# Plantilla de Entrada — Por Persona

Cada integrante del equipo debe tener un archivo `.md` con esta estructura. 
Guarda como `[nombre-apellido].md` (ej: `carlos-morales.md`).

---

## Template

```markdown
# [Nombre Apellido]

## Período: [1er/2do] Semestre [YYYY]
## Área / Equipo: [nombre del equipo o área]

---

## Portafolio de Productos

| # | Producto | R | A | E | I | C | Observaciones |
|---|---|---|---|---|---|---|---|
| 1 | [Nombre del producto] | [val] | [val] | [val] | [val] | [val] | [qué se entregó / qué pasó] |
| 2 | [Nombre del producto] | [val] | NA | NA | [val] | [val] | [observaciones] |
| ... | | | | | | | |

**Leyenda de valores:**
- Número ≤ peso base del criterio: logro (completo si igual, parcial si menor)
- 0: criterio aplica pero no se logró
- NA: criterio no aplica a este producto

---

## Evidencia Oral — Sesión de Avances [Fecha]

[Citas textuales o paráfrasis de lo que dijo la persona durante la sesión de presentación.
Incluir contexto de cada cita: en qué producto o momento lo dijo.]

- Sobre [producto/tema]: *"[cita textual]"*
- Reflexión de cierre: *"[cita textual]"*
- Sobre colaboración: *"[cita textual]"*

---

## Notas del Evaluador

[Observaciones adicionales del evaluador que no están en la tabla de criterios:
- Patrones de comportamiento observados
- Contexto de bloqueos o incumplimientos
- Factores externos que afectaron el resultado
- Fortalezas no evidentes en los números]

---

## Calificación como Responsable (opcional — puedes dejarlo en blanco)
[Si ya tienes la calificación calculada: XX (Nivel)]
[Si no, el skill la calculará basándose en el promedio de productos y las notas del evaluador]
```

---

## Ejemplo de archivo relleno

```markdown
# Ana Ramírez

## Período: 1er Semestre 2026
## Área: Desarrollo Frontend

---

## Portafolio de Productos

| # | Producto | R | A | E | I | C | Observaciones |
|---|---|---|---|---|---|---|---|
| 1 | Portal Ciudadano | 25 | 20 | 20 | 15 | 15 | Entregado en tiempo. Mejora en accesibilidad. Colaboró con UX. |
| 2 | Componentes Base | 20 | 25 | NA | 15 | 10 | Migración completada. Adopción no medida. |
| 3 | Dashboard Admin | 25 | NA | 20 | NA | NA | Funcional. Sin segundo responsable capacitado. |
| 4 | CI/CD Frontend | 10 | 10 | 15 | NA | 0 | Pipeline configurado. Sin documentación. Sin colaboración. |

---

## Evidencia Oral — Sesión de Avances 2026-05-15

- Sobre Portal Ciudadano: *"trabajé de cerca con el equipo de UX para validar los flujos antes de lanzar, eso nos ahorró dos rondas de correcciones"*
- Sobre Componentes Base: *"la migración la hice sola porque no encontré el momento para involucrar a alguien más"*
- Reflexión de cierre: *"lo que más me llevo del semestre es que documentar desde el principio vale más que documentar al final"*

---

## Notas del Evaluador

- CI/CD: dejó la documentación pendiente argumentando falta de tiempo. Patrón: prioriza entrega funcional sobre transferencia.
- Componentes Base: adopción no medida porque no hay métricas de uso en el equipo. No es falla de Ana, es brecha de proceso.
- Se destaca el trabajo con UX en Portal Ciudadano — único producto con validación externa antes del lanzamiento.

---

## Calificación como Responsable
79 (Bueno)
```

---

## Guía para llenar los valores de criterios

### Resultado (R — peso base 25)
- 25: El producto entregó su objetivo completamente y el usuario tiene acceso al valor
- 20: Entregó el objetivo con observaciones menores o parcialmente validado con usuarios
- 15: Entregó funcionalidad pero el objetivo de negocio no está claramente cumplido
- 10: Avance parcial significativo (≥50% del objetivo)
- 5: Avance menor (<50%)
- 0: No hubo entrega funcional
- NA: No aplica (raro para Resultado — casi siempre aplica)

### Arquitectura (A — peso base 25)
- 25: Decisiones documentadas, patrón replicable, alineado con arquitectura de referencia
- 20: Bien estructurado técnicamente con documentación parcial
- 15: Funcional pero sin evidencia de decisiones arquitectónicas documentadas
- 10: Deuda técnica identificada, estructura irregular
- 0: Sin evidencia de consideración arquitectónica
- NA: Producto operativo/mantenimiento sin componente de diseño arquitectónico

### Estándares (E — peso base 20)
- 20: Cumple estándares de código, seguridad, y documentación del equipo
- 15: Cumple parcialmente (ej: código sí, documentación no)
- 10: Cumplimiento básico con brechas notables
- 0: No sigue estándares del equipo
- NA: Producto de exploración/investigación sin código productivo

### Innovación (I — peso base 15)
- 15: Introduce una nueva capacidad, patrón o tecnología con impacto institucional
- 10: Mejora incremental relevante sobre el estado previo
- 5: Pequeña mejora o exploración sin impacto medido aún
- 0: Sin componente de innovación o mejora
- NA: Producto de continuidad operativa pura (mantenimiento, soporte)

### Colaboración (C — peso base 15)
- 15: Trabajó activamente con pares, documentó y transfirió conocimiento
- 10: Coordinó con al menos 1 persona del equipo en el producto
- 5: Mínima colaboración o solo con externos (no pares del equipo)
- 0: Trabajo completamente aislado sin transferencia de ningún tipo
- NA: Producto unipersonal por diseño donde la colaboración no era aplicable
