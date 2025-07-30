OGame Automation Bot
Automatyczny bot do zarządzania rozwojem planet w OGame: buduje kopalnie, infrastrukturę, badania i obronę na podstawie łatwo edytowalnego pliku konfiguracyjnego.

Wymagania

Python 3.8+ (polecany: 3.9, 3.10, 3.11)

Przeglądarka Google Chrome (najlepiej najnowsza)

Serwer OGame (np. s264-pl.ogame.gameforge.com)

Polecam środowisko virtualenv (opcjonalnie)

Narzędzia i zależności z pliku requirements.txt

Instalacja Pythona

macOS

Zainstaluj Homebrew jeśli jeszcze go nie masz:

text
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
Zainstaluj wybraną wersję Pythona (np. Python 3.10):

text
brew install python@3.10
Upewnij się, że ścieżka do Pythona jest w $PATH (jeśli masz kilka wersji):

text
echo 'export PATH="/opt/homebrew/opt/python@3.10/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
Sprawdź wersję:

text
python3 --version
Linux (Ubuntu/Debian)
Zainstaluj Pythona (przykład dla 3.10):

text
sudo apt update
sudo apt install python3.10 python3-pip
Sprawdź wersję:

text
python3 --version
Windows
Pobierz Python 3.10 i zainstaluj, zaznaczając opcję „Add Python to PATH”.

Sprawdź w PowerShellu:

powershell
python --version
Jeśli posiadasz wiele wersji, użyj:

powershell
py -3.10
Instalacja bibliotek bota
Pobierz repozytorium na swój komputer.

Zainstaluj wymagania:

text
pip3 install -r requirements.txt
Plik requirements.txt zawiera:

text
undetected-chromedriver
selenium
beautifulsoup4
(Opcjonalnie) Aktywuj wirtualne środowisko:

text
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
.\venv\Scripts\activate    # Windows
Jak używać bota
Wstaw własne współrzędne do config.json
Ustaw poziomy docelowe i pozycje przycisków do kliknięcia zgodnie z Twoim ekranem.

Uruchom z terminala/PowerShella (podaj swój link serwera OGame):

text
python3 ogame_bot.py --server https://s264-pl.ogame.gameforge.com
Po uruchomieniu zobaczysz przeglądarkę Chrome –
ZALOGUJ SIĘ RĘCZNIE na swoje konto OGame, wybierz serwer, kliknij „Play” i poczekaj na załadowanie widoku gry („page=ingame...” w URL).

Bot sam przełączy się na odpowiednią kartę i zacznie działać w pętli –
będzie klikał na wybrane przez Ciebie pozycje i budował jednostki zgodnie ze strategią w pliku config.json.

Aby zakończyć działanie, zamknij terminal lub przerwij program (Ctrl+C).

Własna konfiguracja
Zmień pozycje kliknięć i poziomy docelowe budynków/badań/obrony w pliku config.json.

Możesz rozbudować mapę obiektów (np. dodać nowe typy obrony czy badania), dopisując ich koszty i pozycje kliknięcia.

Przykładowy fragment config.json:

json
"click_coordinates": {
  "metal_mine": [380, 310],
  "crystal_mine": [480, 310],
  ...
},
"max_levels": {
  "metal": 10,
  "crystal": 10,
  "robotics": 5,
  ...
}
Najczęstsze problemy
Nie klika w żądane miejsce?
Popraw współrzędne kliknięć w config.json i upewnij się, że masz odpowiednią rozdzielczość okna przeglądarki!

Bot nie widzi gry?
Musisz samemu wejść do gry, bot przejmie ją dopiero po zalogowaniu.

Błąd z add_argument?
Upewnij się, że wszystkie opcje w selenium_client.py używają pojedynczego argumentu, np. opts.add_argument("--lang=pl-PL").

Uwaga / Bezpieczeństwo
Korzystanie z bota na własne ryzyko!
OGame oficjalnie zabrania automatyzacji, grozi tym banem. Bot nie gwarantuje 100% bezpieczeństwa — używasz go na własną odpowiedzialność.

Powodzenia!
Chcesz dodać niestandardową strategię lub obsługę innych obiektów — otwórz issue lub pull request w repozytorium.
