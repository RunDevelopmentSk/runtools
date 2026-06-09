---
name: e2e-testing
description: Spúšťanie a tvorba end-to-end testov projektu (Playwright + pytest + Odoo RPC). Použi keď máš pridať/upraviť E2E test, alebo overiť existujúce testy po zmene funkcionality.
---

# e2e-testing

Projekt má vyše 270 E2E testov, ktoré bežia oproti **živej Odoo 19 inštancii** v Dockeri,
nie oproti mockom.

## Povinné čítanie pred generovaním testov

- [`tests/e2e/AGENT_GUIDE.md`](../../../tests/e2e/AGENT_GUIDE.md) – záväzné pravidlá pre AI agentov
  (žiadne hardcoded ID, vždy docstring, `pytest.skip()` namiesto fail, copy-paste šablóny, …)
- [`docs/e2e-testing-guide.md`](../../../docs/e2e-testing-guide.md) – prehľadová dokumentácia
- [`tests/e2e/README.md`](../../../tests/e2e/README.md) – operačný README (markery, env premenné, profily)
- [`tests/e2e/odoo_e2e/E2E_GUIDE.md`](../../../tests/e2e/odoo_e2e/E2E_GUIDE.md) – framework fixtures referencia

## Spúšťanie cez Makefile

| Cieľ | Význam |
|---|---|
| `make e2e` | Spusti všetky E2E testy (auto-setup pri prvom behu) |
| `make e2e-fresh` | Drop + recreate DB a spusti testy nanovo |
| `make e2e-setup` | Iba pripraviť venv + Playwright |
| `make e2e-excise` | Iba excise testy (`02_excise/`) |
| `make e2e-purchase` | Iba purchase testy (`01_purchase/`) |
| `make e2e-docker-start` | Spustí samostatný E2E Docker stack + Odoo |
| `make e2e-docker-stop` | Zastaví E2E Docker stack |

## Štruktúra fáz

Testy sú rozdelené do očíslovaných fáz (`00_infrastructure`, `01_purchase`,
`02_excise`, `03_stock`, `04_eshop`, `05_reports`). Závislosti medzi fázami sú
riešené **gate súbormi** – nikdy nepreskakuj `00_infrastructure`, ak gate ešte nepadol.

## Anti-pattern

- ❌ Nehardcoduj ID záznamov (`partner_id = 17`) – vyhľadávaj cez xmlid alebo doménu.
- ❌ Nepoužívaj `assert False` – použi `pytest.skip("…")` s vysvetlením.
- ❌ Nemodifikuj `tests/e2e/odoo_e2e/` (vendored framework) bez vedomia.
