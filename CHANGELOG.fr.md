# Journal des modifications

🇩🇪 [Deutsch](CHANGELOG.md) · 🇬🇧 [English](CHANGELOG.en.md) · 🇪🇸 [Español](CHANGELOG.es.md) · 🇮🇹 [Italiano](CHANGELOG.it.md) · 🇵🇱 [Polski](CHANGELOG.pl.md) · 🇨🇳 [简体中文](CHANGELOG.zh.md)

Toutes les modifications notables de SC Playtime. Format inspiré de
[Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).

## [1.6.0] – 2026-10-17

### Nouveautés
- **Anti-AFK** (Windows) : Menu → Anti-AFK garde Star Citizen éveillé. Appuie à intervalles
  réguliers sur la touche à droite de P (par défaut toutes les 5 s) et/ou bouge la souris selon
  un petit motif (droite–gauche, haut–bas, carré, cercle, aléatoire ; amplitude, vitesse et
  rythme réglables). De vrais scancodes sont envoyés – uniquement si le jeu est au premier plan.
  Activation par le menu ou **Ctrl+Maj+F12** ; des anneaux à côté de l'horloge montrent le rythme
  et activent l'action d'un clic. Ses saisies ne comptent pas pour la détection AFK.

## [1.5.0] – 2026-10-09

### Nouveautés
- **Plantages et déconnexions serveur par patch :** après la fermeture du jeu, SC Playtime
  lit le `Game.log` de Star Citizen et retient si vous avez quitté, si le jeu a planté ou si
  le serveur a coupé la connexion. L'analyse affiche par patch les plantages (p. ex.
  « 2 · toutes les 6h 30m ») et les déconnexions, la fenêtre des sessions une colonne
  « Issue ». Les sessions plus anciennes sont classées au démarrage à partir des journaux
  sauvegardés (`logbackups`).
- **Déroulé de la journée** dans l'analyse : une journée en frise de 0 à 24 h avec toutes
  les sessions dans la couleur de leur canal, les pauses en trous, plantage (rouge) et
  déconnexion serveur (jaune) en marques ; ‹ › passe d'un jour joué à l'autre.
- **Réunir deux PC :** Menu → Données → « Importer les sessions d'un autre PC … » ajoute le
  temps de jeu du `playtime.db` (ou d'une sauvegarde) d'un autre PC. Les sessions déjà
  présentes sont reconnues et ignorées ; les données actuelles sont sauvegardées avant.
- **Depuis quand on compte :** la tuile TOTAL affiche en haut à droite la date du premier
  enregistrement.
- **Aide et journal des modifications dans les sept langues** (avant : allemand et anglais
  seulement).

### Modifications
- L'export CSV/JSON contient une colonne `ending` (`quit`, `crash`, `server`).

## [1.4.1] – 2026-10-09

### Améliorations
- **Overlay plus rapide avec un long historique :** les statistiques étaient recalculées
  entièrement chaque seconde, et le travail croissait au carré du nombre de sessions
  (1,5 s pour 5000 sessions – chaque seconde, au-dessus du jeu). Les sessions terminées
  sont maintenant évaluées une seule fois et seule la session en cours est ajoutée chaque
  seconde : 2 ms au lieu de 1500 ms.
- Le point pulsant redessine l'overlay 8 fois par seconde au lieu de 16.

### Sécurité
- Les mises à jour ne sont installées que si le fichier téléchargé correspond à la somme de
  contrôle indiquée par GitHub pour la version.
- Les réglages sont d'abord écrits entièrement dans un fichier temporaire puis échangés –
  un plantage pendant l'enregistrement ne les remet plus à zéro.

## [1.4.0] – 2026-10-04

### Nouveautés
- **Remonter dans le graphique :** pour JOUR, SEMAINE et MOIS, les flèches ‹ › en haut à
  droite du graphique reculent dans le passé, la molette pas à pas – jusqu'à la première
  session.
- **Analyse** (Menu → Analyse …) : carte de chaleur « Quand joues-tu ? » par jour et heure,
  plus le **temps de jeu par patch**. La version de Star Citizen (p. ex. 4.3.1) est
  désormais lue dans le dossier d'installation et enregistrée avec chaque session.
- **Modifier les sessions** (Menu → Modifier les sessions …) : corriger début et fin ou
  supprimer des sessions, p. ex. après une mise en veille avec le jeu ouvert.
- **Détection AFK** (Menu → Détection AFK) : pause facultative après 5 à 30 minutes sans
  saisie ; la session se termine à la dernière touche et une nouvelle commence à la saisie
  suivante. L'overlay affiche alors « AFK ».
- **Raccourcis globaux** (Windows) : Ctrl+Maj+F9 affiche/masque l'overlay, Ctrl+Maj+F11
  active/désactive « Laisser passer les clics » – même en jeu. À modifier sous Menu →
  Raccourcis clavier ….
- **Export** de toutes les sessions en CSV (pour Excel) ou JSON (Menu → Données).
- **Sauvegarde automatique :** une copie de la base de données par jour dans `backups`, les
  7 dernières sont conservées ; plus « Sauvegarder maintenant » dans le menu.
- **Nouvelles langues :** Français, Español, Italiano, Polski et 简体中文 (aide et journal
  des modifications alors en anglais).
- **À propos de SC Playtime** dans le menu, avec version, liens et bouton de don (PayPal).

### Corrections
- Le menu contextuel (ainsi que le sélecteur de couleur ou les messages) disparaissait
  souvent derrière l'overlay ou le jeu. Menus et boîtes de dialogue restent maintenant
  toujours au premier plan, et l'overlay ne passe plus devant tant que l'un d'eux est
  ouvert.

## [1.3.2] – 2026-09-29

### Corrections
- **Graphique avec filtre de canal :** avec p. ex. PTU sélectionné, le graphique semblait
  identique à TOUS, car il s'adaptait toujours à sa plus grande barre – 6 minutes de PTU
  remplissaient la hauteur comme 11 heures au total. L'échelle reste maintenant celle de
  TOUS, le total est affiché en gris derrière et le canal choisi est dessiné en couleur
  devant. Le survol affiche « PTU 6m / 11h 31m ».

## [1.3.1] – 2026-09-29

### Nouveautés
- **Preuve de provenance :** chaque fichier publié peut être vérifié via une attestation
  GitHub (`gh attestation verify …`). La signature Windows via SignPath Foundation a été
  demandée et est préparée dans la compilation.
- Licence : MIT.
- Aide : section sur l'avertissement SmartScreen.

## [1.3.0] – 2026-09-29

### Nouveautés
- **Langue anglaise :** Menu → Langue avec drapeaux (🇩🇪 Deutsch, 🇬🇧 English) ou
  « Automatique » selon la langue du système. Overlay, menu, messages, aide et journal des
  modifications sont entièrement traduits ; d'autres langues s'ajoutent facilement.
- **Prise en charge de Linux :** détection des processus via `/proc` (y compris Star
  Citizen sous Wine/Proton/Lutris avec canal), démarrage automatique via
  `~/.config/autostart`, données dans `~/.local/share/SC-Playtime`, démarrage automatique
  via XWayland. Programme prêt à l'emploi `SC-Playtime-linux-x86_64` dans la version,
  mise à jour automatique aussi sous Linux.
- Compilations et tests automatiques pour Windows et Linux via GitHub Actions.

### Corrections
- Les messages (p. ex. « Pas de mise à jour ») affichaient un texte sombre sur fond sombre et
  semblaient vides.

## [1.2.0] – 2026-09-29

### Nouveautés
- **Fonction de mise à jour :** vérifie sur GitHub au démarrage et toutes les 12 heures
  s'il existe une nouvelle version. Si oui, un message apparaît à l'icône de notification
  et « Installer la mise à jour » en haut du menu. L'EXE télécharge la nouvelle version, se
  remplace et redémarre – la session en cours est enregistrée avant.
- Menu : **Rechercher des mises à jour** et **Rechercher automatiquement des mises à jour**
  (désactivable).
- Menu : **Aide** et **Nouveautés** ouvrent l'aide et le journal des modifications
  directement dans le programme, même hors ligne.
- Après une mise à jour, « Nouveautés » s'affiche automatiquement une fois.
- Numéro de version dans le titre du menu et dans les fenêtres.

## [1.1.0] – 2026-09-29

### Nouveautés
- **Couleurs réglables** (Menu → Couleurs) :
  - *Tuiles de statistiques (en jeu)* : modèles Vert, Cyan, Ambre ou « Sans couleur », plus
    libre choix des couleurs de fond et de texte.
  - *Canal actif* : modèles pour la puce de canal sélectionnée plus libre choix des
    couleurs.
- Les tuiles de statistiques sont colorées pendant que le jeu tourne (par défaut : vert avec
  texte foncé). Hors ligne, elles restent sombres dans le style HUD.
- Aide (`HILFE.md`) décrivant toutes les fonctions.

### Corrections
- Pendant le jeu, les tuiles et puces de canal étaient remplies par erreur de vert clair,
  rendant le texte blanc difficile à lire. En cause : la couleur de remplissage du point
  d'état, restée active ensuite.

## [1.0.0] – 2026-09-28

Première version.

### Nouveautés
- Overlay sans bordure dans le style HUD de Star Citizen, toujours au premier plan.
- Détection automatique de `StarCitizen.exe` (liste des processus, toutes les 2 s, en
  lecture seule).
- Détection du canal depuis le dossier d'installation : LIVE, PTU, EPTU, HOTFIX,
  TECH-PREVIEW ; statistiques par canal ou ensemble.
- Plusieurs jeux : ajouter et retirer n'importe quel EXE.
- Vue compacte : horloge de session, aujourd'hui, semaine.
- Statistiques dépliées : tuiles (aujourd'hui, semaine, mois, année, total, série),
  graphique en barres jour / semaine / mois / année / total avec valeurs au survol,
  sessions, moyenne et session la plus longue.
- Transparence du fond et transparence globale réglables séparément.
- Verrouiller la position, laisser passer les clics, n'afficher que pendant qu'un jeu
  tourne.
- Icône de notification, instance unique, démarrage avec Windows (sans administrateur).
- Stockage en SQLite dans `%APPDATA%\SC-Playtime\` ; fin de session enregistrée toutes les
  30 s.
- Compilation en un seul EXE via PyInstaller (`build.py`).
