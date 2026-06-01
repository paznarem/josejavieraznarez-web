# Flujo de trabajo — blog de psicología (José Javier)

Manual de referencia del pipeline. Vive en el repo.

---

## El pipeline: dónde vive cada etapa

1. **Adaptación** — *contenido*. En **Claude web**. Subes el archivo maestro (`adaptacion-maestro-AAAA-MM-DD.md`) + el texto de tu padre. Sale el texto adaptado en español, en Markdown. → **Pausa: tu padre aprueba.** → Capturas sus correcciones y Claude te devuelve el maestro actualizado.
2. **Migración** — *presentación*. En **Claude Code**. Skill `migracion-articulo`. Mete el texto adaptado en el template HTML (`blog/<archivo>.html`). → Al terminar, **encadena la traducción**.
3. **Traducción** — *idioma*. En **Claude Code**. Skill `traduccion-articulo`. Crea `en/blog/<archivo>.html` y enlaza las dos versiones.

Regla de oro: **contenido → presentación → idioma**. Siempre así.

**Dónde está la única parada humana:** entre la etapa 1 y la 2. Tu padre aprueba el texto adaptado antes de maquetar. Las etapas 2 y 3 son mecánicas y corren encadenadas en Code. Nada se publica hasta que tu padre revisa el diff de la rama.

---

## Setup

### En el repo (Claude Code) — dos skills:

```
.claude/skills/
├── migracion-articulo/
│   ├── SKILL.md
│   └── references/
│       └── procedimiento.md
└── traduccion-articulo/
    ├── SKILL.md
    └── references/
        └── procedimiento.md
```

### Fuera del repo (Claude web) — un archivo:

`adaptacion-maestro-AAAA-MM-DD.md` — se guarda en tu dispositivo. Subes siempre la versión de fecha más reciente. Contiene el método, la voz del autor, el glosario y los precedentes de corrección, todo en un solo archivo que se autoactualiza con cada entrega.

### Archivos del repo que las skills necesitan:

`blog-template.html`, `translation-glossary.md`, y los artículos EN de referencia en `en/blog/`.

---

## Reglas transversales

- **El visto bueno de tu padre es el filtro de contenido**, y va siempre en la etapa 1, antes de migrar.
- **Trabaja en rama.** Nada toca lo publicado hasta que tu padre aprueba el diff.
- **Antes de migrar, el Markdown va limpio:** sin "Control de publicación", sin "Informe de cambios", sin `[BLOQUE PARA JOSÉ JAVIER]` sin resolver.
- **Cierra el bucle de mejora.** Cada corrección de tu padre → Claude web te devuelve el maestro actualizado. Cada término inglés nuevo de la traducción → se añade a `translation-glossary.md`.

---

## Escenario A — Artículo NUEVO

1. **Claude web:** sube `adaptacion-maestro-AAAA-MM-DD.md` + el texto técnico de tu padre. → Diagnóstico + adaptación (o solo diagnóstico si lo pides). → Guarda el texto adaptado en un `.md`.
2. **Revisión de tu padre.** Aplica correcciones → se las pegas a Claude web → te devuelve el maestro actualizado. Guárdalo (sobrescribe el anterior).
3. **Prepara el Markdown final:** quita control de publicación e informe de cambios; resuelve cualquier `[BLOQUE PARA JOSÉ JAVIER]`.
4. **Claude Code — rama:** `git checkout -b nuevo-<slug>`
5. **Claude Code:** *"Migra este artículo a `blog/<archivo>.html`"* → la skill migra y encadena la traducción sola. Commits + `git push`.
6. **Tu padre revisa el diff** → merge → publicado.

## Escenario B — Artículo YA PUBLICADO (revisión)

1. **Claude web:** sube el maestro + el artículo publicado (o el texto original de tu padre si lo conservas — mejor). Pide solo diagnóstico. → Decide si merece readaptar.
2. Si sí → readapta en Claude web, revisión de tu padre, captura de precedente (igual que A1-A2).
3. **Prepara el Markdown** (igual que A3).
4. **Claude Code — rama:** `git checkout -b readaptacion-<slug>`
5. **Claude Code:** *"Migra este artículo a `blog/<archivo>.html`"* → migración + traducción encadenadas.
6. **Tu padre revisa el diff** → merge.

---

## Resumen en una línea

**Nuevo:** Claude web (adaptar) → padre aprueba → Claude Code (migrar + traducir) → padre revisa diff → merge.
**Publicado:** Claude web (diagnosticar → readaptar si procede) → padre aprueba → Claude Code (migrar + traducir) → merge.
