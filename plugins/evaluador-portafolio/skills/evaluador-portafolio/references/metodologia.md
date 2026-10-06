# Metodología de Scoring — Evaluador de Portafolio Tecnológico

## Criterios y pesos base

| Criterio | Código | Peso Base |
|---|---|---|
| Resultado | R | 25 |
| Arquitectura | A | 25 |
| Estándares | E | 20 |
| Innovación | I | 15 |
| Colaboración | C | 15 |
| **Total** | | **100** |

## Fórmula de cálculo

```
Score = Σ(valor_criterio_i) / Σ(peso_base_criterio_i_aplicable) × 100
```

Donde:
- `valor_criterio_i` = el número asignado al criterio en la tabla (puede ser el peso base completo, un valor parcial, o 0)
- `peso_base_criterio_i_aplicable` = el peso base de ese criterio (solo para criterios que NO son NA)

## Reglas de NA

- `NA` en un criterio significa que ese criterio **no aplica** al producto.
- Los criterios NA **se excluyen del denominador** — no penalizan el score.
- El denominador se ajusta sumando solo los pesos base de los criterios aplicables.

## Reglas de valores parciales

- Si un criterio tiene valor igual al peso base → logro completo (contribuye 100% de ese criterio)
- Si tiene valor menor al peso base → logro parcial (contribuye la fracción correspondiente)
- Si tiene valor 0 → criterio falló (contribuye 0 pero sigue en el denominador)

## Ejemplos de cálculo

### Ejemplo 1: Producto con todos los criterios aplicables
| Criterio | Valor | Peso Base |
|---|---|---|
| R | 25 | 25 |
| A | 25 | 25 |
| E | 20 | 20 |
| I | 15 | 15 |
| C | 15 | 15 |
| **Total** | **100** | **100** |

Score = 100 / 100 × 100 = **100 (Sobresaliente)**

### Ejemplo 2: Producto con criterios NA (R+C únicos aplicables)
| Criterio | Valor | Peso Base |
|---|---|---|
| R | 25 | 25 |
| A | NA | (excluido) |
| E | NA | (excluido) |
| I | NA | (excluido) |
| C | 15 | 15 |

Score = (25 + 15) / (25 + 15) × 100 = **100 (Sobresaliente)**

### Ejemplo 3: Logros parciales
| Criterio | Valor | Peso Base |
|---|---|---|
| R | 20 | 25 |
| A | 25 | 25 |
| E | 20 | 20 |
| I | NA | (excluido) |
| C | NA | (excluido) |

Score = (20 + 25 + 20) / (25 + 25 + 20) × 100 = 65 / 70 × 100 = **92.9 → 93 (Excelente)**

### Ejemplo 4: Con criterio fallido (valor 0)
| Criterio | Valor | Peso Base |
|---|---|---|
| R | 10 | 25 |
| A | 10 | 25 |
| E | NA | (excluido) |
| I | NA | (excluido) |
| C | 0 | 15 |

Score = (10 + 10 + 0) / (25 + 25 + 15) × 100 = 20 / 65 × 100 = **30.8 → 31 (Crítico)**

## Escala de niveles

| Rango | Nivel | Semáforo | Significado |
|---|---|---|---|
| 97–100 | Sobresaliente | 🟢 | Resultado excepcional, supera expectativas |
| 92–96 | Excelente | 🟢 | Resultado superior a lo esperado |
| 85–91 | Muy Bueno | 🟢 | Resultado sólido, cumple con calidad |
| 75–84 | Bueno | 🟡 | Cumple el objetivo, áreas de mejora menores |
| 65–74 | Aceptable | 🟠 | Cumple parcialmente, riesgos identificados |
| 50–64 | Requiere Mejora | 🔴 | No cumple el objetivo, intervención necesaria |
| 0–49 | Crítico | 🔴 | Falla grave, acción inmediata requerida |

## Semáforo del portafolio individual

| Promedio | Estado |
|---|---|
| 85+ | 🟢 Consolidado |
| 75–84 | 🟡 En Evolución |
| 65–74 | 🟠 En Riesgo |
| 0–64 | 🔴 Crítico |

## Calificación como responsable vs. promedio de productos

Son distintas métricas:

- **Promedio de productos**: media aritmética de los scores individuales. Refleja el resultado promedio del portafolio.
- **Calificación como responsable**: evalúa a la persona más allá de los números. Puede diferir del promedio hasta ±5 puntos.

Factores que pueden reducir la calificación como responsable por debajo del promedio:
- Concentración extrema de conocimiento sin ninguna transferencia documentada
- Aislamiento operativo en todos los productos (patrón "islitas")
- No escalar bloqueos que afectaron el resultado
- Atribuir el incumplimiento exclusivamente a factores externos

Factores que pueden subir la calificación como responsable sobre el promedio:
- Alta carga de trabajo (muchos productos, carga desproporcionada del equipo)
- Evolución demostrada durante el semestre en dimensiones clave
- Colaboración activa que benefició a otros productos del equipo
- Reflexión madura y concreta sobre sus propias limitaciones

## Dimensiones de evaluación por responsable

Además del score por producto, cada responsable se evalúa en estas dimensiones:

| Dimensión | Descripción |
|---|---|
| Capacidad técnica | Dominio técnico de las tecnologías que opera |
| Capacidad de ejecución | Cumplimiento de objetivos con calidad |
| Colaboración | Trabajo con pares, transferencia activa |
| Comunicación | Comunicación interna y con usuarios externos |
| Transferencia de conocimiento | Documentación, sesiones, respaldo |
| Autonomía | Capacidad de avanzar sin supervisión constante |
| Uso de IA | Efectividad del uso de herramientas de IA |
| Planeación | Estimaciones, manejo de riesgos, escalamiento |
| Cumplimiento | Porcentaje de objetivos alcanzados |
| Madurez profesional | Responsabilidad ante errores, iniciativa |

Niveles por dimensión: Crítico → Bajo → Medio → Medio-Alto → Alto → Muy Alto

Usa las dimensiones relevantes para cada persona — no es necesario incluir todas si algunas no aplican.
