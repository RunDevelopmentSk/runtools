---
name: add-implementation-doc
description: Pridanie alebo aktualizácia popisu implementačných detailov do `docs/implementation-details/`. Použi po implementácii novej funkcionality alebo nekoncepčnej zmeny, ktorá si vyžaduje dokumentáciu.
---

# add-implementation-doc

Implementačné detaily zapracovanej funkcionality patria do `docs/implementation-details/`.

## Pravidlá názvoslovia

- Súbor: `{ticket-id}-{slug}.md`
  - napr. `8897-excise-release-flow.md`, `8897-excise-release-automation.md`
- Obrázky: `docs/implementation-details/img/{slug}-NN.png`
  - napr. `excise-release-01.png`, `excise-release-02.png`
  - názov obrázka **sa zhoduje s `{slug}` súboru**, kde sa používa

## Štýl obsahu

Z `AGENTS.md`: *"Pri dopĺňaní dokumentácie je potrebné dbať na to, aby dokumentácia
zapracovanej funkcionality bola stručná, vecná a pravdivá."*

Odporúčaná štruktúra dokumentu:

```markdown
# {Stručný názov funkcionality}

Tiket: {ticket-id}

## Cieľ / motivácia

(1–3 vety: prečo to existuje, aký problém rieši)

## Implementácia

(Konkrétne moduly/modely/views/automatizmy, ktorých sa zmena dotkla.
Odkazuj na súbory v repe relatívnymi cestami.)

## Konfigurácia / spustenie

(Ak treba ručné kroky pri inicializácii v novej DB.
Ak je úvodná konfigurácia automatizovaná, popíš to v `docs/initial-configuration.md`
a odkáž sem.)

## Súvisiace

(Odkazy na iné implementačné popisy, AIS/NIS dokumenty, externé špecifikácie.)
```

## Checklist

- [ ] Súbor má prefix s tiket ID
- [ ] Slug v názve súboru zodpovedá obsahu (krátky, kebab-case)
- [ ] Obrázky majú prefix `{slug}-NN` a sú v `docs/implementation-details/img/`
- [ ] Ak funkcionalita pridáva úvodnú konfiguráciu, je popísaná aj v `docs/initial-configuration.md`
- [ ] Žiadne marketingové/subjektívne hodnotenia ("elegantné riešenie", "robustné", …)

## Anti-pattern

- ❌ Nepíš redundantné komentáre/popisy, ktoré sú zrejmé z kódu.
- ❌ Nevytváraj `README.md` v moduloch, pokiaľ to nie je explicitne potrebné.
