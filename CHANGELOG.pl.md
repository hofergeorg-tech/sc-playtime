# Lista zmian

🇩🇪 [Deutsch](CHANGELOG.md) · 🇬🇧 [English](CHANGELOG.en.md) · 🇫🇷 [Français](CHANGELOG.fr.md) · 🇪🇸 [Español](CHANGELOG.es.md) · 🇮🇹 [Italiano](CHANGELOG.it.md) · 🇨🇳 [简体中文](CHANGELOG.zh.md)

Wszystkie istotne zmiany w SC Playtime. Format oparty na
[Keep a Changelog](https://keepachangelog.com/pl/1.1.0/).

## [1.6.0] – 2026-10-17

### Nowości
- **Anty-AFK** (Windows): Menu → Anty-AFK utrzymuje Star Citizen w gotowości. Naciska w rytmie
  klawisz na prawo od P (domyślnie co 5 s) i/lub porusza myszą według małego wzoru (prawo–lewo,
  góra–dół, kwadrat, koło, losowo; zasięg, tempo i rytm do ustawienia). Wysyłane są prawdziwe
  scancode'y – tylko gdy gra jest na pierwszym planie. Włączanie w menu lub **Ctrl+Shift+F12**;
  pierścienie obok zegara pokazują rytm i przełączają akcję kliknięciem. Jego akcje nie liczą
  się do wykrywania AFK.

## [1.5.0] – 2026-10-09

### Nowości
- **Awarie i rozłączenia z serwerem według patcha:** po zamknięciu gry SC Playtime
  odczytuje `Game.log` Star Citizen i zapamiętuje, czy sam zakończyłeś grę, czy nastąpiła
  awaria, czy serwer zerwał połączenie. Analiza pokazuje według patcha awarie (np.
  „2 · co 6h 30m”) i rozłączenia, okno sesji – kolumnę „Wynik”. Starsze sesje są
  klasyfikowane przy uruchomieniu na podstawie zapisanych logów (`logbackups`).
- **Przebieg dnia** w analizie: jeden dzień jako oś czasu od 0 do 24 ze wszystkimi sesjami
  w kolorze ich kanału, przerwy jako luki, awaria (czerwona) i rozłączenie (żółte) jako
  znaczniki; strzałkami ‹ › przechodzi się między dniami, w które grałeś.
- **Łączenie dwóch komputerów:** Menu → Dane → „Importuj sesje z innego komputera …” dodaje
  czas gry z pliku `playtime.db` (lub kopii zapasowej) innego komputera. Istniejące już
  sesje są rozpoznawane i pomijane; najpierw tworzona jest kopia obecnych danych.
- **Od kiedy liczy:** kafelek ŁĄCZNIE pokazuje w prawym górnym rogu datę pierwszego
  zapisu.
- **Pomoc i lista zmian we wszystkich siedmiu językach** (wcześniej tylko po niemiecku i
  angielsku).

### Zmiany
- Eksport CSV/JSON zawiera kolumnę `ending` (`quit`, `crash`, `server`).

## [1.4.1] – 2026-10-09

### Ulepszenia
- **Szybsza nakładka przy długiej historii gry:** statystyki były co sekundę liczone od
  nowa, a nakład pracy rósł kwadratowo z liczbą sesji (1,5 s przy 5000 sesji – co sekundę,
  nad grą). Teraz zakończone sesje są oceniane tylko raz, a co sekundę dochodzi jedynie
  bieżąca: 2 ms zamiast 1500 ms.
- Pulsująca kropka odświeża nakładkę 8 zamiast 16 razy na sekundę.

### Bezpieczeństwo
- Aktualizacje są instalowane tylko wtedy, gdy pobrany plik zgadza się z sumą kontrolną
  podaną przez GitHub dla wydania.
- Ustawienia są najpierw w całości zapisywane do pliku tymczasowego, a potem podmieniane –
  awaria podczas zapisu nie resetuje ich już do domyślnych.

## [1.4.0] – 2026-10-04

### Nowości
- **Przewijanie wykresu wstecz:** dla DZIEŃ, TYDZIEŃ i MIESIĄC strzałki ‹ › w prawym
  górnym rogu wykresu przewijają w przeszłość, kółko myszy krok po kroku – aż do pierwszej
  sesji.
- **Analiza** (Menu → Analiza …): mapa cieplna „Kiedy grasz?” według dnia i godziny oraz
  **czas gry według patcha**. Wersja Star Citizen (np. 4.3.1) jest teraz odczytywana z
  folderu instalacji i zapisywana z każdą sesją.
- **Edycja sesji** (Menu → Edytuj sesje …): poprawianie początku i końca lub usuwanie
  sesji, np. po uśpieniu komputera z otwartą grą.
- **Wykrywanie AFK** (Menu → Wykrywanie AFK): opcjonalna pauza po 5–30 minutach bez
  aktywności; sesja kończy się w chwili ostatniego naciśnięcia klawisza, a przy następnej
  aktywności zaczyna się nowa. Nakładka pokazuje wtedy „AFK”.
- **Globalne skróty** (Windows): Ctrl+Shift+F9 pokazuje/ukrywa nakładkę, Ctrl+Shift+F11
  włącza/wyłącza „Przepuszczaj kliknięcia” – także w grze. Zmiana w Menu → Skróty
  klawiszowe ….
- **Eksport** wszystkich sesji jako CSV (do Excela) lub JSON (Menu → Dane).
- **Automatyczna kopia zapasowa:** jedna kopia bazy dziennie w `backups`, zostaje 7
  ostatnich; dodatkowo „Utwórz kopię teraz” w menu.
- **Nowe języki:** Français, Español, Italiano, Polski i 简体中文 (pomoc i lista zmian
  wtedy po angielsku).
- **O programie SC Playtime** w menu, z wersją, linkami i przyciskiem darowizny (PayPal).

### Poprawki
- Menu kontekstowe (a także wybór koloru i komunikaty) często znikało za nakładką lub za
  grą. Teraz menu i okna dialogowe zawsze pozostają na wierzchu, a nakładka nie wysuwa się
  już przed nie, gdy któreś jest otwarte.

## [1.3.2] – 2026-09-29

### Poprawki
- **Wykres z filtrem kanału:** przy wybranym np. PTU wykres wyglądał tak samo jak przy
  WSZYSTKIE, bo zawsze skalował się do własnego najwyższego słupka – 6 minut PTU
  wypełniało wysokość tak jak 11 godzin łącznie. Teraz skala pozostaje taka jak dla
  WSZYSTKIE, suma jest pokazana na szaro w tle, a wybrany kanał rysowany jest w swoim
  kolorze z przodu. Po najechaniu widać „PTU 6m / 11h 31m”.

## [1.3.1] – 2026-09-29

### Nowości
- **Potwierdzenie pochodzenia:** każdy opublikowany plik można sprawdzić atestacją GitHub
  (`gh attestation verify …`). Podpis Windows przez SignPath Foundation został zamówiony i
  jest przygotowany w procesie budowania.
- Licencja: MIT.
- Pomoc: rozdział o ostrzeżeniu SmartScreen.

## [1.3.0] – 2026-09-29

### Nowości
- **Język angielski:** Menu → Język z flagami (🇩🇪 Deutsch, 🇬🇧 English) lub
  „Automatycznie” według języka systemu. Nakładka, menu, komunikaty, pomoc i lista zmian
  są w pełni przetłumaczone; kolejne języki łatwo dodać.
- **Obsługa Linuksa:** wykrywanie procesów przez `/proc` (także Star Citizen pod
  Wine/Proton/Lutris z kanałem), autostart przez `~/.config/autostart`, dane w
  `~/.local/share/SC-Playtime`, automatyczne uruchamianie przez XWayland. Gotowy program
  `SC-Playtime-linux-x86_64` w wydaniu, samoaktualizacja także w Linuksie.
- Automatyczne budowanie i testy dla Windows i Linuksa przez GitHub Actions.

### Poprawki
- Komunikaty (np. „Brak aktualizacji”) pokazywały ciemny tekst na ciemnym tle i wyglądały
  na puste.

## [1.2.0] – 2026-09-29

### Nowości
- **Funkcja aktualizacji:** przy starcie i co 12 godzin sprawdza na GitHubie, czy jest nowa
  wersja. Jeśli tak, przy ikonie w zasobniku pojawia się powiadomienie, a na górze menu
  „Zainstaluj aktualizację”. Plik EXE pobiera nową wersję, podmienia się i uruchamia
  ponownie – bieżąca sesja jest najpierw zapisywana.
- Menu: **Sprawdź aktualizacje** i **Automatycznie sprawdzaj aktualizacje** (można
  wyłączyć).
- Menu: **Pomoc** i **Co nowego?** otwierają pomoc i listę zmian bezpośrednio w programie,
  także offline.
- Po aktualizacji „Co nowego?” wyświetla się automatycznie jeden raz.
- Numer wersji w tytule menu i w oknach.

## [1.1.0] – 2026-09-29

### Nowości
- **Regulowane kolory** (Menu → Kolory):
  - *Kafelki statystyk (w grze)*: zestawy Zielony, Cyjan, Bursztynowy lub „Bez koloru”,
    a także dowolny wybór koloru tła i tekstu.
  - *Aktywny kanał*: zestawy dla wybranego kanału oraz dowolny wybór koloru.
- Kafelki statystyk są kolorowane, gdy gra działa (domyślnie: zielone z ciemnym tekstem).
  Offline pozostają ciemne w stylu HUD.
- Pomoc (`HILFE.md`) opisująca wszystkie funkcje.

### Poprawki
- W trakcie gry kafelki i znaczniki kanałów były przez pomyłkę wypełniane jasnozielonym
  kolorem, przez co biały tekst był słabo czytelny. Przyczyną był kolor wypełnienia kropki
  stanu, który potem pozostawał aktywny.

## [1.0.0] – 2026-09-28

Pierwsze wydanie.

### Nowości
- Nakładka bez ramki w stylu HUD Star Citizen, zawsze na wierzchu.
- Automatyczne wykrywanie `StarCitizen.exe` (lista procesów, co 2 s, tylko odczyt).
- Wykrywanie kanału z folderu instalacji: LIVE, PTU, EPTU, HOTFIX, TECH-PREVIEW;
  statystyki według kanału lub łącznie.
- Kilka gier: dodawanie i usuwanie dowolnego pliku EXE.
- Widok kompaktowy: zegar sesji, dziś, tydzień.
- Rozwinięte statystyki: kafelki (dziś, tydzień, miesiąc, rok, łącznie, seria), wykres
  słupkowy dzień / tydzień / miesiąc / rok / łącznie z wartościami po najechaniu, sesje,
  średnia i najdłuższa sesja.
- Przezroczystość tła i całości regulowane osobno.
- Blokada pozycji, przepuszczanie kliknięć, pokazywanie tylko wtedy, gdy gra działa.
- Ikona w zasobniku, jedna instancja, autostart z Windows (bez administratora).
- Zapis w SQLite w `%APPDATA%\SC-Playtime\`; koniec sesji zapisywany co 30 s.
- Budowanie jednego pliku EXE przez PyInstaller (`build.py`).
