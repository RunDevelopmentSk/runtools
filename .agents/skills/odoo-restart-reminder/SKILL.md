---
name: odoo-restart-reminder
description: Pripomenutie ako (a kedy) reštartovať alebo aktualizovať Odoo po zmene kódu. Použi vždy keď si urobil zmenu v moduloch, manifeste, modeloch, views alebo data súboroch. Odoo NIKDY nespúšťaj ani neaktualizuj automaticky – iba upozorni používateľa.
---

# odoo-restart-reminder

Po zmene zdrojákov je potrebné, aby používateľ ručne reštartoval/aktualizoval Odoo.
**Agent to nesmie robiť automaticky** (aby používateľ mal kontrolu nad reštartom
a logmi a aby sa neprerušila prebiehajúca práca).

## Kedy upozorniť a čo navrhnúť

| Typ zmeny | Odporúčaný príkaz | Poznámka |
|---|---|---|
| Python kód (`*.py`) | `make odoo` alebo `odoo --dev reload` | `--dev reload` zachytí zmeny bez reštartu |
| Manifest (`__manifest__.py`), models s novými poľami, security, data, views | `odoo -u <module>` | Trigger upgrade modulu (DB migrácia + reload views) |
| Viacero modulov | `odoo -u module_a,module_b` | Čiarkami oddelený zoznam |
| Konkrétna DB | `odoo -d <db> -u <module>` | Východzia DB je `odoo` |
| Nový modul (prvá inštalácia) | Apps → Update Apps List → Install | Cez UI; alebo `odoo -i <module>` |

## Formulácia upozornenia

Štandardná veta na koniec úlohy:

> Zmeny si vyžadujú reštart/upgrade Odoo. Spusti prosím **ručne**:
> `odoo -u <moduly>` (a voliteľne `-d <db>` ak nepoužívaš východziu `odoo`).

## Anti-pattern

- ❌ Nespúšťaj `odoo …` cez `launch-process` ani v žiadnom skripte v rámci automatickej úlohy.
- ❌ Nereštartuj systémd službu `odoo.service`.
- ❌ Nepoužívaj `pkill odoo` ani `kill -HUP`.
