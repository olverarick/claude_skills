# olverarick/claude_skills

Marketplace de plugins de Claude Code con skills institucionales desarrolladas para el trabajo de gobierno de arquitectura tecnológica (MGAT) y gestión de TI en INEGI/DCMTIC.

Repositorio público, publicado bajo licencia [MIT](./LICENSE).

Cada skill vive como un plugin independiente, para poder instalarse, versionarse y actualizarse por separado.

## Skills incluidas

| Plugin | Qué hace |
|---|---|
| [`adr-mgat`](./plugins/adr-mgat) | Crea y clasifica Architecture Decision Records (ADR) dentro del MGAT, listos para el Nivel 4 del marco. |
| [`mga-clasificacion`](./plugins/mga-clasificacion) | Dictamina si una tecnología, práctica o procedimiento debe incorporarse al MGAT y en qué instrumento. |
| [`process-modeler`](./plugins/process-modeler) | Documenta y estandariza procesos de TI bajo ITIL 4, BPMN 2.0 y RACI en Markdown versionable. |
| [`evaluador-portafolio`](./plugins/evaluador-portafolio) | Evaluación semestral de portafolio tecnológico: scoring ponderado, reporte ejecutivo y fichas de retroalimentación. |
| [`licencias-ssptic`](./plugins/licencias-ssptic) | Correo mensual de reasignación de licencias para SSPTIC a partir de un CSV de seguimiento. |
| [`correo-reasignacion-github-copilot`](./plugins/correo-reasignacion-github-copilot) | Correo mensual de reasignación de licencias de GitHub Copilot para cualquier equipo/área. |
| [`fichas-tecnicas`](./plugins/fichas-tecnicas) | Fichas informativas técnicas en Markdown, estilo Pato Bug Traduce, con referencias verificables. |
| [`pdf-to-md`](./plugins/pdf-to-md) | Convierte PDFs a Markdown con auditoría de calidad del proceso de conversión. |

## Instalación

Desde Claude Code:

```bash
/plugin marketplace add olverarick/claude_skills
/plugin install adr-mgat@olverarick-skills
```

Repite el segundo comando con el nombre de cada plugin que quieras habilitar (ver la tabla arriba), o instala todos los que necesites.

Para actualizar el marketplace tras un cambio en el repositorio:

```bash
/plugin marketplace update olverarick-skills
```

## Estructura del repositorio

```
claude_skills/
├── .claude-plugin/
│   └── marketplace.json       # catálogo del marketplace (nombre, owner, lista de plugins)
├── plugins/
│   └── <nombre-skill>/
│       ├── .claude-plugin/
│       │   └── plugin.json    # manifiesto del plugin
│       └── skills/
│           └── <nombre-skill>/
│               ├── SKILL.md   # instrucciones de la skill
│               ├── references/
│               ├── scripts/
│               └── assets/
└── README.md
```

Cada plugin es independiente: tiene su propio `plugin.json` con `name`, `version`, `description` y `author`, y contiene una sola skill bajo `skills/<nombre>/SKILL.md`. Esto permite agregar, quitar o versionar skills una por una sin afectar a las demás.

## Agregar una nueva skill

1. Crea `plugins/<nombre-skill>/.claude-plugin/plugin.json` siguiendo el patrón de cualquiera de los plugins existentes.
2. Crea `plugins/<nombre-skill>/skills/<nombre-skill>/SKILL.md` (y `references/`, `scripts/`, `assets/` si aplica).
3. Agrega una entrada en `.claude-plugin/marketplace.json` dentro del arreglo `plugins`, con `name`, `source` (`./plugins/<nombre-skill>`), `description` y `version`.
4. Agrega la skill a la tabla de este README.
5. Haz commit y push. Quien ya tenga el marketplace agregado recibe la skill nueva con `/plugin marketplace update olverarick-skills`.

## Actualizar una skill existente

Edita el `SKILL.md` o sus archivos de soporte, sube de versión el `version` en el `plugin.json` del plugin y, si cambió la descripción, actualízala también en `marketplace.json`. Haz commit y push.

## Referencia

Formato de `marketplace.json` y `plugin.json`: [documentación oficial de Claude Code sobre plugins](https://code.claude.com/docs/en/plugins/marketplace-reference).
