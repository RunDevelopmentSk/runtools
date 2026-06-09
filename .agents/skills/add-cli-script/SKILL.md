---
name: add-cli-script
description: Pridanie nového pomocného Python CLI skriptu do projektu runtools podľa projektových konvencií. Použi keď máš vytvoriť nový samostatne spustiteľný nástroj a sprístupniť ho ako konzolový príkaz.
---

# add-cli-script

Nový pomocný nástroj patrí do `src/runtools/<name>.py` a sprístupňuje sa ako
konzolový príkaz cez `pyproject.toml` → `[project.scripts]`. Každý skript musí
byť spustiteľný aj samostatne (`python ./src/runtools/<name>.py`).

## Konvencie (vzor podľa existujúcich skriptov)

- Cieľová verzia je Python 3.10+ (viď `pyproject.toml`).
- Preferuj štandardnú knižnicu; novú závislosť pridávaj cez package manager (pip),
  nie ručnou úpravou `pyproject.toml`.
- `main()` vracia int (exit code): `0` pri úspechu, nenulové pri chybe.
- Na konci súboru je vždy `if __name__ == "__main__": raise SystemExit(main())`.
- `print()` je v týchto CLI nástrojoch určený na výstup pre používateľa.
- Pri `subprocess.run(...)` použi explicitné `check=` a ošetri návratový kód.
- Pri práci so súbormi over existenciu a práva (vzor v `gitexport.py`).

## Šablóna skriptu

```python
#!/usr/bin/env python3
import sys


def print_help():
    print("python3 <name>.py [ARGS]")
    print()
    print("Stručný popis čo nástroj robí.")


def main():
    argv = sys.argv[1:]

    if "-h" in argv or "--help" in argv:
        print_help()
        return 0

    # ... logika nástroja ...

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Registrácia konzolového príkazu

Do `pyproject.toml` pridaj do sekcie `[project.scripts]` riadok:

```toml
<name> = "runtools.<name>:main"
```

Po inštalácii (`pipx install --force …` alebo `pip install -e .`) je príkaz
dostupný globálne ako `<name>`.

## Checklist

- [ ] Súbor `src/runtools/<name>.py` so `main() -> int` a `raise SystemExit(main())`
- [ ] Skript je spustiteľný aj samostatne: `python ./src/runtools/<name>.py`
- [ ] Príkaz zaregistrovaný v `pyproject.toml` → `[project.scripts]`
- [ ] Nástroj doplnený do zoznamu príkazov v `README.md`
- [ ] Nové závislosti (ak nejaké) pridané cez package manager, nie ručne

## Anti-pattern

- ❌ Neumiestňuj logiku mimo `main()` tak, že sa spustí už pri importe modulu.
- ❌ Nehardkóduj heslá/tokeny; URL chránené heslom sťahuj cez `curl -u …` (viď `AGENTS.md`).
- ❌ Nepridávaj závislosť ručným zápisom do `pyproject.toml` – použi package manager.
