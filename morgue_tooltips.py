"""Bilingual button help, shared by existing and dynamically created windows.
Eigrutel Lab / Simon Léturgie. GNU AGPL v3 or later.
"""
import tkinter as tk
from morgue_i18n import language, LocalText, rendered
from morgue_translations import EN

# Method names disambiguate identical symbols such as i, stars and crosses.
ACTIONS = {
'open_metadata_dialog': ('Afficher les informations du fichier : chemin, taille et dimensions.', 'Show file details: path, size and dimensions.'),
'open_info_window': ('Ouvrir l’aide, les préférences d’infobulles et les crédits.', 'Open help, tooltip preferences and credits.'),
'open_info_dialog': ('Ouvrir l’aide, les préférences d’infobulles et les crédits.', 'Open help, tooltip preferences and credits.'),
'choose_classification': ('Choisir le modèle français ou anglais de cette bibliothèque, sans renommer les fichiers existants.', 'Choose the French or English template for this library without renaming existing files.'),
'auto_sort_documentation_lvl3': ('Ranger les fichiers DOCUMENTATION dans les dossiers correspondant à leurs catégories.', 'Move DOCUMENTATION files into folders matching their categories.'),
'rename_and_next': ('Renommer l’image avec le nom cible puis passer à la suivante. Raccourci : Entrée.', 'Rename the image using the target name, then advance to the next image. Shortcut: Enter.'),
'rename_current_file': ('Appliquer le nom saisi à l’image sélectionnée et mettre à jour l’index.', 'Apply the entered filename to the selected image and update the index.'),
'inject_current_name': ('Copier le nom actuel du fichier dans le champ du nom cible.', 'Copy the current filename into the target name field.'),
'reset_nomenclature': ('Recalculer le nom cible à partir des catégories, coches et précisions choisies.', 'Rebuild the target name from the selected categories, tags and details.'),
'_import_structure_architecture': ('Importer une architecture de catégories depuis un fichier .docarch.json.', 'Import a category structure from a .docarch.json file.'),
'_export_structure_architecture': ('Sauvegarder vos catégories et leur langue dans un fichier .docarch.json.', 'Save your categories and their language to a .docarch.json file.'),
'_reset_structure_architecture': ('Rétablir les catégories par défaut après confirmation.', 'Restore default categories after confirmation.'),
'open_lvl1_popup': ('Ouvrir la gestion des catégories de niveau 1.', 'Open level 1 category management.'),
'open_lvl2_popup': ('Ouvrir la gestion des catégories de niveau 2.', 'Open level 2 category management.'),
'open_lvl3_popup': ('Ouvrir la gestion des sous-thèmes de niveau 3.', 'Open level 3 subcategory management.'),
'_do_clear': ('Vider ce champ.', 'Clear this field.'),
'choose_folder': ('Choisir le dossier de documentation commun aux deux espaces.', 'Choose the documentation folder shared by both workspaces.'),
'open_folder': ('Choisir le dossier d’images à classer ou renommer.', 'Choose the image folder to organize or rename.'),
'_on_toggle_subdirs': ('Inclure aussi les images contenues dans les sous-dossiers.', 'Also include images stored in subfolders.'),
'toggle_favorites_only': ('Afficher uniquement les images marquées comme favorites.', 'Show only images marked as favorites.'),
'toggle_collected_only': ('Afficher uniquement les images de la collecte.', 'Show only collected images.'),
'toggle_current_favorite': ('Ajouter ou retirer l’image sélectionnée des favoris.', 'Add or remove the selected image from favorites.'),
'toggle_current_collected': ('Ajouter ou retirer l’image sélectionnée de la collecte.', 'Add or remove the selected image from the collection.'),
'collect_all_results': ('Ajouter à la collecte tous les résultats actuellement chargés.', 'Add all currently loaded results to the collection.'),
'show_collected': ('Afficher les images de la collecte.', 'Show collected images.'),
'clear_collected': ('Vider la collecte après confirmation, sans supprimer les fichiers images.', 'Clear the collection after confirmation without deleting image files.'),
'export_collected': ('Copier les images de la collecte dans le dossier de votre choix.', 'Copy collected images into a folder of your choice.'),
'reset_search_filters': ('Effacer la recherche et réinitialiser les filtres.', 'Clear the search and reset filters.'),
'load_more_results': ('Charger la tranche suivante de 500 résultats.', 'Load the next batch of 500 results.'),
'open_current_image': ('Ouvrir l’image dans votre application par défaut.', 'Open the image in your default application.'),
'open_current_folder': ('Ouvrir le dossier contenant l’image dans l’Explorateur.', 'Open the folder containing this image.'),
'open_current': ('Ouvrir l’image dans votre application par défaut.', 'Open the image in your default application.'),
'reveal_current': ('Ouvrir le dossier contenant le fichier.', 'Open the folder containing the file.'),
'show_previous_image': ('Afficher l’image précédente dans les résultats.', 'Show the previous image in the results.'),
'show_next_image': ('Afficher l’image suivante dans les résultats.', 'Show the next image in the results.'),
'prev_image': ('Afficher l’image précédente.', 'Show the previous image.'),
'next_image': ('Afficher l’image suivante.', 'Show the next image.'),
'toggle_atelier_panel': ('Ouvrir ou refermer les réglages de la séance de croquis.', 'Open or close sketch session settings.'),
'hide_atelier_panel': ('Fermer les réglages de l’Atelier.', 'Close Atelier settings.'),
'choose_atelier_external_file': ('Choisir une image externe pour la séance de croquis.', 'Choose an external image for the sketch session.'),
'choose_atelier_external_folder': ('Choisir un dossier externe d’images pour la séance.', 'Choose an external image folder for the session.'),
'start_atelier_from_panel': ('Lancer la séance de croquis avec les réglages choisis.', 'Start the sketch session with the selected settings.'),
'cycle_display_mode': ('Changer le rendu de la référence : normal, gris, valeurs ou flou.', 'Cycle reference rendering: normal, grayscale, values or blur.'),
'toggle_composition': ('Afficher ou masquer les repères de composition.', 'Show or hide composition guides.'),
'on_grid_toggle_from_checkbox': ('Afficher ou masquer la grille de proportions.', 'Show or hide the proportion grid.'),
'toggle_flip_vertical': ('Retourner la référence verticalement.', 'Flip the reference vertically.'),
'toggle_flip_horizontal': ('Retourner la référence horizontalement.', 'Flip the reference horizontally.'),
'rotate_image': ('Faire pivoter la référence d’un quart de tour.', 'Rotate the reference by a quarter turn.'),
'previous_image': ('Revenir à la référence précédente de la séance.', 'Return to the previous session reference.'),
'toggle_pause': ('Mettre le chronomètre en pause ou reprendre la séance.', 'Pause the timer or resume the session.'),
'return_to_atelier': ('Quitter la séance et revenir aux réglages de l’Atelier.', 'Leave the session and return to Atelier settings.'),
'cycle_grid_color': ('Changer la couleur de la grille pour mieux la distinguer.', 'Change the grid color for better visibility.'),
}
LABELS = {
 'Manuel complet': ('Ouvrir le manuel complet hors connexion, dans votre navigateur et dans la langue de Morgue.', 'Open the complete offline manual in your browser, in Morgue’s current language.'),
'i': ACTIONS['open_info_window'],
'FR': ('Afficher l’interface en français, sans changer les noms de fichiers.', 'Show the interface in French without changing filenames.'),
'EN': ('Afficher l’interface en anglais, sans changer les noms de fichiers.', 'Show the interface in English without changing filenames.'),
'Bibliothèque': ('Revenir à la recherche et à la consultation des références.', 'Return to reference search and browsing.'),
'Classer / Renommer': ('Classer ou renommer la référence sélectionnée.', 'Organize or rename the selected reference.'),
'Indexer / Réindexer': ('Analyser le dossier et actualiser l’index des images DOCUMENTATION_.', 'Scan the folder and refresh the DOCUMENTATION_ image index.'),
'+': ('Ajouter au niveau correspondant la catégorie saisie dans ce champ.', 'Add the category entered in this field to the corresponding level.'),
'-': ('Supprimer la catégorie sélectionnée à ce niveau, après confirmation.', 'Delete the selected category at this level after confirmation.'),
'✕': ('Vider ce champ ou fermer ce panneau.', 'Clear this field or close this panel.'),
'×': ('Fermer ce panneau.', 'Close this panel.'),
'Fermer': ('Fermer cette fenêtre.', 'Close this window.'),
'Annuler': ('Fermer sans appliquer de changement.', 'Close without applying changes.'),
'Appliquer le modèle': ('Remplacer l’architecture par le modèle choisi, après confirmation.', 'Replace the structure with the selected template after confirmation.'),
'Modèle français': ('Utiliser les catégories et les mots de classement français.', 'Use French categories and naming tags.'),
'Modèle anglais': ('Utiliser les catégories et les mots de classement anglais.', 'Use English categories and naming tags.'),
'À propos': ('Consulter la version, les crédits et les licences du programme.', 'Read the program version, credits and licenses.'),
'Aide Morgue': ('Consulter le guide de l’espace utilisé.', 'Read the guide for the current workspace.'),
'Afficher les infobulles': ('Activer ou désactiver les aides au survol dans tout le programme. Ce choix est mémorisé.', 'Enable or disable hover help throughout the application. This preference is saved.'),
}


def describe(label, command='', english=False, check=False, renamer=False):
    for name in sorted(ACTIONS, key=len, reverse=True):
        if name in command:
            return ACTIONS[name][int(english)]
    if label in LABELS:
        return LABELS[label][int(english)]
    if not label:
        return ''
    visible = EN.get(label,label) if english else label
    if check:
        if renamer:
            return (f'Add or remove “{visible}” from the naming selection.' if english else
                    f'Ajouter ou retirer « {visible} » de la sélection de nomenclature.')
        return (f'Enable or disable the “{visible}” option.' if english else
                f'Activer ou désactiver l’option « {visible} ».')
    return (f'{visible} / activate this command.' if english else f'{visible} / activer cette commande.')


class Tooltips:
    CLASSES = ('Button','TButton','Checkbutton','TCheckbutton','Radiobutton','TRadiobutton','Menubutton','TMenubutton')
    def __init__(self, root, enabled=True, on_change=None):
        self.root, self.on_change = root, on_change
        self.enabled = tk.BooleanVar(root, value=enabled)
        self.pending = self.tip = self.target = None
        self.enabled.trace_add('write', self._changed)
        for cls in self.CLASSES:
            root.bind_class(cls,'<Enter>',self.enter,add='+')
            root.bind_class(cls,'<Leave>',self.leave,add='+')
        root.bind_all('<ButtonPress>', lambda e:self.hide(), add='+')
        root.bind_all('<KeyPress>', lambda e:self.hide(), add='+')
        root.bind_all('<Unmap>', lambda e:self.hide() if e.widget is self.target else None, add='+')

    def _changed(self,*args):
        self.hide()
        if self.on_change:
            self.on_change(bool(self.enabled.get()))

    def enter(self,event):
        self.hide()
        if not self.enabled.get():
            return
        self.target=event.widget
        self.pending=self.root.after(550,self.show)

    def leave(self,event):
        if event.widget is self.target:
            self.hide()

    def hide(self):
        if self.pending is not None:
            self.root.after_cancel(self.pending)
            self.pending=None
        if self.tip is not None:
            self.tip.destroy()
            self.tip=None
        self.target=None

    def show(self):
        self.pending=None
        widget=self.target
        if widget is None or not self.enabled.get():
            return
        try:
            if not widget.winfo_exists() or not widget.winfo_ismapped():
                return
            label = getattr(widget,'_local_text',None)
            label = label.source if isinstance(label,LocalText) else str(widget.cget('text'))
            command=str(widget.cget('command'))
            controller=getattr(self.root,'_morgue_controller',None)
            renamer=False
            parent=widget
            while parent is not None:
                if controller is not None and parent is getattr(controller,'renamer',None):
                    renamer=True
                    break
                parent=getattr(parent,'master',None)
            message=describe(label,command,language()=='en', 'checkbutton' in widget.winfo_class().lower(),renamer)
            if not message:
                return
            tip=self.tip=tk.Toplevel(widget)
            tip.withdraw()
            tip.overrideredirect(True)
            tip.attributes('-topmost',True)
            tip.configure(bg='#D8D0C4')
            tk.Label(tip,text=message,bg='#F4F1EA',fg='#243033',font=('Segoe UI',10),
                     wraplength=360,justify='left',padx=12,pady=8).pack(padx=1,pady=1)
            tip.update_idletasks()
            x=widget.winfo_pointerx()+12
            y=widget.winfo_rooty()+widget.winfo_height()+8
            width,height=tip.winfo_reqwidth(),tip.winfo_reqheight()
            x=max(0,min(x,widget.winfo_screenwidth()-width-8))
            if y+height>widget.winfo_screenheight()-8:
                y=max(0,widget.winfo_rooty()-height-8)
            tip.geometry(f'+{x}+{y}')
            tip.deiconify()
        except tk.TclError:
            self.hide()
