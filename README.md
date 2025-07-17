# ASTEK ING Cookies Task Solution

Repozytorium zawiera zautomatyzowany test weryfikujący wybranie analitycznych ciasteczek.
W tym celu użyty został język Python oraz framework Playwright, a także biblioteka PyTest w celu łatwiejszego uruchamiania testów (jeśli pojawiłoby się ich w przyszłości więcej).

## Wymagania

- Python 3.8+
- pip

## Instalacja

```bash
git clone https://github.com/Zeimdall/astek-ing-task.git
cd ing-cookie-test
pip install -r requirements.txt
playwright install
```

## Uruchomienie testu
W celu uruchomienia testu lokalnie trzeba wykonać powyższe kroki a natępnie użyć polecenia:
```bash
pytest
```

## Puszczanie testów w CI
Specjalnie przygotowany plik yaml o nazwie playwright-ci.yml, który jest pod tą ścieżką: `.github/workflows/playwright-ci.yml` zawiera wszystko co potrzebne w celu uruchomienia testu.


## Problem z hCaptcha
❗️Uwaga: Ze względu na zabezpieczenia (Incapsula/hCaptcha), test może nie działać w środowiskach CI/CD bez odpowiedniego proxy lub storage_state.
