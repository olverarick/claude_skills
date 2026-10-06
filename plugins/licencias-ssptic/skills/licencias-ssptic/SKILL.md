---
name: licencias-ssptic
description: Genera el correo mensual de notificación de reasignación de licencias para SSPTIC (INEGI) a partir de un CSV de seguimiento con columnas nombre, usuario, correo y una columna por mes (SI/NO) que indica si la licencia sigue activa. Produce un archivo Markdown con la tabla de licencias que se mantienen, la tabla de licencias que se remueven, los criterios institucionales vigentes de reasignación (umbral de uso, consistencia de casos de uso documentados) y la solicitud de justificación de no uso con la fecha límite indicada. Usa este skill siempre que el usuario mencione reasignación de licencias, baja de licencias, remoción de licencias, notificación al SSPTIC, "correo de licencias", o pida generar el reporte/correo mensual de licencias a partir de un csv de seguimiento — incluso si solo dice "genera el correo de licencias de este mes" o adjunta un csv de licencias sin mencionar "SSPTIC" explícitamente.
---

# Correo de reasignación de licencias — SSPTIC

Genera el correo mensual que notifica qué licencias se mantienen y cuáles se remueven, y solicita la justificación de no uso a quienes pierden la licencia ese mes.

## Qué necesitas del usuario

Antes de correr el script, confirma (pide lo que falte, en una sola pregunta si es posible):

1. **CSV de seguimiento** — ruta o archivo adjunto. Formato esperado: columnas `nombre`, `usuario`, `correo`, y una columna por mes (`marzo`, `abril`, `mayo`, …) con valores `SI`/`NO`. Es común que el CSV tenga columnas `baja` repetidas entre meses; el script las ignora, solo usa la columna cuyo nombre coincide con el mes indicado.
2. **Mes a evaluar** — debe coincidir (sin distinguir mayúsculas) con el nombre exacto de la columna en el CSV, p. ej. `agosto`.
3. **Fecha límite de justificación** — texto libre, p. ej. `7 de agosto de 2026`.

Opcionales (si no los da, el correo queda con placeholders `[pendiente]` que el usuario debe llenar antes de enviar):
- Destinatario (por defecto: `Juan Muñoz López`) y su correo.
- Remitente y correo (por defecto: `Ricardo Olvera Navarro` / `RICARDO.OLVERA@inegi.org.mx`) y puesto/área.

## Antes de generar: revisa los criterios institucionales

Los criterios de reasignación cambian con el tiempo (ya pasó varias veces en la conversación donde se originó este skill: primero fue solo el umbral de 40%, luego se agregó el criterio de consistencia de casos de uso, luego el umbral subió a 70%). El texto vigente vive en `references/criterios_institucionales.md`, separado del script, precisamente para que se pueda editar sin tocar código.

**Antes de generar el correo, pregúntale al usuario si esos criterios siguen vigentes o si hubo un ajuste.** Si hay cambios, edita `references/criterios_institucionales.md` primero (mismo formato Markdown, se inserta tal cual en el correo) y luego corre el script. No asumas que el archivo sigue actualizado solo porque existe.

## Cómo generar el correo

Corre el script con los datos confirmados:

```bash
python3 scripts/generar_correo.py \
  --csv "/ruta/al/ssptic.csv" \
  --mes "agosto" \
  --fecha-limite "7 de agosto de 2026" \
  --destinatario "Juan Muñoz López" \
  --out "correo_ssptic_reasignacion_licencias.md"
```

Parámetros opcionales: `--correo-destinatario`, `--remitente`, `--correo-remitente`, `--puesto-remitente`, `--criterios` (ruta alterna al archivo de criterios, si no se usa el de `references/` por defecto).

El script imprime al final cuántas personas quedaron en cada categoría (mantienen / remueven / a revisar). Si hay personas en "a revisar" (valor en la columna del mes que no es `SI` ni `NO` — vacío, `" - /"`, etc.), quedan fuera de ambas tablas y se listan en una nota al final del correo: revísalas con el usuario antes de enviar, no las descartes en silencio.

## Después de generar

1. Lee el `.md` resultante y muéstraselo al usuario (o entrégaselo como archivo).
2. Señala explícitamente cualquier placeholder `[pendiente]` que haya quedado (destinatario, correo, puesto) y la nota de "a revisar" si aplica.
3. Si el usuario pide ajustes de redacción o de criterios, edítalos directamente en el `.md` de salida (o en `references/criterios_institucionales.md` si el cambio es al criterio institucional, para que quede reflejado en la próxima corrida).
