# ASTEK ING Cookies Task Solution

Repozytorium zawiera zautomatyzowany test weryfikujący wybranie analitycznych ciasteczek.
W tym celu użyty został język Python oraz framework Playwright, a także biblioteka PyTest w celu łatwiejszego uruchamiania testów (jeśli pojawiłoby się ich w przyszłości więcej).

## Wymagania

- Python 3.8+
- pip

## Instalacja

```bash
git clone https://github.com/twoj-login/ing-cookie-test.git
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
Przy próbie puszczania testów z CI/CD napotkałem na problem, że wyświetla się hCaptcha, której nie potrafiłem obejść. Próbowałem wieloma sposobami, niestety z marnym skutkiem. Nie sprawdzałem płatnych rozwiązań, ponieważ nigdy takowych nie używałem i nie chciałem wtopić pieniędzy w coś co nie będzie działało jak należy.
