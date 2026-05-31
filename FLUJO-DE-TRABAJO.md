# Flujo de trabajo — blog de psicología (José Javier)

Manual de referencia del pipeline. Vive en el repo. Lo consultáis tú, tu padre y Claude Code.

---

## El pipeline: tres skills encadenadas

El trabajo de un artículo pasa por tres etapas **separadas y en orden**, cada una una skill de Claude Code. Cada una tiene una responsabilidad distinta, es autocontenida (lleva su procedimiento dentro, en su `references/`) y **pasa el testigo a la siguiente**:

1. **Adaptación** — *contenido*. Skill `divulgacion-psicologia`. Convierte el texto técnico de tu padre en texto para todos los públicos, en español, en Markdown. (Diagnóstico → reescritura → control de publicación.) → al terminar, **pausa para la revisión del autor**.
2. **Migración** — *presentación*. Skill `migracion-articulo`. Mete el texto adaptado en el template HTML (`blog/<archivo>.html`): CSS, dark mode, bloques de diseño, scripts. → al terminar, **encadena la traducción**.
3. **Traducción** — *idioma*. Skill `traduccion-articulo`. Crea la versión inglesa (`en/blog/<archivo>.html`) y enlaza las dos. → cierre.

Regla de oro: **contenido → presentación → idioma**. Nunca al revés. Se adapta primero (en limpio), luego se maqueta, luego se traduce.

**Dónde está la única parada humana:** entre la etapa 1 y la 2. La adaptación termina y **tu padre aprueba el texto** antes de maquetar. Las etapas 2 y 3 son mecánicas y corren encadenadas. Nada se publica hasta que tu padre revisa el diff de la rama al final.

---

## Setup (una sola vez)

Instala las **tres skills** como skills de proyecto, dentro del repo:

```
.claude/skills/
├── divulgacion-psicologia/
│   ├── SKILL.md                      ← v3
│   └── references/
│       ├── voz-del-autor.md          ← el de siempre, sin cambios
│       ├── glosario-tecnico.md       ← actualizado (índice)
│       └── correcciones-del-autor.md ← actualizado (índice)
├── migracion-articulo/
│   ├── SKILL.md
│   └── references/
│       └── procedimiento.md          ← el antiguo prompt de migración, ahora dentro
└── traduccion-articulo/
    ├── SKILL.md
    └── references/
        └── procedimiento.md          ← el antiguo prompt de traducción, ahora dentro
```

Cada `SKILL.md` va directo en la carpeta de su skill (no anidado un nivel de más). Los procedimientos viven **dentro** de cada skill (`references/procedimiento.md`); ya no hay prompts sueltos que pegar, y se editan ahí. Commit, **sesión nueva** de Claude Code, y `/skills` para confirmar que aparecen las tres.

Archivos del repo que las skills dan por hechos (no van dentro de la skill, ya están en el repo): `blog-template.html`, `translation-glossary.md`, y los artículos EN de referencia en `en/blog/`.

---

## Reglas transversales (valen para los dos escenarios)

- **El visto bueno de tu padre es el filtro de contenido**, y va siempre en la etapa 1 (texto adaptado en español), antes de migrar. Lo que viene después (HTML, inglés) es maquetación e idioma.
- **Trabaja en rama.** Nada toca lo publicado hasta que tu padre aprueba el diff de la rama.
- **Antes de migrar, el Markdown va limpio.** La skill de migración lo verifica, pero conviene saberlo: quita el bloque **"Control de publicación"** y el **"Informe de cambios"** que añade la etapa 1 (son notas de edición, no el artículo) y resuelve cualquier **`[BLOQUE PARA JOSÉ JAVIER]`** antes (lo rellena tu padre; no se maqueta un placeholder).
- **Cierra el bucle de mejora.** Cada corrección nueva de tu padre se captura como precedente numerado en la skill de adaptación (`references/correcciones-del-autor.md`); y cada término inglés nuevo que decida la traducción se añade a `translation-glossary.md`. Así las skills dejan de repetir los mismos fallos.

---

## Escenario A — Artículo NUEVO

Punto de partida: un texto técnico de tu padre (Markdown o texto plano).

1. **Rama:** `git checkout -b nuevo-<slug>`
2. **Adaptación.** En Claude Code: *"Adapta este texto para el blog"* (dispara `divulgacion-psicologia`) + pegas el texto o le das la ruta del borrador. Sale el diagnóstico; si hay una decisión grande (dividir en serie, cortes grandes…) se pausa y te propone un plan. Tras eso, el texto adaptado en español + el control de publicación. Guárdalo en un borrador, p. ej. `drafts/<slug>.md`.
3. **Revisión de tu padre** sobre el texto adaptado. Aplica sus correcciones y **captúralas** en `divulgacion-psicologia/references/correcciones-del-autor.md`.
4. **Prepara el Markdown final:** quita el control de publicación y el informe de cambios; comprueba que no queda ningún `[BLOQUE PARA JOSÉ JAVIER]`. (La skill de migración también lo verifica.)
5. **Migración + traducción (encadenadas).** En Claude Code: *"Migra este artículo a `blog/<archivo>.html`"* (dispara `migracion-articulo`). Al terminar (commit `Rewrite content: <archivo>`), **encadena sola la traducción** (`traduccion-articulo`): crea `en/blog/<archivo>.html`, switchers ES↔EN, dos commits (`Add English version…`, `Add EN switcher link…`) + `git push`. Si solo quieres maquetar y no traducir aún, díselo.
6. **Tu padre revisa el diff de la rama** → merge → publicado.

---

## Escenario B — Artículo YA PUBLICADO (revisión)

1. **Triaje** (barato, no toca nada). En Claude Code: *"Usa `divulgacion-psicologia` en modo solo diagnóstico sobre cada artículo de `blog/`. No reescribas nada. Para cada uno: nivel (limpieza menor / parcial / profunda), 2-3 problemas, y si detectas términos eliminados o contenido clínico que parezca inventado. Vuélcalo en `triage-divulgacion.md`."*
2. **Decide con la tabla:** "limpieza menor" → déjalo. "Parcial / profunda" → rehacer. Prioriza los hechos con versiones más antiguas, los más leídos, y los que más corrigió tu padre.
3. Para cada uno a rehacer, **rama:** `git checkout -b readaptacion-<slug>`
4. **Re-adaptación.** *Importante:* parte del **texto técnico original de tu padre** si lo conservas. Así se recuperan los términos que una versión vieja pudo haber borrado. Si solo tienes el HTML publicado, la skill mejora lo que hay, pero **no puede restaurar términos que nunca llega a ver** — si el triaje sospecha términos eliminados, esa es la señal para buscar el manuscrito original.
5. **Revisión de tu padre** + captura de precedente (igual que A3).
6. **Prepara el Markdown final** (igual que A4).
7. **Migración + traducción (encadenadas)** sobre el archivo existente, igual que en A5: `migracion-articulo` reemplaza el cuerpo y homogeneiza CSS/scripts (`Rewrite content: <archivo>`), y encadena `traduccion-articulo`, que actualiza `en/blog/<archivo>.html`. Commits + `git push`.
8. **Tu padre revisa el diff de la rama** → merge.

---

## Cómo corre ahora (resumen)

Una frase por escenario, ya con todo automatizado:

- **Nuevo:** rama → *"adapta este texto"* → (revisión de tu padre + captura de precedente) → *"migra a `blog/<archivo>.html`"* → se encadena la traducción sola → tu padre revisa el diff → merge.
- **Publicado:** *"diagnóstico de `blog/`"* → eliges los flojos → por cada uno, rama → *"adapta"* → (revisión) → *"migra"* → traducción encadenada → revisión del diff → merge.

No queda nada externo que pegar: los tres procedimientos viven dentro de sus skills, y el testigo pasa de una a otra salvo en la única parada humana (la aprobación de contenido de tu padre).
