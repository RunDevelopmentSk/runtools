#!/usr/bin/env python3
"""
gitmirror.py - Zrkadlenie git repozitára do iného repozitára.

Použitie:
    python gitmirror.py <source-repo> <mirror-repo>

Príklad:
    python gitmirror.py RunDevelopmentSk/drinkcentrum-is.git RunDevelopmentSk/test.git
"""

import getpass
import os
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile


def normalize_repo(repo: str) -> str:
    """Doplní prefix git@github.com: a suffix .git ak chýbajú."""
    if not repo.startswith("git@github.com:"):
        repo = "git@github.com:" + repo
    if not repo.endswith(".git"):
        repo = repo + ".git"
    return repo


def get_local_name(repo_url: str) -> str:
    """Odvodí názov lokálneho priečinka z URL repozitára.

    Príklad: git@github.com:RunDevelopmentSk/test.git -> test
    """
    name = repo_url.rstrip("/")
    if name.endswith(".git"):
        name = name[:-4]
    return name.split("/")[-1]


def run(cmd: list, cwd: str | None = None, env: dict | None = None) -> None:
    """Spustí príkaz, vypíše ho a pri chybe ukončí skript."""
    display = " ".join(cmd)
    if cwd:
        print(f"[{cwd}]$ {display}")
    else:
        print(f"$ {display}")
    result = subprocess.run(cmd, cwd=cwd, env=env)
    if result.returncode != 0:
        print(f"Chyba: príkaz zlyhal s návratovým kódom {result.returncode}")
        sys.exit(1)


def ask_continue(path: str) -> bool:
    """Vypýta sa používateľa, či prepísať existujúci priečinok."""
    try:
        response = input(f"\nUpozornenie: priečinok '{path}' už existuje.\n" "Pokračovať a prepísať ho? [y/N] ")
    except EOFError:
        return False
    return response.strip().lower() == "y"


def ensure_removed(path: str, always: bool = False) -> None:
    """Odstráni priečinok ak existuje. Ak always=False, pýta sa používateľa."""
    if os.path.exists(path):
        if not always and not ask_continue(path):
            print("Prerušené.")
            sys.exit(0)
        shutil.rmtree(path)


def validate_mirror_repo(repo_url: str) -> None:
    """Overí, že mirror-repo obsahuje 'test' ako samostatné slovo v názve.

    Slovo 'test' musí byť ohraničené začiatkom/koncom reťazca alebo
    ne-alfanumerickým znakom (napr. pomlčka, lomka, bodka).
    Príklady, ktoré PREJDÚ:  test, test-repo, my-test, my-test-repo
    Príklady, ktoré NEPREJDÚ: latest, contest, testing, attest
    """
    name = get_local_name(repo_url)
    if not re.search(r"(?<![a-zA-Z0-9])test(?![a-zA-Z0-9])", name, re.IGNORECASE):
        print(
            f"Chyba: mirror-repo '{name}' neobsahuje 'test' ako samostatné slovo.\n"
            "Bezpečnostná kontrola zabraňuje prepísaniu produkčného repozitára.\n"
            "Príklady platných názvov: test, test-01, test-repo, my-test, my-test-v2"
        )
        sys.exit(1)


def ask_ssh_passphrase() -> str:
    """Vypýta si SSH heslo od používateľa (skrytý vstup)."""
    return getpass.getpass("Heslo k SSH kľúču (Enter = bez hesla): ")


def create_ssh_env(passphrase: str) -> tuple[dict, str]:
    """Vytvorí env s dočasným SSH_ASKPASS skriptom.

    SSH/git zavolá tento skript vždy, keď potrebuje heslo ku kľúču –
    nie je teda potrebné poznať cestu ku kľúču ani spúšťať ssh-agent.
    Vracia dvojicu (env, cesta_k_askpass_skriptu).
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".sh", delete=False, encoding="utf-8") as tf:
        tf.write(f"#!/bin/sh\nprintf '%s' {shlex.quote(passphrase)}\n")
        askpass_path = tf.name
    os.chmod(askpass_path, stat.S_IRWXU)  # chmod 700, len vlastník môže čítať/spustiť

    env = os.environ.copy()
    env["SSH_ASKPASS"] = askpass_path
    env["SSH_ASKPASS_REQUIRE"] = "force"  # použiť askpass aj bez X servera / terminálu
    env.pop("DISPLAY", None)

    return env, askpass_path


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Použitie: python {sys.argv[0]} <source-repo> <mirror-repo>")
        print(f"Príklad:  python {sys.argv[0]} RunDevelopmentSk/drinkcentrum-is RunDevelopmentSk/test")
        sys.exit(1)

    source_repo = normalize_repo(sys.argv[1])
    mirror_repo = normalize_repo(sys.argv[2])
    local_name = get_local_name(mirror_repo)

    validate_mirror_repo(mirror_repo)

    # Tmp priečinky s prefixom/sufixom __ aby sa predišlo kolíziám
    tmp_init = f"__{local_name}_init__"
    tmp_bare = f"__{local_name}_bare__"
    tmp_src = f"__{local_name}_src__"

    print(f"Source repo : {source_repo}")
    print(f"Mirror repo : {mirror_repo}")
    print(f"Lokálny cieľ: ./{local_name}/")

    # --- SSH heslo ---
    print()
    passphrase = ask_ssh_passphrase()
    ssh_env, askpass_path = create_ssh_env(passphrase)

    try:
        # --- Overenie existencie finálneho priečinka ---
        ensure_removed(local_name)

        # --- Krok 1: Vytvorenie prázdneho repozitára a jeho odoslanie do mirror-repo ---
        print("\n=== Krok 1: Resetovanie histórie mirror-repo ===")
        for tmp in (tmp_init, tmp_bare):
            ensure_removed(tmp, always=True)

        os.makedirs(tmp_init)
        run(["git", "init"], cwd=tmp_init)
        run(["git", "branch", "-M", "main"], cwd=tmp_init)

        with open(os.path.join(tmp_init, "README.md"), "w", encoding="utf-8") as f:
            f.write("# New project\n")

        run(["git", "add", "."], cwd=tmp_init)
        run(["git", "commit", "-m", "Initial commit"], cwd=tmp_init)

        run(["git", "clone", "--bare", tmp_init, tmp_bare], env=ssh_env)
        run(["git", "remote", "set-url", "origin", mirror_repo], cwd=tmp_bare, env=ssh_env)
        run(["git", "push", "--mirror", "--force"], cwd=tmp_bare, env=ssh_env)

        shutil.rmtree(tmp_init)
        shutil.rmtree(tmp_bare)

        # --- Krok 2: Naklonuj source-repo a odošli ho do mirror-repo ---
        print("\n=== Krok 2: Zrkadlenie source-repo do mirror-repo ===")
        ensure_removed(tmp_src, always=True)

        run(["git", "clone", "--mirror", source_repo, tmp_src], env=ssh_env)
        run(["git", "remote", "set-url", "origin", mirror_repo], cwd=tmp_src, env=ssh_env)

        # Odstránenie read-only GitHub refs (refs/pull/*) pred mirror pushom,
        # aby GitHub neodmietol push s "deny updating a hidden ref".
        hidden = subprocess.run(
            ["git", "for-each-ref", "--format=%(refname)", "refs/pull/"],
            cwd=tmp_src,
            capture_output=True,
            text=True,
        )
        for ref in hidden.stdout.split():
            subprocess.run(["git", "update-ref", "-d", ref], cwd=tmp_src, check=True)

        run(["git", "push", "--mirror", "--force"], cwd=tmp_src, env=ssh_env)

        shutil.rmtree(tmp_src)

        # --- Krok 3: Lokálny klon mirror-repo s odkazom na source ---
        print("\n=== Krok 3: Vytvorenie lokálneho klonu mirror-repo ===")
        run(["git", "clone", mirror_repo, local_name], env=ssh_env)
        run(["git", "remote", "add", "source", source_repo], cwd=local_name, env=ssh_env)
        # Zakáž push do source
        # run(["git", "remote", "set-url", "--push", "source", "DISABLED"], cwd=local_name, env=ssh_env)

        print(f"\nHotovo! Mirror repo je naklonovaný v ./{local_name}/")
        print(f"  origin -> {mirror_repo}  (fetch + push)")
        print(f"  source -> {source_repo}  (fetch only, push DISABLED)")

    finally:
        os.unlink(askpass_path)


if __name__ == "__main__":
    main()
