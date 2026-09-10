# Morgue / Manuel d’utilisation

**Bibliothèque, classement et étude de références visuelles**

Manuel pour Morgue 3.1.12 / Édition du 10 septembre 2026.

Programme conçu et développé par Simon Léturgie dans le cadre d’Eigrutel BD Academy. Eigrutel Lab / Atelier d’outils libres pour la bande dessinée.

Ce manuel accompagne l’application de bureau Python et son exécutable Windows. Il se lit indépendamment du programme. La version HTML contient les éditions française et anglaise, un sommaire, une recherche et une présentation pour l’impression. Elle fonctionne hors connexion ; son sélecteur de langue ne change pas celui de Morgue.

## 1. Comprendre Morgue

Morgue rassemble dans une seule application les fonctions des anciens programmes Documentation Renamer et Index Documentation. Vous préparez vos références, les retrouvez puis les utilisez pour dessiner sans lancer deux logiciels.

Deux espaces partagent la même fenêtre et le même dossier de travail : **Bibliothèque**, au bandeau bleu sombre, et **Classer / Renommer**, au bandeau rouge sombre. L’**Atelier**, accessible depuis Bibliothèque, ouvre une fenêtre d’étude et de dessin chronométré.

Le principe documentaire repose sur les **noms des fichiers et des dossiers**. Morgue ne reconnaît pas automatiquement ce que représente une image, ne traduit pas son sujet et n’effectue pas de recherche visuelle par intelligence artificielle. Une photographie de cheval nommée `IMG_4582.jpg` ne sera pas retrouvée en tapant « cheval » si ce mot n’apparaît pas dans les informations recherchées.

Le préfixe commun **`DOCUMENTATION_`** permet à la Bibliothèque d’identifier les images à indexer. Il reste identique en français et en anglais. Vos images restent des fichiers ordinaires sur votre disque ; l’index est un catalogue qui permet de les retrouver, pas une copie de ces images.

## 2. Installer et ouvrir

### Utiliser l’exécutable Windows

Placez `Morgue-3.1.12.exe` dans un dossier où vous avez le droit d’écrire, puis ouvrez-le. Python n’est pas nécessaire pour utiliser un exécutable déjà construit. Les ressources et modules nécessaires à l’application sont inclus dans cet exécutable ; les données de travail et les réglages sont enregistrés à côté de lui.

Le dossier du programme et votre dossier d’images ont des rôles différents : le premier contient le logiciel et ses données de fonctionnement ; le second contient les références à consulter et à classer. Choisissez ce dernier dans Morgue.

### Utiliser les sources Python

Conservez ensemble tous les fichiers de l’archive du programme. Avec Python 3.10 ou ultérieur et Tkinter disponibles, ouvrez un terminal dans ce dossier et exécutez :

```text
py -3 -m pip install -r requirements.txt
py -3 EigrutelMorgue.py
```

Pour fabriquer l’exécutable sur Windows, lancez **Construire_Morgue.cmd**. La première construction télécharge les dépendances ; le résultat se trouve dans `dist/Morgue-3.1.12.exe`. Modifier un fichier Python ne met pas à jour un exécutable déjà construit.

### Formats acceptés

Morgue reconnaît les images `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tif` et `.tiff`. Les PDF, vidéos, documents texte et fichiers Photoshop ne font pas partie de ce parcours. Une extension reconnue ne garantit pas qu’un fichier endommagé sera lisible.

La Bibliothèque exige aussi le préfixe `DOCUMENTATION_`. Classer / Renommer accepte les images compatibles avant leur renommage. L’Atelier peut ouvrir un fichier ou un dossier externe sans exiger ce préfixe.

## 3. Première utilisation

### Vos images ne sont pas encore préparées

1. Ouvrez **Classer / Renommer**, puis **Choisir dossier**.
2. Cochez **Inclure sous-dossiers** si les images sont réparties dans plusieurs dossiers.
3. Choisissez vos niveaux de classement, puis les marqueurs utiles et éventuellement une précision.
4. Lisez le **Nom cible** et cliquez sur **RENOMMER (Entrée)**. Le programme passe à l’image suivante.
5. Pour organiser aussi les dossiers physiques, utilisez **Ranger DOCUMENTATION**, décrit au chapitre 12.
6. Passez dans **Bibliothèque**, vérifiez le dossier choisi et lancez **Indexer / Réindexer** pour établir le catalogue initial de votre ensemble.

### Vos images portent déjà des noms DOCUMENTATION_

1. Dans Bibliothèque, cliquez sur **charger DOCUMENTATION** et choisissez la racine de votre documentation.
2. Cliquez sur **Indexer / Réindexer**. Les sous-dossiers sont inclus dans cette indexation.
3. Attendez la fin, puis saisissez un mot présent dans un nom de fichier ou un dossier.
4. Cliquez sur une vignette pour examiner l’image. Marquez-la comme favorite ou ajoutez-la à la collecte si elle vous intéresse.

Une réindexation n’est pas nécessaire après chaque renommage réalisé dans Morgue : les modifications internes sont synchronisées avec l’index. Elle reste utile pour découvrir un ensemble existant ou des changements effectués hors de Morgue.

## 4. Navigation, langues et aide

Le titre **Morgue** reste à la même place dans les deux bandeaux. Les boutons de navigation indiquent aussi leur destination par leur couleur : rouge pour Classer / Renommer, bleu sombre pour Bibliothèque. Cliquer sur l’espace déjà actif ne recommence pas le parcours.

Depuis Bibliothèque, **Classer / Renommer** reprend l’image sélectionnée et les résultats actuellement chargés. Les boutons Précédent et Suivant du renommeur parcourent alors cet ensemble. Pour traiter tout un dossier, utilisez **Choisir dossier** dans le renommeur. Ne confondez pas ce parcours limité aux résultats avec le rangement automatique, qui examine le dossier source selon l’option sous-dossiers.

**FR / EN** change immédiatement les commandes et les aides. Le choix est mémorisé, mais vos fichiers, catégories et mots de recherche ne sont pas traduits. Le bouton **Classement…**, dans Classer / Renommer, choisit séparément le modèle de catégories et le vocabulaire des futurs noms. Voir le chapitre 11.

Le **i du bandeau** ouvre l’aide de l’espace courant et la page **À propos**, avec sommaire cliquable. Le bouton **Manuel complet**, en bas du panneau, ouvre ce manuel dans votre navigateur, hors connexion et dans la langue active de Morgue. Il est accessible depuis les deux espaces et depuis les pages Aide et À propos. Le manuel est inclus dans l’exécutable ; la page reste consultable après la fermeture de Morgue. La case **Afficher les infobulles** active ou désactive les aides au survol pour tout le programme. Ce choix est conservé entre les ouvertures. Le **petit i sous l’image du renommeur** affiche les métadonnées du fichier : c’est une autre fonction.

Sur les versions compatibles de Windows, la barre de titre adopte la couleur de l’espace actif. Si cette personnalisation n’est pas prise en charge, Windows conserve son habillage habituel.

## 5. Bibliothèque : indexer et parcourir

La Bibliothèque présente les vignettes à gauche, une grande image au centre et les commandes de recherche, collecte et Atelier à droite. Le nombre d’images indexées décrit le catalogue ; le nombre de résultats dépend de la recherche courante.

**Indexer / Réindexer** analyse le dossier choisi et ses sous-dossiers. L’ancien index reste disponible jusqu’à la réussite de la nouvelle indexation. **Échap** permet d’interrompre l’opération. Pendant ce traitement, Morgue bloque le renommage, le rangement et le changement de dossier pour éviter des chemins incohérents.

Les résultats se chargent par **tranches de 500**. Une indication comme `500 / 9491` signifie que 500 correspondances sont chargées sur 9 491. Utilisez le bouton de chargement supplémentaire au bas de la grille pour poursuivre. La commande de collecte de tous les résultats et la source « Recherche actuelle » de l’Atelier utilisent uniquement les résultats chargés.

| Geste ou commande | Effet |
| --- | --- |
| Clic sur une vignette | Sélectionner l’image et l’afficher au centre. |
| Double-clic sur une vignette | Ouvrir le fichier dans l’application associée du système. |
| Molette sur les résultats | Faire défiler les vignettes. |
| Précédent / Suivant | Parcourir les résultats chargés. |
| Ouvrir image | Ouvrir l’image courante dans votre visionneuse habituelle. |
| Ouvrir dossier | Accéder à son emplacement sur le disque. |

Sous l’aperçu, le nom et le dossier permettent de retrouver le fichier réel. L’image affichée est un aperçu ; son affichage ne transforme pas le fichier source.

## 6. Rechercher efficacement

La recherche ignore la casse et les accents et accepte des fragments de mots. Plusieurs termes doivent tous correspondre, éventuellement dans des endroits différents du nom et du chemin. Une courte temporisation lance la recherche pendant la frappe ; **Entrée** la déclenche immédiatement.

| Requête | Résultat recherché |
| --- | --- |
| `cheval` | Présence de ce fragment dans le nom ou le chemin. |
| `cheval rouge` | Présence des deux termes. |
| `cheval -course` | Cheval, en excluant les correspondances contenant course. |
| `-chat` | Exclusion seule, sans terme positif obligatoire. |
| `"scene de rue"` | Groupe de mots recherché ensemble dans le texte normalisé. |
| `nom:cheval` | Recherche limitée au nom du fichier. |
| `dossier:costume` | Recherche limitée au chemin du dossier. |
| `ext:jpg` | Extension jpg ; jpeg est une extension distincte. |
| `dossier:costume -nom:essai` | Dossier contenant costume, sans essai dans le nom. |

Les alias anglais **`name:`** et **`folder:`** fonctionnent aussi lorsque l’interface est en français. Les alias français fonctionnent en anglais. En revanche, `cheval` et `horse` ne sont pas traduits l’un en l’autre : recherchez les termes réellement présents dans votre documentation.

Les underscores des noms sont également interprétés comme des séparateurs de mots pendant la recherche. Ainsi, `"scene de rue"` peut retrouver `scene_de_rue`. Sans guillemets, `scene rue` impose les deux termes sans imposer leur proximité.

Les cases **Composition, Forme, Silhouette, Couleur, Lumière, Valeurs, Échelle** ajoutent leurs mots à la recherche. Elles n’analysent pas l’image. Plusieurs cases cumulent les critères. Les mots insérés correspondent à la langue de classement, pas nécessairement à celle de l’interface.

**Favoris** et **Collecte** limitent la recherche aux images marquées. Si les deux sont cochés, les images appartenant à l’un **ou** à l’autre groupe sont retenues, tout en respectant les autres termes de recherche. Les boutons **=★** et **=☑** du bandeau activent ces filtres ; ils ne marquent pas l’image courante.

**Reset recherche** vide la requête et désactive les filtres. Il n’efface ni les fichiers, ni les favoris, ni la collecte. Dans le champ Recherche, les flèches haut et bas rappellent l’historique ; le clic droit permet de l’effacer.

Commencez par un terme simple. Si les résultats sont trop nombreux, ajoutez une notion d’usage graphique, un dossier ou une exclusion. Si la recherche ne donne rien, retirez les filtres avant de conclure que l’image manque.

## 7. Favoris, collecte et export

Un **favori** désigne une référence que vous souhaitez retrouver durablement. La **collecte** constitue une sélection de travail, par exemple pour une scène ou un album. Les deux indicateurs sont indépendants et mémorisés par bibliothèque ; la collecte n’est pas effacée simplement en fermant Morgue.

| Commande | Effet |
| --- | --- |
| Étoile sous l’aperçu | Ajouter ou retirer le favori de l’image courante. |
| Petit carré sur une vignette | Ajouter ou retirer cette image de la collecte. |
| Carré sous l’aperçu / bouton Image | Ajouter ou retirer l’image courante de la collecte. |
| Tous les résultats | Ajouter à la collecte les résultats actuellement chargés. |
| Afficher collecte | Afficher la collecte en effaçant la recherche textuelle courante. |
| Purger collecte | Retirer tous les indicateurs de collecte après confirmation. Les images restent sur le disque. |
| Exporter collecte | Copier les images collectées dans le dossier de votre choix. |

L’export concerne l’ensemble de la collecte indexée de la bibliothèque active, même si toutes ses vignettes ne sont pas chargées. Il rassemble les copies dans le dossier choisi, sans reproduire l’arborescence d’origine. Un nom déjà présent reçoit un suffixe pour éviter l’écrasement. Les erreurs de copie sont signalées ; les originaux restent en place.

Une méthode utile consiste à collecter largement pour un projet, puis à marquer comme favorites les références les plus claires. Le marqueur **Master** du nom de fichier est encore autre chose : cocher Master dans le renommeur ne crée pas automatiquement un favori dans la base.

## 8. Corriger un nom depuis Bibliothèque

Sélectionnez l’image, modifiez le champ sous l’aperçu et cliquez sur **Renommer**, ou utilisez **Ctrl+Entrée dans ce champ**. Cette commande renomme réellement le fichier dans son dossier et actualise l’index.

Conservez l’extension d’origine. Si vous l’omettez, Morgue la remet ; si vous tentez de la changer, il le refuse. Les noms vides, les caractères interdits sous Windows et les collisions sont refusés. Changer un nom de fichier ne convertit pas son format.

Conservez aussi le préfixe `DOCUMENTATION_` pour que le document reste admissible à l’indexation. Un nom modifié peut ne plus correspondre à la recherche en cours et donc disparaître des résultats sans que le fichier ait été supprimé.

Pour construire un nom à partir des niveaux, des types et des usages graphiques, passez dans **Classer / Renommer**.

## 9. Classer / Renommer : construire les noms

À gauche se trouvent l’image, le **Nom actuel**, le **Nom cible** et la navigation. À droite se trouvent les types, les usages graphiques, l’architecture des niveaux et les champs de réglage.

**Choisir dossier** charge les images compatibles. **Inclure sous-dossiers** étend le parcours aux dossiers descendants ; modifier cette option recharge la liste. L’indicateur `x / y` donne votre position dans les images chargées, pas le nombre de fichiers déjà renommés avec succès.

### Du général au particulier

Sélectionnez un **Niveau 1**, puis un **Niveau 2** appartenant au premier. Cochez ensuite, si nécessaire, un ou plusieurs **Niveaux 3** de cette branche. Par exemple, une structure personnelle pourrait contenir `Animaux > Chevaux > Profil`. Cet exemple illustre la méthode ; vous pouvez créer les termes absents de votre modèle.

Changer le parent actualise les niveaux disponibles. Les petits menus à côté des titres ouvrent une sélection plus confortable. Les listes disposent d’un défilement lorsque toutes les entrées ne tiennent pas à l’écran.

### Types et usages graphiques

| Marqueur | Utilité documentaire |
| --- | --- |
| PHOTO / Dessin | Indiquer la nature de la référence. |
| Master | Signaler une référence particulièrement utile ou exemplaire. |
| Composition | Organisation des masses, cadrage et circulation du regard. |
| Forme / Silhouette | Volumes, contours et lisibilité d’une pose. |
| Couleur | Harmonies, dominantes et rapports colorés. |
| Lumiere / Valeurs | Éclairage et répartition des clairs et des foncés. |
| Echelle | Rapports de taille et repères dimensionnels. |
| Marche / Course / Combat | Appuis, mouvement et narration gestuelle. |

Les niveaux décrivent le sujet ; les marqueurs décrivent aussi son intérêt pour le dessin. Cochez les usages réellement utiles pour éviter que toutes les images portent toutes les étiquettes. Les dix cases d’usage affichées dans cette version sont celles du tableau ; « Saut », cité dans une ancienne aide, n’est pas une case proposée dans ce panneau.

### Ordre du nom automatique

```text
DOCUMENTATION_N1_N2_N3_Type_Inspiration_Precision_001.jpg
```

Les parties non renseignées sont omises. Plusieurs N3, types ou inspirations peuvent se succéder. Exemple avec un modèle personnalisé :

```text
DOCUMENTATION_Animaux_Chevaux_Profil_PHOTO_Valeurs_contrejour_001.jpg
```

Les éléments automatiques sont nettoyés : accents retirés, espaces remplacés par `_`, caractères interdits supprimés et éléments limités à 80 caractères chacun. Cette limite par élément n’est pas une garantie sur la longueur totale du chemin. L’extension d’origine est conservée.

Le **Compteur** ajoute un numéro d’au moins trois chiffres (`001`, `002`, puis `1000` si nécessaire). Il augmente après un renommage réussi. Vide, il n’ajoute pas de suffixe numérique. **Précision** ajoute un complément libre avant ce numéro. Les petites croix effacent les champs correspondants.

### Valider et poursuivre

Vérifiez toujours le Nom cible, puis cliquez sur **RENOMMER (Entrée)**. Le fichier est renommé sur le disque et l’image suivante s’affiche. Une collision est refusée : modifiez la précision ou le compteur. Les choix de nomenclature restent disponibles pour traiter une série ; revérifiez ceux qui ne conviennent plus à l’image suivante.

Les boutons **Nom actuel** et **Nomenclature** servent à changer de méthode. Nom actuel copie le nom existant dans le champ cible pour une correction manuelle. Taper directement dans ce champ active également le mode manuel. Nomenclature réactive le calcul automatique à partir des choix courants ; ce n’est pas une annulation du dernier renommage.

**Ouvrir fichier**, **Dossier**, **Précédent**, **Suivant** et le petit **i** complètent le parcours. Les métadonnées comprennent notamment le chemin, la taille du fichier, sa date de modification et ses dimensions lorsqu’elles sont disponibles.

## 10. Rechercher et modifier les niveaux

**Recherche niveaux** interroge toute la hiérarchie, sans distinction de casse ou d’accents. Vous pouvez saisir plusieurs termes pour retrouver une branche. La frappe seule ne remplace pas vos choix : consultez la suggestion, parcourez les propositions avec **haut / bas**, puis validez avec **Entrée**. Dans ce champ, Entrée choisit la suggestion au lieu de renommer le fichier. La croix vide la recherche.

Les champs **N1**, **N2** et **N3** du bas servent à modifier l’architecture :

| Action | Procédure |
| --- | --- |
| Ajouter un N1 | Saisir son nom dans N1, puis cliquer sur +. |
| Ajouter un N2 | Sélectionner d’abord son N1 parent, saisir N2, puis +. |
| Ajouter un N3 | Sélectionner N1 et N2, saisir N3, puis +. |
| Supprimer un N1 ou N2 | Sélectionner la catégorie, puis utiliser son bouton - et confirmer. |
| Supprimer des N3 | Cocher les éléments concernés, utiliser - et confirmer. |
| Supprimer depuis une liste | Utiliser le clic droit sur l’entrée concernée. |

Supprimer une catégorie modifie l’architecture, et supprimer un parent retire sa branche. Cela ne supprime ni ne renomme les fichiers qui utilisaient ces mots. Ces fichiers peuvent encore être recherchés par leur nom, mais le rangement automatique peut ne plus reconnaître leur ancienne catégorie.

Les champs d’ajout ne remplacent pas les sélections : écrire un mot dans N2 sans cliquer sur + ne crée pas une catégorie.

## 11. Architecture et langue de classement

**Sauver architecture** exporte la hiérarchie dans un fichier `.docarch.json`, avec la langue de classement. **Charger architecture** remplace la structure courante par celle d’un fichier exporté. Ce fichier contient des catégories, pas vos images, favoris ou collectes.

**Reset**, dans le bloc d’architecture, revient au modèle d’origine de la langue de classement après confirmation. Il ne doit pas être confondu avec Reset recherche dans Bibliothèque. Sauvegardez vos catégories personnalisées avant un remplacement ou une réinitialisation.

**Classement…** permet de choisir un modèle français ou anglais. Le choix concerne les catégories et les marqueurs ajoutés aux futurs noms, indépendamment du sélecteur FR / EN de l’interface. Par exemple :

| Classement français | Classement anglais |
| --- | --- |
| `DOCUMENTATION_Animaux_Chevaux_001.jpg` | `DOCUMENTATION_Animals_Horses_001.jpg` |
| Marqueur Couleur | Marqueur Color |
| Marqueur Master | Marqueur Prime |

Ce changement ne traduit pas les fichiers déjà renommés ni les précisions que vous avez écrites. Il remplace l’architecture après confirmation. Une bibliothèque mêlant des noms français et anglais reste consultable, mais vos requêtes doivent utiliser les bons termes ; le rangement dépend aussi des catégories du modèle actif.

Morgue mémorise une architecture et une langue de classement par dossier de travail, y compris vos suppressions de catégories. Lorsqu’un ancien fichier d’architecture ne précise pas sa langue, l’import conserve la langue de classement courante.

## 12. Ranger les fichiers dans les dossiers

**Renommer** change le nom dans le dossier courant. **Ranger DOCUMENTATION** déplace les fichiers dans une arborescence construite à partir des niveaux reconnus dans leurs noms. Ce sont deux opérations différentes.

1. Vérifiez le dossier source et l’option **Inclure sous-dossiers**. Le rangement porte sur ce périmètre, pas seulement sur l’image affichée ou les résultats transmis par Bibliothèque.
2. Vérifiez que l’architecture active correspond aux noms de vos fichiers.
3. Cliquez sur **Ranger DOCUMENTATION**.
4. Choisissez une racine Documentation existante, ou l’emplacement où en créer une.
5. Consultez le bilan des déplacements et des fichiers non reconnus.

| Niveaux reconnus | Destination dans la racine choisie |
| --- | --- |
| N1, N2 et un seul N3 | `N1/N2/N3` |
| N1 et N2, sans N3 unique ou avec plusieurs N3 | `N1/N2` |
| N1 seul | `N1` |
| Aucun N1 reconnu | Fichier ignoré et signalé. |

Le rangement examine les noms commençant par `DOCUMENTATION`. Pour l’indexation dans Bibliothèque, utilisez bien la nomenclature complète avec `DOCUMENTATION_`. Les noms déjà présents à destination reçoivent un suffixe ; les fichiers existants ne sont pas écrasés.

Les déplacements faits dans Morgue mettent à jour l’index et conservent les favoris et la collecte. Si la destination constitue une autre bibliothèque, elle devient le dossier de travail après rangement. Il n’existe pas de commande générale permettant d’annuler toute une opération de rangement : conservez une sauvegarde de vos images avant une réorganisation importante.

## 13. Atelier : préparer une séance

Dans Bibliothèque, cliquez sur **Atelier**. Le panneau propose cinq sources : les résultats de la **Recherche actuelle**, les **Favoris**, la **Collecte**, un **fichier externe** ou un **dossier externe**. Le dossier externe est parcouru avec ses sous-dossiers, sans imposer le préfixe documentaire.

La Recherche actuelle utilise uniquement les résultats chargés. Les sources Favoris et Collecte utilisent leurs ensembles indexés dans la bibliothèque active, indépendamment de cette limite d’affichage.

Choisissez une durée par image : **30 secondes, 1, 2, 5, 10 ou 30 minutes**. **Temps libre** signifie ici une durée personnalisée saisie en minutes, et non une séance sans chronomètre. Pour observer sans décompte, utilisez Pause pendant la séance.

Choisissez ensuite l’ordre **Normal** ou **Aléatoire**, toutes les images ou une limite, puis un fond **Sombre**, **Blanc** ou **Neutre**. Avec l’ordre aléatoire et une limite, le mélange précède la sélection du nombre demandé.

Cliquez sur **Démarrer**. La séance s’ouvre dans sa propre fenêtre, avec progression automatique au terme de chaque durée. Elle se termine après la dernière image ; vous pouvez aussi la quitter avant.

## 14. Atelier : observer et analyser

Les outils de séance modifient uniquement l’affichage. Ils ne réécrivent pas vos fichiers originaux et ne constituent pas un export d’images retouchées.

| Outil | Usage |
| --- | --- |
| Normal | Voir les couleurs d’origine. |
| Gris | Lire l’image sans les différences de teinte. |
| Noir et blanc | Examiner une séparation forte entre clairs et foncés. |
| Trois valeurs / Cinq valeurs | Simplifier l’organisation tonale. |
| Flou | Observer les grandes masses en atténuant les détails. |
| Composition | Superposer des repères de tiers et de diagonales. |
| Grille / Prise de mesure | Comparer les proportions avec une grille dont la taille et les décalages horizontal et vertical sont réglables. |
| Couleur de grille | Choisir un contraste plus lisible sur l’image. |
| Miroirs horizontal et vertical | Renouveler la perception des formes et des déséquilibres. |
| Rotation | Changer l’orientation d’observation. |
| Fond sombre, blanc ou neutre | Comparer la lecture des valeurs selon leur environnement. |

Le clic droit dans la séance ouvre les commandes d’affichage. Précédent et Suivant changent de référence ; **Espace** met en pause ou reprend le décompte. **Échap** ferme d’abord la fenêtre de réglage de grille si elle est ouverte, puis permet de quitter la séance.

Pour un exercice de silhouettes, choisissez des poses, réglez 30 secondes et observez surtout les appuis et la direction générale. Pour une étude de composition, préférez une durée longue, puis comparez l’image normale, le flou et les trois valeurs. Ces suggestions ne sont pas des modes automatiques supplémentaires.

## 15. Raccourcis clavier

Les commandes dépendent de l’espace actif. Les raccourcis par lettres et les flèches de navigation de Bibliothèque ne doivent pas être confondus avec la saisie dans un champ texte.

### Bibliothèque

| Raccourci | Action |
| --- | --- |
| Ctrl+O | Choisir le dossier de bibliothèque. |
| Ctrl+L / Ctrl+N | Activer la recherche / le champ de renommage. |
| Entrée dans Recherche | Lancer la recherche. |
| Haut / Bas dans Recherche | Parcourir l’historique. |
| Ctrl+Entrée dans le nom | Appliquer le renommage rapide. |
| Gauche / Droite, hors saisie | Image précédente / suivante. |
| f / k | Basculer le favori / la collecte de l’image. |
| Maj+K | Ajouter les résultats chargés à la collecte. |
| Ctrl+K / Ctrl+Maj+K | Afficher / purger la collecte. |
| Alt+K | Exporter la collecte. |
| F6 ou a / Maj+F6 | Afficher le panneau Atelier / démarrer la séance. |
| F1 | Ouvrir l’aide. |
| Échap | Fermer le panneau Atelier ou interrompre l’indexation. |

### Classer / Renommer

| Raccourci | Action |
| --- | --- |
| Ctrl+O | Choisir le dossier à traiter. |
| Ctrl+Maj+O / Ctrl+Maj+F | Ouvrir l’image / son dossier. |
| Ctrl+I / Ctrl+R | Injecter le nom actuel / réactiver la nomenclature. |
| Gauche / Droite, hors saisie | Image précédente / suivante. |
| Entrée | Renommer et poursuivre ; dans Recherche niveaux, valider la suggestion. |
| Haut / Bas dans Recherche niveaux | Parcourir les suggestions. |

### Fenêtre de séance Atelier

| Raccourci | Action |
| --- | --- |
| Gauche / Droite | Référence précédente / suivante. |
| Espace | Pause / reprise. |
| 1 / 2 / 3 | Normal / gris / noir et blanc. |
| 4 / 5 / 6 | Trois valeurs / cinq valeurs / flou. |
| 7 / 8 / 9 | Composition / couleur de grille / afficher ou masquer la grille. |
| m / p / r | Miroir horizontal / miroir vertical / rotation. |
| Échap | Fermer les réglages de grille, ou quitter la séance. |

Les chiffres du pavé numérique sont également reconnus dans la séance. Si un raccourci n’agit pas, cliquez dans la fenêtre concernée et vérifiez qu’un champ de saisie ou une boîte de dialogue n’a pas le focus.

## 16. Réglages, sauvegarde et déplacement

Morgue travaille localement. Il ne fournit pas de compte en ligne ni de synchronisation distante de votre documentation. Les réglages enregistrés automatiquement assurent la continuité de travail, mais ne remplacent pas une sauvegarde des images.

| Élément | Contenu ou rôle |
| --- | --- |
| Votre dossier de documentation | Les fichiers images eux-mêmes. |
| `morgue_settings.json` | Dossier partagé, langue d’interface, infobulles, architectures et langues de classement par bibliothèque. |
| `index_documentation.db` | Catalogue et indicateurs de favoris et de collecte. |
| `index_documentation_settings.json` | Préférences de Bibliothèque, historique et réglages d’Atelier. |
| `settings.json` | Réglages du renommeur : dossier, compteur, précision et sélections notamment. |
| `documentation_structure_user.json` | Données d’architecture historique conservées pour la reprise des versions antérieures. |
| `index_documentation_thumbs` | Cache des vignettes, reconstituable. |
| `logs` | Journaux utiles au diagnostic ; ils ne constituent pas une commande d’annulation. |
| Fichiers `.docarch.json` exportés | Copies indépendantes de vos architectures. |

Pour une sauvegarde complète, fermez Morgue puis copiez **le dossier du programme avec ses données et le dossier des images** sur votre support de sauvegarde. Un export d’architecture ne suffit pas à conserver les favoris ; un export de collecte ne contient que les images sélectionnées.

Pour une mise à jour, conservez les fichiers de données et remplacez le logiciel. Si vous utilisez l’exécutable, placez la nouvelle version dans le dossier contenant vos données existantes. Évitez d’ouvrir simultanément les anciens programmes et Morgue sur les mêmes fichiers.

Les chemins jouent un rôle dans l’index et les indicateurs. Copier la bibliothèque ailleurs avec l’Explorateur puis réindexer ne garantit pas de retrouver les favoris et la collecte associés aux anciens chemins. Les déplacements réalisés par **Ranger DOCUMENTATION** bénéficient de la synchronisation interne. Pour une migration vers un autre ordinateur ou un autre disque, conservez les sauvegardes avant toute réorganisation et vérifiez vos indicateurs après reprise.

## 17. Résoudre les difficultés courantes

| Situation | Vérification et action |
| --- | --- |
| Aucune image dans Bibliothèque | Vérifiez la racine, les extensions, le préfixe `DOCUMENTATION_`, puis indexez et réinitialisez la recherche. |
| Les images apparaissent dans le renommeur, pas dans Bibliothèque | Le renommeur accepte les noms bruts ; la Bibliothèque exige la nomenclature documentaire. |
| Une recherche anglaise ne retrouve pas un nom français | La langue d’interface ne traduit pas les fichiers. Cherchez les mots de leur nom ou de leur dossier. |
| Je ne vois que 500 résultats | Chargez la tranche suivante au bas des vignettes. |
| Un fichier renommé disparaît des résultats | Vérifiez s’il correspond encore à la requête et s’il conserve le préfixe. |
| La nomenclature ne modifie plus le Nom cible | Cliquez sur Nomenclature pour quitter l’édition manuelle. |
| Une collision empêche le renommage | Choisissez un compteur ou une précision qui produit un nom encore libre. |
| Le rangement ne reconnaît pas mes noms | Vérifiez la langue et les catégories de l’architecture active. Consultez le bilan des fichiers ignorés. |
| Mes changements externes ne sont pas visibles | Réindexez après modification dans l’Explorateur ou un autre programme. |
| Des commandes sont bloquées | Vérifiez si une indexation est en cours ; attendez ou interrompez-la avec Échap. |
| Les infobulles ont disparu | Ouvrez i, puis cochez Afficher les infobulles. |
| Les champs du bas sont hors écran | Agrandissez la fenêtre et faites défiler les listes de niveaux dans leurs propres zones. Vérifiez aussi la mise à l’échelle de l’écran. |
| L’ancienne icône ou l’ancien design apparaît | Lancez le nouvel exécutable reconstruit et remplacez le raccourci épinglé vers l’ancienne version. |
| Une image refuse de s’ouvrir | Vérifiez qu’elle existe encore et essayez Ouvrir image dans la visionneuse du système. |

## 18. Repères et crédits

**Architecture** : vocabulaire hiérarchisé des niveaux. **Index** : catalogue des fichiers. **Nomenclature** : règle de construction de leurs noms. **Favori** : indicateur mémorisé d’une référence privilégiée. **Collecte** : sélection de travail exportable. **Atelier** : espace d’observation et d’exercice. **Dossier de travail** : racine documentaire active, commune aux deux espaces.

Morgue / Eigrutel Lab. Programme conçu et développé par **Simon Léturgie**, dans le cadre d’**Eigrutel BD Academy**.

Code source et programme compilé : **GNU AGPL v3.0 ou version ultérieure**. Documentation et ressources : **CC BY-SA 4.0, sauf mention contraire**. Les bibliothèques tierces conservent leurs licences respectives. Marques, logos et signes distinctifs Eigrutel / Eigrutel Lab / Eigrutel BD Academy : **réservés**.

Les mentions de licence du logiciel et de ce manuel ne modifient pas les droits attachés aux images que vous classez. Ce manuel a été établi à partir des anciens manuels et du code de Morgue 3.1.12. Les libellés et fonctions décrits se rapportent à cette version.
