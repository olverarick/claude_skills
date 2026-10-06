---
name: pdf-to-md
description: >
  Transforma documentos PDF a Markdown con auditoría completa del proceso de
  conversión. Úsalo siempre que el usuario quiera convertir, transformar,
  extraer o transcribir un PDF a texto, Markdown o formato legible por máquina,
  incluso si solo dice "pásame esto a MD", "convierte el PDF", "extrae el texto
  de este PDF", "necesito el PDF en texto plano", o adjunta un PDF y pide un
  resumen/análisis (primero conviértelo). Maneja PDFs escaneados (solo imagen),
  PDFs estructurados con texto nativo, PDFs mixtos (texto + imágenes), PDFs con
  tablas, columnas, fórmulas y layouts complejos. Produce un .md limpio más un
  bloque de auditoría con quality score 0–100. Usa este skill aunque el PDF
  parezca simple — la auditoría siempre agrega valor.
---

# PDF → Markdown Skill

## Tu objetivo

Convertir un documento PDF a Markdown de la manera más fiel posible y dejar
un registro honesto de lo que ocurrió durante la conversión. El usuario necesita
dos cosas: el contenido en formato usable, y saber qué pudo perderse.

## Herramientas disponibles (siempre presentes en el entorno)

- **pdfplumber** – extracción de texto nativo, tablas y coordenadas de fuente (`page.chars`, `extract_words()`)
- **pdf2image** – renderizar páginas como imágenes (para OCR)
- **pytesseract** – OCR sobre imágenes de página (provider por defecto)
- **Pillow** – manipulación de imágenes
- **pdftotext / pdfimages** (CLI, poppler-utils) – alternativa rápida

Usa el script `scripts/pdf_to_md.py` incluido en este skill como motor de extracción.
Los scripts auxiliares `scripts/layout_analyzer.py` y `scripts/validator.py` construyen
el Layout IR y validan la calidad respectivamente.

---

## Flujo de trabajo

### 1. Recibir el PDF

El PDF puede llegar como:
- Ruta a un archivo en el filesystem (de un upload del usuario)
- Adjunto en la conversación (lo encontrarás en el directorio de uploads)

Localízalo primero. Si el usuario no adjuntó nada aún, pídele el archivo.

### 2. Clasificar el PDF antes de extraer

Ejecuta una inspección rápida con pdfplumber para determinar el tipo:

```python
import pdfplumber

with pdfplumber.open(pdf_path) as pdf:
    sample_pages = pdf.pages[:min(3, len(pdf.pages))]
    text_chars = sum(len(p.extract_text() or "") for p in sample_pages)
    total_pages = len(pdf.pages)
```

| Situación | Clasificación | Estrategia |
|-----------|--------------|-----------|
| `text_chars > 100` por página promedio | PDF con texto nativo | Extracción directa con pdfplumber + análisis de layout |
| `text_chars < 20` en todas las páginas | PDF escaneado (imagen) | OCR página por página |
| Mezcla (algunas páginas texto, otras no) | PDF mixto | Ambas estrategias por página |
| Texto nativo + objetos imagen embebidos | PDF estructurado con imágenes | Extracción + clustering de figuras |

### 3. Ejecutar extracción con análisis de layout

```bash
python scripts/pdf_to_md.py <ruta_al_pdf> \
    --output <nombre_salida> \
    --lang spa+eng \
    --provider tesseract \
    [--save-ir]
```

El script produce:
- `<nombre_salida>.md` — el Markdown del contenido
- `<nombre_salida>_audit.md` — reporte de auditoría con quality score
- `images/` — carpeta con figuras recortadas del render
- `ir.json` — Layout IR en JSON (solo con `--save-ir`, útil para depuración)

**Pasos internos por página:**

1. **Clasificar página** — nativa / OCR / blank
2. **Detectar columnas** — calcular distribución X de `extract_words()`.
   Si ambas mitades de la página tienen palabras → 2 columnas; separar col1 (x < mid) y col2 (x ≥ mid)
3. **Detectar font sizes** — usar `page.chars` para obtener `body_size` (tamaño más frecuente).
   Líneas con size > body_size+2 → heading. Nivel `##` o `###` según distancia al body.
4. **Filtrar elementos de layout** — ver sección dedicada
5. **Construir Layout IR** por página con bloques tipados
6. **Validar IR** — checks de conteo, duplicados, jerarquía
7. **Serializar** IR → Markdown en orden de lectura correcto

### 4. Revisar y refinar el output

Después de correr el script, **lee el MD generado** y corrígelo si detectas:

- Texto con OCR roto en medio de palabras → únelos
- Tablas que se convirtieron como texto plano → reformatéalas como tabla Markdown
- Encabezados que aún aparecen como párrafos → promociónales a `##` / `###`
- Columnas de doble página que se concatenaron mal → reorganízalas

### 5. Generar el bloque de auditoría

El script genera el audit automáticamente con el nuevo formato de niveles y quality score:

```markdown
## Auditoría de conversión

| Dimensión | Estado | Detalle |
|-----------|--------|---------|
| Texto nativo | ✅ OK | 17 páginas extraídas directamente |
| OCR | ≈ APPROX | 5 páginas · confianza 83–93% |
| Columnas | ✅ OK | 2-col detectado en 6 páginas |
| Encabezados | ✅ OK | 8 headings marcados con ## / ### |
| Figuras | ✅ OK | 16 figuras limpias (92 fragmentos agrupados) |
| Captions | ✅ OK | 14 captions ligadas a imágenes |
| Numeración de pág. | ✅ OK | Filtrados 28 números de página |
| Notas al pie | ✅ OK | 2 notas al pie como blockquote |

### Quality Score: 88/100

| Dimensión | Peso | Score |
|-----------|------|-------|
| Estructura | 20% | 20/20 |
| Texto | 20% | 18/20 |
| Imágenes | 15% | 15/15 |
| Tablas | 10% | 10/10 |
| OCR | 10% | 8/10  |
| Layout | 25% | 17/25 |

### 📝 Notas del proceso
- Tipo detectado: mixed — 17 pág. nativas, 5 OCR, 6 en blanco
- Provider OCR: tesseract (spa+eng)
- Páginas con 2 columnas: 6
- Figuras: 92 fragmentos → 16 PNGs limpios
```

**Niveles de estado en la auditoría:**
- `✅ OK` — completamente correcto, sin pérdida
- `≈ APPROX` — convertido con aproximación aceptable (ej. OCR 85%+)
- `⚠️ WARNING` — convertido parcialmente; revisar sección
- `❌ ERROR` — no convertido o con pérdida significativa
- `📎 ASSET` — elemento visual capturado como PNG (sin texto extraíble)

---

## Filtros de elementos de layout

### Números de página
Los números de página (romanos o arábigos) que aparecen solos en la franja
superior o inferior de la página (top/bottom 10%) se descartan automáticamente.
No se incluyen en el Markdown.

```python
import re
PAGE_NUM_RE = re.compile(r'^\s*([IVXLCDM]+|\d{1,4})\s*$', re.IGNORECASE)

def is_page_number(text, y_ratio):
    return (y_ratio < 0.08 or y_ratio > 0.92) and PAGE_NUM_RE.match(text.strip())
```

### Notas al pie
Texto en la franja inferior de la página (> 82% de la altura) con font size
menor al body se convierte en blockquote marcado:

```markdown
> ¹ De las actividades agropecuarias y forestales, solo la pesca y la acuicultura…
```

### Captions de figura
El texto inmediatamente debajo del bbox de cada figura (dentro de 20pt) se
extrae como caption y se liga a la imagen en el IR:

```markdown
![Figura extraída de página 16](images/fig_p16_1.png)
*Unidad que cumple con las características para ser considerado establecimiento*
```

### De-hifenación
Los guiones tipográficos de final de línea (justificación) se resuelven:
`estableci-\nmiento` → `establecimiento\n`.

### Listas y viñetas
Líneas que inician con `•`, `–`, `-`, `*` o `1.` se convierten a lista Markdown:
```markdown
- elemento de lista
- otro elemento
```

---

## Arquitectura interna: Layout Intermediate Representation (IR)

El script no convierte directamente PDF → Markdown. Usa un IR JSON como capa
intermedia que permite validar y reordenar el contenido antes de serializar.

```
PDF → Extracción → Layout IR (JSON) → Validación → Markdown + Audit
```

**Tipos de bloque en el IR:**

| Tipo | Descripción | Salida en MD |
|------|-------------|--------------|
| `heading` | Encabezado (nivel 1–3 por font size) | `#` / `##` / `###` |
| `paragraph` | Párrafo de cuerpo | texto plano |
| `list_item` | Elemento de lista | `- item` |
| `footnote` | Nota al pie (área inferior) | `> nota` |
| `page_number` | Número de página | descartado |
| `image` | Figura (PNG recortado) | `![alt](path)` |
| `caption` | Leyenda ligada a imagen | `*texto*` |
| `table` | Tabla extraída | tabla Markdown |
| `blank_page` | Página en blanco | nota informativa |

---

## Abstracción de provider OCR/LLM

Para compatibilidad con Tesseract, Ollama y proveedores remotos, el script
usa una interfaz común en `providers/`:

```bash
# Tesseract (por defecto):
python scripts/pdf_to_md.py archivo.pdf --provider tesseract

# Ollama (requiere Ollama corriendo localmente con modelo multimodal):
python scripts/pdf_to_md.py archivo.pdf --provider ollama --ollama-model llava:13b

# Con descripción visual de figuras (alt text):
python scripts/pdf_to_md.py archivo.pdf --provider ollama --describe-images
```

El proveedor maneja tanto OCR de páginas escaneadas como descripción opcional
de figuras para generar alt text en Markdown.

---

## Casos especiales y cómo manejarlos

### PDFs escaneados de baja calidad
Si el OCR produce <70% de caracteres reconocibles (muchos `###`, `|||`, `???`):
- Intenta preprocesar la imagen (contrast enhance, thresholding) antes del OCR
- Documenta en el audit: "Página N: baja calidad de imagen, texto puede contener errores"
- Incluye el texto OCR de todos modos, marcado con `> ⚠️ OCR de baja confianza`

### PDFs con tablas complejas
pdfplumber tiene extracción de tablas. Si falla:
- Convierte la página a imagen y describe la tabla visualmente
- En el audit: "Tabla en página N: convertida a descripción por complejidad del layout"

### PDFs con fórmulas matemáticas
No hay conversión automática a LaTeX. Opciones:
- Si son pocas: descríbelas textualmente ("integral de f(x) dx de 0 a 1")
- Extrae la imagen de la fórmula y refiérela con `![formula_pN](images/formula_pN.png)`
- Documenta en audit como "no convertible automáticamente"

### PDFs con múltiples columnas
El script detecta automáticamente 2 columnas por distribución X de palabras.
Si la detección falla:
- Usa `page.extract_words()` con coordenadas para separar columnas manualmente
- O reorganiza el texto leído con sentido común

### PDFs con páginas rotadas
PDFs generados por sistemas institucionales frecuentemente tienen el contenido rotado 90° o 270°.
El script detecta la rotación con `page.rotation` y hace fallback automático a OCR.
El audit reportará `Fallback a OCR: Página rotada Xº`.

Si sospechas rotación y el audit no lo detectó, fuerza OCR completo:
```bash
python scripts/pdf_to_md.py archivo.pdf --ocr-only
```

### PDFs con fuentes personalizadas / logo fonts (tipo `text-with-ocr-fallback`)
Muchos PDFs institucionales (formularios de universidades, cartas de gobierno, etc.) usan
fuentes de logos donde los glifos visuales y los code points Unicode no coinciden. pdfplumber
extrae el texto "real" del stream pero produce palabras sin sentido como `WMuaa`, `DsGe`, `2s5t`.

El script detecta estos artefactos en las primeras palabras y hace fallback automático a OCR,
que sí respeta el orden visual. El audit reportará `text-with-ocr-fallback` como tipo.

El OCR en estos casos suele tener 85-95% de confianza con acento ocasional faltante — normal
en documentos en español con tesseract. El usuario debe revisar las `é`, `ó`, `ñ` después de la conversión.

### PDFs con encoding CID sin mapeo Unicode (tipo `text-with-ocr-fallback`)
PDFs generados por sistemas institucionales (INEGI, SEP, IMSS, etc.) que usan fuentes CID
internas sin tabla ToUnicode. pdfplumber extrae el texto como tokens `(cid:0)`, `(cid:32)`, etc.
— completamente ilegibles.

El script detecta automáticamente cuando >10% de los "tokens" del texto son CID y hace
fallback a OCR. El audit reportará la razón: `"Encoding CID sin mapeo Unicode (N tokens CID)"`.
No es necesario usar `--ocr-only` manualmente.

### PDFs con texto de baja calidad / encoding corrupto
El script detecta cuando el ratio de caracteres no-alfanuméricos es >25% y hace fallback a OCR.
Verifica el campo "Fallback a OCR" en el audit para saber qué páginas fueron afectadas.

### PDFs con páginas en blanco (manuales, libros, informes impresos)
Los documentos con diseño editorial incluyen versos en blanco intencionales entre capítulos.
El script los detecta (sin texto, sin imágenes, sin vectores) y los reporta en una sección
propia del audit: `⬜ Páginas en blanco (sin contenido en el original)`.

**No son errores.** Si el audit reporta páginas en blanco, no las presentes al usuario como
contenido perdido ni como fallo de OCR — son páginas que efectivamente no tienen nada.

### PDFs con figuras fragmentadas (diseño editorial)
Los PDFs maquetados profesionalmente no guardan una foto como un objeto: la cortan en franjas
horizontales y le añaden capas de sombra y máscaras de transparencia (SMask). Una página con
2 fotos puede contener 16 objetos-imagen; extraerlos uno a uno produce tiras inservibles.

El script agrupa los fragmentos por adyacencia espacial (`cluster_image_regions`) y recorta
cada figura completa del render de la página a 150 DPI. El resultado son PNGs limpios
(`fig_pN_M.png`) con la figura entera, incluidos marcos y pies de foto.

### PDFs protegidos / encriptados
pdfplumber lanzará un error si está encriptado. Informa al usuario que el PDF está protegido
y pídele que lo desbloquee primero.

### PDFs con texto en imagen (no OCR-able por idioma)
Si el idioma no es español/inglés/portugués:
```bash
# Con Tesseract:
python scripts/pdf_to_md.py archivo.pdf --lang fra

# Idiomas disponibles: tesseract --list-langs
# Con Ollama, el idioma se detecta automáticamente del modelo
```

---

## Validación antes de serializar

El script valida el IR antes de generar el Markdown final:

| Check | Condición | Nivel |
|-------|-----------|-------|
| Imágenes sin captions | count(images) > 0 y count(captions) == 0 | WARNING |
| Captions huérfanas | count(captions) > count(images) | WARNING |
| Texto duplicado | mismo bloque de texto en >1 página | WARNING |
| Heading sin padre | heading nivel 3 sin nivel 2 previo | WARNING |
| Números de página | se filtran siempre, nunca son error | INFO |
| OCR baja confianza | confianza < 80% | WARNING |
| PDF encriptado | pdfplumber error al abrir | ERROR |

---

## Métrica de calidad (Quality Score 0–100)

El score total es la suma ponderada de 6 dimensiones:

| Dimensión | Peso | Evalúa |
|-----------|------|--------|
| Estructura | 20% | Headings detectados; jerarquía coherente # / ## / ### |
| Texto | 20% | Cobertura de extracción; de-hifenación aplicada |
| Imágenes | 15% | Figuras extraídas como PNGs limpios; captions ligadas |
| Tablas | 10% | Tablas convertidas a Markdown (N/A = 100%) |
| OCR | 10% | Confianza promedio Tesseract/provider en páginas OCR |
| Layout | 25% | Columnas, pág-num filtrados, notas al pie, listas |

**Rangos:**
- 90–100: excelente, listo para uso directo
- 70–89: bueno, revisión puntual recomendada
- 50–69: aceptable, requiere revisión de secciones WARNING
- < 50: conversión parcial, comunicar al usuario antes de entregar

---

## Estructura de salida

```
output/
├── documento.md          # El Markdown principal
├── documento_audit.md    # Reporte de auditoría con quality score
├── ir.json               # Layout IR (solo con --save-ir)
└── images/
    ├── fig_p1_1.png      # Figuras recortadas del render, referenciadas en el MD
    └── fig_p3_2.png
```

En el MD principal, las imágenes van referenciadas:
```markdown
![Descripción de la figura](images/fig_p3_1.png)
*Unidad que cumple con las características para ser considerado establecimiento*
```

---

## Comunicación con el usuario

Al terminar, presenta:
1. El archivo `.md` (con `SendUserFile`)
2. El archivo `_audit.md` (con `SendUserFile`)
3. Un resumen en 2–3 líneas: cuántas páginas, qué tipo de PDF era, quality score obtenido

Si hay problemas graves (PDF encriptado, score < 50), díselo
claramente antes de entregar el archivo.

---

## Referencia: scripts

### pdf_to_md.py (motor principal)

```
python pdf_to_md.py <input.pdf> [--output nombre] [--lang es] [--dpi 300]
                    [--ocr-only] [--no-images] [--save-ir]
                    [--provider tesseract|ollama]
                    [--ollama-model llava:13b]
                    [--describe-images]
```

- `--lang`           : idioma para tesseract (default: `spa+eng`)
- `--dpi`            : resolución para renderizar páginas escaneadas (default: 300)
- `--ocr-only`       : forzar OCR aunque haya texto nativo
- `--no-images`      : no extraer imágenes embebidas (solo texto)
- `--save-ir`        : guardar Layout IR en ir.json para depuración
- `--provider`       : proveedor OCR (default: `tesseract`)
- `--ollama-model`   : modelo Ollama multimodal (default: `llava:13b`)
- `--describe-images`: generar alt text con provider de visión

### layout_analyzer.py (constructor del IR)

```
python layout_analyzer.py <ir_raw.json> [--output ir.json]
```

Convierte la extracción raw (coordenadas, fuentes, imágenes) en bloques
tipados con reading order correcto.

### validator.py (checks y quality score)

```
python validator.py <ir.json> [--audit audit_prev.md]
```

Valida el IR contra los checks definidos y produce el quality score.
