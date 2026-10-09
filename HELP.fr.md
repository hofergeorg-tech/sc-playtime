# SC Playtime – Aide

🇩🇪 [Deutsch](HILFE.md) · 🇬🇧 [English](HELP.md) · 🇪🇸 [Español](HELP.es.md) · 🇮🇹 [Italiano](HELP.it.md) · 🇵🇱 [Polski](HELP.pl.md) · 🇨🇳 [简体中文](HELP.zh.md)

SC Playtime est un petit overlay qui compte combien de temps vous jouez à Star Citizen (ou
à d'autres jeux). Il se place en fin panneau au-dessus du jeu et affiche la session en
cours ainsi que vos statistiques. Il fonctionne sous **Windows** et **Linux**.

- [Installation et démarrage](#installation-et-démarrage)
- [L'overlay](#loverlay)
- [Utilisation à la souris](#utilisation-à-la-souris)
- [Le menu](#le-menu)
- [Couleurs](#couleurs)
- [Langue](#langue)
- [Plusieurs jeux](#plusieurs-jeux)
- [Canaux (LIVE, PTU, …)](#canaux-live-ptu-)
- [Analyse (carte de chaleur, déroulé de la journée, patchs)](#analyse-carte-de-chaleur-déroulé-de-la-journée-patchs)
- [Modifier les sessions](#modifier-les-sessions)
- [Détection AFK](#détection-afk)
- [Raccourcis clavier](#raccourcis-clavier)
- [Export et sauvegarde](#export-et-sauvegarde)
- [Comment le temps est compté](#comment-le-temps-est-compté)
- [Mises à jour](#mises-à-jour)
- [Linux](#linux)
- [Vos données](#vos-données)
- [Questions fréquentes](#questions-fréquentes)

---

## Installation et démarrage

**Windows :** téléchargez `SC-Playtime.exe` depuis la
[page des versions](https://github.com/hofergeorg-tech/sc-playtime/releases/latest),
placez-le dans son propre dossier (p. ex. `Documents\SC-Playtime`) et lancez-le. Aucune
installation nécessaire ; l'icône de la zone de notification (une horloge dans un cadre)
apparaît en bas à droite de la barre des tâches.

**Linux :** voir [Linux](#linux).

**Depuis le code source (Windows) :**

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\pythonw.exe run.pyw
```

Une seule instance tourne à la fois. Un deuxième lancement (p. ex. démarrage automatique
plus lancement manuel) se ferme aussitôt, pour que rien ne soit compté deux fois.

> **Important :** Star Citizen doit tourner en mode **« Fenêtré sans bordure »**. En plein
> écran exclusif, aucun overlay ne peut s'afficher par-dessus – c'est valable pour tous
> les overlays.

## L'overlay

### Vue compacte

| Élément | Signification |
| --- | --- |
| Point en haut à gauche | pulse en vert tant que le jeu tourne ; jaune en AFK ; gris hors ligne |
| Nom du jeu | le jeu affiché, à côté le canal (p. ex. **LIVE**) |
| **EN JEU** / **AFK** / **HORS LIGNE** | état en haut à droite (AFK : voir [Détection AFK](#détection-afk)) |
| Grande horloge | durée de la session en cours ; hors ligne, durée de la dernière session |
| AUJOURD'HUI / SEMAINE | temps joué aujourd'hui et depuis lundi |

### Statistiques dépliées

Un clic sur l'en-tête de l'overlay déplie ou replie les statistiques.

- **Filtre de canal** (TOUS, LIVE, PTU, …) : affiche les statistiques d'un seul canal ou
  de tous ensemble. Apparaît dès que des sessions avec canal ont été enregistrées.
- **Tuiles :**

  | Tuile | Signification |
  | --- | --- |
  | AUJOURD'HUI | temps de jeu depuis minuit |
  | SEMAINE | depuis lundi 0 h |
  | MOIS | depuis le 1er du mois |
  | ANNÉE | depuis le 1er janvier |
  | TOTAL | tout ce qui a été enregistré ; en haut à droite la date du premier enregistrement (depuis quand on compte) |
  | SÉRIE | jours consécutifs avec au moins 1 minute de jeu. Ne pas encore avoir joué aujourd'hui n'interrompt pas la série. |

- **Graphique** avec les onglets :

  | Onglet | affiche |
  | --- | --- |
  | JOUR | les 14 derniers jours |
  | SEMAINE | les 12 dernières semaines |
  | MOIS | les 12 derniers mois |
  | ANNÉE | les 5 dernières années |
  | TOTAL | chaque année depuis votre première session |

  La période actuelle est mise en évidence en vert. En survolant une barre, la période
  exacte et le temps de jeu s'affichent en bas.

  **Remonter dans le temps** (JOUR, SEMAINE, MOIS) : les flèches ‹ › en haut à droite du
  graphique reculent d'un demi-graphique dans le passé ou reviennent vers aujourd'hui. La
  **molette** au-dessus du graphique avance pas à pas (vers le haut = plus ancien). On ne
  remonte pas plus loin que la première session. Changer d'onglet ou de filtre ramène à
  aujourd'hui.

  Avec un filtre de canal actif (p. ex. PTU), les barres colorées ne montrent que ce
  canal. Derrière, le total de tous les canaux apparaît en gris et l'échelle reste celle
  de « TOUS » – on voit d'un coup d'œil la part du canal. Au survol s'affiche p. ex.
  « PTU 6m / 11h 31m ».
- **Pied de page :** nombre de sessions, session moyenne et la plus longue (les sessions
  de moins d'une minute ne comptent pas ici).

## Utilisation à la souris

| Action | Effet |
| --- | --- |
| Clic sur l'en-tête | déplier/replier les statistiques |
| Glisser avec le bouton gauche | déplacer l'overlay (sauf si « Verrouiller la position » est actif) |
| Clic sur une puce de canal | choisir le filtre de canal |
| Clic sur un onglet | changer la période du graphique |
| Clic sur ‹ / › du graphique | reculer / avancer |
| Molette sur le graphique | une période en arrière (haut) ou en avant (bas) |
| Survol d'une barre | valeurs exactes dans le pied de page |
| Clic droit sur l'overlay | menu |
| Clic gauche sur l'icône de notification | afficher/masquer l'overlay |
| Clic droit sur l'icône de notification | menu (même si l'overlay est masqué) |

Position, état déplié, onglet et filtre choisis sont enregistrés et restaurés au
prochain démarrage.

## Le menu

| Entrée | Fonction |
| --- | --- |
| Afficher/Masquer l'overlay | uniquement dans le menu de notification |
| Afficher les statistiques | comme un clic sur l'en-tête |
| Jeu | choisir le jeu affiché, ajouter ou retirer des jeux |
| Analyse … | carte de chaleur, déroulé de la journée et temps de jeu par patch, voir [Analyse](#analyse-carte-de-chaleur-déroulé-de-la-journée-patchs) |
| Modifier les sessions … | corriger ou supprimer des sessions, voir [Modifier les sessions](#modifier-les-sessions) |
| ARRIÈRE-PLAN (curseur) | opacité du fond sombre uniquement ; le texte reste entièrement visible |
| OPACITÉ GLOBALE (curseur) | opacité de tout l'overlay (20–100 %) |
| Couleurs | voir [Couleurs](#couleurs) |
| Langue | voir [Langue](#langue) |
| Verrouiller la position | l'overlay ne peut plus être déplacé |
| Laisser passer les clics | les clics traversent l'overlay vers le jeu. Ne se désactive plus que via l'**icône de notification** ou le [raccourci](#raccourcis-clavier). |
| Afficher seulement pendant qu'un jeu tourne | l'overlay se masque automatiquement hors ligne |
| Détection AFK | ne pas compter le temps sans saisie, voir [Détection AFK](#détection-afk) |
| Raccourcis clavier … | touches globales pour afficher/masquer, voir [Raccourcis clavier](#raccourcis-clavier) |
| Lancer avec Windows / Lancer à la connexion | démarrage automatique à la connexion (sans droits d'administrateur) |
| Aide … | cette aide |
| Nouveautés … | journal des modifications de chaque version |
| À propos de SC Playtime … | version, liens, licence et bouton de don (PayPal) |
| Rechercher des mises à jour | vérifier tout de suite sur GitHub, voir [Mises à jour](#mises-à-jour) |
| Rechercher automatiquement des mises à jour | au démarrage et toutes les 12 heures (par défaut : activé) |
| ⬆ Installer la mise à jour … | apparaît tout en haut quand une nouvelle version est disponible |
| Données | export CSV/JSON, sauvegardes, sessions d'un autre PC, dossier de données, voir [Export et sauvegarde](#export-et-sauvegarde) |
| Quitter | fermer l'overlay ; la session en cours est enregistrée avant |

## Couleurs

**Menu → Couleurs** comporte deux parties. Chacune propose des modèles ainsi que
« Choisir la couleur de fond … » et « Choisir la couleur du texte … ».

**Tuiles de statistiques (en jeu)** – hors ligne, les tuiles restent sombres dans le style
HUD. Dès que le jeu tourne, elles sont colorées :

- Vert / Foncé (par défaut)
- Cyan / Foncé
- Ambre / Foncé
- Sans couleur (HUD) – les tuiles restent sombres en jeu aussi

**Canal actif** – la puce de canal sélectionnée (dans l'en-tête et le filtre) :

- Automatique (couleur du canal, texte foncé) – LIVE vert, PTU jaune, …
- Vert foncé / Blanc, Noir / Vert, Bleu foncé / Blanc, Blanc / Noir

Astuce : pour une bonne lisibilité, associez un fond clair à un texte sombre et
inversement.

## Langue

**Menu → Langue** (avec drapeau) propose :

- **Automatique (système)** – par défaut ; la langue du système si elle est prise en
  charge, sinon l'anglais
- 🇩🇪 **Deutsch**
- 🇬🇧 **English**
- 🇫🇷 **Français**, 🇪🇸 **Español**, 🇮🇹 **Italiano**, 🇵🇱 **Polski**, 🇨🇳 **简体中文**

Le changement s'applique immédiatement à l'overlay, au menu, aux messages, à l'aide et aux
« Nouveautés » – l'aide et le journal des modifications existent dans les sept
langues.

## Plusieurs jeux

`StarCitizen.exe` est suivi par défaut. Pour ajouter d'autres jeux :

1. Clic droit → **Jeu → Ajouter un jeu …**
2. Choisir le programme du jeu (Windows : le `.exe` ; Linux : voir plus bas).
3. Saisir un nom d'affichage.

Le jeu est reconnu à son nom de programme. Quand un jeu tourne, l'overlay l'affiche
automatiquement ; s'il y en a plusieurs, celui choisi dans le menu. **Retirer un jeu**
arrête le suivi – ses sessions passées restent enregistrées.

## Canaux (LIVE, PTU, …)

Le canal est lu dans le dossier d'installation :

```
…\StarCitizen\LIVE\Bin64\StarCitizen.exe   →  LIVE
…\StarCitizen\PTU\Bin64\StarCitizen.exe    →  PTU
```

De même EPTU, HOTFIX et TECH-PREVIEW. Chaque session retient son canal ; les statistiques
s'affichent ainsi par canal ou toutes ensemble (« TOUS »).

## Analyse (carte de chaleur, déroulé de la journée, patchs)

**Menu → Analyse …** ouvre une fenêtre pour le jeu affiché et le filtre de canal choisi :

- **Quand joues-tu ?** – une carte de chaleur avec les jours de la semaine en lignes et
  les 24 heures en colonnes. Plus une case est claire, plus vous avez joué à ce moment.
  Le survol d'une case affiche le temps exact ; en dessous figurent le jour et l'heure
  les plus joués.
- **Déroulé de la journée** – une journée en frise de 0 à 24 h : chaque session est une
  barre de la couleur de son canal, les trous sont des pauses ou de l'AFK. Une **marque
  rouge** en fin de session signifie un plantage, une **jaune** une déconnexion serveur.
  Avec ‹ › on passe d'un jour joué à l'autre ; le survol d'une barre montre l'heure, la
  durée, le canal, le patch et la façon dont la session s'est terminée.
- **Temps de jeu par patch** – temps de jeu, part, nombre de sessions, **plantages**,
  **déconnexions serveur** et période pour chaque version de Star Citizen (p. ex. 4.3.1).
  Pour les plantages s'affiche aussi leur fréquence, p. ex. « 2 · toutes les 6h 30m » –
  on voit ainsi si un patch est plus stable que le précédent. Le patch est lu au début de
  chaque session dans `build_manifest.id` ou `Game.log` du dossier d'installation (p. ex.
  `…\StarCitizen\LIVE\`). Les sessions antérieures à la version 1.4 et les jeux sans ces
  fichiers apparaissent comme « inconnu ».

### Plantages et déconnexions serveur

Quand Star Citizen se ferme, SC Playtime lit la fin de `Game.log` (en lecture seule) :

| Dans le journal | Signification |
| --- | --- |
| `<SystemQuit>` avec « Quit via console command » / « User closed the application » | **quitté** – vous avez arrêté vous-même |
| `<SystemQuit>` avec une autre raison, p. ex. « Back-end services are unresponsive » | **déconnexion serveur** – connexion au serveur/backend perdue |
| pas de ligne `<SystemQuit>`, mais une transmission au collecteur de plantages | **plantage** |

Les sessions plus anciennes sont classées au démarrage de SC Playtime : Star Citizen
conserve le journal de chaque lancement dans le dossier `logbackups`, et le bon journal est
retrouvé grâce à l'heure de fin de la session. Ne peuvent pas être classées : les sessions
sans journal, les jeux autres que Star Citizen et les sessions terminées par une pause AFK.
L'installation est trouvée automatiquement (dossier par défaut ou dossier d'où le jeu a
été lancé).

## Modifier les sessions

**Menu → Modifier les sessions …** liste toutes les sessions du jeu affiché, les plus
récentes en haut. Cela permet de corriger des erreurs, p. ex. si le PC était en veille
alors que le jeu était ouvert :

- La colonne **Issue** indique comment la session s'est terminée : quitté, **plantage**
  (rouge) ou **déconnexion serveur** (jaune), voir
  [Plantages et déconnexions serveur](#plantages-et-déconnexions-serveur).
- **Modifier …** (ou double-clic) : changer le début et la fin.
- **Supprimer** : retirer une ou plusieurs sessions sélectionnées (Ctrl/Maj pour la
  sélection multiple). Impossible à annuler – en cas de doute, [sauvegardez](#export-et-sauvegarde) d'abord.

La session en cours (verte, « en cours ») est verrouillée jusqu'à la fermeture du jeu.

## Détection AFK

**Menu → Détection AFK** permet de ne pas compter le temps sans saisie : **Désactivée**
(par défaut) ou pause après **5, 10, 15 ou 30 minutes** sans clavier, souris ni manette.

- Une fois ce délai atteint, la session se termine à la **dernière touche pressée** – le
  temps d'attente lui-même ne compte donc pas. L'overlay affiche **AFK** avec un point
  jaune.
- Dès qu'une nouvelle saisie arrive et que le jeu tourne encore, une nouvelle session
  commence automatiquement.
- Toute saisie sur le PC compte, pas seulement dans le jeu.
- Sous Linux, cela fonctionne avec X11/XWayland (bibliothèque `libXss`) ; sans elle, la
  détection reste sans effet.

## Raccourcis clavier

Les raccourcis globaux fonctionnent partout, même quand le jeu est au premier plan
(**Windows** uniquement) :

| Par défaut | Effet |
| --- | --- |
| **Ctrl+Maj+F9** | afficher/masquer l'overlay |
| **Ctrl+Maj+F11** | activer/désactiver « Laisser passer les clics » |

À modifier sous **Menu → Raccourcis clavier …** : cliquer dans le champ, appuyer sur la
nouvelle combinaison, vider avec ✕ (= aucun raccourci). Sont autorisés les lettres,
chiffres, F1–F24, Début/Fin/Inser/Suppr, Page↑/↓, flèches, Pause et Espace – sauf pour les
touches F, toujours avec Ctrl, Maj, Alt ou Win. Si une combinaison est déjà utilisée par
un autre programme, un message s'affiche.

## Export et sauvegarde

Sous **Menu → Données** :

| Entrée | Fonction |
| --- | --- |
| Exporter en CSV … | toutes les sessions de tous les jeux en tableau, p. ex. pour Excel (colonnes : jeu, canal, patch, début, fin, durée en secondes et minutes, fin `quit`/`crash`/`server`) |
| Exporter en JSON … | la même chose en JSON, heures en plus avec fuseau horaire et en horodatage Unix |
| Sauvegarder maintenant | créer tout de suite une copie de la base de données |
| Sauvegarde automatique quotidienne (7 jours) | une copie par jour ; les 7 dernières sont conservées (par défaut : activé) |
| Ouvrir le dossier des sauvegardes | dossier `backups` dans le dossier de données |
| Importer les sessions d'un autre PC … | ajouter le temps de jeu d'un deuxième PC, voir plus bas |
| Ouvrir le dossier des données | dossier avec la base de données et les réglages |

**Restaurer une sauvegarde :** quitter l'overlay, remplacer `playtime.db` dans le dossier
de données par le fichier voulu de `backups` (p. ex. copier `playtime-2026-10-04.db` et le
renommer en `playtime.db`), relancer l'overlay.

### Réunir deux PC

Si vous jouez sur plusieurs PC, ajoutez le temps de jeu de l'autre PC ainsi :

1. Sur l'autre PC, récupérez le fichier `playtime.db` du dossier de données (ou une
   sauvegarde de `backups`), p. ex. par clé USB ou dossier cloud.
2. Ici, **Menu → Données → Importer les sessions d'un autre PC …** et choisir le fichier.
3. SC Playtime indique combien de sessions sont nouvelles et combien existent déjà, puis
   n'importe que les nouvelles après votre confirmation. Les données actuelles sont
   sauvegardées avant.

Une session est considérée comme « déjà là » si elle chevauche dans le temps une session
du même jeu ici – le même jeu ne tourne pas sur deux PC en même temps. On peut donc
importer plus tard le même fichier sans que rien ne compte deux fois. Canal, patch et fin
sont importés aussi. Les jeux qui n'existent pas encore ici sont indiqués : leurs sessions
sont enregistrées et apparaissent dès que vous ajoutez le jeu sous le même nom.

## Comment le temps est compté

- La liste des processus est lue toutes les 2 secondes. Elle est seulement **lue** – rien
  n'est injecté dans le jeu.
- Si vous lancez l'overlay alors que le jeu tourne déjà, la session compte quand même
  depuis le vrai démarrage du jeu.
- La fin de session est enregistrée toutes les 30 secondes. Si le PC plante, ces 30
  secondes au plus sont perdues.
- Les sessions qui passent minuit (ou une limite de semaine/mois) sont réparties au
  prorata.

## Mises à jour

La version actuelle figure en haut du menu (p. ex. « SC PLAYTIME 1.5.0 »).

- **Automatique :** si « Rechercher automatiquement des mises à jour » est actif, SC
  Playtime vérifie sur GitHub peu après le démarrage puis toutes les 12 heures. S'il y a
  une nouvelle version, un message apparaît à l'icône de notification et l'entrée
  **« ⬆ Installer la mise à jour … »** en haut du menu.
- **Manuellement :** Menu → « Rechercher des mises à jour ».
- **Installer :** après confirmation, la nouvelle version est téléchargée et comparée à la
  somme de contrôle indiquée par GitHub pour la version – si elle ne correspond pas, rien
  n'est installé. L'overlay enregistre la session en cours, se ferme, remplace le
  programme et redémarre. « Nouveautés » s'affiche ensuite une fois. Réglages et
  temps de jeu sont conservés.
- Si SC Playtime tourne depuis le code source (`run.pyw`) au lieu du programme compilé,
  « Installer » ouvre la page des versions dans le navigateur – il n'y a pas de fichier
  programme à remplacer. Pour des mises à jour en un clic, utilisez l'EXE et désactivez
  puis réactivez le démarrage automatique dans le menu.

Toutes les versions sont aussi disponibles sur
<https://github.com/hofergeorg-tech/sc-playtime/releases>.

## Linux

**Programme prêt à l'emploi :** téléchargez `SC-Playtime-linux-x86_64` depuis la
[page des versions](https://github.com/hofergeorg-tech/sc-playtime/releases/latest),
placez-le p. ex. dans `~/Applications/`, rendez-le exécutable et lancez-le :

```bash
chmod +x SC-Playtime-linux-x86_64
./SC-Playtime-linux-x86_64
```

**Depuis le code source :**

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python run.pyw
```

Remarques :

- **Star Citizen sous Wine/Proton/Lutris** est détecté comme sous Windows – canal compris
  (LIVE, PTU, …), car le chemin Windows du jeu est lu aussi. Les plantages et
  déconnexions serveur ne sont détectés que sous Windows.
- **Jeux Linux natifs :** les ajouter via « Ajouter un jeu … » avec leur programme
  (régler le filtre sur « Tous les fichiers »). Ils sont reconnus à leur nom de programme.
- **Wayland :** sous Wayland, les fenêtres ne peuvent ni choisir leur position ni rester au
  premier plan. SC Playtime démarre donc automatiquement via **XWayland**, présent sur
  presque tous les bureaux. Pour un autre choix, définissez vous-même `QT_QPA_PLATFORM`.
- **Icône de notification sous GNOME :** GNOME n'affiche les icônes qu'avec l'extension
  « AppIndicator and KStatusNotifierItem Support ». KDE, XFCE, Cinnamon & co. n'ont besoin
  de rien.
- Le **démarrage automatique** s'appelle « Lancer à la connexion » dans le menu et crée
  `~/.config/autostart/sc-playtime.desktop`.
- Les **données** se trouvent dans `~/.local/share/SC-Playtime/`.

## Vos données

Tout est stocké localement (Menu → « Ouvrir le dossier des données ») :

- Windows : `%APPDATA%\SC-Playtime\`
- Linux : `~/.local/share/SC-Playtime/`

| Fichier | Contenu |
| --- | --- |
| `playtime.db` | base SQLite avec toutes les sessions (jeu, canal, début, fin, patch, fin de session) |
| `settings.json` | position, transparence, couleurs, langue, liste des jeux, dossiers de Star Citizen trouvés, … |
| `backups/` | copies quotidiennes de la base, voir [Export et sauvegarde](#export-et-sauvegarde) |

Vos temps de jeu et réglages ne quittent jamais votre PC. La seule connexion à Internet
est la recherche de mises à jour : elle ne récupère que les informations publiques de
version sur GitHub et peut être désactivée dans le menu. Pour sauvegarder ou déménager,
copiez simplement le dossier. Pour réinitialiser les réglages, supprimez `settings.json`
overlay fermé.

## Questions fréquentes

**L'overlay n'est pas visible en jeu.**
Réglez Star Citizen sur « Fenêtré sans bordure ». Vérifiez que l'overlay n'a pas été
masqué via l'icône de notification.

**Je ne peux plus cliquer sur l'overlay.**
« Laisser passer les clics » est actif. Appuyez sur **Ctrl+Maj+F11** ou faites un clic
droit sur l'icône de notification et décochez l'option.

**Le menu ou une fenêtre apparaît derrière le jeu.**
Depuis la version 1.4, menus et boîtes de dialogue s'affichent toujours devant l'overlay et
le jeu. Si une fenêtre reste cachée, passez-y avec Alt+Tab.

**Le temps de jeu est faux parce que j'ai laissé le jeu ouvert.**
Corrigez la session sous **Menu → Modifier les sessions …** et activez à l'avenir la
[détection AFK](#détection-afk).

**L'overlay a disparu.**
Un clic gauche sur l'icône de notification le réaffiche. Avec « Afficher seulement pendant
qu'un jeu tourne », il n'apparaît pas hors ligne.

**Le démarrage automatique ne fonctionne plus.**
L'entrée pointe vers l'emplacement du programme ou de `run.pyw`. Après avoir déplacé le
dossier, désactivez puis réactivez le démarrage automatique dans le menu.

**La mise à jour échoue.**
Vérifiez la connexion Internet et réessayez avec « Rechercher des mises à jour ». Si le
programme se trouve dans un dossier protégé (p. ex. `C:\Program Files` ou `/usr/bin`), il
ne peut pas se remplacer – téléchargez la nouvelle version depuis la page des versions ou
placez le programme dans son propre dossier.

**Windows affiche « Windows a protégé votre ordinateur ».**
L'EXE n'est pas encore signé numériquement (demande en cours, voir
[CODE_SIGNING.md](CODE_SIGNING.md)), SmartScreen avertit donc pour les nouveaux
téléchargements. Cliquez sur « Informations complémentaires » → « Exécuter quand même ».
Pour vérifier que le fichier a vraiment été construit depuis ce dépôt :
`gh attestation verify SC-Playtime.exe --repo hofergeorg-tech/sc-playtime`

**Est-ce que cela gêne l'anti-triche ?**
SC Playtime lit seulement la liste des processus et l'heure de démarrage du jeu via des
fonctions normales du système, comme le Gestionnaire des tâches, et après la fermeture du
jeu le fichier texte `Game.log`. Il n'accède pas au jeu.

**Une session n'a pas de fin indiquée.**
Le journal ne montrait ni fin normale ni plantage – p. ex. si Star Citizen a été fermé via
le Gestionnaire des tâches, en cas de coupure de courant, si la session s'est terminée par
une pause AFK ou s'il n'existe plus de journal. Ce classement ne sert qu'aux statistiques
et ne change rien au temps de jeu.
