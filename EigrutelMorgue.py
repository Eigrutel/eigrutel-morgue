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

"""Single entry point for Morgue: library, renamer and sketch sessions."""
from __future__ import annotations
from morgue_i18n import tr, trf

from ui_common import resource_path
import os
import copy
import morgue_i18n as i18n
from morgue_structure_en import STRUCTURE_EN
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ui_common import UI, apply_style, apply_app_icon, app_dir, load_json, save_json
import morgue_library as library
import morgue_renamer as renamer
from morgue_workspace import relocate_indexed_file

VERSION = '3.1.12'
SETTINGS_FILE = os.path.join(app_dir(), 'morgue_settings.json')
ABOUT = """Eigrutel Lab / Atelier d'outils libres pour la bande dessinée
Programme conçu et développé par Simon Léturgie
dans le cadre d'Eigrutel BD Academy.

Morgue / Version 3.1.12 / 10-09-2026
Application de bureau : Python (.py) et exécutable Windows (.exe).

Code source et programme compilé : GNU AGPL v3.0 ou version ultérieure.
Documentation et ressources : CC BY-SA 4.0, sauf mention contraire.
Les bibliothèques tierces conservent leurs licences respectives.
Marques, logos et signes distinctifs Eigrutel / Eigrutel Lab /
Eigrutel BD Academy : réservés.
"""


class Morgue:
    def __init__(self, root):
        self.root = root
        self.active_view = None
        self.refresh_pending = False
        self.closing = False
        self.folder = ''
        self.settings = load_json(SETTINGS_FILE, {})
        if not isinstance(self.settings, dict):
            self.settings = {}
        i18n.install()
        i18n.set_language(self.settings.get('language', 'fr'))
        from morgue_tooltips import Tooltips
        root._morgue_controller = self
        self.tooltips = Tooltips(root, self.settings.get('tooltips_enabled', True), self.set_tooltips_enabled)
        root._morgue_tooltips = self.tooltips
        root.title('Morgue / Eigrutel Lab')
        root.minsize(1280, 640)
        root.geometry('1440x900')
        try:
            root.state('zoomed')
        except tk.TclError:
            pass
        apply_style(root)
        apply_app_icon(root)
        self.folder_var = tk.StringVar(value=tr('Choisissez un dossier de travail'))
        self.language_var = tk.StringVar(value=i18n.language().upper())
        self.navigation_var = tk.StringVar(value='library')
        style = ttk.Style(root)
        self.chrome_style = style
        # Pages retain Notebook focus/event behavior; navigation lives in each toolbar.
        style.layout('Pages.TNotebook', [('Frame.border', {'sticky': 'nswe'})])
        style.layout('Pages.TNotebook.Tab', [])
        style.configure('Pages.TNotebook', borderwidth=0, padding=0, tabmargins=0, relief='flat', background='#1F3A44')
        style.configure('Pages.TFrame', borderwidth=0, relief='flat', background='#1F3A44')
        for name, color in (('Library', '#1F3A44'), ('Renamer', '#7F2D30')):
            style.configure(name+'.Topbar.TFrame', background=color)
            style.configure(name+'.Topbar.TLabel', background=color, foreground='#FAFAF7')
            style.configure(name+'.TopbarTitle.TLabel', background=color, foreground='#FAFAF7')
            style.configure(name+'.Topbar.TCheckbutton', background=color, foreground='#FAFAF7')
            style.map(name+'.Topbar.TCheckbutton', background=[('active',color)])
            tab_style = name+'.Nav.TRadiobutton'
            style.layout(tab_style, style.layout('TButton'))
            style.configure(tab_style, background=color, foreground='#FAFAF7',
                padding=(12,9), font=('Segoe UI',10), borderwidth=1, relief='flat')
            selected = '#2D4C57' if name == 'Library' else '#A63D40'
            style.map(tab_style, background=[('selected',selected),('active',selected)],
                foreground=[('selected','#FAFAF7'),('active','#FAFAF7')])
            lang_style = name+'.Language.TRadiobutton'
            style.layout(lang_style, style.layout('TButton'))
            style.configure(lang_style, background=color, foreground='#D8D0C4',
                padding=(7,6), font=('Segoe UI',9,'bold'), borderwidth=1, relief='flat')
            style.map(lang_style, background=[('selected',selected),('active',selected)],
                foreground=[('selected','#FAFAF7'),('active','#FAFAF7')],
                relief=[('selected','solid'),('!selected','flat')])
        self.tabs = ttk.Notebook(root, style='Pages.TNotebook')
        self.tabs.pack(fill='both', expand=True)
        self.library_page = ttk.Frame(self.tabs, style='Pages.TFrame')
        self.rename_page = ttk.Frame(self.tabs, style='Pages.TFrame')
        self.tabs.add(self.library_page, text=tr('Bibliothèque'))
        self.tabs.add(self.rename_page, text=tr('Classer / Renommer'))
        self.library = library.MorgueApp(self.library_page, self)
        self.renamer = renamer.DocumentationRenamer(self.rename_page, self)
        self._legacy_structure = copy.deepcopy(self.renamer.structure)
        self.library._create_local_styles()
        self.active_view = self.library
        self.tabs.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        root.bind('<Map>', lambda event: root.after_idle(self.update_title_color) if event.widget is root else None, add='+')
        root.after_idle(self.update_title_color)
        root.protocol('WM_DELETE_WINDOW', self.close)
        folder = self.settings.get('folder') or self.library.folder or self.renamer.folder
        if folder and os.path.isdir(folder):
            self.set_folder(folder)
        else:
            self.library.folder = ''
            self.library.run_search()
        self.library.entry_search.focus_set()

    def set_tooltips_enabled(self, enabled):
        self.settings['tooltips_enabled'] = bool(enabled)
        save_json(SETTINGS_FILE, self.settings)

    def update_title_color(self):
        from morgue_windows_icon import set_caption_color
        color = '#7F2D30' if self.active_view is self.renamer else '#1F3A44'
        if getattr(self, 'chrome_style', None) is not None:
            self.root.configure(bg=color)
            self.chrome_style.configure('Pages.TNotebook', background=color,
                bordercolor=color, lightcolor=color, darkcolor=color)
            self.chrome_style.configure('Pages.TFrame', background=color)
        set_caption_color(self.root, color)

    def create_toolbar(self, parent, section):
        """Same physical height for both workspaces, including Windows scaling."""
        bar = ttk.Frame(parent, style=section+'.Topbar.TFrame',
            padding=(14,0), borderwidth=0, relief='flat', height=round(self.root.winfo_fpixels('48p')))
        bar.pack(fill='x')
        bar.pack_propagate(False)
        return bar

    def add_toolbar_navigation(self, parent, section, help_command):
        """Identical controls in both original toolbars, with shared state."""
        info = tk.Button(parent, text='i', command=help_command, bg='#F4F1EA',
            fg='#7F2D30', activebackground='#FFFFFF', activeforeground='#7F2D30',
            font=('Segoe UI',11,'bold'), padx=13, pady=7, bd=0, cursor='hand2')
        info.pack(side='right', padx=(8,0), pady=6)
        nav = ttk.Frame(parent, style=section+'.Topbar.TFrame')
        nav.pack(side='right', padx=(10,0), pady=6)
        for key, label in (('library', tr('Bibliothèque')), ('renamer', tr('Classer / Renommer'))):
            ttk.Radiobutton(nav, text=label, variable=self.navigation_var, value=key,
                style=('Library' if key == 'library' else 'Renamer')+'.Nav.TRadiobutton',
                command=lambda target=key: self.navigate(target)).pack(side='left')
        languages = ttk.Frame(parent, style=section+'.Topbar.TFrame')
        languages.pack(side='right', padx=(8,0))
        for code in ('FR','EN'):
            ttk.Radiobutton(languages, text=code, value=code, variable=self.language_var,
                style=section+'.Language.TRadiobutton',
                command=self.change_language).pack(side='left')

    def navigate(self, target):
        # Preserve the bridge: the selected reference follows entry to the renamer.
        if target == 'library':
            if self.tabs.select() != str(self.library_page):
                self.show_library()
        elif self.tabs.select() != str(self.rename_page):
            self.edit_selection()

    def change_language(self, event=None):
        if getattr(self, 'tooltips', None):
            self.tooltips.hide()
        chosen = self.language_var.get().lower()
        i18n.set_language(chosen)
        self.settings['language'] = i18n.language()
        self.tabs.tab(self.library_page, text=tr('Bibliothèque'))
        self.tabs.tab(self.rename_page, text=tr('Classer / Renommer'))
        save_json(SETTINGS_FILE, self.settings)
        # Update computed summaries. Search terms, selected image and naming data
        # are intentionally untouched when changing the interface language.
        self.library.refresh_indexed_counter()
        self.library.refresh_collected_counter()
        self.library.refresh_atelier_panel_counts()

    def save_classification(self):
        if not self.folder or not hasattr(self, 'renamer'):
            return
        self.settings.setdefault('classification_profiles', {})[self.folder] = {
            'language': getattr(self.renamer, 'naming_language', 'fr'),
            'structure': copy.deepcopy(self.renamer.structure),
        }
        save_json(SETTINGS_FILE, self.settings)

    def update_classification_filters(self):
        labels = {'composition':'Composition', 'forme':'Forme', 'silhouette':'Silhouette',
                  'couleur':'Couleur', 'lumiere':'Lumiere', 'valeurs':'Valeurs', 'echelle':'Echelle'}
        for item in self.library.filter_definitions:
            item['query'] = self.renamer.naming_token(labels[item['key']]).lower()
        self.classification_button.configure(text=trf('Classement : {0}', self.renamer.naming_language.upper()))

    def choose_classification(self):
        if not self.can_modify():
            return
        if not self.folder:
            messagebox.showinfo('Morgue', tr('Choisissez un dossier de travail'), parent=self.root)
            return
        win = tk.Toplevel(self.root)
        win.title(tr('Langue de classement'))
        win.transient(self.root)
        win.grab_set()
        apply_app_icon(win)
        win.configure(bg='#F4F1EA')
        win.resizable(False, False)
        header = tk.Frame(win, bg='#7F2D30', padx=24, pady=18)
        header.pack(fill='x')
        tk.Label(header, text='MORGUE', bg='#7F2D30', fg='#F4F1EA',
                 font=('Segoe UI',9,'bold')).pack(anchor='w')
        tk.Label(header, text=tr('Langue de classement'), bg='#7F2D30', fg='#FAFAF7',
                 font=('Segoe UI',20,'bold')).pack(anchor='w', pady=(5,0))
        tk.Frame(win, height=3, bg='#F4F1EA').pack(fill='x')
        frame = tk.Frame(win, bg='#FAFAF7', padx=24, pady=20)
        frame.pack(fill='both', expand=True, padx=16, pady=16)
        tk.Label(frame, text=tr('Choisissez le modèle de catégories pour cette bibliothèque.\nLes fichiers et dossiers existants ne seront pas renommés.'),
                 bg='#FAFAF7', fg='#243033', font=('Segoe UI',11),
                 wraplength=560, justify='left').pack(anchor='w', pady=(0,18))
        selected = tk.StringVar(value=self.renamer.naming_language)
        choices = tk.Frame(frame, bg='#FAFAF7')
        choices.pack(fill='x')
        cards = []
        def highlight():
            for code, card, button, example in cards:
                background = '#F4F1EA' if selected.get()==code else '#FAFAF7'
                card.configure(bg=background, highlightbackground='#7F2D30' if selected.get()==code else '#D8D0C4')
                button.configure(bg=background)
                example.configure(bg=background)
        for column, (code, title, example_text) in enumerate((
            ('fr', tr('Modèle français'), 'Animaux / Chevaux'),
            ('en', tr('Modèle anglais'), 'Animals / Horses'),
        )):
            choices.columnconfigure(column, weight=1, uniform='language')
            card = tk.Frame(choices, bg='#FAFAF7', highlightthickness=2, highlightbackground='#D8D0C4')
            card.grid(row=0, column=column, sticky='nsew', padx=(0,12) if column==0 else (0,0))
            button = tk.Radiobutton(card, text=title, variable=selected, value=code,
                command=highlight, bg='#FAFAF7', fg='#7F2D30', activebackground='#F4F1EA',
                activeforeground='#7F2D30', selectcolor='#F4F1EA',
                font=('Segoe UI',12,'bold'), anchor='w', padx=12, pady=12, bd=0)
            button.pack(fill='x')
            example = tk.Label(card, text=example_text, bg='#FAFAF7', fg='#6F7473',
                font=('Segoe UI',10), padx=16, pady=10, anchor='w')
            example.pack(fill='x')
            example.bind('<Button-1>', lambda event, radio=button: radio.invoke())
            cards.append((code, card, button, example))
        highlight()
        tk.Label(frame, text='DOCUMENTATION_', font=('Consolas',10,'bold'),
            bg='#FAFAF7', fg='#7F2D30', anchor='w').pack(fill='x', pady=(18,0))
        footer = tk.Frame(win, bg='#F4F1EA', padx=16, pady=12)
        footer.pack(fill='x')
        def apply():
            if not messagebox.askyesno('Morgue', tr('Remplacer les catégories actuelles par ce modèle ?\nExportez votre architecture auparavant si vous souhaitez en garder une copie.\nAucun fichier ne sera renommé.'), parent=win):
                return
            self.renamer.naming_language = selected.get()
            self.renamer.structure = copy.deepcopy(STRUCTURE_EN if selected.get() == 'en' else renamer.STRUCTURE_BASE)
            self.renamer._refresh_structure_views()
            self.save_classification()
            self.update_classification_filters()
            self.library.sync_filter_checkboxes_from_search()
            win.destroy()
        ttk.Button(footer, text=tr('Appliquer le modèle'), style='Red.Accent.TButton', command=apply).pack(side='right')
        ttk.Button(footer, text=tr('Annuler'), style='Side.TButton', command=win.destroy).pack(side='right', padx=(0,10))
        win.bind('<Escape>', lambda event: win.destroy())

    def on_tab_changed(self, event=None):
        self.tooltips.hide()
        self.navigation_var.set('library' if self.tabs.select() == str(self.library_page) else 'renamer')
        self.active_view = self.library if self.tabs.select() == str(self.library_page) else self.renamer
        self.update_title_color()
        if self.active_view is self.renamer:
            self.library.hide_atelier_panel()
            self.renamer.level_search_entry.focus_set()
        else:
            self.library.entry_search.focus_set()

    def can_modify(self):
        if self.library.indexing:
            messagebox.showinfo('Morgue', tr('Attendez la fin de l’indexation avant de renommer, ranger ou changer de dossier.'), parent=self.root)
            return False
        return True

    def choose_folder(self):
        if not self.can_modify():
            return
        path = filedialog.askdirectory(parent=self.root, title=tr('Choisir le dossier de travail'), initialdir=self.folder or None)
        if path:
            self.set_folder(path)

    def set_folder(self, path):
        if self.library.indexing:
            return
        if self.folder:
            self.save_classification()
        self.folder = library.normalize_library_root(path)
        profile = self.settings.get('classification_profiles', {}).get(self.folder)
        if isinstance(profile, dict) and isinstance(profile.get('structure'), dict):
            self.renamer.structure = copy.deepcopy(profile['structure'])
            self.renamer.naming_language = 'en' if profile.get('language') == 'en' else 'fr'
        else:
            self.renamer.structure = copy.deepcopy(self._legacy_structure)
            self.renamer.naming_language = 'fr'
        self.renamer._refresh_structure_views()
        self.update_classification_filters()
        self.save_classification()
        self.folder_var.set(self.folder)
        self.settings['folder'] = self.folder
        save_json(SETTINGS_FILE, self.settings)
        self.library.folder = self.folder
        self.library.settings['folder'] = self.folder
        save_json(library.SETTINGS_FILE, self.library.settings)
        self.renamer.folder = self.folder
        self.renamer._load_files()
        self.renamer.idx = 0
        self.renamer._load_current()
        self.renamer._save_settings()
        self.library.results_signature = ()
        self.library.run_search()
        self.library.refresh_indexed_counter()
        self.library.refresh_collected_counter()
        n = library.count_indexed_images(self.folder)
        self.library.status_var.set(trf('{0} images indexées / Réindexer pour analyser ce dossier.', n))

    def show_library(self):
        self.tabs.select(self.library_page)
        self.active_view = self.library
        self.navigation_var.set('library')
        if self.refresh_pending:
            # Let geometry and paint events finish before loading changed results.
            self.root.after_idle(lambda: self.root.after(20, self.refresh_library))

    def edit_selection(self):
        item = self.library.current_item
        if item:
            items = self.library.results
            self.renamer.files = [renamer.FileItem(path=i['path'], rel=os.path.relpath(i['path'], self.folder)) for i in items]
            self.renamer.idx = self.library.current_idx
            self.renamer._load_current()
        self.tabs.select(self.rename_page)
        self.active_view = self.renamer

    def relocate(self, source, destination, destination_root=None):
        if self.library.indexing:
            raise RuntimeError(tr('Indexation en cours : attendez sa fin.'))
        relocate_indexed_file(source, destination, self.folder, destination_root)
        # These objects may be shared by the library/Atelier; update in place.
        for item in self.library.results:
            if item['path'] == source:
                item.update(path=destination, filename=os.path.basename(destination), folder=os.path.dirname(destination))
        for item in self.renamer.files:
            if item.path == source:
                item.path = destination
                item.rel = os.path.relpath(destination, self.folder)
        if not self.refresh_pending:
            self.refresh_pending = True
            self.root.after_idle(self.refresh_library)

    def refresh_library(self):
        # Keep changes pending while the renamer is visible; coalesce callbacks.
        if not self.refresh_pending or self.active_view is not self.library:
            return
        self.refresh_pending = False
        # Cached thumbnails are keyed by path, mtime and size; unchanged ones
        # remain valid after a rename and must not be decoded again.
        self.library.results_signature = ()
        self.library.preserve_results_scroll = True
        self.library.run_search()
        self.library.refresh_indexed_counter()
        self.library.refresh_collected_counter()

    def about(self):
        messagebox.showinfo(tr('À propos de Morgue'), tr(ABOUT), parent=self.root)

    def close(self):
        if self.library.indexing:
            self.closing = True
            self.library.index_cancel.set()
            self.folder_var.set(tr('Fermeture après interruption de l’indexation…'))
            self.root.after(100, self.close)
            return
        self.renamer._save_settings()
        self.save_classification()
        save_json(SETTINGS_FILE, self.settings)
        self.root.destroy()


def main():
    from morgue_windows_icon import prepare_identity, install, log_error
    try:
        prepare_identity()
    except (AttributeError, OSError) as error:
        log_error(error)
    root = tk.Tk()
    Morgue(root)
    install(root)
    root.mainloop()


if __name__ == '__main__':
    main()
