# -*- coding: utf-8 -*-
# Eigrutel Lab / Atelier d'outils libres pour la bande dessinée
# Programme conçu et développé par Simon Léturgie
# dans le cadre d'Eigrutel BD Academy.
# Nom public : Morgue
# Version : 3.1.12
# Date : 10-09-2026
# Application de bureau : sources Python (.py) et exécutable Windows (.exe).
# Code source et programme compilé : GNU AGPL v3.0 ou version ultérieure.
# Documentation et ressources : CC BY-SA 4.0, sauf mention contraire.
# Les bibliothèques tierces conservent leurs licences respectives.
# Marques, logos et signes distinctifs Eigrutel / Eigrutel Lab /
# Eigrutel BD Academy : réservés.

"""Bilingual help, including classification and image-analysis principles."""
import textwrap
import tkinter as tk
from tkinter import ttk, messagebox
from morgue_i18n import tr, trf, language, watch

FR = {
'library': '''MORGUE / BIBLIOTHÈQUE

DÉMARRER
Choisissez un dossier de travail, puis cliquez sur Indexer / Réindexer. Seules les images dont le nom commence par DOCUMENTATION_ sont indexées, dans le dossier et ses sous-dossiers. Le renommeur peut, lui, ouvrir des images qui n’ont pas encore ce préfixe.

RECHERCHER
La recherche porte sur les noms de fichiers et les chemins des dossiers, sans distinction de casse ou d’accents. Plusieurs termes imposent leur présence conjointe ; ils peuvent être partiels.
Exemples : cheval rouge ; cheval -rouge ; -chat ; "scene de rue".
Champs : nom:cheval, dossier:costume, ext:jpg.
Les alias name: et folder: fonctionnent aussi en français. Les mots de recherche ne sont pas traduits : recherchez les termes effectivement présents dans vos noms et dossiers.
Les filtres Inspiration insèrent les mots de la langue de classement, indépendamment de la langue de l’écran.

RÉSULTATS ET NAVIGATION
Cliquez sur une vignette pour voir l’image ; double-cliquez pour l’ouvrir dans votre application habituelle. Les flèches gauche/droite parcourent les résultats quand aucun champ texte n’est actif. La molette fait défiler les vignettes.
Les résultats sont chargés par tranches de 500. Le bouton en bas de la grille permet de charger la suite. Le compteur indique le total des correspondances. La collecte des résultats et les sessions Atelier depuis la recherche utilisent les résultats actuellement chargés.

FAVORIS ET COLLECTE
L’étoile repère vos références privilégiées. La collecte rassemble temporairement les documents utiles à un projet. Les deux sont mémorisés par bibliothèque.
Le petit carré d’une vignette ajoute ou retire l’image de la collecte. Vous pouvez afficher, vider ou exporter cette sélection. L’export copie les fichiers ; il ne déplace pas vos originaux. Les conflits de noms à l’export reçoivent un suffixe.
Cocher Favoris et Collecte affiche les images appartenant à l’un ou à l’autre.

DE LA COLLECTION À L’ESSENTIEL
Les favoris aident à resserrer la documentation : 50 images, 10 intéressantes, 3 utiles, une image maîtresse. Recherchez une référence claire par idée, plutôt qu’une accumulation indifférenciée. Un marqueur personnel tel que _TOTEM peut également servir à retrouver ces images.

RENOMMER ET CLASSER
L’onglet « Classer / Renommer » de la barre ouvre le second espace sur la sélection ; sa navigation parcourt alors les résultats chargés. Pour traiter tout un dossier, choisissez de nouveau le dossier de travail.
Le renommage rapide de la Bibliothèque conserve l’extension. Les renommages et rangements réalisés dans Morgue mettent à jour l’index et conservent les favoris et la collecte. Les modifications externes nécessitent une réindexation.
La réindexation conserve l’ancien index jusqu’à sa réussite. Échap l’interrompt. Le renommage et le changement de dossier sont bloqués pendant cette opération.

ATELIER / DESSIN ET ANALYSE
Ouvrez le panneau Atelier pour choisir la source : recherche chargée, favoris, collecte, fichier externe ou dossier externe. Réglez la durée par image, l’ordre normal ou aléatoire, le nombre d’images et le fond. « Temps libre » permet de saisir une durée personnalisée en minutes.
La session s’ouvre dans une fenêtre dédiée. Étudiez les proportions avec la grille réglable ; les tiers et diagonales aident à lire la composition. Les miroirs modifient votre perception de l’image. Les modes gris, noir et blanc, trois valeurs, cinq valeurs et flou permettent d’étudier les masses, les contrastes et la hiérarchie visuelle. Le fond sombre, blanc ou neutre change le contexte de lecture des valeurs.

RACCOURCIS / BIBLIOTHÈQUE
Entrée dans la recherche : rechercher.
Ctrl+O : choisir un dossier. Ctrl+L : recherche. Ctrl+N : champ de renommage.
F1 : aide. F6 ou a : panneau Atelier. Maj+F6 : démarrer une session.
Échap : fermer le panneau ou interrompre l’indexation.
f : favori ; k : collecte ; Maj+K : collecter les résultats chargés.
Ctrl+K : afficher la collecte ; Ctrl+Maj+K : vider la collecte ; Alt+K : exporter.
Flèches haut/bas dans la recherche : historique. Clic droit : effacer l’historique.
Les lettres de commande ne s’activent pas pendant la saisie dans un champ texte.

RACCOURCIS / SESSION ATELIER
Gauche/droite : précédent/suivant. Espace : pause/reprise. Échap : quitter ; la fenêtre de grille se ferme d’abord si elle est ouverte.
1 : normal ; 2 : gris ; 3 : noir et blanc ; 4 : trois valeurs ; 5 : cinq valeurs ; 6 : flou.
7 : composition ; 8 : couleur de grille ; 9 : afficher/masquer la grille.
m : miroir horizontal ; p : miroir vertical ; r : rotation.
Le pavé numérique et le menu contextuel donnent accès aux mêmes modes.

LANGUE ET CLASSEMENT
FR / EN change l’interface immédiatement et mémorise le choix. La recherche, la sélection, les catégories, les dossiers et les noms existants restent inchangés.
« Classement » choisit un modèle français ou anglais pour la bibliothèque active, après confirmation. Exportez une architecture personnalisée avant de la remplacer. Le préfixe reste DOCUMENTATION_ dans les deux langues. Changer le modèle ne renomme aucun fichier existant.
''',
'renamer': '''MORGUE / CLASSER / RENOMMER

PRINCIPE
Le nom du fichier devient une information exploitable. L’objectif est de préparer une collection durable de références pour le dessin, pas seulement de produire des noms propres.

LES NIVEAUX : DU GÉNÉRAL AU PARTICULIER
Les trois niveaux s’emboîtent : Niveau 1, grande famille ; Niveau 2, sous-famille ; Niveau 3, détail. Exemple français : Animaux > Domestiques > Chats. Exemple anglais : Animals > Domestic > Cats.
Un niveau 3 appartient à un niveau 2, lui-même inclus dans un niveau 1. Cette hiérarchie doit rester cohérente, car le rangement automatique lit la structure inscrite dans les noms.

CONSTRUIRE LE NOM
Le nom cible combine DOCUMENTATION, les niveaux choisis, les cases de type et d’inspiration, la précision facultative et le compteur facultatif. Un compteur vide n’ajoute pas de suffixe numérique. L’extension de l’image est conservée.
« Nom actuel » injecte le nom existant pour l’éditer manuellement. « Nomenclature » revient à la construction automatique. Vérifiez le nom cible, puis cliquez sur Renommer ou appuyez sur Entrée. Un nom déjà présent n’est pas écrasé.
Les flèches changent d’image ; les commandes d’ouverture donnent accès au fichier ou à son dossier. Le bouton d’information sous l’image affiche les métadonnées.

DEUX AXES COMPLÉMENTAIRES
Les niveaux décrivent ce que l’image montre. Le bloc Inspiration décrit ce qu’elle apporte graphiquement. Une rue peut être classée par lieu tout en servant pour sa composition, sa lumière ou ses valeurs. Ce second axe permet de chercher transversalement, sans connaître la catégorie du sujet.
Cette sélection agit comme un entonnoir : on passe d’un ensemble de documents à des références adaptées à une intention de dessin.

INSPIRATION
Composition : organisation des masses, cadrage, circulation du regard et découpage de l’espace.
Forme : simplification des volumes, contours et lisibilité des masses.
Silhouette : lecture immédiate d’une pose ou d’un personnage par son contour.
Couleur : harmonies, dominantes, contrastes et rapports chaud/froid.
Lumière : direction, intensité, contre-jour, lumière diffuse ou dure.
Valeurs : répartition des clairs et des foncés, structure tonale et lecture en noir et blanc.
Échelle : rapports de taille, grandeur, petitesse et repères dimensionnels.
Marche, Course, Saut et Combat : appuis, mouvement, trajectoires et narration gestuelle.
PHOTO et Dessin précisent la nature du document. Master, affiché Prime en anglais, signale une référence particulièrement utile ou exemplaire.

RECHERCHER ET MODIFIER LES CATÉGORIES
La recherche parcourt toute la hiérarchie : par exemple costume femme manteaux. Les flèches haut/bas parcourent les suggestions ; Entrée choisit le chemin. La frappe seule ne change pas vos catégories.
Les commandes N1, N2 et N3 enrichissent la structure. Créez d’abord le parent, puis ses sous-catégories. Les catégories personnelles ne sont pas traduites lorsque la langue de l’écran change.
Chargez ou sauvegardez une architecture au format .docarch.json. La langue de classement y est enregistrée. Réinitialiser remet le modèle d’origine de cette langue après confirmation. Les architectures personnalisées sont conservées par bibliothèque, y compris les suppressions.

RANGEMENT
« Ranger DOCUMENTATION » examine les fichiers du dossier source selon l’option sous-dossiers. Choisissez une racine Documentation existante ou un emplacement où la créer. Le programme lit les niveaux dans les noms et range les fichiers dans les dossiers correspondants. Si plusieurs niveaux 3 sont présents, le rangement s’arrête au niveau 2. Les fichiers non reconnus sont signalés. Les collisions de noms reçoivent un suffixe ; les originaux ne sont pas écrasés.
Les favoris et la collecte suivent les déplacements réalisés dans Morgue. Après rangement vers une autre bibliothèque, le dossier de destination devient le dossier de travail.

LANGUE DE L’ÉCRAN ET LANGUE DES NOMS
FR / EN traduit les commandes et les aides. Cela ne change pas votre architecture ni les noms existants.
Le bouton Classement propose séparément un modèle français ou anglais. Le modèle anglais produit par exemple DOCUMENTATION_Animals_Horses_001.jpg. Le modèle français conserve par exemple DOCUMENTATION_Animaux_Chevaux_001.jpg.
Le choix de classement détermine aussi les mots de type et d’inspiration ajoutés aux futurs noms. Exportez votre architecture personnalisée avant de la remplacer par un modèle.

RACCOURCIS
Gauche/droite : précédent/suivant, hors des champs texte.
Entrée : renommer ; dans la recherche des niveaux, Entrée choisit la suggestion.
Ctrl+O : choisir un dossier. Ctrl+Maj+O : ouvrir le fichier. Ctrl+Maj+F : ouvrir son dossier.
Ctrl+I : injecter le nom actuel. Ctrl+R : revenir à la nomenclature automatique.
'''}
EN = {
'library': '''MORGUE / LIBRARY

GETTING STARTED
Choose a working folder, then click Index / Reindex. Only images whose names begin with DOCUMENTATION_ are indexed, including subfolders. The renamer can also open images that do not yet have this prefix.

SEARCH
Search matches filenames and folder paths, ignoring case and accents. All entered terms must match; partial words are accepted.
Examples: horse red; horse -red; -cat; "street scene".
Fields: name:horse, folder:costume, ext:jpg. The French aliases nom: and dossier: also work.
Search words are not translated: use the words actually present in your filenames and folders. Inspiration filters insert the terms of the classification language, independently of the interface language.

RESULTS AND NAVIGATION
Click a thumbnail to preview the image; double-click to open it in your usual application. Left/right arrows browse results when no text field is active. The mouse wheel scrolls the thumbnails.
Results load in groups of 500. Use the button at the bottom of the grid to load more. The counter shows the exact total. Collecting all results and Studio sessions based on a search use the results currently loaded.

FAVORITES AND COLLECTION
The star marks preferred references. The collection temporarily gathers documents for a project. Both are saved for each library.
Click the small square on a thumbnail to add or remove an image. You can view, clear or export the collection. Export copies files and leaves the originals in place. Duplicate names receive a suffix.
Selecting both Favorites and Collection displays images belonging to either group.

FROM A COLLECTION TO THE ESSENTIAL
Favorites help narrow down references: 50 images, 10 interesting ones, 3 useful ones, one key image. Seek one clear reference per idea rather than an undifferentiated pile. A personal filename marker such as _TOTEM can help retrieve these key images.

RENAMING AND ORGANIZING
The “Organize / Rename” toolbar tab opens the second workspace on your selection; its navigation then browses the loaded search results. To process a complete folder, select the working folder again.
Quick renaming in the Library preserves the extension. Renaming and sorting within Morgue update the index and preserve favorites and collection flags. Changes made outside Morgue require reindexing.
Reindexing preserves the previous index until successful completion. Esc cancels it. Renaming and switching folders are blocked during indexing.

STUDIO / DRAWING AND ANALYSIS
Open the Studio panel to choose a source: loaded search results, favorites, collection, external file or external folder. Set the time per image, normal or random order, image count and background. Custom time accepts a duration in minutes.
The session opens in its own window. Study proportions with the adjustable grid; thirds and diagonals help reveal composition. Flipping changes how you perceive an image. Grayscale, black and white, three values, five values and blur help study masses, contrasts and visual hierarchy. A dark, white or neutral background changes the context in which values are read.

SHORTCUTS / LIBRARY
Enter in the search field: search.
Ctrl+O: choose folder. Ctrl+L: focus search. Ctrl+N: focus filename.
F1: help. F6 or a: Studio panel. Shift+F6: start a session.
Esc: close the panel or cancel indexing.
f: favorite; k: collection; Shift+K: collect loaded results.
Ctrl+K: show collection; Ctrl+Shift+K: clear collection; Alt+K: export.
Up/down in the search field: history. Right-click: clear history.
Letter shortcuts do not run while typing in a text field.

SHORTCUTS / STUDIO SESSION
Left/right: previous/next. Space: pause/resume. Esc: exit; if the grid settings window is open, it closes first.
1: normal; 2: grayscale; 3: black and white; 4: three values; 5: five values; 6: blur.
7: composition; 8: grid color; 9: show/hide grid.
m: flip horizontally; p: flip vertically; r: rotate.
The number pad and context menu provide the same display modes.

INTERFACE AND CLASSIFICATION LANGUAGE
FR / EN changes the interface immediately and saves your choice. Your search, selection, categories, folders and existing filenames stay unchanged.
Classification separately offers a French or English template for the active library, after confirmation. Export a custom structure before replacing it. The prefix remains DOCUMENTATION_ in both languages. Applying a template does not rename existing files.
''',
'renamer': '''MORGUE / ORGANIZE / RENAME

GENERAL PRINCIPLE
A filename becomes usable information. The goal is a durable collection of drawing references, not just clean names.

LEVELS: FROM GENERAL TO SPECIFIC
The three levels are nested: Level 1 is a broad family, Level 2 a subfamily and Level 3 a detail. English example: Animals > Domestic > Cats. French example: Animaux > Domestiques > Chats.
A Level 3 item belongs to Level 2, which belongs to Level 1. Keep this hierarchy consistent: automatic sorting reads the structure embedded in filenames.

BUILDING A NAME
The target name combines DOCUMENTATION, selected levels, type and inspiration tags, optional details and an optional counter. An empty counter adds no numeric suffix. The image extension is preserved.
Current name inserts the existing filename for manual editing. Naming rules restores automatic name construction. Check the target name, then click Rename or press Enter. An existing file is never overwritten.
Use the arrows to navigate and the open commands to access the image or its folder. The information button below the preview shows metadata.

TWO COMPLEMENTARY AXES
Levels describe what the image shows. Inspiration describes what it offers visually. A street photograph can be classified by location while being useful for its composition, light or values. This second axis allows searches across subjects, without knowing their category.
This selection acts as a funnel: it turns an accumulation of documents into references suited to a specific drawing intention.

INSPIRATION
Composition: arrangement of masses, framing, eye flow and spatial division.
Form: simplified volumes, contours and clearly readable masses.
Silhouette: immediate readability of a pose or character through its outline.
Color: harmonies, dominant hues, contrasts and warm/cool relationships.
Light: direction, intensity, backlighting, soft or hard light.
Values: light and dark distribution, tonal structure and black-and-white readability.
Scale: size relationships, grandeur, smallness and dimensional reference.
Walk, Run, Jump and Fight: weight distribution, movement, trajectories and gestural storytelling.
PHOTO and Drawing describe the reference type. Prime, shown as Master in French, marks a particularly useful or exemplary reference.

FINDING AND EDITING CATEGORIES
Level search looks across the complete hierarchy: for example costume women coats. Up/down arrows browse suggestions; Enter selects the path. Typing alone never changes selected categories.
L1, L2 and L3 commands add to the structure. Create the parent before its subcategories. Personal categories are not translated when the interface language changes.
Load or save a structure as .docarch.json. Its classification language is saved too. Reset restores the default template for that language after confirmation. Custom structures, including deleted categories, are saved per library.

AUTOMATIC SORTING
Sort DOCUMENTATION examines files in the source folder according to the subfolder option. Select an existing Documentation root or a location in which to create it. Morgue reads levels from filenames and moves files into the matching folders. When multiple Level 3 items are present, sorting stops at Level 2. Unrecognized files are reported. Name conflicts receive a suffix; originals are not overwritten.
Favorites and collection flags follow moves performed within Morgue. After sorting into a different library, the destination becomes the working folder.

INTERFACE LANGUAGE AND FILENAME LANGUAGE
FR / EN translates commands and help. It does not change your structure or existing filenames.
The Classification button separately offers a French or English template. The English template can produce DOCUMENTATION_Animals_Horses_001.jpg. The French template can produce DOCUMENTATION_Animaux_Chevaux_001.jpg.
Classification also controls the type and inspiration words added to future filenames. Export your custom structure before replacing it with a template.

SHORTCUTS
Left/right: previous/next, outside text fields.
Enter: rename; in level search, Enter selects the suggestion.
Ctrl+O: choose folder. Ctrl+Shift+O: open file. Ctrl+Shift+F: open its folder.
Ctrl+I: insert the current filename. Ctrl+R: restore automatic naming.
'''}


def show_help(root, topic):
    """Shared reading window: contextual manual, contents and program credits."""
    from EigrutelMorgue import ABOUT, VERSION
    from ui_common import apply_app_icon
    colors = dict(blue='#1F3A44', deep='#152B33', light='#2D4C57',
                  paper='#F4F1EA', white='#FAFAF7',
                  ink='#243033', muted='#6F7473', line='#D8D0C4', red='#7F2D30')
    win = tk.Toplevel(root)
    win.title(tr('Aide Morgue'))
    win.configure(bg=colors['paper'])
    win.geometry(f"{min(980, root.winfo_screenwidth()-80)}x{min(720, root.winfo_screenheight()-100)}")
    win.minsize(640, 440)
    apply_app_icon(win)
    header = tk.Frame(win, bg=colors['blue'], padx=24, pady=16)
    header.pack(fill='x')
    tk.Label(header, text='EIGRUTEL LAB', bg=colors['blue'], fg=colors['paper'],
             font=('Segoe UI',9,'bold')).pack(anchor='w')
    tk.Label(header, text='Morgue', bg=colors['blue'], fg=colors['white'],
             font=('Segoe UI',23,'bold')).pack(side='left')
    tk.Label(header, text='v'+VERSION, bg=colors['blue'], fg=colors['paper'],
             font=('Segoe UI',10)).pack(side='right', anchor='s', pady=5)
    tk.Frame(win, bg=colors['paper'], height=3).pack(fill='x')
    footer = tk.Frame(win, bg=colors['paper'], padx=20, pady=10)
    footer.pack(side='bottom', fill='x')
    manager = getattr(root, '_morgue_tooltips', None)
    if manager is not None:
        tk.Checkbutton(footer, text=tr('Afficher les infobulles'), variable=manager.enabled,
            bg=colors['paper'], fg=colors['ink'], activebackground=colors['paper'],
            selectcolor=colors['white'], font=('Segoe UI',10), bd=0).pack(side='left')
    ttk.Button(footer, text=tr('Fermer'), style='Side.TButton', command=win.destroy).pack(side='right')
    def open_complete_manual():
        from morgue_manual import open_manual
        try:
            open_manual(language())
        except Exception as error:
            messagebox.showerror(tr('Manuel complet'),
                trf('Impossible d’ouvrir le manuel dans le navigateur.\n\n{0}', error), parent=win)
    ttk.Button(footer, text=tr('Manuel complet'), style='Side.TButton',
        command=open_complete_manual).pack(side='right', padx=(0, 8))
    body = tk.Frame(win, bg=colors['paper'])
    body.pack(fill='both', expand=True, padx=16, pady=(16,0))
    sidebar = tk.Frame(body, bg=colors['blue'], width=220)
    sidebar.pack(side='left', fill='y', padx=(0,16))
    sidebar.pack_propagate(False)
    state = {'page':'help'}
    buttons = {}
    for key, label in (('help', tr('Aide Morgue')), ('about', tr('À propos'))):
        button = tk.Button(sidebar, text=label, anchor='w', padx=16, pady=12,
            font=('Segoe UI',10,'bold'), relief='flat', bd=0, cursor='hand2',
            bg=colors['blue'], fg=colors['white'], activebackground=colors['light'],
            activeforeground=colors['white'], command=lambda page=key: select_page(page))
        button.pack(fill='x')
        buttons[key] = button
    tk.Frame(sidebar, bg=colors['light'], height=1).pack(fill='x', padx=16, pady=12)
    contents = tk.Listbox(sidebar, bg=colors['blue'], fg=colors['paper'],
        selectbackground=colors['light'], selectforeground=colors['white'],
        activestyle='none', borderwidth=0, highlightthickness=0, exportselection=False,
        font=('Segoe UI',9), height=4)
    contents.pack(fill='both', expand=True, padx=12, pady=(0,12))
    page = tk.Frame(body, bg=colors['white'], highlightthickness=1, highlightbackground=colors['line'])
    page.pack(side='left', fill='both', expand=True)
    text = tk.Text(page, wrap='word', font=('Segoe UI',11), bg=colors['white'],
        fg=colors['ink'], padx=24, pady=22, borderwidth=0, highlightthickness=0,
        spacing1=2, spacing3=8, selectbackground=colors['paper'], selectforeground=colors['ink'])
    scroll = ttk.Scrollbar(page, command=text.yview)
    text.configure(yscrollcommand=scroll.set)
    scroll.pack(side='right', fill='y')
    text.pack(fill='both', expand=True)
    text.tag_configure('title', font=('Segoe UI',19,'bold'), foreground=colors['blue'], spacing3=20)
    text.tag_configure('heading', font=('Segoe UI',11,'bold'), foreground=colors['red'], spacing1=16, spacing3=8)
    text.tag_configure('body', spacing3=10)
    anchors = []
    def refresh():
        position = text.yview()[0]
        contents.delete(0,'end')
        anchors.clear()
        text.configure(state='normal')
        text.delete('1.0','end')
        for key, button in buttons.items():
            button.configure(bg=colors['light'] if state['page']==key else colors['blue'])
        if state['page'] == 'help':
            document = (EN if language()=='en' else FR)[topic].strip()
            title, _, document = document.partition('\n')
            text.insert('end', title, 'title')
            text.insert('end', '\n\n')
            for block in document.strip().split('\n\n'):
                first, sep, rest = block.partition('\n')
                if first.isupper():
                    anchors.append(text.index('end-1c'))
                    contents.insert('end', textwrap.shorten(first.capitalize(), width=29, placeholder='…'))
                    text.insert('end', first.capitalize()+'\n', 'heading')
                    if sep:
                        text.insert('end', rest+'\n\n', 'body')
                else:
                    text.insert('end', block+'\n\n', 'body')
        else:
            text.insert('end', str(tr('À propos'))+'\n\n', 'title')
            headings = ('Conception', 'Version', 'Licences et marques') if language()=='fr' else ('Design and development', 'Version', 'Licenses and trademarks')
            for heading, paragraph in zip(headings, str(tr(ABOUT)).strip().split('\n\n',2)):
                anchors.append(text.index('end-1c'))
                contents.insert('end', heading)
                text.insert('end', heading+'\n', 'heading')
                text.insert('end', paragraph+'\n\n', 'body')
        text.configure(state='disabled')
        text.yview_moveto(position)
    def select_page(page):
        state['page'] = page
        refresh()
        text.yview_moveto(0)
    def jump(event=None):
        selected = contents.curselection()
        if selected and selected[0] < len(anchors):
            text.yview(anchors[selected[0]])
    contents.bind('<<ListboxSelect>>', jump)
    win.bind('<Escape>', lambda event: win.destroy())
    watch(text, refresh)
    refresh()
