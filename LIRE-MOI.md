# Morgue 3.1.12 / Bibliothèque et classement réunis

Programme conçu et développé par Simon Léturgie dans le cadre d’Eigrutel BD Academy.
Eigrutel Lab / Atelier d’outils libres pour la bande dessinée.

## Une application à lancer

Lancez **EigrutelMorgue.py**. Deux onglets partagent la même fenêtre :

- **Bibliothèque** : recherche, aperçus, favoris, collecte, export et Atelier.
- **Classer / Renommer** : nomenclature, catégories, renommage et rangement.

Depuis la Bibliothèque, l’onglet **Classer / Renommer** de la barre ouvre le second espace sur l’image sélectionnée. La navigation du renommeur parcourt alors les résultats chargés. Pour retrouver tous les fichiers du dossier à traiter, utilisez « Choisir dossier » dans Classer / Renommer et sélectionnez votre dossier. L’option « Inclure sous-dossiers » du renommeur reste disponible.

Le dossier de travail est commun aux deux espaces. Les préférences propres à chaque espace restent mémorisées. Les photos à traiter n’ont pas besoin d’être déjà renommées ; la Bibliothèque continue d’indexer les images dont le nom commence par `DOCUMENTATION_`.

## Barre de navigation

Une seule barre par espace : bleu atelier pour la Bibliothèque, rouge sombre pour Classer / Renommer. Les onglets intégrés à droite remplacent les anciens boutons de passage. L’onglet actif reste coloré ; cliquer dessus ne recharge pas votre sélection. Le sélecteur FR / EN prend la forme de deux petits boutons intégrés à cette même barre. Les deux bandeaux ont la même hauteur, adaptée à la mise à l’échelle Windows.

Les listes des niveaux occupent la hauteur disponible au-dessus des champs N1, N2 et N3. Elles peuvent se réduire et disposent chacune d’une barre de défilement.

Le bouton « i » clair ouvre une fenêtre commune avec l’aide de l’espace courant, un sommaire cliquable et une page « À propos ». Le choix du modèle de classement est accessible dans la zone d’architecture du renommeur. Sa fenêtre reprend la présentation de l’aide, avec un en-tête rouge et deux cartes de choix français/anglais. La confirmation avant remplacement de l’architecture reste obligatoire.

Les boutons « Choisir dossier » et « Ranger DOCUMENTATION » reprennent le fond papier chaud et le texte rouge sombre du bouton « i ». Les titres de niveaux, leurs menus, les boutons d’effacement et « Renommer » utilisent le rouge sombre. La fenêtre d’information reprend la palette du programme, avec une hiérarchie de titres et des sections pour la conception, la version et les licences.

Couleurs issues du [nuancier Eigrutel](https://www.stripmee.com/design/).

## Français / English

Le sélecteur **FR / EN**, en haut de la fenêtre, change la langue de l’interface, des aides et de l’Atelier sans redémarrage. Le choix est mémorisé. Il ne modifie ni les fichiers ni les catégories, ni la recherche ou l’image sélectionnée.

Le bouton **Classement : FR / EN** choisit séparément le modèle de catégories et les mots de nomenclature pour le dossier de travail courant. Le modèle anglais reprend l’architecture de l’ancien renommeur anglais, par exemple `Animals / Horses`. Une confirmation précède le remplacement de l’architecture : exportez d’abord vos catégories personnalisées si vous souhaitez les conserver. Les fichiers existants ne sont jamais renommés par ce choix.

Le préfixe reste **`DOCUMENTATION_`** dans les deux langues. Les prochains noms utilisent les catégories sélectionnées et la langue de classement choisie : `Couleur` devient par exemple `Color` dans le modèle anglais. Vos précisions personnelles restent telles que vous les saisissez.

Chaque dossier de travail conserve son architecture complète et sa langue de classement dans `morgue_settings.json`, y compris les suppressions de catégories. L’export d’architecture inclut également la langue de classement. Une ancienne architecture sans cette information conserve la langue de classement courante lors de son import.

La recherche accepte `nom:` et `name:`, ainsi que `dossier:` et `folder:`, quelle que soit la langue d’interface. Elle ne traduit pas les mots recherchés : `cheval` ne recherche pas automatiquement `horse`.

Instructions in English: **README-EN.md**.

## Installation et reprise des données

Fermez les anciens programmes. Conservez une copie de votre dossier de travail logiciel avant le premier essai de cette fusion.

Extrayez tous les fichiers de cette archive dans le même dossier logiciel que vos données existantes, ou dans une copie complète de ce dossier pour l’essai. Les modules internes doivent rester ensemble. Ne lancez que `EigrutelMorgue.py`.

Les données antérieures restent reconnues :

- `index_documentation.db` : index, favoris et collecte ;
- `index_documentation_settings.json` : préférences Bibliothèque ;
- `settings.json` : préférences du renommeur ;
- `documentation_structure_user.json` : architecture personnalisée ;
- `index_documentation_thumbs` : cache de vignettes ;
- `logs` : journaux existants.

Le nouveau fichier `morgue_settings.json` mémorise le dossier partagé. Les noms historiques des fichiers de données sont conservés pour éviter une migration inutile. Au premier lancement, le dossier de la Bibliothèque est prioritaire, à défaut celui du renommeur.

Les fichiers `Morgue.png` et `Morgue.ico` sont fournis : ils reprennent votre icône et remplacent la plume Tkinter dans les fenêtres. Le fichier ICO contient neuf tailles de 16 à 256 pixels. Conservez votre éventuel `DOC.ico` pour les icônes des dossiers Windows ; il est distinct de l’icône du programme.

Sources : Python 3.10 ou ultérieur, avec Tkinter, et Pillow. Installation de Pillow depuis ce dossier :

```text
py -3 -m pip install -r requirements.txt
py -3 EigrutelMorgue.py
```

## Renommage et rangement synchronisés

Les opérations effectuées dans cette application mettent immédiatement à jour l’index : pas besoin de réindexer toute la collection après chaque renommage. Les favoris et la collecte suivent le fichier. Le rangement vers une autre racine Documentation transfère aussi ses indicateurs vers cette racine ; l’application affiche le dossier de destination à la fin du rangement.

En cas de collision, le renommage refuse d’écraser le fichier cible. Si l’écriture SQL échoue après le déplacement, l’application tente de remettre le fichier à son ancien emplacement et signale une éventuelle impossibilité de restauration.

Pendant une réindexation, les renommages, le rangement et le changement de dossier sont bloqués pour éviter de remplacer l’index avec des chemins périmés. La fermeture attend la fin de l’interruption de cette indexation.

Les changements effectués avec l’Explorateur ou un ancien programme indépendant nécessitent toujours une réindexation et ne bénéficient pas de cette liaison. N’utilisez pas simultanément les anciens programmes pour modifier les mêmes fichiers.

Le retour à la Bibliothèque conserve les images déjà chargées si aucun fichier n’a changé. Après une modification effectuée dans le renommeur, la recherche est rafraîchie après l’affichage du bandeau, en réutilisant les vignettes valides.

## Recherche et Atelier

Recherches possibles : `cheval rouge`, `cheval -rouge`, `-chat`, `"scene de rue"`, `nom:cheval`, `dossier:costume`, `ext:jpg`.

Les accents et la casse sont ignorés. Les mots sont recherchés dans les noms et les dossiers, pas dans le contenu visuel des images. Un bouton charge les résultats suivants par tranches de 500. La collecte des résultats et l’Atelier depuis la recherche utilisent les résultats chargés.

Dans Classer / Renommer, la recherche parcourt la hiérarchie complète ; les flèches parcourent les suggestions et Entrée valide la suggestion. Taper ne change pas les catégories choisies.

L’Atelier conserve sa fenêtre de session. Ses raccourcis lui sont propres et ne doivent plus affecter les onglets de la fenêtre principale.

## Construire un seul Morgue-3.1.12.exe

Sur votre PC Windows avec Python installé, double-cliquez sur **Construire_Morgue.cmd**. Ce script crée un environnement Python `.venv`, installe les dépendances de construction puis fabrique **dist/Morgue-3.1.12.exe**. La première construction nécessite une connexion Internet pour télécharger les dépendances.

Placez ensuite `Morgue-3.1.12.exe` dans votre dossier habituel contenant la base, les réglages et l’architecture, puis lancez-le. Les modules Python sont inclus dans l’exécutable ; ils n’ont pas à l’accompagner pour l’utilisation courante. Les données et réglages restent à côté de l’exécutable : choisissez donc un dossier où vous pouvez écrire.

La construction inclut `Morgue.ico` comme icône de l’exécutable et embarque les deux ressources `Morgue.ico` et `Morgue.png`. Il faut reconstruire `Morgue-3.1.12.exe` pour remplacer son icône ; changer les sources ne modifie pas un ancien exécutable. L’icône embarquée est prioritaire : un ancien fichier laissé à côté de l’exécutable ne la remplace plus. Les sources restent utiles pour modifier le programme ou le reconstruire.

Le script utilise les options `--onefile` et `--windowed` décrites dans la [documentation officielle de PyInstaller](https://pyinstaller.org/en/stable/usage.html).

**Aucun exécutable Windows précompilé n’est livré dans cette archive.** La construction n’a pas été exécutée dans cet environnement Linux.

## Manuel complet intégré

Dans les deux espaces, ouvrez **i**, puis **Manuel complet** en bas du panneau. Le bouton reste accessible depuis l’aide et depuis À propos. Le manuel s’ouvre dans votre navigateur, hors connexion, en français ou anglais selon la langue active de Morgue au moment du clic.

Le fichier `Manuel-Morgue.html` est inclus dans cette archive et embarqué par la construction Windows. Ne le retirez pas avant de construire l’exécutable. Les sources Markdown sont dans `docs`. L’exécutable final n’a pas besoin d’un manuel HTML placé à côté : il en conserve une copie de lecture dans `%LOCALAPPDATA%\Morgue\manuals`, qui reste disponible après fermeture du programme. Une nouvelle édition du manuel utilise une nouvelle copie, sans réutiliser l’ancienne par erreur.

## Vérifications

Compilation Python et imports réussis. **49 tests automatisés réussis** : 18 tests de fusion et de navigation, 11 tests bilingues et 7 tests d’icônes et 6 tests d’infobulles et de barre de titre, et 7 tests du manuel intégré. Ils couvrent notamment le renommage avec préservation des favoris, les collisions, le retour arrière sur erreur SQL, les langues indépendantes, les noms de fichiers, les champs de recherche et la sauvegarde des catégories personnalisées.

Exécutez les tests inclus depuis le dossier décompressé :

```text
py -3 -m unittest -v test_morgue_fusion test_morgue_bilingual test_morgue_icons test_morgue_tooltips test_morgue_manual
```

Les variables traduites ont été vérifiées avec Tcl. **L’affichage graphique et la construction de l’exécutable Windows restent à valider sur votre PC** : aucun serveur graphique n’est disponible dans l’environnement de préparation. Vérifiez notamment la disposition des commandes, le passage FR / EN dans les deux onglets, une fenêtre Atelier ouverte et les modèles de classement sur une copie de votre bibliothèque.

## Licences

Code source et programme compilé : GNU AGPL v3.0 ou version ultérieure.
Documentation et ressources : CC BY-SA 4.0, sauf mention contraire.
Les bibliothèques tierces conservent leurs licences respectives.
Marques, logos et signes distinctifs Eigrutel / Eigrutel Lab / Eigrutel BD Academy : réservés.

Ces mentions figurent aussi dans les en-têtes du programme et dans « À propos ».

## Correctif icône Windows (3.1.12)

L’ICO utilise désormais neuf images bitmap 32 bits, et la fenêtre reçoit explicitement son icône. Une solution de repli PNG est prévue si Windows refuse l’ICO ; si les deux méthodes échouent, un diagnostic est écrit dans `logs/morgue-icons.log`.

Le script de construction vérifie les ressources d’icône réellement présentes dans le fichier EXE avant d’annoncer une réussite. Lancez **dist/Morgue-3.1.12.exe**, et non un ancien Morgue.exe. Le nom versionné distingue les fichiers et évite de réutiliser exactement le même chemin dans le cache d’icônes. Si vous utilisez un raccourci épinglé vers l’ancienne version, remplacez-le par un raccourci vers ce nouveau fichier.

La compilation et l’affichage Windows doivent toujours être vérifiés sur votre ordinateur ; ils ne sont pas exécutés ici.

## Icône de la barre des tâches (3.1.12)

Après affichage de la fenêtre, Morgue applique explicitement ses petites et grandes icônes à la fenêtre native Windows. Le réglage est réappliqué quand la fenêtre est de nouveau affichée. Une identité Windows propre à Morgue distingue le programme de Tkinter.

Reconstruisez puis lancez `Morgue-3.1.12.exe`. Si la plume correspond à un ancien raccourci épinglé, détachez cet ancien raccourci puis épinglez le nouveau programme. Ne lancez pas l’ancien raccourci pour tester le correctif. Le contrôle visuel Windows reste à effectuer sur votre ordinateur.

## Infobulles et barre de titre (3.1.12)

Les boutons affichent une aide en français ou anglais après un survol de 550 ms. Les infobulles disparaissent au départ du pointeur, au clic, à la frappe ou au changement d’espace/langue. Le bouton « i » ouvre le panneau d’information : la case **Afficher les infobulles**, en bas, permet de les désactiver pour tout le programme. Le choix est conservé dans `morgue_settings.json` et partagé par les fenêtres d’information ouvertes.

Sous Windows 11, la barre de titre native prend le bleu sombre de la Bibliothèque ou le rouge sombre du renommeur, avec un texte clair. Les boutons système restent natifs. Sur les systèmes ne prenant pas en charge cette option, la barre conserve son apparence système. Référence : [attributs de fenêtre DWM Microsoft](https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute).

La logique des infobulles et le choix des couleurs sont testés automatiquement ; le rendu Windows reste à contrôler sur votre PC.

## Finition des bandeaux et textes (3.1.12)

Le contour Windows est désactivé via DWM quand cette option est disponible. Le conteneur des espaces utilise un habillage plat, sans bordure, dans la couleur du bandeau actif, afin de supprimer le raccord gris sous le titre. Le déplacement, le redimensionnement et les boutons de fenêtre restent gérés par Windows. Le résultat visuel reste à vérifier sur votre configuration.

Les tirets cadratins et demi-cadratins des textes fournis, de l’aide, des crédits et du titre ont été remplacés par des barres obliques ou des tirets simples. Les noms de fichiers et les données personnelles ne sont pas modifiés.

## Raccord du renommeur (3.1.12)

La zone Classer / Renommer rejoint directement le dessous du bandeau, comme la Bibliothèque. Les marges sont placées à l’intérieur du conteneur clair, ce qui évite de laisser apparaître le fond beige du thème autour des panneaux.
