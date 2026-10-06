#!/usr/bin/env python3
"""
Genera el correo mensual de notificación de reasignación de licencias de GitHub Copilot
para el equipo/área indicado, a partir de un CSV de seguimiento con columnas: nombre,
usuario, correo, y una columna por mes (valores SI/NO) que indica si la licencia sigue activa.

Uso:
    python3 generar_correo.py --csv seguridad.csv --equipo "Seguridad" --mes agosto \
        --fecha-limite "7 de agosto de 2026" \
        [--destinatario "Juan Muñoz López"] [--correo-destinatario "juan.munoz@inegi.org.mx"] \
        [--remitente "Ricardo Olvera Navarro"] [--correo-remitente "RICARDO.OLVERA@inegi.org.mx"] \
        [--puesto-remitente "..."] \
        [--criterios references/criterios_institucionales.md] \
        --out correo.md
"""
import argparse
import csv
import sys
from pathlib import Path


def leer_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        raise ValueError("El CSV está vacío.")
    return rows[0], rows[1:]


def col_index(header, name, required=True):
    name_l = name.strip().lower()
    for i, h in enumerate(header):
        if h.strip().lower() == name_l:
            return i
    if required:
        raise ValueError(
            f"No encontré la columna '{name}'. Columnas disponibles: {header}"
        )
    return None


def tabla(personas):
    if not personas:
        return "_Ninguna._\n"
    out = "| Nombre | Usuario | Correo |\n|---|---|---|\n"
    for n, u, c in personas:
        out += f"| {n} | {u} | {c} |\n"
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", required=True)
    ap.add_argument("--mes", required=True, help="Nombre exacto de la columna del mes a evaluar, p.ej. agosto")
    ap.add_argument("--equipo", required=True, help="Nombre del equipo/área al que pertenecen las licencias, p.ej. SSPTIC o Seguridad")
    ap.add_argument("--fecha-limite", required=True, dest="fecha_limite", help='Fecha límite de justificación, p.ej. "7 de agosto de 2026"')
    ap.add_argument("--destinatario", default=None)
    ap.add_argument("--correo-destinatario", default=None, dest="correo_destinatario")
    ap.add_argument("--remitente", default="Ricardo Olvera Navarro")
    ap.add_argument("--correo-remitente", default="RICARDO.OLVERA@inegi.org.mx", dest="correo_remitente")
    ap.add_argument("--puesto-remitente", default=None, dest="puesto_remitente")
    ap.add_argument("--criterios", default=None)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    header, data = leer_csv(args.csv)

    idx_nombre = col_index(header, "nombre")
    idx_usuario = col_index(header, "usuario")
    idx_correo = col_index(header, "correo")
    idx_mes = col_index(header, args.mes)

    mantienen, remueven = [], []
    for row in data:
        if not row or idx_nombre >= len(row) or not row[idx_nombre].strip():
            continue
        nombre = row[idx_nombre].strip()
        usuario = row[idx_usuario].strip() if idx_usuario < len(row) else ""
        correo = row[idx_correo].strip() if idx_correo < len(row) else ""
        valor_crudo = row[idx_mes] if idx_mes < len(row) else ""
        valor = valor_crudo.strip().upper()
        # Valores vacíos o con guión ("-", " -", "- /", etc.) indican que la persona
        # ya no tiene licencia activa desde un mes anterior. Se excluyen silenciosamente.
        if valor in ("SI", "SÍ"):
            mantienen.append((nombre, usuario, correo))
        elif valor == "NO":
            remueven.append((nombre, usuario, correo))

    criterios_md = ""
    ruta_criterios = Path(args.criterios) if args.criterios else (
        Path(__file__).resolve().parent.parent / "references" / "criterios_institucionales.md"
    )
    if ruta_criterios.exists():
        criterios_md = ruta_criterios.read_text(encoding="utf-8").strip()

    correo_dest = args.correo_destinatario or "[correo institucional pendiente]"
    puesto = args.puesto_remitente or "[puesto/área pendiente]"
    destinatario = args.destinatario or "[destinatario pendiente]"
    saludo = f"Estimado(a) {args.destinatario.split()[0]}," if args.destinatario else "Estimado(a),"

    partes = [
        f"**Para:** {destinatario} `{correo_dest}`",
        f"**De:** {args.remitente} ({args.correo_remitente})",
        f"**Asunto:** Notificación de reasignación de licencias — {args.equipo} — {args.mes}",
        "",
        saludo,
        "",
        f"Por medio del presente te comparto el estatus de reasignación de licencias del equipo de "
        f"{args.equipo} correspondiente al mes de {args.mes}, con base en el seguimiento mensual (`{Path(args.csv).name}`):",
        "",
        f"**Licencias que se mantienen ({args.mes} = SI):**",
        "",
        tabla(mantienen),
        f"**Licencias que se remueven ({args.mes} = NO):**",
        "",
        tabla(remueven),
    ]

    if criterios_md:
        partes += [criterios_md, ""]

    partes += ["### Solicitud de justificación de reasignación", ""]

    if remueven:
        partes += [
            f"Para la(s) licencia(s) marcada(s) como removida(s) en {args.mes}, solicitamos la "
            f"justificación de NO USO para su reasignación, a más tardar el **{args.fecha_limite}**, indicando:",
            "",
            "1. Motivo del NO USO de la licencia.",
            "2. Actividades o proyectos que la requieren.",
            "",
            "De no recibir respuesta dentro del plazo, la licencia se considerará disponible para reasignación a otro usuario.",
            "",
            "Cabe mencionar que, en lugar de reasignarse al mismo usuario, la licencia removida puede "
            "asignarse a otro colaborador que actualmente no cuente con una y que no haya tenido la licencia removida por incumplir los criterios de uso.",
        ]
    else:
        partes += [f"No se identificaron licencias removidas en {args.mes}; no aplica solicitud de justificación este mes."]

    partes += [
        "",
        "Quedo atento a cualquier duda.",
        "",
        "Saludos,",
        f"**{args.remitente}**",
        f"`{puesto}`",
    ]

    notas = []
    if not args.destinatario:
        notas.append("falta el destinatario del correo")
    elif not args.correo_destinatario:
        notas.append(f"falta el correo institucional de {args.destinatario}")
    if not args.puesto_remitente:
        notas.append("falta tu puesto/área para completar la firma")

    if notas:
        partes += ["", "---", "", "> Nota: " + "; ".join(notas) + "."]

    Path(args.out).write_text("\n".join(partes) + "\n", encoding="utf-8")
    print(f"Correo generado en: {args.out}")
    print(f"Mantienen: {len(mantienen)} | Remueven: {len(remueven)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
