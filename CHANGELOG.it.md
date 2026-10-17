# Registro delle modifiche

🇩🇪 [Deutsch](CHANGELOG.md) · 🇬🇧 [English](CHANGELOG.en.md) · 🇫🇷 [Français](CHANGELOG.fr.md) · 🇪🇸 [Español](CHANGELOG.es.md) · 🇵🇱 [Polski](CHANGELOG.pl.md) · 🇨🇳 [简体中文](CHANGELOG.zh.md)

Tutte le modifiche importanti di SC Playtime. Formato ispirato a
[Keep a Changelog](https://keepachangelog.com/it-IT/1.1.0/).

## [1.6.0] – 2026-10-17

### Novità
- **Anti-AFK** (Windows): Menu → Anti-AFK tiene sveglio Star Citizen. Preme a intervalli il tasto a
  destra della P (di default ogni 5 s) e/o muove il mouse con un piccolo schema (destra–sinistra,
  su–giù, quadrato, cerchio, casuale; ampiezza, velocità e intervallo regolabili). Vengono inviati
  veri scancode, solo con il gioco in primo piano. Attivazione dal menu o con
  **Ctrl+Maiusc+F12**; anelli accanto all'orologio mostrano il ritmo e attivano l'azione con un
  clic. I suoi input non contano per il rilevamento AFK.

## [1.5.0] – 2026-10-09

### Novità
- **Crash e disconnessioni dal server per patch:** alla chiusura del gioco SC Playtime
  legge il `Game.log` di Star Citizen e ricorda se hai chiuso tu, se il gioco è andato in
  crash o se il server ha interrotto la connessione. L'analisi mostra per patch i crash (ad
  es. «2 · ogni 6h 30m») e le disconnessioni, la finestra delle sessioni una colonna
  «Esito». Le sessioni precedenti vengono classificate all'avvio dai log salvati
  (`logbackups`).
- **Andamento della giornata** nell'analisi: un giorno come linea del tempo da 0 a 24 con
  tutte le sessioni nel colore del loro canale, le pause come spazi vuoti, crash (rosso) e
  disconnessione (giallo) come segni; con ‹ › si passa da un giorno giocato all'altro.
- **Unire due PC:** Menu → Dati → «Importa le sessioni di un altro PC …» aggiunge il tempo
  di gioco dal `playtime.db` (o da un backup) di un altro PC. Le sessioni già presenti
  vengono riconosciute e saltate; prima viene salvato lo stato attuale.
- **Da quando si conta:** il riquadro TOTALE mostra in alto a destra la data della prima
  registrazione.
- **Guida e registro delle modifiche in tutte e sette le lingue** (prima solo tedesco e
  inglese).

### Modifiche
- L'esportazione CSV/JSON contiene una colonna `ending` (`quit`, `crash`, `server`).

## [1.4.1] – 2026-10-09

### Miglioramenti
- **Overlay più veloce con una lunga cronologia:** le statistiche venivano ricalcolate da
  capo ogni secondo, e il lavoro cresceva al quadrato con il numero di sessioni (1,5 s con
  5000 sessioni – ogni secondo, sopra il gioco). Ora le sessioni concluse vengono valutate
  una sola volta e ogni secondo si aggiunge solo quella in corso: 2 ms invece di 1500 ms.
- Il punto che pulsa ridisegna l'overlay 8 volte al secondo invece di 16.

### Sicurezza
- Gli aggiornamenti vengono installati solo se il file scaricato corrisponde al checksum
  che GitHub indica per la release.
- Le impostazioni vengono prima scritte per intero in un file temporaneo e poi sostituite –
  un crash durante il salvataggio non le azzera più.

## [1.4.0] – 2026-10-04

### Novità
- **Tornare indietro nel grafico:** per GIORNO, SETT. e MESE le frecce ‹ › in alto a destra
  del grafico sfogliano il passato, la rotella del mouse passo per passo – fino alla prima
  sessione.
- **Analisi** (Menu → Analisi …): mappa di calore «Quando giochi?» per giorno e ora, più il
  **tempo di gioco per patch**. La versione di Star Citizen (ad es. 4.3.1) ora viene letta
  dalla cartella di installazione e salvata con ogni sessione.
- **Modifica sessioni** (Menu → Modifica sessioni …): correggere inizio e fine o eliminare
  sessioni, ad es. dopo uno standby con il gioco aperto.
- **Rilevamento AFK** (Menu → Rilevamento AFK): pausa facoltativa dopo 5–30 minuti senza
  input; la sessione termina all'ultimo tasto premuto e ne inizia una nuova con l'input
  successivo. L'overlay mostra allora «AFK».
- **Scorciatoie globali** (Windows): Ctrl+Maiusc+F9 mostra/nasconde l'overlay,
  Ctrl+Maiusc+F11 attiva/disattiva «Lascia passare i clic» – anche in gioco. Si cambiano in
  Menu → Scorciatoie da tastiera ….
- **Esportazione** di tutte le sessioni come CSV (per Excel) o JSON (Menu → Dati).
- **Backup automatico:** una copia del database al giorno in `backups`, restano le ultime
  7; in più «Esegui backup ora» nel menu.
- **Nuove lingue:** Français, Español, Italiano, Polski e 简体中文 (guida e registro delle
  modifiche allora in inglese).
- **Informazioni su SC Playtime** nel menu, con versione, link e pulsante per donare
  (PayPal).

### Correzioni
- Il menu contestuale (e il selettore di colore o i messaggi) finiva spesso dietro
  l'overlay o dietro il gioco. Ora menu e finestre di dialogo restano sempre in primo piano
  e l'overlay non si porta più davanti mentre uno di essi è aperto.

## [1.3.2] – 2026-09-29

### Correzioni
- **Grafico con filtro canale:** con ad es. PTU selezionato il grafico sembrava uguale a
  TUTTI, perché si adattava sempre alla sua barra più alta – 6 minuti di PTU riempivano
  l'altezza come 11 ore in totale. Ora la scala resta quella di TUTTI, il totale è mostrato
  in grigio dietro e il canale scelto è disegnato nel suo colore davanti. Al passaggio del
  mouse compare «PTU 6m / 11h 31m».

## [1.3.1] – 2026-09-29

### Novità
- **Prova di provenienza:** ogni file pubblicato si può verificare con un'attestazione
  GitHub (`gh attestation verify …`). La firma di Windows tramite SignPath Foundation è
  stata richiesta ed è predisposta nella compilazione.
- Licenza: MIT.
- Guida: sezione sull'avviso di SmartScreen.

## [1.3.0] – 2026-09-29

### Novità
- **Lingua inglese:** Menu → Lingua con bandiere (🇩🇪 Deutsch, 🇬🇧 English) o «Automatica»
  in base alla lingua del sistema. Overlay, menu, messaggi, guida e registro delle
  modifiche sono completamente tradotti; si possono aggiungere facilmente altre lingue.
- **Supporto Linux:** rilevamento dei processi tramite `/proc` (incluso Star Citizen con
  Wine/Proton/Lutris con canale), avvio automatico tramite `~/.config/autostart`, dati in
  `~/.local/share/SC-Playtime`, avvio automatico tramite XWayland. Programma pronto
  `SC-Playtime-linux-x86_64` nella release, aggiornamento automatico anche su Linux.
- Compilazioni e test automatici per Windows e Linux con GitHub Actions.

### Correzioni
- I messaggi (ad es. «Nessun aggiornamento») mostravano testo scuro su sfondo scuro e
  sembravano vuoti.

## [1.2.0] – 2026-09-29

### Novità
- **Funzione di aggiornamento:** all'avvio e ogni 12 ore controlla su GitHub se c'è una
  nuova versione. Se c'è, compare un avviso sull'icona di notifica e «Installa
  l'aggiornamento» in cima al menu. L'EXE scarica la nuova versione, si sostituisce e si
  riavvia – prima viene salvata la sessione in corso.
- Menu: **Cerca aggiornamenti** e **Cerca aggiornamenti automaticamente** (disattivabile).
- Menu: **Guida** e **Novità** aprono guida e registro delle modifiche direttamente nel
  programma, anche offline.
- Dopo un aggiornamento, «Novità» viene mostrato automaticamente una volta.
- Numero di versione nel titolo del menu e nelle finestre.

## [1.1.0] – 2026-09-29

### Novità
- **Colori regolabili** (Menu → Colori):
  - *Riquadri statistiche (in gioco)*: modelli Verde, Ciano, Ambra o «Senza colore», più
    libera scelta del colore di sfondo e del testo.
  - *Canale attivo*: modelli per il chip del canale selezionato più libera scelta del
    colore.
- I riquadri delle statistiche vengono colorati mentre il gioco è in esecuzione
  (predefinito: verde con testo scuro). Offline restano scuri in stile HUD.
- Guida (`HILFE.md`) con tutte le funzioni.

### Correzioni
- Durante il gioco, riquadri e chip dei canali venivano riempiti per errore di verde
  chiaro, rendendo difficile leggere il testo bianco. La causa era il colore di
  riempimento del punto di stato, rimasto attivo in seguito.

## [1.0.0] – 2026-09-28

Prima versione.

### Novità
- Overlay senza bordi in stile HUD di Star Citizen, sempre in primo piano.
- Rilevamento automatico di `StarCitizen.exe` (elenco dei processi, ogni 2 s, solo
  lettura).
- Rilevamento del canale dalla cartella di installazione: LIVE, PTU, EPTU, HOTFIX,
  TECH-PREVIEW; statistiche per canale o tutte insieme.
- Più giochi: aggiungere e rimuovere qualsiasi EXE.
- Vista compatta: orologio della sessione, oggi, settimana.
- Statistiche espanse: riquadri (oggi, settimana, mese, anno, totale, serie), grafico a
  barre giorno / settimana / mese / anno / totale con valori al passaggio del mouse,
  sessioni, media e sessione più lunga.
- Trasparenza dello sfondo e trasparenza totale regolabili separatamente.
- Blocca posizione, lascia passare i clic, mostra solo mentre un gioco è in esecuzione.
- Icona di notifica, istanza singola, avvio con Windows (senza amministratore).
- Salvataggio in SQLite in `%APPDATA%\SC-Playtime\`; fine della sessione salvata ogni
  30 s.
- Compilazione in un unico EXE con PyInstaller (`build.py`).
