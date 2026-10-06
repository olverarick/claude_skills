---
name: correo-reasignacion-github-copilot
description: Genera el correo mensual de notificación de reasignación de licencias de GitHub Copilot (INEGI) para cualquier equipo/área (SSPTIC, Seguridad, etc.) a partir de un CSV de seguimiento con columnas nombre, usuario, correo y una columna por mes (SI/NO) que indica si la licencia sigue activa. Produce un archivo Markdown con la tabla de licencias que se mantienen, la tabla de licencias que se remueven, los criterios institucionales vigentes de reasignación (umbral de uso, consistencia de casos de uso documentados) y la solicitud de justificación de no uso con la fecha límite indicada. Usa este skill siempre que el usuario mencione reasignación de licencias de Copilot, baja de licencias, remoción de licencias, notificación de licencias a un equipo o área, "correo de licencias", o pida generar el reporte/correo mensual de licencias a partir de un csv de seguimiento — incluso si solo dice "genera el correo de licencias de este mes" o adjunta un csv de licencias de otro equipo distinto de SSPTIC.
---

# Correo de reasignación de licencias — GitHub Copilot

Genera el correo mensual que notifica, para el equipo/área que indique el usuario, qué licencias de GitHub Copilot se mantienen y cuáles se remueven, y solicita la justificación de no uso a quienes pierden la licencia ese mes.

## Qué necesitas del usuario

Antes de correr el script, confirma (pide lo que falte, en una sola pregunta si es posible):

1. **CSV de seguimiento** — ruta o archivo adjunto. Formato esperado: columnas `nombre`, `usuario`, `correo`, y una columna por mes (`marzo`, `abril`, `mayo`, …) con valores `SI`/`NO`. Es común que el CSV tenga columnas `baja` repetidas entre meses; el script las ignora, solo usa la columna cuyo nombre coincide con el mes indicado.
2. **Equipo/área** — a quién pertenecen estas licencias (p. ej. `SSPTIC`, `Seguridad`). Cada CSV suele corresponder a un equipo distinto: no asumas que siempre es SSPTIC solo porque fue el primer caso de uso. Pregúntalo siempre que no sea evidente por el nombre del archivo o lo dicho por el usuario.
3. **Mes a evaluar** — debe coincidir (sin distinguir mayúsculas) con el nombre exacto de la columna en el CSV, p. ej. `agosto`.
4. **Fecha límite de justificación** — texto libre, p. ej. `7 de agosto de 2026`.

Opcionales (si no los da, el correo queda con placeholders `[pendiente]` que el usuario debe llenar antes de enviar):
- Destinatario (quien recibe el reporte por parte del equipo/área) y su correo.
- Remitente y correo (por defecto: `Ricardo Olvera Navarro` / `RICARDO.OLVERA@inegi.org.mx`) y puesto/área.

## Antes de generar: revisa los criterios institucionales

Los criterios de reasignación cambian con el tiempo y a veces tienen vigencia programada (p. ej. "el 40% aplica en agosto, el 70% empieza en septiembre"). El texto vigente vive en `references/criterios_institucionales.md`, separado del script, precisamente para que se pueda editar sin tocar código.

**Antes de generar el correo, pregúntale al usuario si esos criterios siguen vigentes para el mes que se va a notificar, o si hubo un ajuste.** Si hay cambios (incluyendo cambios de vigencia por mes), edita `references/criterios_institucionales.md` primero (mismo formato Markdown, se inserta tal cual en el correo) y luego corre el script. No asumas que el archivo sigue actualizado solo porque existe, y no mezcles criterios de meses distintos en la misma corrida sin confirmarlo.

## Cómo generar el correo

Corre el script con los datos confirmados:

```bash
python3 scripts/generar_correo.py \
  --csv "/ruta/al/archivo.csv" \
  --equipo "SSPTIC" \
  --mes "agosto" \
  --fecha-limite "7 de agosto de 2026" \
  --destinatario "Juan Muñoz López" \
  --out "correo_reasignacion_licencias.md"
```

Parámetros opcionales: `--correo-destinatario`, `--remitente`, `--correo-remitente`, `--puesto-remitente`, `--criterios` (ruta alterna al archivo de criterios, si no se usa el de `references/` por defecto).

El script imprime al final cuántas personas quedaron en cada categoría (mantienen / remueven / a revisar). Si hay personas en "a revisar" (valor en la columna del mes que no es `SI` ni `NO` — vacío, `" - /"`, etc.), quedan fuera de ambas tablas y se listan en una nota al final del correo: revísalas con el usuario antes de enviar, no las descartes en silencio.

## Después de generar

1. Lee el `.md` resultante y muéstraselo al usuario (o entrégaselo como archivo).
2. Señala explícitamente cualquier placeholder `[pendiente]` que haya quedado (destinatario, correo, puesto) y la nota de "a revisar" si aplica.
3. Si el usuario pide ajustes de redacción o de criterios, edítalos directamente en el `.md` de salida (o en `references/criterios_institucionales.md` si el cambio es al criterio institucional, para que quede reflejado en la próxima corrida).
