---
name: fichas-tecnicas
description: >
  Genera fichas informativas técnicas en Markdown, al estilo Pato Bug Traduce — con definición
  clara, mitos vs realidad, diagrama de cómo funciona, ejemplos de uso y referencias verificables.
  Usa este skill siempre que el usuario pida: "crea una ficha de X", "explícame X como Pato Bug",
  "haz una tarjeta técnica de X", "ficha informativa de X", "ficha técnica de X", "qué es X en
  formato ficha", o cuando quiera documentar un concepto técnico de forma visual y educativa,
  incluso si no menciona explícitamente el formato. La ficha debe incluir siempre referencias
  validadas (documentación oficial, RFC, papers, artículos técnicos reconocidos) — nunca inventar
  fuentes. Si hay debate técnico real sobre el tema, reflejar las posturas con evidencia y no
  limitarte a la visión mainstream.
---

# Skill: Fichas Técnicas Informativas

Crea una ficha informativa completa sobre el concepto solicitado, en Markdown, siguiendo la
estructura Pato Bug Traduce. El objetivo es que alguien sin experiencia en el tema entienda
qué es, por qué importa y cómo usarlo — pero con suficiente rigor para que un practicante
experimentado también la encuentre valiosa.

## Proceso de investigación (hazlo siempre)

Antes de escribir la ficha, **busca fuentes primarias** del concepto:
- Documentación oficial (spec, RFC, docs del proyecto/lenguaje)
- Papers o propuestas originales si el concepto tiene origen académico o de standards
- Al menos una fuente secundaria reconocida (blog de ingeniería de empresa tech, libro de
  referencia, curso oficial)

Si encuentras debate técnico real (e.g., "¿son los webhooks realmente más eficientes que
polling en todos los casos?"), **no lo ocultes**: refleja las posturas con evidencia en la
sección correspondiente, aunque contradigan la visión popular.

---

## Estructura de la ficha

Usa exactamente este orden de secciones. No omitas ninguna, pero sí puedes ajustar el
contenido a la profundidad que merece el concepto.

```markdown
# ¿Qué es [CONCEPTO]?

> [Definición de una sola oración, directa y sin jerga innecesaria.]

---

## ❓ ¿Qué significa?

[2-4 oraciones explicando la idea central. Usa analogías del mundo real si ayudan.
Evita repetir la definición; aquí profundizas el *por qué* existe.]

---

## 📡 ¿Dónde lo encontrarás?

[Lista los contextos reales donde aparece el concepto. Sé específico:
no "en sistemas distribuidos" sino "en colas de mensajes como RabbitMQ, Kafka, AWS SQS".]

---

## ❌ Lo que muchos creen

> [Mito o malentendido más común — una sola idea, formulada como lo diría alguien
> que lo malentiende.]

## ✅ La realidad

[Corrección técnica precisa. Si hay matices o el mito es *parcialmente* correcto,
dilo — la precisión importa más que el contraste limpio.]

---

## ⚙️ ¿Cómo funciona?

[Descripción del mecanismo paso a paso. Incluye un diagrama ASCII o tabla
que muestre el flujo. Ejemplo de formato de diagrama:]

```
[Componente A] ──mensaje──▶ [Cola] ──pull──▶ [Componente B]
                                ↑
                         (espera su turno)
```

[Después del diagrama, explica cada paso en 1-2 oraciones.]

---

## 🧩 Ejemplos de uso

| Caso de uso | Por qué encaja aquí |
|-------------|---------------------|
| [Ejemplo 1] | [Razón técnica]     |
| [Ejemplo 2] | [Razón técnica]     |
| [Ejemplo 3] | [Razón técnica]     |
| [Ejemplo 4] | [Razón técnica]     |

---

## 🗺️ Diagrama simple

```
[Diagrama minimalista que muestre la idea en su versión más reducida.
Usa ASCII art. Debe ser comprensible en 5 segundos.]
```

---

> 💡 **Tip:** [Un consejo práctico accionable. Algo que el lector pueda aplicar
> esta semana, no una generalidad como "úsalo cuando necesites escalabilidad".]

---

## 📚 Referencias

[Lista de fuentes verificables usadas para construir la ficha. Mínimo 3, máximo 6.
Prioriza: (1) especificaciones oficiales / RFC, (2) documentación del proyecto,
(3) papers originales, (4) posts de ingeniería de empresas reconocidas.
NUNCA inventes URLs — si no puedes verificar que existe, no la incluyas.]

- [Título descriptivo](URL) — *[Tipo de fuente y por qué es relevante]*
- [Título descriptivo](URL) — *[Tipo de fuente y por qué es relevante]*
- [Título descriptivo](URL) — *[Tipo de fuente y por qué es relevante]*
```

---

## Pautas de calidad

**Definición:** Debe funcionar como respuesta a "explícame esto en 10 segundos". No uses
el término a definir dentro de su propia definición.

**Mito vs realidad:** El mito debe ser algo que alguien *realmente* podría creer — no un
hombre de paja obvio. La corrección debe tener fundamento técnico, no solo "la realidad es más
compleja". Si el debate es genuino (e.g., REST vs GraphQL), presenta ambas posturas con
evidencia en lugar de declarar un ganador.

**Diagrama:** El ASCII debe ser legible en Markdown renderizado. Usa `──▶` para flechas,
`[Caja]` para componentes, y añade etiquetas en las conexiones cuando el tipo de relación
importa.

**Referencias:** Si al buscar encuentras que la fuente más relevante *contradice* algún punto
de la ficha, actualiza la ficha. Las referencias no son decoración — son la garantía técnica
del contenido.

**Idioma:** Español por defecto. Si el concepto tiene un nombre en inglés sin traducción
canónica (como "queue", "webhook", "callback"), mantenlo en inglés en el título y explica la
traducción aproximada en la definición.

**Longitud:** Una ficha completa cabe en una pantalla promedio de laptop. Si el contenido
crece más allá de ~600 palabras, revisa si estás duplicando información entre secciones.
