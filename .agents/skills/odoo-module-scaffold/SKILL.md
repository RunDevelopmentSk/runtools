---
name: odoo-module-scaffold
description: Vytvorenie nového Odoo modulu v `extra-addons/` podľa projektových konvencií. Použi keď máš pridať nový vlastný modul (nie rozšírenie existujúceho v rámci `run_wms` micro-modulov).
---

# odoo-module-scaffold

Postupuj iba ak je nová funkcionalita natoľko izolovaná, že nestačí ju pridať do
niektorého z existujúcich modulov (pozri `extra-addons/run_wms/__manifest__.py`).
Stratégia projektu je **vyhnúť sa programovaniu** – uprednostni konfiguráciu
existujúcich Odoo modulov.

## Štruktúra (vzor podľa `extra-addons/excise_tax`)

```
extra-addons/<module>/
  __init__.py                # from . import models
  __manifest__.py
  models/
    __init__.py
    <model>.py
  views/
    <model>_views.xml
  security/
    ir.model.access.csv
  i18n/                      # generuje Odoo (`odoo --i18n-export …`)
  tests/                     # voliteľné; pre projektové E2E pozri skill `e2e-testing`
```

## `__manifest__.py` šablóna

```python
{
    "name": "<Ľudský názov>",
    "version": "1.0",
    "description": """
<Krátky popis modulu.>
    """,
    "depends": [
        "base",
        # ďalšie závislosti
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/<model>_views.xml",
    ],
    "assets": {},
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}
```

## Checklist

- [ ] `__manifest__.py` s `depends`, `data`, `license`
- [ ] `security/ir.model.access.csv` ak modul definuje nový model
- [ ] Pridať modul do `extra-addons/run_wms/__manifest__.py` → `depends`, aby sa automaticky
      inštaloval ako súčasť WMS suity
- [ ] Po vytvorení/úprave: upozorni používateľa na `odoo -u <module>` (skill `odoo-restart-reminder`)
- [ ] Pridať implementačný popis do `docs/implementation-details/` (skill `add-implementation-doc`)

## Anti-pattern

- ❌ Nevytváraj modul pre triviálne rozšírenie existujúceho – pridaj to do `run_wms`.
- ❌ Nedotvor `vendor-addons/` priamo (tie sú externé, nemodifikuj ich).
- ❌ Nepoužívaj `auto_install: True` bez konzultácie – modul sa inštaluje sám pri matchnutí
  všetkých `depends`, čo môže byť nečakané.
