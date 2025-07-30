OGame Automation Bot
Automatyczny bot do zarządzania rozwojem planet w OGame.
Buduje kopalnie, infrastrukturę, badania i obronę według konfiguracji.

Wymagania
Python ≥ 3.8 (rekomendowany 3.9–3.11)

Google Chrome (najnowsza wersja)

Zainstalowane biblioteki (wymienione w requirements.txt)

Instalacja



macOS


Zainstaluj Homebrew (jeśli jeszcze nie masz):


bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
Zainstaluj Pythona (np. 3.10):


bash
brew install python@3.10
Dodaj Pythona do PATH:


bash
echo 'export PATH="/opt/homebrew/opt/python@3.10/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
Sprawdź wersję poleceniem:


bash
python3 --version
Linux (Ubuntu/Debian)
Zainstaluj Pythona:


bash
sudo apt update
sudo apt install python3 python3-pip
Sprawdź wersję:


bash
python3 --version
Windows
Pobierz instalator z python.org


Podczas instalacji zaznacz opcję „Add Python to PATH”


Sprawdź wersję:


powershell
python --version
Instalacja zależności
W katalogu projektu (tam gdzie jest requirements.txt) uruchom:


bash
pip install -r requirements.txt
Zawartość requirements.txt:


text
undetected-chromedriver
selenium
beautifulsoup4
Ustawienia gry i konfiguracji
Skonfiguruj plik config.json zgodnie z własną rozdzielczością i pozycjami klikanych elementów.


Przykładowe fragmenty config.json:


json
{
  "screen_width": 1366,
  "screen_height": 768,
  "click_coordinates": {
    "metal_mine": [380, 310],
    "crystal_mine": [480, 310],
    "deuterium_mine": [580, 310],
    "robotics": [300, 600],
    "nanite_factory": [400, 600],
    "shipyard": [500, 600]
  },
  "max_levels": {
    "metal": 10,
    "crystal": 10,
    "deuterium": 8,
    "robotics": 4,
    "nanite_factory": 1,
    "shipyard": 3
  }
}


Uruchomienie bota


Uruchom skrypt:


bash
python3 ogame_bot.py --server https://sXNN.en.ogame.gameforge.com
Zastąp sXNN odpowiednim serwerem.


Jak działa bot
Bot otwiera przeglądarkę Chrome i pozwala na ręczne zalogowanie.


Po wykryciu gry przejmuje kartę z rozgrywką.


W pętli cyklicznie:


Sprawdza, czy coś jest w trakcie budowy.

Jeśli nie, podejmuje działania zgodnie z konfiguracją (budowa kopalni, badania itd.).

Klikania są realizowane jako symulowane kliknięcia JavaScript na pozycjach wskazanych w config.json.

Po każdym działaniu bot robi przerwę dopasowaną do obecnego statusu (dłużej jeśli trwa budowa).

Bezpieczeństwo i uwagi
Korzystasz na własną odpowiedzialność.

Oficjalny regulamin OGame zabrania stosowania botów, użycie automatyzacji grozi banem.

Uruchamiaj bota ostrożnie i nie pozostawiaj go bez nadzoru.

Wsparcie i rozwój
Pytania i problemy zgłaszaj na Issues GitHub.

Kontrybucje do rozwoju mile widziane.

Dokumentację i konfigurację można rozwijać.

Dziękuję za korzystanie z bota i życzę powodzenia!
