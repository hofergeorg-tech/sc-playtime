# SC Playtime – Guida

🇩🇪 [Deutsch](HILFE.md) · 🇬🇧 [English](HELP.md) · 🇫🇷 [Français](HELP.fr.md) · 🇪🇸 [Español](HELP.es.md) · 🇵🇱 [Polski](HELP.pl.md) · 🇨🇳 [简体中文](HELP.zh.md)

SC Playtime è un piccolo overlay che conta quanto tempo giochi a Star Citizen (o ad altri
giochi). Si posiziona come un pannello sottile sopra il gioco e mostra la sessione in corso
e le tue statistiche. Funziona su **Windows** e **Linux**.

- [Installazione e avvio](#installazione-e-avvio)
- [L'overlay](#loverlay)
- [Uso con il mouse](#uso-con-il-mouse)
- [Il menu](#il-menu)
- [Colori](#colori)
- [Lingua](#lingua)
- [Più giochi](#più-giochi)
- [Canali (LIVE, PTU, …)](#canali-live-ptu-)
- [Analisi (mappa di calore, andamento della giornata, patch)](#analisi-mappa-di-calore-andamento-della-giornata-patch)
- [Modificare le sessioni](#modificare-le-sessioni)
- [Rilevamento AFK](#rilevamento-afk)
- [Scorciatoie da tastiera](#scorciatoie-da-tastiera)
- [Esportazione e backup](#esportazione-e-backup)
- [Come viene contato il tempo](#come-viene-contato-il-tempo)
- [Aggiornamenti](#aggiornamenti)
- [Linux](#linux)
- [I tuoi dati](#i-tuoi-dati)
- [Domande frequenti](#domande-frequenti)

---

## Installazione e avvio

**Windows:** scarica `SC-Playtime.exe` dalla
[pagina delle versioni](https://github.com/hofergeorg-tech/sc-playtime/releases/latest),
mettilo in una cartella dedicata (ad es. `Documenti\SC-Playtime`) e avvialo. Non serve
installare nulla; l'icona nell'area di notifica (un orologio in una cornice) compare in
basso a destra nella barra delle applicazioni.

**Linux:** vedi [Linux](#linux).

**Dal codice sorgente (Windows):**

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\pythonw.exe run.pyw
```

Gira sempre una sola istanza. Un secondo avvio (ad es. avvio automatico più avvio manuale)
si chiude subito, così nulla viene contato due volte.

> **Importante:** Star Citizen deve girare in modalità **«Finestra senza bordi»**. A
> schermo intero esclusivo non si può disegnare alcun overlay sopra – vale per tutti gli
> overlay.

## L'overlay

### Vista compatta

| Elemento | Significato |
| --- | --- |
| Punto in alto a sinistra | pulsa in verde finché il gioco è in esecuzione; giallo in AFK; grigio offline |
| Nome del gioco | il gioco mostrato, accanto il canale (ad es. **LIVE**) |
| **IN GIOCO** / **AFK** / **OFFLINE** | stato in alto a destra (AFK: vedi [Rilevamento AFK](#rilevamento-afk)) |
| Orologio grande | durata della sessione in corso; offline, quella dell'ultima sessione |
| OGGI / SETTIMANA | giocato oggi e da lunedì di questa settimana |

### Statistiche espanse

Un clic sull'intestazione dell'overlay espande o chiude le statistiche.

- **Filtro canale** (TUTTI, LIVE, PTU, …): mostra le statistiche di un solo canale o di
  tutti insieme. Compare non appena sono state registrate sessioni con canale.
- **Riquadri:**

  | Riquadro | Significato |
  | --- | --- |
  | OGGI | tempo di gioco da mezzanotte |
  | SETTIMANA | da lunedì alle 0:00 |
  | MESE | dal 1° del mese |
  | ANNO | dal 1° gennaio |
  | TOTALE | tutto ciò che è stato registrato; in alto a destra la data della prima registrazione (da quando si conta) |
  | SERIE | giorni consecutivi con almeno 1 minuto di gioco. Non aver ancora giocato oggi non interrompe la serie. |

- **Grafico** con le schede:

  | Scheda | mostra |
  | --- | --- |
  | GIORNO | gli ultimi 14 giorni |
  | SETT. | le ultime 12 settimane |
  | MESE | gli ultimi 12 mesi |
  | ANNO | gli ultimi 5 anni |
  | TOTALE | ogni anno dalla tua prima sessione |

  Il periodo attuale è evidenziato in verde. Passando il mouse su una barra, in basso
  compaiono il periodo esatto e il tempo di gioco.

  **Tornare indietro** (GIORNO, SETT., MESE): le frecce ‹ › in alto a destra del grafico
  saltano di mezzo grafico nel passato o di nuovo verso oggi. Con la **rotella del mouse**
  sul grafico si procede passo per passo (in su = più vecchio). Non si va più indietro
  della prima sessione. Cambiando scheda o filtro il grafico torna a oggi.

  Con un filtro canale attivo (ad es. PTU), le barre colorate mostrano solo quel canale.
  Dietro compare in grigio il totale di tutti i canali e la scala resta quella di «TUTTI» –
  così si vede subito la quota del canale. Al passaggio del mouse compare ad es.
  «PTU 6m / 11h 31m».
- **Piè di pagina:** numero di sessioni, sessione media e più lunga (le sessioni sotto
  1 minuto qui non contano).

## Uso con il mouse

| Azione | Effetto |
| --- | --- |
| Clic sull'intestazione | espandere/chiudere le statistiche |
| Trascinare con il tasto sinistro | spostare l'overlay (tranne con «Blocca posizione») |
| Clic su un chip di canale | impostare il filtro canale |
| Clic su una scheda | cambiare il periodo del grafico |
| Clic su ‹ / › del grafico | indietro / avanti |
| Rotella sul grafico | un periodo indietro (su) o avanti (giù) |
| Mouse su una barra | valori esatti nel piè di pagina |
| Clic destro sull'overlay | menu |
| Clic sinistro sull'icona di notifica | mostrare/nascondere l'overlay |
| Clic destro sull'icona di notifica | menu (anche con l'overlay nascosto) |

Posizione, stato espanso, scheda e filtro scelti vengono salvati e ripristinati al
prossimo avvio.

## Il menu

| Voce | Funzione |
| --- | --- |
| Mostra/Nascondi overlay | solo nel menu dell'area di notifica |
| Mostra statistiche | come un clic sull'intestazione |
| Gioco | scegliere il gioco mostrato, aggiungere o rimuovere giochi |
| Analisi … | mappa di calore, andamento della giornata e tempo per patch, vedi [Analisi](#analisi-mappa-di-calore-andamento-della-giornata-patch) |
| Modifica sessioni … | correggere o eliminare sessioni, vedi [Modificare le sessioni](#modificare-le-sessioni) |
| SFONDO (cursore) | opacità solo dello sfondo scuro; il testo resta pienamente visibile |
| OPACITÀ TOTALE (cursore) | opacità dell'intero overlay (20–100 %) |
| Colori | vedi [Colori](#colori) |
| Lingua | vedi [Lingua](#lingua) |
| Blocca posizione | l'overlay non si può più spostare |
| Lascia passare i clic | i clic attraversano l'overlay fino al gioco. Si disattiva solo dall'**icona di notifica** o con la [scorciatoia](#scorciatoie-da-tastiera). |
| Mostra solo mentre un gioco è in esecuzione | l'overlay si nasconde da solo quando sei offline |
| Rilevamento AFK | non contare il tempo senza input, vedi [Rilevamento AFK](#rilevamento-afk) |
| Scorciatoie da tastiera … | tasti globali per mostrare/nascondere, vedi [Scorciatoie da tastiera](#scorciatoie-da-tastiera) |
| Avvia con Windows / Avvia all'accesso | avvio automatico all'accesso (senza diritti di amministratore) |
| Guida … | questa guida |
| Novità … | registro delle modifiche di ogni versione |
| Informazioni su SC Playtime … | versione, link, licenza e pulsante per donare (PayPal) |
| Cerca aggiornamenti | controllare subito su GitHub, vedi [Aggiornamenti](#aggiornamenti) |
| Cerca aggiornamenti automaticamente | all'avvio e ogni 12 ore (predefinito: attivo) |
| ⬆ Installa l'aggiornamento … | compare in cima quando è disponibile una nuova versione |
| Dati | esportazione CSV/JSON, backup, sessioni di un altro PC, cartella dati, vedi [Esportazione e backup](#esportazione-e-backup) |
| Esci | chiudere l'overlay; prima viene salvata la sessione in corso |

## Colori

**Menu → Colori** ha due sezioni. Ognuna offre modelli e inoltre «Scegli colore di
sfondo …» e «Scegli colore del testo …».

**Riquadri statistiche (in gioco)** – offline i riquadri sono sempre scuri in stile HUD.
Appena il gioco è in esecuzione vengono colorati:

- Verde / Scuro (predefinito)
- Ciano / Scuro
- Ambra / Scuro
- Senza colore (HUD) – i riquadri restano scuri anche in gioco

**Canale attivo** – il chip del canale selezionato (nell'intestazione e nel filtro):

- Automatico (colore del canale, testo scuro) – LIVE verde, PTU giallo, …
- Verde scuro / Bianco, Nero / Verde, Blu scuro / Bianco, Bianco / Nero

Consiglio: per leggere bene abbina sfondi chiari a testo scuro e viceversa.

## Lingua

**Menu → Lingua** (con bandiera) offre:

- **Automatica (sistema)** – predefinita; la lingua del sistema operativo se supportata,
  altrimenti l'inglese
- 🇩🇪 **Deutsch**
- 🇬🇧 **English**
- 🇫🇷 **Français**, 🇪🇸 **Español**, 🇮🇹 **Italiano**, 🇵🇱 **Polski**, 🇨🇳 **简体中文**

Il cambio vale subito per overlay, menu, messaggi, guida e «Novità» – guida e registro
delle modifiche esistono in tutte e sette le lingue.

## Più giochi

Per impostazione predefinita viene seguito `StarCitizen.exe`. Per aggiungere altri giochi:

1. Clic destro → **Gioco → Aggiungi gioco …**
2. Scegli il programma del gioco (Windows: il `.exe`; Linux: vedi sotto).
3. Inserisci un nome da mostrare.

Il gioco viene riconosciuto dal nome del programma. Quando un gioco è in esecuzione,
l'overlay lo mostra automaticamente; se ce ne sono più d'uno, quello scelto nel menu.
**Rimuovi gioco** smette di seguirlo – le sessioni passate restano salvate.

## Canali (LIVE, PTU, …)

Il canale viene letto dalla cartella di installazione:

```
…\StarCitizen\LIVE\Bin64\StarCitizen.exe   →  LIVE
…\StarCitizen\PTU\Bin64\StarCitizen.exe    →  PTU
```

Lo stesso vale per EPTU, HOTFIX e TECH-PREVIEW. Ogni sessione ricorda il suo canale, così
le statistiche si possono mostrare per canale o tutte insieme («TUTTI»).

## Analisi (mappa di calore, andamento della giornata, patch)

**Menu → Analisi …** apre una finestra per il gioco mostrato e il filtro canale scelto:

- **Quando giochi?** – una mappa di calore con i giorni della settimana come righe e le
  24 ore come colonne. Più una casella è chiara, più hai giocato in quel momento. Con il
  mouse su una casella vedi il tempo esatto; sotto compaiono il giorno e l'ora più giocati.
- **Andamento della giornata** – un giorno come linea del tempo da 0 a 24: ogni sessione è
  una barra nel colore del suo canale, gli spazi vuoti sono pause o tempo AFK. Un **segno
  rosso** alla fine di una sessione indica un crash, uno **giallo** una disconnessione dal
  server. Con ‹ › passi da un giorno giocato all'altro; con il mouse su una barra vedi
  orario, durata, canale, patch e come è terminata la sessione.
- **Tempo di gioco per patch** – tempo di gioco, quota, numero di sessioni, **crash**,
  **disconnessioni** e periodo per ogni versione di Star Citizen (ad es. 4.3.1). Per i
  crash viene mostrata anche la frequenza, ad es. «2 · ogni 6h 30m» – così vedi se una
  patch è più stabile della precedente. La patch viene letta all'avvio di ogni sessione da
  `build_manifest.id` o `Game.log` nella cartella di installazione (ad es.
  `…\StarCitizen\LIVE\`). Le sessioni precedenti alla versione 1.4 e i giochi senza questi
  file compaiono come «sconosciuta».

### Crash e disconnessioni dal server

Quando Star Citizen si chiude, SC Playtime legge la fine di `Game.log` (solo lettura):

| Nel log | Significato |
| --- | --- |
| `<SystemQuit>` con «Quit via console command» / «User closed the application» | **chiuso** – hai smesso tu |
| `<SystemQuit>` con un altro motivo, ad es. «Back-end services are unresponsive» | **disconnessione dal server** – connessione al server/backend persa |
| nessuna riga `<SystemQuit>`, ma un passaggio al raccoglitore dei crash | **crash** |

Le sessioni precedenti vengono classificate all'avvio di SC Playtime: Star Citizen
conserva il log di ogni avvio nella cartella `logbackups`, e il log giusto viene trovato in
base all'ora in cui è finita la sessione. Non si possono classificare le sessioni senza
log, i giochi diversi da Star Citizen e le sessioni terminate in una pausa AFK.
L'installazione viene trovata automaticamente (cartella predefinita o cartella da cui è
partito il gioco).

## Modificare le sessioni

**Menu → Modifica sessioni …** elenca tutte le sessioni del gioco mostrato, le più recenti
in alto. Serve a correggere errori, ad es. se il PC era in standby con il gioco aperto:

- La colonna **Esito** mostra come è finita la sessione: chiuso, **crash** (rosso) o
  **disconnessione dal server** (giallo), vedi
  [Crash e disconnessioni dal server](#crash-e-disconnessioni-dal-server).
- **Modifica …** (o doppio clic): cambiare inizio e fine.
- **Elimina**: rimuovere una o più sessioni selezionate (Ctrl/Maiusc per la selezione
  multipla). Non si può annullare – nel dubbio fai prima un [backup](#esportazione-e-backup).

La sessione in corso (verde, «in corso») resta bloccata finché il gioco non viene chiuso.

## Rilevamento AFK

In **Menu → Rilevamento AFK** puoi fare in modo che il tempo senza input non conti:
**Disattivato** (predefinito) oppure pausa dopo **5, 10, 15 o 30 minuti** senza tastiera,
mouse o controller.

- Raggiunto il tempo, la sessione termina all'**ultimo tasto premuto** – così anche l'attesa
  non conta. L'overlay mostra **AFK** con un punto giallo.
- Appena arriva di nuovo un input e il gioco è ancora in esecuzione, inizia
  automaticamente una nuova sessione.
- Conta qualsiasi input sul PC, non solo nel gioco.
- Su Linux funziona con X11/XWayland (libreria `libXss`); senza di essa il rilevamento non
  ha effetto.

## Scorciatoie da tastiera

Le scorciatoie globali funzionano ovunque, anche con il gioco in primo piano (solo
**Windows**):

| Predefinita | Effetto |
| --- | --- |
| **Ctrl+Maiusc+F9** | mostrare/nascondere l'overlay |
| **Ctrl+Maiusc+F11** | attivare/disattivare «Lascia passare i clic» |

Si cambiano in **Menu → Scorciatoie da tastiera …**: fai clic sul campo, premi la nuova
combinazione, svuotalo con ✕ (= nessuna scorciatoia). Sono ammessi lettere, cifre,
F1–F24, Home/Fine/Ins/Canc, PagSu/PagGiù, frecce, Pausa e Spazio – tranne che per i tasti
F, sempre con Ctrl, Maiusc, Alt o Win. Se un altro programma usa già la combinazione,
compare un avviso.

## Esportazione e backup

In **Menu → Dati**:

| Voce | Funzione |
| --- | --- |
| Esporta come CSV … | tutte le sessioni di tutti i giochi come tabella, ad es. per Excel (colonne: gioco, canale, patch, inizio, fine, durata in secondi e minuti, esito `quit`/`crash`/`server`) |
| Esporta come JSON … | lo stesso in JSON, orari anche con fuso orario e come timestamp Unix |
| Esegui backup ora | creare subito una copia del database |
| Backup automatico giornaliero (7 giorni) | una copia al giorno; restano le ultime 7 (predefinito: attivo) |
| Apri cartella dei backup | cartella `backups` nella cartella dei dati |
| Importa le sessioni di un altro PC … | aggiungere il tempo di gioco di un secondo PC, vedi sotto |
| Apri cartella dei dati | cartella con database e impostazioni |

**Ripristinare un backup:** chiudi l'overlay, sostituisci `playtime.db` nella cartella dei
dati con il file desiderato da `backups` (ad es. copia `playtime-2026-10-04.db` e rinominalo
in `playtime.db`), riavvia l'overlay.

### Unire due PC

Se giochi su più PC, aggiungi il tempo di gioco dell'altro PC così:

1. Sull'altro PC prendi il file `playtime.db` dalla cartella dei dati (o un backup da
   `backups`), ad es. con una chiavetta USB o una cartella cloud.
2. Qui, **Menu → Dati → Importa le sessioni di un altro PC …** e scegli il file.
3. SC Playtime mostra quante sessioni sono nuove e quante ci sono già, e dopo la tua
   conferma importa solo quelle nuove. Prima viene salvato lo stato attuale.

Una sessione conta come «già presente» se si sovrappone nel tempo a una sessione dello
stesso gioco qui – lo stesso gioco non gira contemporaneamente su due PC. Per questo puoi
importare di nuovo lo stesso file più avanti senza che nulla venga contato due volte.
Vengono importati anche canale, patch ed esito. I giochi che qui non esistono ancora
vengono elencati: le loro sessioni sono salvate e compaiono appena aggiungi il gioco con
lo stesso nome.

## Come viene contato il tempo

- L'elenco dei processi viene letto ogni 2 secondi. Viene solo **letto** – nulla viene
  iniettato nel gioco.
- Se avvii l'overlay con il gioco già aperto, la sessione conta comunque dall'avvio reale
  del gioco.
- La fine della sessione viene salvata ogni 30 secondi. Se il PC si blocca, si perdono al
  massimo quei 30 secondi.
- Le sessioni a cavallo della mezzanotte (o di un limite di settimana/mese) vengono
  ripartite in proporzione.

## Aggiornamenti

La versione attuale compare in cima al menu (ad es. «SC PLAYTIME 1.5.0»).

- **Automatico:** con «Cerca aggiornamenti automaticamente» attivo, SC Playtime controlla
  GitHub poco dopo l'avvio e poi ogni 12 ore. Se c'è una nuova versione, compare un avviso
  sull'icona di notifica e in cima al menu la voce **«⬆ Installa l'aggiornamento …»**.
- **A mano:** Menu → «Cerca aggiornamenti».
- **Installare:** dopo la conferma la nuova versione viene scaricata e confrontata con il
  checksum che GitHub indica per la release – se non corrisponde, non viene installato
  nulla. L'overlay salva la sessione in corso, si chiude, sostituisce il programma e si
  riavvia. Poi viene mostrato una volta «Novità». Impostazioni e tempi di gioco restano.
- Se SC Playtime gira dal codice sorgente (`run.pyw`) invece che come programma pronto,
  «Installa» apre la pagina delle versioni nel browser – non c'è un file di programma da
  sostituire. Per aggiornare con un clic usa l'EXE e disattiva e riattiva l'avvio
  automatico nel menu.

Tutte le versioni si trovano anche su
<https://github.com/hofergeorg-tech/sc-playtime/releases>.

## Linux

**Programma pronto:** scarica `SC-Playtime-linux-x86_64` dalla
[pagina delle versioni](https://github.com/hofergeorg-tech/sc-playtime/releases/latest),
mettilo ad es. in `~/Applicazioni/`, rendilo eseguibile e avvialo:

```bash
chmod +x SC-Playtime-linux-x86_64
./SC-Playtime-linux-x86_64
```

**Dal codice sorgente:**

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python run.pyw
```

Note:

- **Star Citizen con Wine/Proton/Lutris** viene rilevato come su Windows – canale
  compreso (LIVE, PTU, …), perché viene letto anche il percorso Windows del gioco. Crash e
  disconnessioni vengono rilevati solo su Windows.
- **Giochi Linux nativi:** aggiungili con «Aggiungi gioco …» scegliendo il loro programma
  (imposta il filtro su «Tutti i file»). Vengono riconosciuti dal nome del programma.
- **Wayland:** sotto Wayland le finestre non possono scegliere la propria posizione né
  restare in primo piano. Per questo SC Playtime parte automaticamente tramite
  **XWayland**, presente su quasi tutti i desktop. Per scegliere diversamente imposta tu
  `QT_QPA_PLATFORM`.
- **Icona di notifica su GNOME:** GNOME mostra le icone solo con l'estensione «AppIndicator
  and KStatusNotifierItem Support». KDE, XFCE, Cinnamon e simili non hanno bisogno di
  nulla.
- L'**avvio automatico** si chiama «Avvia all'accesso» nel menu e crea
  `~/.config/autostart/sc-playtime.desktop`.
- I **dati** si trovano in `~/.local/share/SC-Playtime/`.

## I tuoi dati

Tutto resta in locale (Menu → «Apri cartella dei dati»):

- Windows: `%APPDATA%\SC-Playtime\`
- Linux: `~/.local/share/SC-Playtime/`

| File | Contenuto |
| --- | --- |
| `playtime.db` | database SQLite con tutte le sessioni (gioco, canale, inizio, fine, patch, esito) |
| `settings.json` | posizione, trasparenza, colori, lingua, elenco giochi, cartelle di Star Citizen trovate, … |
| `backups/` | copie giornaliere del database, vedi [Esportazione e backup](#esportazione-e-backup) |

I tuoi tempi di gioco e le impostazioni non lasciano mai il tuo PC. L'unica connessione a
Internet è la ricerca degli aggiornamenti: legge solo le informazioni pubbliche sulle
versioni da GitHub e si può disattivare nel menu. Per fare un backup o traslocare basta
copiare la cartella. Per ripristinare le impostazioni elimina `settings.json` con
l'overlay chiuso.

## Domande frequenti

**L'overlay non si vede nel gioco.**
Imposta Star Citizen su «Finestra senza bordi». Controlla che l'overlay non sia stato
nascosto dall'icona di notifica.

**Non riesco più a cliccare sull'overlay.**
«Lascia passare i clic» è attivo. Premi **Ctrl+Maiusc+F11** oppure fai clic destro
sull'icona di notifica e togli la spunta.

**Il menu o una finestra compare dietro il gioco.**
Dalla versione 1.4 menu e finestre di dialogo vengono sempre mostrati davanti all'overlay
e al gioco. Se una finestra resta comunque coperta, passaci con Alt+Tab.

**Il tempo di gioco è sbagliato perché ho lasciato il gioco aperto.**
Correggi la sessione in **Menu → Modifica sessioni …** e in futuro attiva il
[rilevamento AFK](#rilevamento-afk).

**L'overlay è sparito.**
Un clic sinistro sull'icona di notifica lo mostra di nuovo. Con «Mostra solo mentre un
gioco è in esecuzione» non compare offline.

**L'avvio automatico non funziona più.**
La voce punta alla posizione del programma o di `run.pyw`. Dopo aver spostato la cartella,
disattiva e riattiva l'avvio automatico nel menu.

**L'aggiornamento non riesce.**
Controlla la connessione a Internet e riprova con «Cerca aggiornamenti». Se il programma
si trova in una cartella protetta (ad es. `C:\Programmi` o `/usr/bin`), non può
sostituirsi da solo – scarica la nuova versione dalla pagina delle versioni o metti il
programma in una cartella dedicata.

**Windows dice «PC protetto da Windows».**
L'EXE non è ancora firmato digitalmente (richiesta in corso, vedi
[CODE_SIGNING.md](CODE_SIGNING.md)), quindi SmartScreen avvisa per i nuovi download. Fai
clic su «Ulteriori informazioni» → «Esegui comunque». Per verificare che il file sia stato
davvero compilato da questo repository:
`gh attestation verify SC-Playtime.exe --repo hofergeorg-tech/sc-playtime`

**Disturba l'anti-cheat?**
SC Playtime legge solo l'elenco dei processi e l'ora di avvio del gioco con normali
funzioni del sistema operativo, come Gestione attività, e dopo la chiusura del gioco il
file di testo `Game.log`. Non accede al gioco.

**Una sessione non ha esito.**
Nel log non c'era né una chiusura normale né un crash – ad es. se Star Citizen è stato
chiuso da Gestione attività, è mancata la corrente, la sessione è finita in una pausa AFK
o non esiste più un log. La classificazione serve solo alle statistiche e non cambia il
tempo di gioco.
