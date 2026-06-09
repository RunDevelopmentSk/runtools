---
description: Skontroluje necommitnuté zmeny, zhrnie ich a upozorní na potenciálne problémy pred commitom.
---

# Review Changes

Skontroluj aktuálne necommitnuté zmeny v repozitári a priprav prehľad pre code review.

## Kroky

1. Zobraz zoznam zmenených súborov: `git status --short`
2. Zobraz diff zmenených súborov: `git diff`
3. Skontroluj, či zmeny:
   - Neobsahujú debug výpisy, `print()`, `_logger.debug()` volania určené len na vývoj
   - Neobsahujú zakomentovaný kód (skôr zmaž než zakomentovaj)
   - Neobsahujú citlivé údaje (heslá, API kľúče, tokeny)
   - Sú konzistentné s konvenciami projektu z `AGENTS.md`
4. Zhrň zmeny stručne: čo sa menilo a prečo
5. Ak sú problémy, vypíš ich zoznam; ak nie, potvrď, že zmeny vyzerajú v poriadku
