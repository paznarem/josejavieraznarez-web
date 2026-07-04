# Qué se versiona en `.claude/` (y por qué importa)

GitHub es lo **único** que sobrevive si se borra el Codespace / Claude Space.
Todo lo que no esté commiteado y empujado a GitHub se pierde. En mayo/julio de
2026 se perdieron así las tres skills del pipeline del blog porque
`.claude/skills/` estaba en `.gitignore`. Para que no vuelva a pasar:

## SÍ se versiona (va a GitHub)
- `settings.json` — permisos y hooks del proyecto (compartidos).
- `skills/` — las skills del pipeline del blog (`divulgacion-psicologia`,
  `migracion-articulo`, `traduccion-articulo`) y sus `references/`.
  Ver [FLUJO-DE-TRABAJO.md](../FLUJO-DE-TRABAJO.md) para su estructura.
- Este `README.md`.

## NO se versiona (local de la máquina, en `.gitignore`)
- `scheduled_tasks.lock` — lock de la máquina.
- `settings.local.json` — permisos locales tuyos; regenerable, no crítico.

## Regla
Después de crear o editar una skill: `git add .claude/skills/ && git commit && git push`.
Si no está en GitHub, no existe.
