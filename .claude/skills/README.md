# Skills de escrita (terceiros)

Instaladas a pedido do autor e versionadas aqui para sobreviverem entre sessões.

| Pasta | Origem | Licença |
|---|---|---|
| `novel-writing/` | github.com/EchoAI-Design/novel-writing-skill | MIT (segundo o README) |
| `creative-writing/` | github.com/pavelkudrna83/creative-writing-skill | não declarada |
| `book-bible/`, `continuity-check/`, `daily-write/`, `dev-edit/`, `hint-*/`, `manuscript-organize/`, `research/`, `story-analysis/`, `voice-extract/` | github.com/chianglianglin/novel-hint | MIT (`LICENSE` em cada pasta) |

Ajustes feitos na cópia do novel-hint: cada skill foi movida para `.claude/skills/<nome>/` (o repositório original as aninha em `skills/`) e ganhou o cabeçalho `name`/`description`, que faltava. `hint-core/` fica ao lado das outras porque elas o leem via `../hint-core/hint-core.md`.

**Precedência:** em qualquer conflito, valem `CLAUDE.md`, `docs/ESTILO.md`, `docs/BIBLIA.md` e `docs/ROTEIRO_V2.md`. Estas skills são ferramentas de apoio, não regras do livro. O novel-hint espera uma pasta `wiki/` e capítulos `chapter_NN.md`; neste projeto a bíblia está em `docs/` e os capítulos em `manuscrito/parteN/capNN.txt` — indique os caminhos ao usá-las.
