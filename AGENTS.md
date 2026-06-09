---
type: "always_apply"
---

# Project Agent Instructions

Tento súbor je **single source of truth** pre všetkých AI agentov v projekte
(Augment Code, Claude Code, Antigravity, Codex). Augment Code, Antigravity
a Codex ho čítajú natívne; Claude Code ho číta cez symlink `CLAUDE.md → AGENTS.md`.

## Všeobecný popis

Tento projekt slúži na vývoj pomocných Python skriptov. Skripty sú písané:

- pre Python 3.10+ (viď aj `pyproject.toml`)
- tak, aby každý z nich mohol byť spustiteľný aj samostatne (napr. `python ./src/runtools/dockerinfo.py`)

Viď aj `README.md`.

## AI agenti

Viď `docs/ai-agents.md`.

## Rôzne

### Načítanie URL adries chránených pomocou hesla

Pri načítaní URL adries chránených pomocou hesla použi `curl`. Napríklad pri basic HTTP authentication použi `curl -u <user>:<pwd> https://example.sk/some/protected/page`
