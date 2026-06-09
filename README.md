# runtools

Pomocné Python skripty pre projekty RunDevelopment. Po inštalácii sú
k dispozícii ako konzolové príkazy:

- `dockerinfo` – prehľad Docker images, kontajnerov, volumes a build cache
- `gitexport` – export zmien z Git repozitára
- `gitmirror` – zrkadlenie Git repozitára do iného repozitára

## Inštalácia

### Z konzoly

```bash
python -m pip install "runtools @ git+ssh://git@github.com/RunDevelopmentSk/runtools.git@main"
```

### Cez `requirements.txt`

Pridaj do `requirements.txt`:

```
runtools @ git+ssh://git@github.com/RunDevelopmentSk/runtools.git@main
```

a nainštaluj:

```bash
python -m pip install -r requirements.txt
```

## Aktualizácia

Keďže inštalácia ide vždy z vetvy `main` (bez verzovania), pip pri opätovnom
spustení `install` nemusí zaznamenať zmenu commit hashu. Pre aktualizáciu na
najnovší stav `main` pridaj `--upgrade --force-reinstall`:

```bash
python -m pip install --upgrade --force-reinstall \
    "runtools @ git+ssh://git@github.com/RunDevelopmentSk/runtools.git@main"
```

Pri inštalácii z `requirements.txt`:

```bash
python -m pip install --upgrade --force-reinstall -r requirements.txt
```
