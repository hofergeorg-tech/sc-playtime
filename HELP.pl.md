# SC Playtime – Pomoc

🇩🇪 [Deutsch](HILFE.md) · 🇬🇧 [English](HELP.md) · 🇫🇷 [Français](HELP.fr.md) · 🇪🇸 [Español](HELP.es.md) · 🇮🇹 [Italiano](HELP.it.md) · 🇨🇳 [简体中文](HELP.zh.md)

SC Playtime to mała nakładka, która liczy, jak długo grasz w Star Citizen (lub inne gry).
Wyświetla się jako wąski panel nad grą i pokazuje bieżącą sesję oraz twoje statystyki.
Działa w systemach **Windows** i **Linux**.

- [Instalacja i uruchomienie](#instalacja-i-uruchomienie)
- [Nakładka](#nakładka)
- [Obsługa myszą](#obsługa-myszą)
- [Menu](#menu)
- [Kolory](#kolory)
- [Język](#język)
- [Kilka gier](#kilka-gier)
- [Kanały (LIVE, PTU, …)](#kanały-live-ptu-)
- [Analiza (mapa cieplna, przebieg dnia, patche)](#analiza-mapa-cieplna-przebieg-dnia-patche)
- [Edycja sesji](#edycja-sesji)
- [Wykrywanie AFK](#wykrywanie-afk)
- [Skróty klawiszowe](#skróty-klawiszowe)
- [Eksport i kopie zapasowe](#eksport-i-kopie-zapasowe)
- [Jak liczony jest czas](#jak-liczony-jest-czas)
- [Aktualizacje](#aktualizacje)
- [Linux](#linux)
- [Twoje dane](#twoje-dane)
- [Częste pytania](#częste-pytania)

---

## Instalacja i uruchomienie

**Windows:** pobierz `SC-Playtime.exe` ze
[strony wydań](https://github.com/hofergeorg-tech/sc-playtime/releases/latest), umieść go
we własnym folderze (np. `Dokumenty\SC-Playtime`) i uruchom. Instalacja nie jest
potrzebna; ikona w zasobniku (zegar w ramce) pojawia się w prawym dolnym rogu paska
zadań.

**Linux:** zobacz [Linux](#linux).

**Z kodu źródłowego (Windows):**

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\pythonw.exe run.pyw
```

Działa zawsze tylko jedna instancja. Drugie uruchomienie (np. autostart plus ręczne
uruchomienie) od razu się kończy, żeby nic nie zostało policzone podwójnie.

> **Ważne:** Star Citizen musi działać w trybie **„Okno bez ramki”**. W wyłącznym trybie
> pełnoekranowym żadna nakładka nie może się nad nim wyświetlić – dotyczy to wszystkich
> nakładek.

## Nakładka

### Widok kompaktowy

| Element | Znaczenie |
| --- | --- |
| Kropka w lewym górnym rogu | pulsuje na zielono, gdy gra działa; żółta przy AFK; szara offline |
| Nazwa gry | wyświetlana gra, obok kanał (np. **LIVE**) |
| **W GRZE** / **AFK** / **OFFLINE** | stan w prawym górnym rogu (AFK: zobacz [Wykrywanie AFK](#wykrywanie-afk)) |
| Duży zegar | długość bieżącej sesji; offline długość ostatniej sesji |
| DZIŚ / TYDZIEŃ | czas gry dzisiaj i od poniedziałku tego tygodnia |

### Rozwinięte statystyki

Kliknięcie nagłówka nakładki rozwija lub zwija statystyki.

- **Filtr kanału** (WSZYSTKIE, LIVE, PTU, …): pokazuje statystyki jednego kanału albo
  wszystkich razem. Pojawia się, gdy zapisano sesje z kanałem.
- **Kafelki:**

  | Kafelek | Znaczenie |
  | --- | --- |
  | DZIŚ | czas gry od północy |
  | TYDZIEŃ | od poniedziałku 0:00 |
  | MIESIĄC | od 1. dnia miesiąca |
  | ROK | od 1 stycznia |
  | ŁĄCZNIE | wszystko, co kiedykolwiek zapisano; w prawym górnym rogu data pierwszego zapisu (od kiedy liczy) |
  | SERIA | kolejne dni z co najmniej 1 minutą gry. Jeśli dziś jeszcze nie grałeś, seria się nie przerywa. |

- **Wykres** z zakładkami:

  | Zakładka | pokazuje |
  | --- | --- |
  | DZIEŃ | ostatnie 14 dni |
  | TYDZIEŃ | ostatnie 12 tygodni |
  | MIESIĄC | ostatnie 12 miesięcy |
  | ROK | ostatnie 5 lat |
  | ŁĄCZNIE | każdy rok od twojej pierwszej sesji |

  Bieżący okres jest wyróżniony na zielono. Po najechaniu myszą na słupek na dole widać
  dokładny okres i czas gry.

  **Przewijanie wstecz** (DZIEŃ, TYDZIEŃ, MIESIĄC): strzałki ‹ › w prawym górnym rogu
  wykresu przeskakują o pół wykresu w przeszłość lub z powrotem w stronę dziś. **Kółkiem
  myszy** nad wykresem przewijasz krok po kroku (w górę = starsze). Nie da się cofnąć
  dalej niż do pierwszej sesji. Zmiana zakładki lub filtra wraca do dziś.

  Przy aktywnym filtrze kanału (np. PTU) kolorowe słupki pokazują tylko ten kanał. Za
  nimi na szaro widać sumę wszystkich kanałów, a skala pozostaje taka jak przy
  „WSZYSTKIE” – od razu widać, jaki udział ma kanał. Po najechaniu pojawia się np.
  „PTU 6m / 11h 31m”.
- **Stopka:** liczba sesji, średnia i najdłuższa sesja (sesje krótsze niż 1 minuta nie
  są tu liczone).

## Obsługa myszą

| Działanie | Efekt |
| --- | --- |
| Kliknięcie nagłówka | rozwinięcie/zwinięcie statystyk |
| Przeciąganie lewym przyciskiem | przesuwanie nakładki (chyba że włączone jest „Zablokuj pozycję”) |
| Kliknięcie kanału | ustawienie filtra kanału |
| Kliknięcie zakładki | zmiana okresu wykresu |
| Kliknięcie ‹ / › na wykresie | wstecz / naprzód |
| Kółko myszy nad wykresem | jeden okres wstecz (w górę) lub naprzód (w dół) |
| Najechanie na słupek | dokładne wartości w stopce |
| Prawy przycisk na nakładce | menu |
| Lewy przycisk na ikonie w zasobniku | pokazanie/ukrycie nakładki |
| Prawy przycisk na ikonie w zasobniku | menu (także gdy nakładka jest ukryta) |

Pozycja, stan rozwinięcia, wybrana zakładka i filtr są zapisywane i przywracane przy
następnym uruchomieniu.

## Menu

| Pozycja | Funkcja |
| --- | --- |
| Pokaż/Ukryj nakładkę | tylko w menu zasobnika |
| Pokaż statystyki | jak kliknięcie nagłówka |
| Gra | wybór wyświetlanej gry, dodawanie i usuwanie gier |
| Analiza … | mapa cieplna, przebieg dnia i czas gry według patcha, zobacz [Analiza](#analiza-mapa-cieplna-przebieg-dnia-patche) |
| Edytuj sesje … | poprawianie lub usuwanie sesji, zobacz [Edycja sesji](#edycja-sesji) |
| TŁO (suwak) | przezroczystość tylko ciemnego tła; tekst pozostaje w pełni widoczny |
| PRZEZROCZYSTOŚĆ CAŁOŚCI (suwak) | przezroczystość całej nakładki (20–100 %) |
| Kolory | zobacz [Kolory](#kolory) |
| Język | zobacz [Język](#język) |
| Zablokuj pozycję | nakładki nie da się już przesunąć |
| Przepuszczaj kliknięcia | kliknięcia przechodzą przez nakładkę do gry. Wyłączyć można to tylko przez **ikonę w zasobniku** lub [skrót](#skróty-klawiszowe). |
| Pokazuj tylko, gdy gra jest uruchomiona | nakładka sama się ukrywa, gdy nie grasz |
| Wykrywanie AFK | nie liczyć czasu bez aktywności, zobacz [Wykrywanie AFK](#wykrywanie-afk) |
| Skróty klawiszowe … | globalne klawisze do pokazywania/ukrywania, zobacz [Skróty klawiszowe](#skróty-klawiszowe) |
| Uruchamiaj z Windows / Uruchamiaj po zalogowaniu | autostart po zalogowaniu (bez uprawnień administratora) |
| Pomoc … | ta pomoc |
| Co nowego? … | lista zmian w każdej wersji |
| O programie SC Playtime … | wersja, linki, licencja i przycisk darowizny (PayPal) |
| Sprawdź aktualizacje | od razu sprawdzić na GitHubie, zobacz [Aktualizacje](#aktualizacje) |
| Automatycznie sprawdzaj aktualizacje | przy starcie i co 12 godzin (domyślnie: włączone) |
| ⬆ Zainstaluj aktualizację … | pojawia się na samej górze, gdy jest nowa wersja |
| Dane | eksport CSV/JSON, kopie zapasowe, sesje z innego komputera, folder danych, zobacz [Eksport i kopie zapasowe](#eksport-i-kopie-zapasowe) |
| Zakończ | zamknięcie nakładki; bieżąca sesja jest najpierw zapisywana |

## Kolory

**Menu → Kolory** ma dwie części. Każda zawiera gotowe zestawy oraz „Wybierz kolor tła …”
i „Wybierz kolor tekstu …”.

**Kafelki statystyk (w grze)** – offline kafelki są zawsze ciemne w stylu HUD. Gdy gra
działa, zostają pokolorowane:

- Zielony / Ciemny (domyślnie)
- Cyjan / Ciemny
- Bursztynowy / Ciemny
- Bez koloru (HUD) – kafelki pozostają ciemne także w grze

**Aktywny kanał** – wybrany kanał (w nagłówku i w filtrze):

- Automatycznie (kolor kanału, ciemny tekst) – LIVE zielony, PTU żółty, …
- Ciemnozielony / Biały, Czarny / Zielony, Granatowy / Biały, Biały / Czarny

Wskazówka: dla dobrej czytelności łącz jasne tło z ciemnym tekstem i odwrotnie.

## Język

**Menu → Język** (z flagą) oferuje:

- **Automatycznie (system)** – domyślnie; język systemu operacyjnego, jeśli jest
  obsługiwany, w przeciwnym razie angielski
- 🇩🇪 **Deutsch**
- 🇬🇧 **English**
- 🇫🇷 **Français**, 🇪🇸 **Español**, 🇮🇹 **Italiano**, 🇵🇱 **Polski**, 🇨🇳 **简体中文**

Zmiana działa od razu na nakładkę, menu, komunikaty, pomoc i „Co nowego?” – pomoc i lista
zmian są dostępne we wszystkich siedmiu językach.

## Kilka gier

Domyślnie śledzony jest `StarCitizen.exe`. Aby dodać kolejne gry:

1. Prawy przycisk → **Gra → Dodaj grę …**
2. Wybierz program gry (Windows: plik `.exe`; Linux: zobacz niżej).
3. Wpisz wyświetlaną nazwę.

Gra jest rozpoznawana po nazwie programu. Gdy gra działa, nakładka pokazuje ją
automatycznie; gdy działa kilka, tę wybraną w menu. **Usuń grę** kończy jej śledzenie –
dotychczasowe sesje pozostają zapisane.

## Kanały (LIVE, PTU, …)

Kanał jest odczytywany z folderu instalacji:

```
…\StarCitizen\LIVE\Bin64\StarCitizen.exe   →  LIVE
…\StarCitizen\PTU\Bin64\StarCitizen.exe    →  PTU
```

Podobnie EPTU, HOTFIX i TECH-PREVIEW. Każda sesja pamięta swój kanał, dzięki czemu
statystyki można pokazać osobno dla kanału lub łącznie („WSZYSTKIE”).

## Analiza (mapa cieplna, przebieg dnia, patche)

**Menu → Analiza …** otwiera okno dla wyświetlanej gry i wybranego filtra kanału:

- **Kiedy grasz?** – mapa cieplna z dniami tygodnia w wierszach i 24 godzinami w
  kolumnach. Im jaśniejsze pole, tym więcej grałeś o tej porze. Najechanie na pole
  pokazuje dokładny czas; pod spodem widać najczęstszy dzień i godzinę gry.
- **Przebieg dnia** – jeden dzień jako oś czasu od 0 do 24: każda sesja to słupek w
  kolorze jej kanału, przerwy to pauzy lub czas AFK. **Czerwony znacznik** na końcu sesji
  oznacza awarię, **żółty** rozłączenie z serwerem. Strzałkami ‹ › przechodzisz między
  dniami, w które grałeś; najechanie na słupek pokazuje godzinę, długość, kanał, patch i
  sposób zakończenia sesji.
- **Czas gry według patcha** – czas gry, udział, liczba sesji, **awarie**,
  **rozłączenia** i okres dla każdej wersji Star Citizen (np. 4.3.1). Przy awariach widać
  też ich częstość, np. „2 · co 6h 30m” – tak sprawdzisz, czy patch jest stabilniejszy od
  poprzedniego. Patch jest odczytywany na początku każdej sesji z `build_manifest.id` lub
  `Game.log` w folderze instalacji (np. `…\StarCitizen\LIVE\`). Sesje sprzed wersji 1.4 i
  gry bez tych plików pojawiają się jako „nieznany”.

### Awarie i rozłączenia z serwerem

Gdy Star Citizen się zamyka, SC Playtime odczytuje koniec pliku `Game.log` (tylko
odczyt):

| W logu | Znaczenie |
| --- | --- |
| `<SystemQuit>` z „Quit via console command” / „User closed the application” | **zamknięta** – sam zakończyłeś grę |
| `<SystemQuit>` z innym powodem, np. „Back-end services are unresponsive” | **rozłączenie z serwerem** – utracono połączenie z serwerem/backendem |
| brak linii `<SystemQuit>`, za to przekazanie do zbieracza awarii | **awaria** |

Starsze sesje są klasyfikowane przy uruchomieniu SC Playtime: Star Citizen przechowuje log
każdego uruchomienia w folderze `logbackups`, a właściwy log jest znajdowany po godzinie
zakończenia sesji. Nie da się sklasyfikować sesji bez logu, gier innych niż Star Citizen
ani sesji zakończonych pauzą AFK. Instalacja jest znajdowana automatycznie (domyślny folder
lub folder, z którego uruchomiono grę).

## Edycja sesji

**Menu → Edytuj sesje …** pokazuje wszystkie sesje wyświetlanej gry, najnowsze na górze.
Służy do poprawiania błędów, np. gdy komputer był uśpiony przy otwartej grze:

- Kolumna **Wynik** pokazuje, jak zakończyła się sesja: zamknięta, **awaria** (czerwona)
  lub **rozłączenie z serwerem** (żółte), zobacz
  [Awarie i rozłączenia z serwerem](#awarie-i-rozłączenia-z-serwerem).
- **Edytuj …** (lub dwuklik): zmiana początku i końca.
- **Usuń**: usunięcie jednej lub kilku zaznaczonych sesji (Ctrl/Shift do wyboru wielu).
  Nie da się tego cofnąć – w razie wątpliwości najpierw zrób
  [kopię](#eksport-i-kopie-zapasowe).

Bieżąca sesja (zielona, „trwa”) jest zablokowana do zamknięcia gry.

## Wykrywanie AFK

W **Menu → Wykrywanie AFK** można ustawić, by czas bez aktywności nie był liczony:
**Wyłączone** (domyślnie) albo pauza po **5, 10, 15 lub 30 minutach** bez klawiatury,
myszy lub kontrolera.

- Po upływie tego czasu sesja kończy się w chwili **ostatniego naciśnięcia klawisza** –
  sam czas oczekiwania też nie jest liczony. Nakładka pokazuje **AFK** z żółtą kropką.
- Gdy tylko znów pojawi się aktywność, a gra nadal działa, automatycznie zaczyna się nowa
  sesja.
- Liczy się każda aktywność na komputerze, nie tylko w grze.
- W Linuksie działa to pod X11/XWayland (biblioteka `libXss`); bez niej wykrywanie nie
  działa.

## Skróty klawiszowe

Globalne skróty działają wszędzie, także gdy gra jest na pierwszym planie (tylko
**Windows**):

| Domyślnie | Efekt |
| --- | --- |
| **Ctrl+Shift+F9** | pokazanie/ukrycie nakładki |
| **Ctrl+Shift+F11** | włączenie/wyłączenie „Przepuszczaj kliknięcia” |

Zmienisz je w **Menu → Skróty klawiszowe …**: kliknij pole, naciśnij nową kombinację,
wyczyść przyciskiem ✕ (= brak skrótu). Dozwolone są litery, cyfry, F1–F24,
Home/End/Insert/Delete, PgUp/PgDn, strzałki, Pause i Spacja – poza klawiszami F zawsze z
Ctrl, Shift, Alt lub Win. Jeśli kombinacja jest już zajęta przez inny program, pojawi się
komunikat.

## Eksport i kopie zapasowe

W **Menu → Dane**:

| Pozycja | Funkcja |
| --- | --- |
| Eksportuj jako CSV … | wszystkie sesje wszystkich gier jako tabela, np. do Excela (kolumny: gra, kanał, patch, początek, koniec, czas w sekundach i minutach, wynik `quit`/`crash`/`server`) |
| Eksportuj jako JSON … | to samo w JSON, czasy dodatkowo ze strefą czasową i jako znacznik czasu Unix |
| Utwórz kopię teraz | od razu utworzyć kopię bazy danych |
| Codzienna automatyczna kopia (7 dni) | jedna kopia dziennie; zostaje 7 ostatnich (domyślnie: włączone) |
| Otwórz folder kopii | folder `backups` w folderze danych |
| Importuj sesje z innego komputera … | dodanie czasu gry z drugiego komputera, zobacz niżej |
| Otwórz folder danych | folder z bazą danych i ustawieniami |

**Przywracanie kopii:** zamknij nakładkę, zastąp `playtime.db` w folderze danych wybranym
plikiem z `backups` (np. skopiuj `playtime-2026-10-04.db` i zmień nazwę na
`playtime.db`), uruchom nakładkę ponownie.

### Łączenie dwóch komputerów

Jeśli grasz na kilku komputerach, dodaj czas gry z drugiego komputera tak:

1. Na drugim komputerze weź plik `playtime.db` z folderu danych (lub kopię z `backups`),
   np. przez pendrive albo folder w chmurze.
2. Tutaj wybierz **Menu → Dane → Importuj sesje z innego komputera …** i wskaż plik.
3. SC Playtime pokaże, ile sesji jest nowych, a ile już istnieje, i po twoim
   potwierdzeniu zaimportuje tylko nowe. Najpierw tworzona jest kopia obecnych danych.

Sesja uznawana jest za „już istniejącą”, jeśli nakłada się w czasie na tutejszą sesję tej
samej gry – ta sama gra nie działa jednocześnie na dwóch komputerach. Dlatego ten sam plik
możesz później zaimportować ponownie i nic nie zostanie policzone podwójnie. Importowane są
też kanał, patch i wynik. Gry, których tu jeszcze nie ma, zostaną wymienione: ich sesje są
zapisane i pojawią się, gdy dodasz grę o tej samej nazwie.

## Jak liczony jest czas

- Lista procesów jest odczytywana co 2 sekundy. Jest tylko **odczytywana** – nic nie jest
  wstrzykiwane do gry.
- Jeśli uruchomisz nakładkę, gdy gra już działa, sesja i tak liczy się od faktycznego
  startu gry.
- Koniec sesji jest zapisywany co 30 sekund. Gdy komputer się zawiesi, przepada najwyżej
  te 30 sekund.
- Sesje przechodzące przez północ (lub granicę tygodnia/miesiąca) są dzielone
  proporcjonalnie.

## Aktualizacje

Bieżąca wersja jest widoczna na górze menu (np. „SC PLAYTIME 1.5.0”).

- **Automatycznie:** przy włączonym „Automatycznie sprawdzaj aktualizacje” SC Playtime
  sprawdza GitHub krótko po starcie, a potem co 12 godzin. Jeśli jest nowa wersja, przy
  ikonie w zasobniku pojawia się powiadomienie, a na górze menu pozycja
  **„⬆ Zainstaluj aktualizację …”**.
- **Ręcznie:** Menu → „Sprawdź aktualizacje”.
- **Instalacja:** po potwierdzeniu nowa wersja jest pobierana i porównywana z sumą
  kontrolną, którą GitHub podaje dla wydania – jeśli się nie zgadza, nic nie jest
  instalowane. Nakładka zapisuje bieżącą sesję, zamyka się, podmienia plik programu i
  uruchamia się ponownie. Potem raz wyświetla się „Co nowego?”. Ustawienia i czasy gry
  zostają zachowane.
- Jeśli SC Playtime działa z kodu źródłowego (`run.pyw`) zamiast jako gotowy program,
  „Zainstaluj” otwiera stronę wydań w przeglądarce – nie ma pliku programu do podmiany. Aby
  aktualizować jednym kliknięciem, używaj pliku EXE i wyłącz oraz włącz ponownie autostart
  w menu.

Wszystkie wersje są też dostępne pod adresem
<https://github.com/hofergeorg-tech/sc-playtime/releases>.

## Linux

**Gotowy program:** pobierz `SC-Playtime-linux-x86_64` ze
[strony wydań](https://github.com/hofergeorg-tech/sc-playtime/releases/latest), umieść go
np. w `~/Aplikacje/`, nadaj prawo wykonywania i uruchom:

```bash
chmod +x SC-Playtime-linux-x86_64
./SC-Playtime-linux-x86_64
```

**Z kodu źródłowego:**

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python run.pyw
```

Uwagi:

- **Star Citizen pod Wine/Proton/Lutris** jest wykrywany jak w Windows – razem z kanałem
  (LIVE, PTU, …), bo odczytywana jest też windowsowa ścieżka gry. Awarie i rozłączenia są
  wykrywane tylko w Windows.
- **Natywne gry linuksowe:** dodaj je przez „Dodaj grę …”, wybierając ich program (ustaw
  filtr na „Wszystkie pliki”). Są rozpoznawane po nazwie programu.
- **Wayland:** w Waylandzie okna nie mogą same wybrać pozycji ani pozostać na wierzchu.
  Dlatego SC Playtime uruchamia się automatycznie przez **XWayland**, dostępny na prawie
  wszystkich pulpitach. Aby wybrać inaczej, ustaw samodzielnie `QT_QPA_PLATFORM`.
- **Ikona w zasobniku w GNOME:** GNOME pokazuje ikony tylko z rozszerzeniem „AppIndicator
  and KStatusNotifierItem Support”. KDE, XFCE, Cinnamon i inne nic nie potrzebują.
- **Autostart** nazywa się w menu „Uruchamiaj po zalogowaniu” i tworzy
  `~/.config/autostart/sc-playtime.desktop`.
- **Dane** znajdują się w `~/.local/share/SC-Playtime/`.

## Twoje dane

Wszystko jest przechowywane lokalnie (Menu → „Otwórz folder danych”):

- Windows: `%APPDATA%\SC-Playtime\`
- Linux: `~/.local/share/SC-Playtime/`

| Plik | Zawartość |
| --- | --- |
| `playtime.db` | baza SQLite ze wszystkimi sesjami (gra, kanał, początek, koniec, patch, wynik) |
| `settings.json` | pozycja, przezroczystość, kolory, język, lista gier, znalezione foldery Star Citizen, … |
| `backups/` | codzienne kopie bazy danych, zobacz [Eksport i kopie zapasowe](#eksport-i-kopie-zapasowe) |

Twoje czasy gry i ustawienia nigdy nie opuszczają twojego komputera. Jedynym połączeniem
z Internetem jest sprawdzanie aktualizacji: pobiera ono tylko publiczne informacje o
wersjach z GitHuba i można je wyłączyć w menu. Aby zrobić kopię lub przenieść dane, po
prostu skopiuj folder. Aby zresetować ustawienia, usuń `settings.json` przy zamkniętej
nakładce.

## Częste pytania

**Nakładki nie widać w grze.**
Ustaw Star Citizen na „Okno bez ramki”. Sprawdź, czy nakładka nie została ukryta przez
ikonę w zasobniku.

**Nie mogę już kliknąć nakładki.**
Włączone jest „Przepuszczaj kliknięcia”. Naciśnij **Ctrl+Shift+F11** lub kliknij prawym
przyciskiem ikonę w zasobniku i odznacz opcję.

**Menu lub okno pojawia się za grą.**
Od wersji 1.4 menu i okna dialogowe są zawsze pokazywane przed nakładką i grą. Jeśli
okno mimo to jest zasłonięte, przełącz się na nie przez Alt+Tab.

**Czas gry jest błędny, bo zostawiłem grę otwartą.**
Popraw sesję w **Menu → Edytuj sesje …** i na przyszłość włącz
[wykrywanie AFK](#wykrywanie-afk).

**Nakładka zniknęła.**
Kliknięcie lewym przyciskiem ikony w zasobniku pokazuje ją ponownie. Przy włączonym
„Pokazuj tylko, gdy gra jest uruchomiona” nie pojawia się, gdy nie grasz.

**Autostart przestał działać.**
Wpis wskazuje na miejsce programu lub pliku `run.pyw`. Po przeniesieniu folderu wyłącz i
ponownie włącz autostart w menu.

**Aktualizacja się nie udaje.**
Sprawdź połączenie z Internetem i spróbuj ponownie przez „Sprawdź aktualizacje”. Jeśli
program leży w chronionym folderze (np. `C:\Program Files` lub `/usr/bin`), nie może się
sam podmienić – pobierz nową wersję ze strony wydań lub przenieś program do własnego
folderu.

**Windows wyświetla „System Windows ochronił ten komputer”.**
Plik EXE nie jest jeszcze podpisany cyfrowo (wniosek złożony, zobacz
[CODE_SIGNING.md](CODE_SIGNING.md)), dlatego SmartScreen ostrzega przy nowych pobraniach.
Kliknij „Więcej informacji” → „Uruchom mimo to”. Aby sprawdzić, czy plik naprawdę
zbudowano z tego repozytorium:
`gh attestation verify SC-Playtime.exe --repo hofergeorg-tech/sc-playtime`

**Czy to przeszkadza systemowi anti-cheat?**
SC Playtime odczytuje tylko listę procesów i czas uruchomienia gry zwykłymi funkcjami
systemu, tak jak Menedżer zadań, a po zamknięciu gry plik tekstowy `Game.log`. Nie ma
dostępu do gry.

**Sesja nie ma wyniku.**
W logu nie było ani normalnego zakończenia, ani awarii – np. gdy Star Citizen zamknięto
przez Menedżer zadań, zabrakło prądu, sesja zakończyła się pauzą AFK lub log już nie
istnieje. Klasyfikacja służy tylko statystykom i nie zmienia czasu gry.
