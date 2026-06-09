---
name: psql-inspect
description: Skúmanie štruktúry a obsahu Odoo PostgreSQL databázy cez `psql` v devcontaineri. Použi keď potrebuješ overiť existenciu tabuľky, stĺpcov, alebo načítať skutočné dáta zo živej databázy.
---

# psql-inspect

Devcontainer má PostgreSQL prístup na hoste `db`, používateľ `odoo`, heslo `odoo`,
databáza `odoo`. Skratka cez `Makefile`: `make db-cli` (otvorí interaktívny `psql`).

## Bežné dopyty

```bash
# Zoznam všetkých tabuliek
PGPASSWORD=odoo psql -h db -U odoo -d odoo -c "\dt"

# Štruktúra konkrétnej tabuľky
PGPASSWORD=odoo psql -h db -U odoo -d odoo -c "\d res_users"

# Obsah tabuľky
PGPASSWORD=odoo psql -h db -U odoo -d odoo -c "SELECT id, login FROM res_users LIMIT 20"

# Hľadanie tabuliek podľa vzoru (napr. modul `stock`)
PGPASSWORD=odoo psql -h db -U odoo -d odoo -c "\dt stock_*"

# Zoznam stĺpcov tabuľky filtrovaný
PGPASSWORD=odoo psql -h db -U odoo -d odoo \
  -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='res_partner'"
```

## Konvencie

- **Nikdy** nepíš `UPDATE`/`DELETE`/`INSERT` priamo cez `psql`. Modifikuj dáta cez Odoo ORM
  (modul, demo data, `odoo shell`), nie cez surové SQL – aby sa zachovala konzistencia
  computed polí, ACL pravidiel a audit logu.
- Ak potrebuješ migráciu schémy, použi Odoo migračný framework v `<module>/migrations/<version>/`,
  nie ručné `ALTER TABLE`.
- Citlivé dáta (heslá, tokeny) nevypisuj do logov ani chat výstupu.

## Súvisiace

- Odoo shell: `make odoo-shell` (Python REPL s `env`)
- Makefile cieľ: `make db-cli`
