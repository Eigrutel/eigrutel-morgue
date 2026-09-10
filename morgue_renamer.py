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

# -*- coding: utf-8 -*-
"""
documentation.py / Documentation Renamer (UI cohérente, sans scrollbar)

Ajouts / corrections:
- Ajout affichage "Nom cible : …" sous le nom du fichier (colonne gauche, barre nav)
- Calcul du nom cible sans recharger l’image (update live)
- Update du nom cible quand:
  - on change N1 / N2 / N3
  - on coche Inspiration
  - on modifie Précision
  - on change le compteur (Numéro départ) / auto-incrément
- AJOUT: deux cases à cocher "Photo" / "Dessin" à côté d'Inspiration
  - intégrées dans le nom cible après "Inspiration"
  - sauvegardées/restaurées dans settings.json
"""

from __future__ import annotations
from morgue_i18n import tr, trf
from morgue_structure_en import STRUCTURE_EN


# Révision technique : 09-09-2026 / recherche, affichage et fiabilité.

import ctypes
from ui_common import resource_path
import os
import re
import json
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import shutil
from PIL import Image, ImageTk, ImageOps
Image.MAX_IMAGE_PIXELS = None

from ui_common import UI, apply_style, app_dir, load_json, save_json, new_session_id, log_rename, open_with_default_app
from ui_common import apply_app_icon, bind_digits_only

# =========================
# CONFIG
# =========================
APP_TITLE = "Documentation - Eigrutel tools"
APP_CODE = "DOCUMENTATION"
INDEX_DOC_WINDOW_TITLE = "Morgue - Eigrutel tools"

IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff")
INVALID_WIN = r'[<>:"/\\|?*\n\r\t]'

INSPIRATION_MAIN_ITEMS = [
    "Composition", "Forme", "Silhouette", "Couleur", "Lumiere", "Valeurs", "Echelle"
]

INSPIRATION_MOVEMENT_ITEMS = [
    "Marche", "Course", "Saut", "Combat"
]

INSPIRATION_ITEMS = INSPIRATION_MAIN_ITEMS + INSPIRATION_MOVEMENT_ITEMS
INSPIRATION_TYPES = ["PHOTO", "Dessin", "Master"]

SETTINGS_FILE = os.path.join(app_dir(), "settings.json")
STRUCTURE_USER_FILE = os.path.join(app_dir(), "documentation_structure_user.json")
STRUCTURE_BACKUP_EXT = ".docarch.json"

# =========================
# STRUCTURE (base)
# =========================
STRUCTURE_BASE = {
    "Animaux": {
        "Chevaux": ["Ranch_Western", "Travail", "Trotteurs_Course_Saut"],
        "Divers": ["Insectes", "Oiseaux", "Poissons", "Reptiles"],
        "Domestiques": ["Bovins", "Chats", "Chiens", "Lapins", "Ovins", "Porcs", "Rongeurs"],
        "Sauvages": ["Cerfs", "Chameaux", "Elephants", "Felins", "Loups", "Ours", "Renards", "Singes"],
    },
    "Arts et sciences": {
        "Arts": ["Composition", "Couleurs", "Sculpture"],
        "Sciences": ["Astronomie", "Laboratoire", "Medical"],
    },
    "Costume": {
        "Divers": ["Armures", "Militaire", "Noblesse", "Theatre", "Uniformes"],
        "Epoque": ["15eme", "16eme", "17eme", "18eme", "19eme", "20eme", "Antiquite", "Moyen_Age"],
        "Mode Enfant": ["Bijoux", "Chapeaux", "Chaussures", "Chemises", "Coiffures", "Costumes",
                        "Lingerie", "Lunettes", "Manteaux", "Pantalons", "Pulls", "Pyjamas"],
        "Mode Femme": ["Bijoux", "Chapeaux", "Chaussures", "Chemises", "Coiffures", "Costumes",
                       "Fourrures", "Lingerie", "Lunettes", "Manteaux", "Pantalons", "Pulls", "Pyjamas"],
        "Mode Homme": ["Chapeaux", "Chaussures", "Chemises", "Coiffures", "Costumes",
                       "Lingerie", "Lunettes", "Manteaux", "Pantalons", "Pulls", "Pyjamas"],
        "Tissus": ["Drapeaux", "Motifs", "Plis", "Textures"],
    },
    "Dessinateurs": {
        "Animation": ["Milt_Kahl", "Chuck_Jones"],
        "Bande dessinée": ["Franquin", "Eisner"],
        "Caricature": ["Mort_Drucker", "Sebastian_Kruger"],
        "Illustration": ["Rockwell", "Frazetta","Wyeth"],
    },
    "Divers": {
        "Catastrophes": ["Explosions", "Incendies", "Inondations", "Tempetes"],
        "Divers": ["Guerre", "Journaux", "Nourritures", "Telephones", "Vacances"],
        "Ecole": ["College", "Fac", "Lycee", "Maternelle", "Primaire"],
        "Etat": ["Gouvernement", "Police", "Poste", "Prison"],
        "Religieux": ["Chamanisme", "Chretiens", "Hindous", "Juifs", "Mariages", "Musulmans"],
        "Rue": ["Lampadaires_Luminaires", "Ponts", "Scenes_de_rue", "Tunnels"],
    },
    "Divertissement": {
        "Cinema": ["Camera_Materiel", "Plateaux", "Salle"],
        "Danse": ["Ballet", "HipHop", "Salle"],
        "Divers": ["Carnavals", "Cirques", "Discotheques", "Fetes", "Radio", "Restaurants", "Television"],
        "Jeux Video": ["FPS_FirstPersonShooter", "Gaming", "PixelArt", "Plateformers"],
        "Musique": ["Chanteurs", "Concerts", "Cordes", "Orchestre", "Percussions", "Vents"],
        "Theatre": ["Coulisses", "Salle", "Scene"],
    },
    "Geographie": {
        "Afrique": ["Centrale", "Egypte", "Est", "Maghreb", "Ouest", "Sud"],
        "Amerique_Centrale_Sud": ["Amazonie", "Bresil", "Caraibes", "Mexique", "Perou"],
        "Amerique_Nord": ["Californie", "Canada", "Est", "Floride", "MiddleWest", "NewYork", "Sud", "WashingtonDC", "West"],
        "Asie": ["Chine", "Coree", "Inde", "Japon", "Vietnam"],
        "Europe": ["Allemagne", "Angleterre", "Balkans", "Espagne", "France", "Italie", "Pays_de_l_Est", "Russie", "Scandinavie"],
        "Oceanie": ["Australie", "Nouvelle_Zelande"],
    },
    "Industrie": {
        "Agriculture": ["Equipement_Agricole", "Fermes", "Granges"],
        "Industrie": ["Acier", "Alimentaire", "Bois", "Chimie", "Construction", "Mines", "Petrole", "Usines"],
        "Magasins_Bureaux": ["Alimentation", "Boucheries", "Boulangeries", "Banques", "Boutiques_Diverses",
                             "Bureaux", "Epiceries", "Pharmacies"],
    },
    "Logement": {
        "Exterieur": ["Clotures_murs", "Escaliers", "Facades", "Garages", "Grilles", "Porches_Terrasses", "Portes_Fenetres"],
        "Interieur": ["Ateliers", "Buanderie", "Chauffages_Ventilations", "Cheminees", "Escaliers", "Murs", "Portes_Fenetres"],
        "Mobilier": ["Argenterie", "Bar", "Ecrans", "Horloges", "Lampes", "Miroirs_Cadres", "ServiceDeTable",
                     "Bureaux", "Canapes", "Chaises", "Commodes_Armoire", "Mobilier_Exterieur", "Tables"],
        "Pieces": ["Chambres", "Cuisines", "Salles_a_manger", "Salles_de_bain", "Salons", "WC"],
    },
    "Nature": {
        "Arbres": ["Avec_feuilles", "Branches_nues", "En_fleur", "Troncs_Ecorces", "Tropiques"],
        "Divers": ["Eclairs", "Montagnes", "Nuages", "Rochers"],
        "Jardins_Fleurs": ["Accessoires_de_jardin", "Fleurs", "Jardins", "Outils_de_jardin", "Plantes", "Vignes"],
        "Neige_Eau": ["Eau", "Glace", "Neige"],
    },
    "Objets": {
        "Contenants": ["Bouteille", "Vase", "Boite"],
        "Outils": ["Marteau", "Ciseaux", "Tournevis"],
        "Sieges_supports": ["Chaise", "Tabouret", "Banc"],
        "Eclairage": ["Lampe", "Lanterne", "Bougie"],
        "Mesure_precision": ["Regle", "Compas", "Balance"],
        "Communication_ecriture": ["Stylo", "Livre", "Telephone"],
        "Fermeture_acces": ["Cle", "Serrure", "Cadenas"],
        "Cuisine": ["Cafetiere", "Casserole", "Tasse"],
        "Transport_portage": ["Valise", "Panier", "Sac"],
    },
    "Peintres": {
        "Renaissance": ["Leonard_de_Vinci", "Michelange"],
        "Baroque": ["Rembrandt", "Vermeer"],
        "Rococo": ["Watteau", "Fragonard"],
        "Neoclassicisme": ["David", "Ingres"],
        "Romantisme": ["Delacroix", "Gericault"],
        "Realisme": ["Courbet", "Millet"],
        "Impressionnisme": ["Monet", "Renoir"],
        "Postimpressionnisme": ["Van_Gogh", "Cezanne"],
        "Symbolisme": ["Moreau", "Redon"],
        "Art_nouveau": ["Klimt", "Mucha"],
        "Expressionnisme": ["Munch", "Kirchner"],
        "Cubisme": ["Picasso", "Braque"],
        "Surrealisme": ["Dali", "Magritte"],
    },
    "Personnes": {
        "Divers": ["Celebrites", "Foules"],
        "Enfants": ["Adolescents", "Aires_de_jeux", "Bebes", "Filles", "Garcons", "Jouets", "Meubles_chambre_enfants"],
        "Femmes": ["Angle", "Emotions_Expressions", "Mature", "Nus", "Modele_assis", "Modele_debout", "Modele_sol", "Profil", "Vieux", "Visage_complet"],
        "Hommes": ["Angle", "Barbes", "Durs_a_cuire", "Emotions_Expressions", "Mature", "Nus", "Modele_assis", "Modele_debout", "Modele_sol", "Profil", "Vieux", "Visage_complet"],
    },
        "Photographes": {
        "XIXe": ["Nadar", "Julia_Margaret_Cameron"],
        "Debut_XXe": ["Eugene_Atget", "Alfred_Stieglitz"],
        "XXe": ["Cartier_Bresson", "Robert_Capa"],
        "Fin_XXe": ["Helmut_Newton", "Richard_Avedon"],
        "Contemporain": ["Annie_Leibovitz", "Steve_McCurry"],
    },
    "Sports": {
        "Evenements": ["Baseball", "Basketball", "Boxe", "Course_automobile", "Football", "Hockey", "Piste", "Tauromachie"],
        "Individuels": ["Bowling", "Camp_pique_nique", "Cyclisme", "Golf", "Gymnase", "Natation", "Peche", "Ski",
                        "Sports_d_hiver", "Tennis", "Tir", "Tir_a_l_arc"],
    },
    "Transports": {
        "Automobiles": ["Anciennes", "Camionnettes", "Camions", "Motos", "Remorques", "Stations_service", "Urbaines"],
        "Avions": ["Avions", "Avions_de_ligne", "Helicopteres", "Parachutes"],
        "Bateaux": ["A_rames", "Canoes", "Croisieres", "Navires_marchands", "Paquebots", "Voiliers"],
        "Publics": ["Bagages", "Bus", "Gares", "Taxis", "Trains"],
    },
    "Références": {
        "Bande Dessinée": ["Franco-Belge", "Comics", "Manga", "Auteur"],
        "Animation": ["Personnage", "Décor", "Disney", "Stopmotion"],
        "Illustration": ["peinture", "Couverture", "Noir_et_blanc", "affiche"],
    },
}


# =========================
# Utils
# =========================
def _strip_accents(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(ch for ch in s if not unicodedata.combining(ch))

def sanitize_token_compact(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return ""
    s = _strip_accents(s)
    s = re.sub(INVALID_WIN, "", s)
    s = s.replace(" ", "_")
    s = re.sub(r"_+", "_", s)
    return s[:80].strip("_")

def apply_windows_folder_icon(folder_path: str, icon_name: str = "DOC.ico") -> None:
    if not sys.platform.startswith("win"):
        return

    try:
        src_icon = resource_path(icon_name)
        dst_icon = os.path.join(folder_path, icon_name)

        if os.path.isfile(src_icon) and not os.path.isfile(dst_icon):
            shutil.copy2(src_icon, dst_icon)

        desktop_ini = os.path.join(folder_path, "desktop.ini")

        with open(desktop_ini, "w", encoding="utf-8") as f:
            f.write(
                "[.ShellClassInfo]\n"
                f"IconResource={icon_name},0\n"
            )

        ctypes.windll.kernel32.SetFileAttributesW(desktop_ini, 0x2 | 0x4)
        ctypes.windll.kernel32.SetFileAttributesW(folder_path, 0x1)

    except Exception:
        pass

def apply_window_icon(win, icon_name: str = "Morgue.ico") -> None:
    apply_app_icon(win)

def bring_window_to_front(window_title: str) -> bool:
    """
    Windows uniquement.
    Cherche une fenêtre par son titre exact, la restaure si minimisée
    et la place au premier plan.
    Retourne True si trouvée, sinon False.
    """
    if not sys.platform.startswith("win"):
        return False

    try:
        user32 = ctypes.windll.user32
        hwnd = user32.FindWindowW(None, window_title)
        if not hwnd:
            return False

        SW_MAXIMIZE = 3
        user32.ShowWindow(hwnd, SW_MAXIMIZE)
        user32.SetForegroundWindow(hwnd)
        return True
    except Exception:
        return False





def deep_merge_structure(base: dict, extra: dict) -> dict:
    out = json.loads(json.dumps(base, ensure_ascii=False))
    if not isinstance(extra, dict):
        return out
    for n1, d2 in extra.items():
        if not isinstance(n1, str) or not isinstance(d2, dict):
            continue
        out.setdefault(n1, {})
        for n2, lst3 in d2.items():
            if not isinstance(n2, str) or not isinstance(lst3, list):
                continue
            out[n1].setdefault(n2, [])
            for x in lst3:
                if isinstance(x, str) and x not in out[n1][n2]:
                    out[n1][n2].append(x)
    return out


@dataclass
class FileItem:
    path: str
    rel: str


# =========================
# App
# =========================

class DocumentationRenamer(ttk.Frame):
    LEFT_W = 760
    RIGHT_W = 460

    def _bind_scoped(self, sequence, callback, add=None):
        def dispatch(event):
            try:
                if self.workspace.active_view is self and event.widget.winfo_toplevel() == self.root:
                    return callback(event)
            except tk.TclError:
                return None
        return self.root.bind(sequence, dispatch, add="+")

    def __init__(self, master, workspace):
        super().__init__(master, style="App.TFrame")
        self.root = master.winfo_toplevel()
        self.workspace = workspace
        self.naming_language = "fr"
        self.session_id = new_session_id("DOC-")

        self.SUBBTN_BG = "#3c4F5F"
        self.SUBBTN_BG_ACTIVE = "#3c4F5F"
        self.SUBBTN_FG = "#FFFFFF"

        # state
        self.folder: str = ""
        self.include_subdirs = tk.BooleanVar(value=False)
        self.files: list[FileItem] = []
        self.idx = 0

        self.counter = 1
        self.manual_mode = False

        self.tk_img: ImageTk.PhotoImage | None = None
        self._src_img: Image.Image | None = None

        # selections
        self.selected_lvl1: str | None = None
        self.selected_lvl2: str | None = None
        self.lvl3_vars: dict[str, tk.IntVar] = {}
        self.lvl3_widgets: dict[str, tk.Widget] = {}

        self.level_search_var = tk.StringVar(value="")
        self.level_search_hint_var = tk.StringVar(value="")

        self.insp_vars: dict[str, tk.IntVar] = {k: tk.IntVar(value=0) for k in INSPIRATION_ITEMS}
        self.insp_type_vars: dict[str, tk.IntVar] = {k: tk.IntVar(value=0) for k in INSPIRATION_TYPES}
        # structure
        extra = load_json(STRUCTURE_USER_FILE, {})
        self.structure = deep_merge_structure(STRUCTURE_BASE, extra)

        # settings
        self.settings = self._load_settings()

        self._build_ui()
        self._bind_keys()
        self._restore_settings()
        self._refresh_top_count()
        self._refresh_status_texts()
        self._update_target_label()

    # ---------- common buttons ----------
    def _sub_button(self, parent, text: str, command, *, small: bool = True) -> tk.Button:
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.SUBBTN_BG,
            fg=self.SUBBTN_FG,
            activebackground=self.SUBBTN_BG_ACTIVE,
            activeforeground=self.SUBBTN_FG,
            bd=0,
            relief="flat",
            cursor="hand2",
        )
        if small:
            btn.configure(padx=8, pady=3)
        else:
            btn.configure(padx=10, pady=6)
        return btn

    def _clear_btn(self, parent, entry: ttk.Entry) -> tk.Button:
        def _do_clear():
            entry.delete(0, "end")
            self._on_field_changed()

        btn = tk.Button(
            parent,
            text="✕",
            command=_do_clear,
            bd=0,
            padx=6,
            pady=2,
            fg="#7F2D30",
            bg=getattr(UI, "PANEL", "#FFFFFF"),
            activeforeground="#7F2D30",
            activebackground=getattr(UI, "PANEL", "#FFFFFF"),
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
        )
        return btn
    
    def launch_index_documentation(self):
        self.workspace.show_library()
    # ---------- settings ----------
    def _load_settings(self) -> dict:
        all_s = load_json(SETTINGS_FILE, {})
        if not isinstance(all_s, dict):
            all_s = {}
        s = all_s.get("documentation")
        return s if isinstance(s, dict) else {}

    def _save_settings(self):
        all_s = load_json(SETTINGS_FILE, {})
        if not isinstance(all_s, dict):
            all_s = {}
        all_s["documentation"] = {
            "last_dir": self.folder,
            "include_subdirs": bool(self.include_subdirs.get()),
            "counter": int(self.counter) if isinstance(self.counter, int) else 1,
            "counter_entry": self.start_var.get().strip() if hasattr(self, 'start_var') else "1",
            "precision": self.precision_var.get() if hasattr(self, 'precision_var') else "",
            "manual_target": self.target_name_var.get() if hasattr(self, 'target_name_var') else "",
            "manual_mode": bool(self.manual_mode),
            "insp": {k: int(v.get()) for k, v in self.insp_vars.items()},
            "insp_types": {k: int(v.get()) for k, v in self.insp_type_vars.items()},
            "selected_lvl1": self.selected_lvl1,
            "selected_lvl2": self.selected_lvl2,
            "selected_lvl3": [k for k, v in self.lvl3_vars.items() if v.get() == 1],
        }
        save_json(SETTINGS_FILE, all_s)

    def _restore_settings(self):
        self.folder = str(self.settings.get("last_dir") or "")
        self.include_subdirs.set(bool(self.settings.get("include_subdirs", False)))

        try:
            self.counter = int(self.settings.get("counter", 1))
        except Exception:
            self.counter = 1
        self.start_var.set(str(self.settings.get("counter_entry", self.counter)))

        self.precision_var.set(str(self.settings.get("precision", "")))

        insp = self.settings.get("insp", {})
        if isinstance(insp, dict):
            for k, v in self.insp_vars.items():
                try:
                    v.set(1 if int(insp.get(k, 0)) else 0)
                except Exception:
                    v.set(0)

        insp_types = self.settings.get("insp_types", {})
        if isinstance(insp_types, dict):
            for k, v in self.insp_type_vars.items():
                try:
                    v.set(1 if int(insp_types.get(k, 0)) else 0)
                except Exception:
                    v.set(0)

        self._refresh_lvl1_list()

        restore_n1 = self.settings.get("selected_lvl1")
        if isinstance(restore_n1, str) and restore_n1 in self.structure:
            keys1 = [self.lvl1_list.get(i) for i in range(self.lvl1_list.size())]
            if restore_n1 in keys1:
                i = keys1.index(restore_n1)
                self.lvl1_list.selection_clear(0, tk.END)
                self.lvl1_list.selection_set(i)
                self.lvl1_list.activate(i)
                self.selected_lvl1 = restore_n1
                self.on_select_lvl1(force_refresh=True)

        restore_n2 = self.settings.get("selected_lvl2")
        if self.selected_lvl1 and isinstance(restore_n2, str):
            keys2 = [self.lvl2_list.get(i) for i in range(self.lvl2_list.size())]
            if restore_n2 in keys2:
                i = keys2.index(restore_n2)
                self.lvl2_list.selection_clear(0, tk.END)
                self.lvl2_list.selection_set(i)
                self.lvl2_list.activate(i)
                self.selected_lvl2 = restore_n2
                self.on_select_lvl2(force_refresh=True)

        restore_n3 = self.settings.get("selected_lvl3", [])
        if isinstance(restore_n3, list):
            for k in restore_n3:
                if k in self.lvl3_vars:
                    self.lvl3_vars[k].set(1)

        if self.folder and os.path.isdir(self.folder):
            self._load_files()
            self.idx = 0
            self._load_current()

        self.manual_mode = bool(self.settings.get("manual_mode", False))
        if self.manual_mode:
            self.target_name_var.set(str(self.settings.get("manual_target", "")))
        else:
            self._update_target_label()

    # ---------- dialogs ----------#
    def open_info_dialog(self):
        from morgue_help import show_help
        show_help(self.root, 'renamer')

    def open_metadata_dialog(self):
        it = self._current_item()
        if not it:
            return
        dlg = tk.Toplevel(self.root)
        dlg.title(tr('Métadonnées'))
        apply_window_icon(dlg)
        dlg.transient(self.root)
        dlg.grab_set()
        dlg.minsize(520, 420)

        outer = ttk.Frame(dlg, padding=12)
        outer.pack(fill="both", expand=True)
        txt = tk.Text(
            outer,
            wrap="word",
            bg=getattr(UI, "PANEL", "#FFFFFF"),
            fg="#111111",
            relief="solid",
            bd=1,
            highlightthickness=0,
            padx=10,
            pady=8,
            font=("Segoe UI", 10),
        )
        txt.pack(fill="both", expand=True)
        txt.insert("1.0", self._metadata_text(it.path))
        txt.configure(state="disabled")
        ttk.Button(outer, text=tr('Fermer'), style="Side.TButton", command=dlg.destroy).pack(anchor="e", pady=(10, 0))

    # ---------- ui ----------
    def _build_ui(self):
        self.pack(fill="both", expand=True)
        top = self.workspace.create_toolbar(self, 'Renamer')

        ttk.Label(top, text='Morgue', style="Renamer.TopbarTitle.TLabel").pack(side="left", padx=(0, 14))
        ttk.Button(top, text=tr('Choisir dossier'), style="Paper.Accent.TButton", command=self.open_folder).pack(side="left", padx=10, pady=8)

        ttk.Checkbutton(
            top,
            text=tr('Inclure sous-dossiers'),
            variable=self.include_subdirs,
            style="Renamer.Topbar.TCheckbutton",
            command=self._on_toggle_subdirs,
        ).pack(side="left", padx=10)

        self.top_count_lbl = ttk.Label(top, text="0 / 0", style="Renamer.Topbar.TLabel")
        self.top_count_lbl.pack(side="left", padx=(12, 0))

        

        self.workspace.add_toolbar_navigation(top, 'Renamer', self.open_info_dialog)

        ttk.Button(
            top,
            text=tr('Ranger DOCUMENTATION'),
            style="Paper.Accent.TButton",
            command=self.auto_sort_documentation_lvl3
        ).pack(side="right", padx=(0, 10), pady=8)
        main = ttk.Frame(self, style="App.TFrame", padding=(12, 0, 12, 12))
        main.pack(fill="both", expand=True)
        main.grid_columnconfigure(0, weight=1, uniform="halves")
        main.grid_columnconfigure(1, weight=1, uniform="halves")
        main.grid_rowconfigure(0, weight=1)

        # Left column = preview + controls below preview
        self.left = ttk.Frame(main, style="Panel.TFrame")
        self.left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        self.left.bind("<Button-1>", self._clear_text_focus)

        self.left.grid_columnconfigure(0, weight=1)
        self.left.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.left, bg="#ECEFF4", highlightthickness=1, highlightbackground=UI.BORDER)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=14, pady=(14, 10))
        self.canvas.bind("<Configure>", lambda e: self._redraw_canvas())
        self.canvas.bind("<Button-1>", self._clear_text_focus)

        controls = ttk.Frame(self.left, style="Panel.TFrame")
        controls.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 14))
        controls.grid_columnconfigure(0, weight=1)

        self.lbl_current = ttk.Label(controls, text=tr('Nom actuel : -'), style="Muted.TLabel")
        self.lbl_current.grid(row=0, column=0, sticky="w")

        ttk.Label(controls, text=tr('Nom cible'), style="Muted.TLabel").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.target_name_var = tk.StringVar(value="")
        self.ent_target = ttk.Entry(controls, textvariable=self.target_name_var)
        self.ent_target.grid(row=2, column=0, sticky="ew", pady=(2, 0))
        self.ent_target.bind("<KeyRelease>", lambda _e: self._on_target_edited())

        btns = ttk.Frame(controls, style="Panel.TFrame")
        btns.grid(row=3, column=0, sticky="w", pady=(10, 0))

        self._sub_button(btns, tr('Nom actuel'), self.inject_current_name, small=True).pack(side="left", padx=(0, 8))
        self._sub_button(btns, tr('↺ Nomenclature'), self.reset_nomenclature, small=True).pack(side="left", padx=(0, 8))
        self._sub_button(btns, tr('📂 Ouvrir fichier'), self.open_current, small=True).pack(side="left", padx=(0, 8))
        self._sub_button(btns, tr('📁 Dossier'), self.reveal_current, small=True).pack(side="left", padx=(0, 8))
        self._sub_button(btns, tr('← Précédent'), self.prev_image, small=True).pack(side="left", padx=(0, 8))
        self._sub_button(btns, tr('Suivant →'), self.next_image, small=True).pack(side="left", padx=(0, 8))
        self._sub_button(btns, "i", self.open_metadata_dialog, small=True).pack(side="left")

        # Right column = documentation logic only
        self.right = ttk.Frame(main, style="Panel.TFrame")
        self.right.grid(row=0, column=1, sticky="nsew")
        self.right.bind("<Button-1>", self._clear_text_focus)
        self.right.grid_columnconfigure(0, weight=1)
        self.right.grid_rowconfigure(1, weight=1)
        self.right.grid_rowconfigure(2, weight=0)

        insp_box = tk.Frame(
            self.right,
            bg=UI.PANEL,
            highlightbackground=UI.BORDER,
            highlightthickness=1,
            bd=0,
        )
        insp_box.grid(row=0, column=0, sticky="ew", padx=6, pady=(6, 0))
        insp_box.grid_columnconfigure(0, weight=1)
        insp_box.grid_columnconfigure(1, weight=0)

        # Ligne haute : types à gauche, architecture à droite
        top_line = ttk.Frame(insp_box, style="Panel.TFrame")
        top_line.grid(row=0, column=0, columnspan=2, sticky="ew", padx=(35, 12), pady=(6, 2))
        top_line.grid_columnconfigure(0, weight=1)
        top_line.grid_columnconfigure(1, weight=0)

        type_grid = ttk.Frame(top_line, style="Panel.TFrame")
        type_grid.grid(row=0, column=0, sticky="w")

        ttk.Label(type_grid, text="Type", style="Small.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 14))

        type_labels = {
            "PHOTO": "PHOTO",
            "Dessin": "Dessin",
            "Master": tr('★ Master'),
        }

        for col, key in enumerate(INSPIRATION_TYPES, start=1):
            cb = ttk.Checkbutton(
                type_grid,
                text=tr(type_labels[key]),
                variable=self.insp_type_vars[key],
                style="Tag.TCheckbutton"
            )
            cb.grid(row=0, column=col, sticky="w", padx=(0, 18))
            cb.bind("<Button-1>", self._clear_text_focus, add="+")

        arch_box = ttk.Frame(top_line, style="Panel.TFrame")
        arch_box.grid(row=1, column=0, columnspan=2, sticky="e", pady=(6,0))

        self._sub_button(
            arch_box,
            tr('Charger architecture'),
            self._import_structure_architecture,
            small=True
        ).pack(side="left", padx=(0, 8))

        self._sub_button(
            arch_box,
            tr('Sauver architecture'),
            self._export_structure_architecture,
            small=True
        ).pack(side="left", padx=(0, 8))

        self._sub_button(
            arch_box,
            tr('Reset'),
            self._reset_structure_architecture,
            small=True
        ).pack(side="left")

        self.workspace.classification_button = ttk.Button(
            top_line, text=tr('Classement…'), command=self.workspace.choose_classification,
            style='Side.TButton')
        self.workspace.classification_button.grid(row=0, column=1, sticky='e', padx=(8,0))

        # Grille principale de coches
        checks_grid = ttk.Frame(insp_box, style="Panel.TFrame")
        checks_grid.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(35, 12), pady=(0, 4))
        for col in range(5):
            checks_grid.grid_columnconfigure(col, weight=1)

        ordered_checks = [
            "Composition", "Forme", "Silhouette", "Marche", "Couleur",
            "Lumiere", "Valeurs", "Course", "Echelle", "Combat",
        ]

        for i, key in enumerate(ordered_checks):
            row = i // 5
            col = i % 5

            cb = ttk.Checkbutton(
                checks_grid,
                text=tr(key),
                variable=self.insp_vars[key],
                style="Tag.TCheckbutton"
            )
            cb.grid(row=row, column=col, sticky="w", padx=(0, 35), pady=1)
            cb.bind("<Button-1>", self._clear_text_focus, add="+")

        levels_wrap = ttk.Frame(self.right, style="Panel.TFrame")
        levels_wrap.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 6))
        levels_wrap.columnconfigure(0, weight=1, uniform="lv")
        levels_wrap.columnconfigure(1, weight=1, uniform="lv")
        levels_wrap.columnconfigure(2, weight=1, uniform="lv")
        levels_wrap.rowconfigure(0, weight=1)
        levels_wrap.rowconfigure(1, weight=0)

        

        box1 = ttk.Frame(levels_wrap, style="Panel.TFrame")
        box1.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        title_row1 = ttk.Frame(box1, style="Panel.TFrame")
        title_row1.pack(fill="x", pady=(0, 8))

        tk.Label(
            title_row1,
            text=tr('Niveau 1'),
            bg=UI.PANEL,
            fg="#7F2D30",
            font=("Segoe UI", 10, "bold"),
            padx=8,
            pady=2,
        ).pack(side="left")

        tk.Button(
            title_row1,
            text="☰",
            command=self.open_lvl1_popup,
            bg=UI.PANEL,
            fg="#7F2D30",
            bd=0,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2"
        ).pack(side="right", padx=6)

        body1 = ttk.Frame(box1, style="Panel.TFrame")
        body1.pack(fill="both", expand=True, padx=10, pady=(0,6))
        self.lvl1_list = tk.Listbox(
            body1,
            height=8,
            exportselection=False,
            selectbackground="#ffc3a1",
            selectforeground="#000000",
            activestyle="none"
        )
        scroll1 = ttk.Scrollbar(body1, orient='vertical', command=self.lvl1_list.yview)
        scroll1.pack(side='right', fill='y')
        self.lvl1_list.configure(yscrollcommand=scroll1.set)
        self.lvl1_list.pack(side='left', fill='both', expand=True)
        self.lvl1_list.bind("<<ListboxSelect>>", lambda e: self.on_select_lvl1())
        self.lvl1_list.bind("<Button-1>", self._clear_text_focus, add="+")
        self.lvl1_list.bind("<Button-3>", self._on_lvl1_right_click)

        box2 = ttk.Frame(levels_wrap, style="Panel.TFrame")
        box2.grid(row=0, column=1, sticky="nsew", padx=(0, 8))

        title_row2 = ttk.Frame(box2, style="Panel.TFrame")
        title_row2.pack(fill="x", pady=(0, 8))

        tk.Label(
            title_row2,
            text=tr('Niveau 2'),
            bg=UI.PANEL,
            fg="#7F2D30",
            font=("Segoe UI", 10, "bold"),
            padx=8,
            pady=2,
        ).pack(side="left")

        tk.Button(
            title_row2,
            text="☰",
            command=self.open_lvl2_popup,
            bg=UI.PANEL,
            fg="#7F2D30",
            bd=0,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2"
        ).pack(side="right", padx=6)


        body2 = ttk.Frame(box2, style="Panel.TFrame")
        body2.pack(fill="both", expand=True, padx=10, pady=(0,6))
        self.lvl2_list = tk.Listbox(
            body2,
            height=8,
            exportselection=False,
            selectbackground="#ffc3a1",
            selectforeground="#000000"
        )
        scroll2 = ttk.Scrollbar(body2, orient='vertical', command=self.lvl2_list.yview)
        scroll2.pack(side='right', fill='y')
        self.lvl2_list.configure(yscrollcommand=scroll2.set)
        self.lvl2_list.pack(side='left', fill='both', expand=True)
        self.lvl2_list.bind("<<ListboxSelect>>", lambda e: self.on_select_lvl2())
        self.lvl2_list.bind("<Button-1>", self._clear_text_focus, add="+")
        self.lvl2_list.bind("<Button-3>", self._on_lvl2_right_click)
        
        box3 = ttk.Frame(levels_wrap, style="Panel.TFrame")
        box3.grid(row=0, column=2, sticky="nsew")

        title_row = ttk.Frame(box3, style="Panel.TFrame")
        title_row.pack(fill="x", pady=(0, 8))

        tk.Label(
            title_row,
            text=tr('Niveau 3'),
            bg=UI.PANEL,
            fg="#7F2D30",
            font=("Segoe UI", 10, "bold"),
            padx=8,
            pady=2,
        ).pack(side="left")

        btn_all = tk.Button(
            title_row,
            text="☰",
            command=self.open_lvl3_popup,
            bg=UI.PANEL,
            fg="#7F2D30",
            bd=0,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2"
        )
        btn_all.pack(side="right", padx=6)

        body3 = ttk.Frame(box3, style="Panel.TFrame")
        body3.pack(fill='both', expand=True, padx=10, pady=(0,6))
        self.n3_canvas = tk.Canvas(
           body3,
            bg=UI.PANEL,
            highlightthickness=1,
            highlightbackground=UI.BORDER,
            height=160
        )
        scroll3 = ttk.Scrollbar(body3, orient='vertical', command=self.n3_canvas.yview)
        scroll3.pack(side='right', fill='y')
        self.n3_canvas.configure(yscrollcommand=scroll3.set)
        self.n3_canvas.pack(side='left', fill='both', expand=True)
        self.n3_canvas.bind("<Button-1>", self._clear_text_focus)
        
        self.n3_frame = ttk.Frame(self.n3_canvas, style="Panel.TFrame")
        self.n3_window = self.n3_canvas.create_window((0, 0), window=self.n3_frame, anchor="nw")

        self.n3_frame.bind(
            "<Configure>",
            lambda e: self.n3_canvas.configure(scrollregion=self.n3_canvas.bbox("all"))
        )
        self.n3_canvas.bind(
            "<Configure>",
            lambda e: self.n3_canvas.itemconfig(self.n3_window, width=e.width)
        )

        search_row = ttk.Frame(levels_wrap, style="Panel.TFrame")
        search_row.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(4, 0))
        search_row.grid_columnconfigure(1, weight=1)

        ttk.Label(search_row, text=tr('Recherche niveaux'), style="Small.TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )

        self.level_search_entry = ttk.Entry(search_row, textvariable=self.level_search_var)
        self.level_search_entry.grid(row=0, column=1, sticky="ew")
        self.level_search_entry.bind("<Return>", self._confirm_level_search)
        self.level_search_entry.bind("<Down>", self._next_level_suggestion)
        self.level_search_entry.bind("<Up>", lambda e: self._next_level_suggestion(e, -1))

        self._clear_btn(search_row, self.level_search_entry).grid(
            row=0, column=2, sticky="w", padx=8
        )

        ttk.Label(
            search_row,
            textvariable=self.level_search_hint_var,
            style="Muted.TLabel"
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(4, 0))



        bottom = ttk.Frame(self.right, style="Panel.TFrame")
        bottom.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 14))
        bottom.grid_columnconfigure(0, weight=1)
        bottom.grid_columnconfigure(1, weight=1)

        manage = ttk.Frame(bottom, style="Panel.TFrame")
        manage.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        BTN_W = 3

        def mk_row(parent, label, add_cmd, del_cmd):
            row = ttk.Frame(parent, style="Panel.TFrame")
            row.pack(fill="x", padx=10, pady=6)

            ttk.Label(row, text=label, style="Small.TLabel", width=4).pack(side="left")

            ent = ttk.Entry(row)
            ent.pack(side="left", fill="x", expand=True, padx=(8, 8))

            btn_add = self._sub_button(row, "+", lambda: add_cmd(ent.get()), small=True)
            btn_add.configure(width=BTN_W)
            btn_add.pack(side="left", padx=(0, 6))

            btn_del = self._sub_button(row, "-", del_cmd, small=True)
            btn_del.configure(width=BTN_W)
            btn_del.pack(side="left")

            return ent

        self.ent_n1 = mk_row(manage, tr('N1'), self._add_n1, self._del_n1)
        self.ent_n2 = mk_row(manage, tr('N2'), self._add_n2, self._del_n2)
        self.ent_n3 = mk_row(manage, tr('N3'), self._add_n3, self._del_n3)

        settings_box = ttk.Frame(bottom, style="Panel.TFrame")
        settings_box.grid(row=0, column=1, sticky="nsew")
        settings_box.grid_columnconfigure(0, weight=0)
        settings_box.grid_columnconfigure(1, weight=1)
        settings_box.grid_columnconfigure(2, weight=0)

        ttk.Label(settings_box, text=tr('Compteur'), style="Small.TLabel").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 6))
        self.start_var = tk.StringVar(value="1")
        self.start_entry = ttk.Entry(settings_box, textvariable=self.start_var, width=12)
        self.start_entry.grid(row=0, column=1, sticky="ew", padx=(0, 0), pady=(10, 6))
        self._clear_btn(settings_box, self.start_entry).grid(row=0, column=2, sticky="w", padx=8, pady=(10, 6))
        bind_digits_only(self.start_entry, self.root)
        self.start_entry.bind("<Return>", lambda e: self.apply_start_number())
        self.start_entry.bind("<FocusOut>", lambda e: self.apply_start_number(silent=True))

        ttk.Label(settings_box, text=tr('Précision'), style="Small.TLabel").grid(row=1, column=0, sticky="w", padx=10, pady=(2, 6))
        self.precision_var = tk.StringVar(value="")
        self.precision_entry = ttk.Entry(settings_box, textvariable=self.precision_var)
        self.precision_entry.grid(row=1, column=1, sticky="ew", padx=(0, 0), pady=(2, 6))
        self._clear_btn(settings_box, self.precision_entry).grid(row=1, column=2, sticky="w", padx=8, pady=(2, 6))

        sort_wrap = ttk.Frame(settings_box, style="Panel.TFrame")
        sort_wrap.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 10))
        sort_wrap.grid_columnconfigure(0, weight=1)

        ttk.Button(
            sort_wrap,
            text=tr('RENOMMER (Entrée)'),
            style="Red.Accent.TButton",
            command=self.rename_and_next,
            width=24
        ).grid(row=0, column=0)

        self.precision_var.trace_add("write", lambda *_: self._on_field_changed())
        self.start_var.trace_add("write", lambda *_: self._update_target_label())
        self.level_search_var.trace_add("write", self._on_level_search_changed)

        for v in self.insp_vars.values():
            v.trace_add("write", lambda *_: self._on_field_changed())
        for v in self.insp_type_vars.values():
            v.trace_add("write", lambda *_: self._on_field_changed())

        self._refresh_lvl1_list()

    
    def _focus_is_text_input(self) -> bool:
        w = self.root.focus_get()
        if w is None:
            return False

        if isinstance(w, (tk.Entry, ttk.Entry, tk.Text)):
            return True

        try:
            widget_class = w.winfo_class()
        except Exception:
            return False

        return widget_class in ("Entry", "TEntry", "Text", "Spinbox", "TCombobox")

    def _clear_text_focus(self, _event=None):
        self.root.focus_set()

    def _return_to_nomenclature(self):
        if self.manual_mode:
            self.manual_mode = False
        self._update_target_label()
        self._save_settings()
    # ---------- binds ----------
    def _bind_keys(self):

        # Navigation
        self._bind_scoped("<Left>", self._on_global_left)
        self._bind_scoped("<Right>", self._on_global_right)
        # Renommer
        self._bind_scoped("<Return>", lambda _e: (self.rename_and_next(), "break")[1])
        self._bind_scoped("<KP_Enter>", lambda _e: (self.rename_and_next(), "break")[1])

        # Ouvrir dossier
        self._bind_scoped("<Control-o>", lambda _e: (self.open_folder(), "break")[1])
        self._bind_scoped("<Control-O>", lambda _e: (self.open_folder(), "break")[1])

        # Ouvrir fichier courant
        self._bind_scoped("<Control-Shift-o>", lambda _e: (self.open_current(), "break")[1])
        self._bind_scoped("<Control-Shift-O>", lambda _e: (self.open_current(), "break")[1])

        # Ouvrir dossier du fichier
        self._bind_scoped("<Control-Shift-f>", lambda _e: (self.reveal_current(), "break")[1])
        self._bind_scoped("<Control-Shift-F>", lambda _e: (self.reveal_current(), "break")[1])

        # Injecter nom actuel
        self._bind_scoped("<Control-i>", lambda _e: (self.inject_current_name(), "break")[1])
        self._bind_scoped("<Control-I>", lambda _e: (self.inject_current_name(), "break")[1])

        # Recalculer nomenclature
        self._bind_scoped("<Control-r>", lambda _e: (self.reset_nomenclature(), "break")[1])
        self._bind_scoped("<Control-R>", lambda _e: (self.reset_nomenclature(), "break")[1])
    
    def _on_global_left(self, _event=None):
        if self._focus_is_text_input():
            return
        self.prev_image()
        return "break"

    def _on_global_right(self, _event=None):
        if self._focus_is_text_input():
            return
        self.next_image()
        return "break"    
    # ---------- helper updates ----------
    def _refresh_top_count(self):
        if not hasattr(self, "top_count_lbl"):
            return

        total = len(self.files)

        if total == 0:
            self.top_count_lbl.configure(text="0 / 0")
            return

        current = self.idx + 1
        self.top_count_lbl.configure(text=f"{current} / {total}")

    def _refresh_status_texts(self):
        it = self._current_item()
        if not it:
            self.lbl_current.configure(text=tr('Nom actuel : -'))
            return
        self.lbl_current.configure(text=trf('Nom actuel : {0}', os.path.basename(it.path)))

    def _on_field_changed(self):
        self.apply_start_number(silent=True)
        if not self.manual_mode:
            self._update_target_label()
        self._save_settings()

    # ---------- list refresh ----------
    def _refresh_lvl1_list(self):
        self.lvl1_list.delete(0, tk.END)
        for k in sorted(self.structure.keys(), key=lambda s: s.lower()):
            self.lvl1_list.insert(tk.END, k)

    # ---------- add/del N1/N2/N3 ----------
    def _add_n1(self, raw: str):
        name = sanitize_token_compact(raw)
        if not name:
            return
        if name in self.structure:
            return
        self.structure[name] = {}
        self._save_structure_user()
        self._refresh_lvl1_list()

    def _del_n1(self):
        if not self.selected_lvl1:
            messagebox.showinfo(tr('Supprimer N1'), tr('Sélectionne un Niveau 1 à supprimer.'))
            return
        n1 = self.selected_lvl1
        if not messagebox.askyesno(tr('Supprimer'), trf('Supprimer N1 : {0} ?', n1)):
            return
        try:
            del self.structure[n1]
        except Exception:
            pass
        self.selected_lvl1 = None
        self.selected_lvl2 = None
        self.lvl2_list.delete(0, tk.END)
        self._reset_lvl3()
        self._save_structure_user()
        self._refresh_lvl1_list()
        self._update_target_label()

    def _add_n2(self, raw: str):
        if not self.selected_lvl1:
            messagebox.showinfo(tr('N2'), tr('Sélectionne d’abord un Niveau 1.'))
            return
        name = sanitize_token_compact(raw)
        if not name:
            return
        d2 = self.structure.setdefault(self.selected_lvl1, {})
        if name in d2:
            return
        d2[name] = []
        self._save_structure_user()
        self.on_select_lvl1(force_refresh=True)

    def _del_n2(self):
        if not (self.selected_lvl1 and self.selected_lvl2):
            messagebox.showinfo(tr('Supprimer N2'), tr('Sélectionne un Niveau 2 à supprimer.'))
            return
        n1, n2 = self.selected_lvl1, self.selected_lvl2
        if not messagebox.askyesno(tr('Supprimer'), trf('Supprimer N2 : {0} ?', n2)):
            return
        try:
            del self.structure[n1][n2]
        except Exception:
            pass
        self.selected_lvl2 = None
        self.lvl2_list.selection_clear(0, tk.END)
        self._reset_lvl3()
        self._save_structure_user()
        self.on_select_lvl1(force_refresh=True)

    def _add_n3(self, raw: str):
        if not (self.selected_lvl1 and self.selected_lvl2):
            messagebox.showinfo(tr('N3'), tr('Sélectionne d’abord un Niveau 1 puis un Niveau 2.'))
            return
        name = sanitize_token_compact(raw)
        if not name:
            return
        lst = self.structure[self.selected_lvl1].setdefault(self.selected_lvl2, [])
        if name in lst:
            return
        lst.append(name)
        self._save_structure_user()
        self.on_select_lvl2(force_refresh=True)

    def _del_n3(self):
        if not (self.selected_lvl1 and self.selected_lvl2):
            messagebox.showinfo(tr('Supprimer N3'), tr('Sélectionne un Niveau 1 puis un Niveau 2.'))
            return
        checked = [k for k, v in self.lvl3_vars.items() if v.get() == 1]
        if not checked:
            messagebox.showinfo(tr('Supprimer N3'), tr('Coche au moins un élément de Niveau 3 à supprimer.'))
            return
        if not messagebox.askyesno(tr('Supprimer'), trf('Supprimer {0} élément(s) N3 cochés ?', len(checked))):
            return
        lst = self.structure[self.selected_lvl1].get(self.selected_lvl2, [])
        self.structure[self.selected_lvl1][self.selected_lvl2] = [x for x in lst if x not in checked]
        self._save_structure_user()
        self.on_select_lvl2(force_refresh=True)

    def _save_structure_user(self):
        self.workspace.save_classification()
    def _refresh_structure_views(self):
        self._refresh_lvl1_list()

        self.selected_lvl1 = None
        self.selected_lvl2 = None

        self.lvl1_list.selection_clear(0, tk.END)
        self.lvl2_list.delete(0, tk.END)
        self._reset_lvl3()

        self._update_target_label()
        self._save_settings()

    def _export_structure_architecture(self):
        initial_name = "Documentation_Architecture.docarch.json"

        path = filedialog.asksaveasfilename(
            title=tr('Enregistrer l’architecture des niveaux'),
            defaultextension=STRUCTURE_BACKUP_EXT,
            initialfile=initial_name,
            filetypes=[
                (tr('Architecture Documentation'), f"*{STRUCTURE_BACKUP_EXT}"),
                (tr('Fichier JSON'), "*.json"),
            ],
        )
        if not path:
            return

        payload = {
            "format": "EigrutelDocumentationArchitecture",
            "version": 1,
            "naming_language": self.naming_language,
            "structure": self.structure,
        }

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            messagebox.showinfo(
                tr('Architecture'),
                tr('Architecture enregistrée avec succès.')
            )
        except Exception as e:
            messagebox.showerror(
                tr('Architecture'),
                trf('Impossible d’enregistrer l’architecture.\n\n{0}', e)
            )

    def _import_structure_architecture(self):
        path = filedialog.askopenfilename(
            title=tr('Charger une architecture des niveaux'),
            filetypes=[
                (tr('Architecture Documentation'), f"*{STRUCTURE_BACKUP_EXT}"),
                (tr('Fichier JSON'), "*.json"),
                (tr('Tous les fichiers'), "*.*"),
            ],
        )
        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict) and "structure" in data:
                imported = data.get("structure")
            else:
                imported = data

            if not isinstance(imported, dict):
                raise ValueError(tr('Le fichier ne contient pas une structure valide.'))

            cleaned = {}
            for n1, d2 in imported.items():
                if not isinstance(n1, str) or not isinstance(d2, dict):
                    continue
                cleaned[n1] = {}
                for n2, lst3 in d2.items():
                    if not isinstance(n2, str) or not isinstance(lst3, list):
                        continue
                    cleaned[n1][n2] = [x for x in lst3 if isinstance(x, str)]

            if not cleaned:
                raise ValueError(tr('Aucune donnée exploitable trouvée.'))

            if not messagebox.askyesno(
                tr('Charger architecture'),
                tr('Charger cette architecture et remplacer l’architecture actuelle ?')
            ):
                return

            self.structure = cleaned
            if isinstance(data, dict) and data.get("naming_language") in ("fr", "en"):
                self.naming_language = data["naming_language"]
                self.workspace.update_classification_filters()
            self._save_structure_user()
            self._refresh_structure_views()

            messagebox.showinfo(
                tr('Architecture'),
                tr('Architecture chargée avec succès.')
            )

        except Exception as e:
            messagebox.showerror(
                tr('Architecture'),
                trf('Impossible de charger cette architecture.\n\n{0}', e)
            )

    def _reset_structure_architecture(self):
        if not messagebox.askyesno(
            tr('Réinitialiser architecture'),
            tr('Revenir à l’architecture d’origine du programme ?\n\nLes ajouts et modifications actuels seront perdus.')
        ):
            return

        self.structure = json.loads(json.dumps(STRUCTURE_EN if self.naming_language == "en" else STRUCTURE_BASE, ensure_ascii=False))
        self._save_structure_user()
        self._refresh_structure_views()
        messagebox.showinfo(tr('Architecture'), tr('Architecture réinitialisée.'))

    def _show_context_menu(self, event, commands: list[tuple[str, callable]]):
        menu = tk.Menu(self.root, tearoff=0)

        for label, cmd in commands:
            menu.add_command(label=label, command=cmd)

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()


    def _on_lvl1_right_click(self, event):
        idx = self.lvl1_list.nearest(event.y)
        if idx < 0:
            return "break"

        self.lvl1_list.selection_clear(0, tk.END)
        self.lvl1_list.selection_set(idx)
        self.lvl1_list.activate(idx)
        self.lvl1_list.see(idx)

        self.selected_lvl1 = self.lvl1_list.get(idx)
        self.on_select_lvl1(force_refresh=True)

        self._show_context_menu(
            event,
            [
                (tr('Supprimer'), self._del_n1),
            ]
        )
        return "break"


    def _on_lvl2_right_click(self, event):
        idx = self.lvl2_list.nearest(event.y)
        if idx < 0:
            return "break"

        self.lvl2_list.selection_clear(0, tk.END)
        self.lvl2_list.selection_set(idx)
        self.lvl2_list.activate(idx)
        self.lvl2_list.see(idx)

        self.selected_lvl2 = self.lvl2_list.get(idx)
        self.on_select_lvl2(force_refresh=True)

        self._show_context_menu(
            event,
            [
                (tr('Supprimer'), self._del_n2),
            ]
        )
        return "break"


    def _on_lvl3_right_click(self, event, label: str):
        if not (self.selected_lvl1 and self.selected_lvl2):
            return "break"

        def _delete_this_lvl3():
            for k, v in self.lvl3_vars.items():
                v.set(1 if k == label else 0)
            self._del_n3()

        self._show_context_menu(
            event,
            [
                (tr('Supprimer'), _delete_this_lvl3),
            ]
        )
        return "break"
    
    def _normalize_search_text(self, s: str) -> str:
        s = _strip_accents((s or "").strip().lower())
        s = s.replace("_", " ")
        s = re.sub(r"\s+", " ", s)
        return s

    def _build_level_search_index(self) -> list[dict]:
        out = []

        for n1, d2 in self.structure.items():
            out.append({
                "level": 1,
                "label": n1,
                "n1": n1,
                "n2": None,
                "n3": None,
                "match": self._normalize_search_text(n1),
                "path": n1,
            })

            if not isinstance(d2, dict):
                continue

            for n2, lst3 in d2.items():
                out.append({
                    "level": 2,
                    "label": n2,
                    "n1": n1,
                    "n2": n2,
                    "n3": None,
                    "match": self._normalize_search_text(n2),
                    "path": f"{n1} > {n2}",
                })

                if not isinstance(lst3, list):
                    continue

                for n3 in lst3:
                    out.append({
                        "level": 3,
                        "label": n3,
                        "n1": n1,
                        "n2": n2,
                        "n3": n3,
                        "match": self._normalize_search_text(n3),
                        "path": f"{n1} > {n2} > {n3}",
                    })

        return out

    def _find_best_level_match(self, query: str):
        q = self._normalize_search_text(query)
        terms = q.split()
        if not terms:
            return None
        candidates = [item for item in self._build_level_search_index()
            if all(term in self._normalize_search_text(item['path']) for term in terms)]
        candidates.sort(key=lambda item: (item['match'] != q,
            not item['match'].startswith(q), len(item['path']), item['path']))
        self._level_matches = candidates
        self._level_match_index = 0
        return candidates[0] if candidates else None

    def _select_lvl1_value(self, value: str) -> bool:
        keys1 = [self.lvl1_list.get(i) for i in range(self.lvl1_list.size())]
        if value not in keys1:
            return False

        i = keys1.index(value)
        self.lvl1_list.selection_clear(0, tk.END)
        self.lvl1_list.selection_set(i)
        self.lvl1_list.activate(i)
        self.lvl1_list.see(i)
        self.selected_lvl1 = value
        self.on_select_lvl1(force_refresh=True)
        return True

    def _select_lvl2_value(self, value: str) -> bool:
        keys2 = [self.lvl2_list.get(i) for i in range(self.lvl2_list.size())]
        if value not in keys2:
            return False

        i = keys2.index(value)
        self.lvl2_list.selection_clear(0, tk.END)
        self.lvl2_list.selection_set(i)
        self.lvl2_list.activate(i)
        self.lvl2_list.see(i)
        self.selected_lvl2 = value
        self.on_select_lvl2(force_refresh=True)
        return True

    def _focus_lvl3_value(self, value: str):
        cb = self.lvl3_widgets.get(value)
        if not cb:
            return

        self.root.update_idletasks()

        try:
            y = cb.winfo_y()
            total_h = max(1, self.n3_frame.winfo_height())
            frac = max(0.0, min(1.0, y / total_h))
            self.n3_canvas.yview_moveto(frac)
        except Exception:
            pass

    def _apply_level_search_match(self, match: dict):
        lvl = match.get("level")
        n1 = match.get("n1")
        n2 = match.get("n2")
        n3 = match.get("n3")

        if not n1:
            return

        ok1 = self._select_lvl1_value(n1)
        if not ok1:
            return

        if lvl >= 2 and n2:
            ok2 = self._select_lvl2_value(n2)
            if not ok2:
                return

        if lvl == 3 and n3:
            self._focus_lvl3_value(n3)

    def _confirm_level_search(self, event=None):
        matches = getattr(self, '_level_matches', [])
        if self.level_search_var.get().strip() and matches:
            self._apply_level_search_match(matches[self._level_match_index])
        return "break"

    def _next_level_suggestion(self, event=None, direction=1):
        matches = getattr(self, '_level_matches', [])
        if matches:
            self._level_match_index = (self._level_match_index + direction) % len(matches)
            item = matches[self._level_match_index]
            self.level_search_hint_var.set(trf('{0}/{1} / {2} / Entrée pour choisir', self._level_match_index + 1, len(matches), item['path']))
        return "break"

    def _on_level_search_changed(self, *_):
        raw = self.level_search_var.get()

        if not raw.strip():
            self._level_matches = []
            self.level_search_hint_var.set("")
            return

        match = self._find_best_level_match(raw)
        if not match:
            self.level_search_hint_var.set(tr('Aucun résultat'))
            self.level_search_entry.focus_set()
            return

        self.level_search_hint_var.set(trf('{0} résultat(s) / {1} / Entrée pour choisir, ↓ suivant', len(self._level_matches), match['path']))
        # Applying is explicit: typing must not clear the user’s selected tags.
        self.level_search_entry.focus_set()

    # ---------- level select ----------
   
    def on_select_lvl1(self, force_refresh: bool = False):
        sel = self.lvl1_list.curselection()
        if not sel and not force_refresh:
            return
        if sel:
            self.selected_lvl1 = self.lvl1_list.get(sel[0])
        if not self.selected_lvl1:
            return

        self.selected_lvl2 = None
        self.lvl2_list.delete(0, tk.END)
        self._reset_lvl3()

        for k in sorted(self.structure.get(self.selected_lvl1, {}).keys(), key=lambda s: s.lower()):
            self.lvl2_list.insert(tk.END, k)

        self._return_to_nomenclature()

    def on_select_lvl2(self, force_refresh: bool = False):
        if not self.selected_lvl1:
            return
        sel = self.lvl2_list.curselection()
        if not sel and not force_refresh:
            return
        if sel:
            self.selected_lvl2 = self.lvl2_list.get(sel[0])
        if not self.selected_lvl2:
            return

        self._populate_lvl3()
        self._return_to_nomenclature()

    def _reset_lvl3(self):
        for w in self.n3_frame.winfo_children():
            w.destroy()
        self.lvl3_vars = {}
        self.lvl3_widgets = {}
        self._update_target_label()

    def _populate_lvl3(self):
        self._reset_lvl3()

        lst = self.structure.get(self.selected_lvl1 or "", {}).get(self.selected_lvl2 or "", [])
        if not lst:
            ttk.Label(self.n3_frame, text=tr('(Aucun niveau 3)'), style="Muted.TLabel").pack(anchor="w", padx=8, pady=8)
            return

        for label in lst:
            v = tk.IntVar(value=0)
            self.lvl3_vars[label] = v

            cb = ttk.Checkbutton(
                self.n3_frame,
                text=label,
                variable=v,
                style="Tag.TCheckbutton"
            )
            cb.pack(anchor="w", padx=8, pady=2)

            self.lvl3_widgets[label] = cb

            v.trace_add("write", lambda *_: self._return_to_nomenclature())
            cb.bind("<Button-1>", self._clear_text_focus, add="+")
            cb.bind("<Button-3>", lambda e, lab=label: self._on_lvl3_right_click(e, lab))

    def open_lvl1_popup(self):
        lst = sorted(self.structure.keys(), key=lambda s: s.lower())
        if not lst:
            return

        dlg = tk.Toplevel(self.root)
        dlg.title(tr('Niveau 1'))
        apply_window_icon(dlg)
        dlg.transient(self.root)
        dlg.grab_set()

        win_w = 460
        win_h = 520

        dlg.update_idletasks()
        screen_w = dlg.winfo_screenwidth()
        screen_h = dlg.winfo_screenheight()
        x = (screen_w // 2) - (win_w // 2)
        y = (screen_h // 2) - (win_h // 2)
        dlg.geometry(f"{win_w}x{win_h}+{x}+{y}")
        dlg.minsize(420, 420)

        outer = ttk.Frame(dlg, padding=12)
        outer.pack(fill="both", expand=True)

        listbox = tk.Listbox(
            outer,
            exportselection=False,
            selectbackground="#ffc3a1",
            selectforeground="#000000"
        )
        listbox.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y", padx=(8, 0))
        listbox.configure(yscrollcommand=scrollbar.set)

        for item in lst:
            listbox.insert(tk.END, item)

        if self.selected_lvl1 in lst:
            idx = lst.index(self.selected_lvl1)
            listbox.selection_set(idx)
            listbox.activate(idx)
            listbox.see(idx)

        def _apply_selection(_event=None):
            sel = listbox.curselection()
            if not sel:
                return
            chosen = listbox.get(sel[0])

            keys1 = [self.lvl1_list.get(i) for i in range(self.lvl1_list.size())]
            if chosen in keys1:
                i = keys1.index(chosen)
                self.lvl1_list.selection_clear(0, tk.END)
                self.lvl1_list.selection_set(i)
                self.lvl1_list.activate(i)
                self.lvl1_list.see(i)
                self.selected_lvl1 = chosen
                self.on_select_lvl1(force_refresh=True)

            _close_popup()

        listbox.bind("<Double-Button-1>", _apply_selection)
        listbox.bind("<Return>", _apply_selection)

        def _close_popup():
            dlg.destroy()

        btns = ttk.Frame(dlg, style="Panel.TFrame")
        btns.pack(fill="x", pady=(0, 12))

        self._sub_button(
            btns,
            tr('Fermer'),
            _close_popup,
            small=True
        ).pack(anchor="center")

    def open_lvl2_popup(self):
        if not self.selected_lvl1:
            return

        lst = sorted(self.structure.get(self.selected_lvl1, {}).keys(), key=lambda s: s.lower())
        if not lst:
            return

        dlg = tk.Toplevel(self.root)
        dlg.title(tr('Niveau 2'))
        apply_window_icon(dlg)
        dlg.transient(self.root)
        dlg.grab_set()

        win_w = 460
        win_h = 520

        dlg.update_idletasks()
        screen_w = dlg.winfo_screenwidth()
        screen_h = dlg.winfo_screenheight()
        x = (screen_w // 2) - (win_w // 2)
        y = (screen_h // 2) - (win_h // 2)
        dlg.geometry(f"{win_w}x{win_h}+{x}+{y}")
        dlg.minsize(420, 420)

        outer = ttk.Frame(dlg, padding=12)
        outer.pack(fill="both", expand=True)

        listbox = tk.Listbox(outer, exportselection=False)
        listbox.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y", padx=(8, 0))
        listbox.configure(yscrollcommand=scrollbar.set)

        for item in lst:
            listbox.insert(tk.END, item)

        if self.selected_lvl2 in lst:
            idx = lst.index(self.selected_lvl2)
            listbox.selection_set(idx)
            listbox.activate(idx)
            listbox.see(idx)

        def _apply_selection(_event=None):
            sel = listbox.curselection()
            if not sel:
                return
            chosen = listbox.get(sel[0])

            keys2 = [self.lvl2_list.get(i) for i in range(self.lvl2_list.size())]
            if chosen in keys2:
                i = keys2.index(chosen)
                self.lvl2_list.selection_clear(0, tk.END)
                self.lvl2_list.selection_set(i)
                self.lvl2_list.activate(i)
                self.lvl2_list.see(i)
                self.selected_lvl2 = chosen
                self.on_select_lvl2(force_refresh=True)

            _close_popup()

        listbox.bind("<Double-Button-1>", _apply_selection)
        listbox.bind("<Return>", _apply_selection)

        def _close_popup():
            dlg.destroy()

        btns = ttk.Frame(dlg, style="Panel.TFrame")
        btns.pack(fill="x", pady=(0, 12))

        self._sub_button(
            btns,
            tr('Fermer'),
            _close_popup,
            small=True
        ).pack(anchor="center")

    def open_lvl3_popup(self):
        if not (self.selected_lvl1 and self.selected_lvl2):
            return

        lst = self.structure.get(self.selected_lvl1, {}).get(self.selected_lvl2, [])
        if not lst:
            return

        dlg = tk.Toplevel(self.root)
        dlg.title(tr('Niveau 3'))
        apply_window_icon(dlg)
        dlg.transient(self.root)
        dlg.grab_set()

        # Taille plus large pour bien loger le contenu + la scrollbar
        win_w = 460
        win_h = 520

        # Centrage écran
        dlg.update_idletasks()
        screen_w = dlg.winfo_screenwidth()
        screen_h = dlg.winfo_screenheight()
        x = (screen_w // 2) - (win_w // 2)
        y = (screen_h // 2) - (win_h // 2)
        dlg.geometry(f"{win_w}x{win_h}+{x}+{y}")
        dlg.minsize(420, 420)

        outer = ttk.Frame(dlg, padding=12)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            outer,
            bg=UI.PANEL,
            highlightthickness=1,
            highlightbackground=UI.BORDER
        )
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y", padx=(8, 0))

        canvas.configure(yscrollcommand=scrollbar.set)

        frame = ttk.Frame(canvas, style="Panel.TFrame")
        window_id = canvas.create_window((0, 0), window=frame, anchor="nw")

        def update_scroll(_e=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def fit_width(e):
            canvas.itemconfigure(window_id, width=e.width)

        frame.bind("<Configure>", update_scroll)
        canvas.bind("<Configure>", fit_width)

        for label in lst:
            if label not in self.lvl3_vars:
                self.lvl3_vars[label] = tk.IntVar(value=0)

            ttk.Checkbutton(
                frame,
                text=label,
                variable=self.lvl3_vars[label],
                style="Tag.TCheckbutton"
            ).pack(anchor="w", padx=10, pady=5)

        # Molette souris
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        dlg.bind("<MouseWheel>", _on_mousewheel)

        def _close_popup():
            try:
                dlg.unbind("<MouseWheel>")
            except Exception:
                pass
            dlg.destroy()

        btns = ttk.Frame(dlg, style="Panel.TFrame")
        btns.pack(fill="x", pady=(0, 12))

        self._sub_button(
            btns,
            tr('Fermer'),
            _close_popup,
            small=True
        ).pack(anchor="center")

    def _reload_current_folder_after_sort(self, previous_folder: str, previous_file_path: str | None = None):
        """
        Recharge proprement le dossier qui était actif avant le tri,
        en conservant si possible la position sur le fichier courant.
        """
        if not previous_folder or not os.path.isdir(previous_folder):
            self.folder = ""
            self.files = []
            self.idx = 0
            self._load_current()
            return

        self.folder = previous_folder
        self._load_files()

        if not self.files:
            self.idx = 0
            self._load_current()
            return

        found_idx = None
        if previous_file_path:
            previous_abs = os.path.abspath(previous_file_path).lower()
            for i, it in enumerate(self.files):
                if os.path.abspath(it.path).lower() == previous_abs:
                    found_idx = i
                    break

        if found_idx is not None:
            self.idx = found_idx
        else:
            self.idx = min(self.idx, len(self.files) - 1)

        self._load_current()


    # ---------- folder/files ----------
    def _on_toggle_subdirs(self):
        if self.folder and os.path.isdir(self.folder):
            self._load_files()
            self.idx = 0
            self._load_current()
        self._save_settings()

    def open_folder(self):
        self.workspace.choose_folder()

    def _load_files(self):
        items: list[FileItem] = []
        if not self.folder or not os.path.isdir(self.folder):
            self.files = []
            self._refresh_top_count()
            return

        if self.include_subdirs.get():
            for rootdir, _dirs, files in os.walk(self.folder):
                for fn in files:
                    if fn.lower().endswith(IMG_EXTS):
                        p = os.path.join(rootdir, fn)
                        rel = os.path.relpath(p, self.folder)
                        items.append(FileItem(path=p, rel=rel))
        else:
            for fn in os.listdir(self.folder):
                p = os.path.join(self.folder, fn)
                if os.path.isfile(p) and fn.lower().endswith(IMG_EXTS):
                    rel = os.path.relpath(p, self.folder)
                    items.append(FileItem(path=p, rel=rel))

        items.sort(key=lambda it: [int(part) if part.isdigit() else part.casefold()
                                  for part in re.split(r"(\d+)", it.rel)])
        self.files = items
        self._refresh_top_count()



    # ---------- navigation ----------
    def prev_image(self):
        if not self.files:
            return
        self.idx = (self.idx - 1) % len(self.files)
        self._load_current()

    def next_image(self):
        if not self.files:
            return
        self.idx = (self.idx + 1) % len(self.files)
        self._load_current()

    def _current_item(self) -> FileItem | None:
        if not self.files:
            return None
        if self.idx < 0 or self.idx >= len(self.files):
            return None
        return self.files[self.idx]

    # ---------- naming / target ----------
    def naming_token(self, key):
        if self.naming_language != 'en':
            return key
        return {'Dessin':'DRAWING', 'Master':'Prime', 'Forme':'Form',
            'Couleur':'Color', 'Lumiere':'Light', 'Valeurs':'Values', 'Echelle':'Scale',
            'Marche':'Walk', 'Course':'Run', 'Saut':'Jump', 'Combat':'Fight'}.get(key, key)

    def _build_target_name_for_item(self, it: FileItem | None) -> str:
        if not it:
            return "-"
        ext = os.path.splitext(it.path)[1]

        parts = [APP_CODE]

        if self.selected_lvl1:
            parts.append(sanitize_token_compact(self.selected_lvl1))
        if self.selected_lvl2:
            parts.append(sanitize_token_compact(self.selected_lvl2))

        for label, var in self.lvl3_vars.items():
            if var.get() == 1:
                parts.append(sanitize_token_compact(label))

        insp_checked = [k for k, v in self.insp_vars.items() if v.get() == 1]
        type_checked = [k for k, v in self.insp_type_vars.items() if v.get() == 1]

        parts.extend([sanitize_token_compact(self.naming_token(k)) for k in type_checked])
        parts.extend([sanitize_token_compact(self.naming_token(k)) for k in insp_checked])

        prec = sanitize_token_compact(self.precision_var.get())
        if prec:
            parts.append(prec)

        base = "_".join([p for p in parts if p])
        raw_counter = (self.start_var.get() or "").strip() if hasattr(self, 'start_var') else ""
        if raw_counter:
            try:
                num = f"{int(raw_counter):03d}"
                return f"{base}_{num}{ext}"
            except Exception:
                pass
        return f"{base}{ext}"

    def _update_target_label(self):
        it = self._current_item()
        if not it:
            self.target_name_var.set("")
            return
        if not self.manual_mode:
            target = self._build_target_name_for_item(it)
            self.target_name_var.set(target)

    def _on_target_edited(self):
        self.manual_mode = True
        self._save_settings()

    def inject_current_name(self):
        it = self._current_item()
        if not it:
            return
        self.target_name_var.set(os.path.basename(it.path))
        self.manual_mode = True
        self._save_settings()

    def reset_nomenclature(self):
        self.manual_mode = False
        self._update_target_label()
        self._save_settings()

    # ---------- metadata ----------
    def _metadata_text(self, path: str) -> str:
        lines = []
        try:
            st = os.stat(path)
            lines.append(trf('Fichier : {0}', os.path.basename(path)))
            lines.append(trf('Chemin : {0}', path))
            lines.append(trf('Poids : {0} octets', st.st_size))
            lines.append(tr('Modifié : ') + __import__('datetime').datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S"))
        except Exception:
            lines.append(trf('Fichier : {0}', os.path.basename(path)))
            lines.append(trf('Chemin : {0}', path))
        if self._src_img is not None:
            try:
                w, h = self._src_img.size
                lines.append(trf('Dimensions : {0} × {1}', w, h))
            except Exception:
                pass
        lines.append(trf('Extension : {0}', os.path.splitext(path)[1].lower()))
        return "\n".join(lines)

    # ---------- display ----------
    def _load_current(self):
        self._refresh_top_count()

        it = self._current_item()
        if not it:
            self.lbl_current.configure(text=tr('Nom actuel : -'))
            self.target_name_var.set("")
            self.canvas.delete("all")
            self._src_img = None
            return

        self.lbl_current.configure(text=trf('Nom actuel : {0}', os.path.basename(it.path)))
        self._load_image(it.path)

        if self.manual_mode:
            self.target_name_var.set(os.path.basename(it.path))
        else:
            self._update_target_label()

        self._save_settings()

    def _load_image(self, path: str):
        try:
            with Image.open(path) as source:
                img = ImageOps.exif_transpose(source)
                img = img.convert("RGBA" if "A" in img.getbands() or "transparency" in img.info else "RGB")
                img.load()
            previous = self._src_img
            self._src_img = img
            if previous is not None:
                previous.close()
        except Exception as e:
            self._src_img = None
            messagebox.showerror("Image", trf('Impossible d’ouvrir:\n{0}\n\n{1}', os.path.basename(path), e))
            return
        self._redraw_canvas()

    def _redraw_canvas(self):
        self.canvas.delete("all")
        img = self._src_img
        if img is None:
            return
        cw = max(1, self.canvas.winfo_width())
        ch = max(1, self.canvas.winfo_height())

        iw, ih = img.size
        ratio = min(cw / iw, ch / ih)
        nw, nh = max(1, int(iw * ratio)), max(1, int(ih * ratio))

        try:
            disp = img.resize((nw, nh), Image.LANCZOS)
        except Exception:
            disp = img.resize((nw, nh))

        self.tk_img = ImageTk.PhotoImage(disp)
        self.canvas.create_image(cw // 2, ch // 2, image=self.tk_img, anchor="center")

    # ---------- counter ----------
    def apply_start_number(self, silent=False):
        raw = (self.start_var.get() or "").strip()
        if not raw:
            self._update_target_label()
            self._save_settings()
            return
        try:
            n = int(raw)
            if n < 0:
                raise ValueError()
        except ValueError:
            if not silent:
                messagebox.showerror(tr('Erreur'), tr('Compteur invalide'))
            return
        self.counter = n
        self._update_target_label()
        self._save_settings()

    # ---------- field reset ----------
    def reset_fields(self):
        self.precision_var.set("")
        self.counter = 1
        self.start_var.set("1")
        self.manual_mode = False
        self._update_target_label()
        self._save_settings()

    # ---------- actions ----------
    def open_current(self):
        it = self._current_item()
        if not it:
            return
        try:
            open_with_default_app(it.path)
        except Exception as e:
            messagebox.showerror(tr('Ouvrir fichier'), str(e))

    def reveal_current(self):
        it = self._current_item()
        if not it:
            return
        try:
            folder = os.path.dirname(it.path)
            os.startfile(folder)  # type: ignore[attr-defined]
        except Exception:
            try:
                subprocess.Popen(["explorer", os.path.dirname(it.path)])
            except Exception as e:
                messagebox.showerror(tr('Dossier'), str(e))

    # ---------- rename ----------
    def rename_and_next(self):
        if not self.workspace.can_modify():
            return
        it = self._current_item()
        if not it:
            return

        self.apply_start_number(silent=True)

        src_path = it.path
        target_name = sanitize_token_compact(os.path.splitext(self.target_name_var.get())[0]) if self.manual_mode else os.path.splitext(self._build_target_name_for_item(it))[0]
        ext = os.path.splitext(src_path)[1]
        if self.manual_mode:
            current_raw = (self.target_name_var.get() or "").strip()
            if current_raw.lower().endswith(ext.lower()):
                final_name = current_raw
            else:
                final_name = f"{sanitize_token_compact(current_raw) or APP_CODE}{ext}"
        else:
            final_name = self._build_target_name_for_item(it)

        if (not final_name or re.search(INVALID_WIN, final_name) or final_name.endswith((' ', '.'))
            or any(ord(c) < 32 for c in final_name)
            or final_name.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL',
                *[f'COM{i}' for i in range(1, 10)], *[f'LPT{i}' for i in range(1, 10)]}):
            messagebox.showerror(tr('Renommage'), tr('Nom de fichier incompatible avec Windows.'))
            return
        dst_path = os.path.join(os.path.dirname(src_path), final_name)
        if os.path.abspath(dst_path).lower() == os.path.abspath(src_path).lower():
            self.next_image()
            return
        if os.path.exists(dst_path):
            messagebox.showerror(tr('Collision'), trf('Le fichier existe déjà:\n{0}', final_name))
            return

        try:
            self.workspace.relocate(src_path, dst_path)
            try:
                log_rename(
                    tool="documentation",
                    session_id=self.session_id,
                    folder=os.path.dirname(src_path),
                    old_path=src_path,
                    new_path=dst_path,
                    old_name=os.path.basename(src_path),
                    new_name=os.path.basename(dst_path),
                    status="ok",
                    user_target_mode=("MANUEL" if self.manual_mode else "AUTO"),
                    conflict_resolution="none",
                )
            except Exception:
                pass
        except Exception as e:
            try:
                log_rename(
                    tool="documentation",
                    session_id=self.session_id,
                    folder=os.path.dirname(src_path),
                    old_path=src_path,
                    new_path=dst_path,
                    old_name=os.path.basename(src_path),
                    new_name=os.path.basename(dst_path),
                    status="failed",
                    error=str(e),
                )
            except Exception:
                pass
            messagebox.showerror(tr('Renommage'), trf('Impossible de renommer:\n{0}', e))
            return

        it.path = dst_path
        it.rel = os.path.relpath(dst_path, self.folder) if self.folder else os.path.basename(dst_path)

        raw_counter = (self.start_var.get() or "").strip()
        if raw_counter:
            try:
                self.counter = int(raw_counter) + 1
                self.start_var.set(str(self.counter))
            except Exception:
                pass

        self._save_settings()
        self.next_image()

    # =========================================================
    # RANGEMENT AUTOMATIQUE / NIVEAU 1
    # =========================================================

    def _iter_candidate_files_for_sort(self) -> list[str]:
        """
        Retourne les fichiers à analyser pour le rangement.
        On respecte le dossier choisi + l'option sous-dossiers.
        Ici on prend tous les fichiers, pas seulement les images,
        car le critère demandé est le préfixe DOCUMENTATION.
        """
        out = []
        if not self.folder or not os.path.isdir(self.folder):
            return out

        if self.include_subdirs.get():
            for rootdir, _dirs, files in os.walk(self.folder):
                for fn in files:
                    out.append(os.path.join(rootdir, fn))
        else:
            for fn in os.listdir(self.folder):
                p = os.path.join(self.folder, fn)
                if os.path.isfile(p):
                    out.append(p)

        return out

    def _build_lvl1_sanitized_map(self) -> dict[str, str]:
        """
        Map 'nom_sanitized' -> 'nom_original'
        Exemple:
            'Arts_et_sciences' -> 'Arts et sciences'
        """
        out = {}
        for n1 in self.structure.keys():
            out[sanitize_token_compact(n1)] = n1
        return out

    def _longest_match_in_keys(self, tokens: list[str], keys) -> tuple[str | None, int]:
        """
        Cherche le plus long match possible entre le début de 'tokens'
        et une liste / vue de clés.
        Retourne (nom_original, nb_tokens_consumed)
        """
        mapping = {sanitize_token_compact(k): k for k in keys}
        max_take = min(len(tokens), 8)

        for size in range(max_take, 0, -1):
            candidate = "_".join(tokens[:size])
            if candidate in mapping:
                return mapping[candidate], size

        return None, 0

    def _extract_lvl1_lvl2_lvl3_from_filename(self, filename: str) -> tuple[str | None, str | None, str | None]:
        """
        Extrait (niveau1, niveau2, niveau3) depuis un nom de fichier DOCUMENTATION_...

        Règle N3 :
        - si un seul N3 valide est trouvé, on le retourne
        - si plusieurs N3 valides sont trouvés, on retourne None pour N3
        - si aucun N3 valide n'est trouvé, on retourne None pour N3

        Le rangement se fera donc :
        - N1/N2/N3 si un seul N3 reconnu
        - sinon N1/N2
        """
        base = os.path.splitext(os.path.basename(filename))[0]

        if not base.startswith("DOCUMENTATION"):
            return None, None, None

        parts = base.split("_")
        if not parts or parts[0] != "DOCUMENTATION":
            return None, None, None

        remaining = parts[1:]
        if not remaining:
            return None, None, None

        # ---- Niveau 1
        lvl1, consumed1 = self._longest_match_in_keys(remaining, self.structure.keys())
        if not lvl1:
            return None, None, None

        rest_after_lvl1 = remaining[consumed1:]

        # ---- Niveau 2
        sub = self.structure.get(lvl1, {})
        if not isinstance(sub, dict) or not sub:
            return lvl1, None, None

        lvl2, consumed2 = self._longest_match_in_keys(rest_after_lvl1, sub.keys())
        if not lvl2:
            return lvl1, None, None

        rest_after_lvl2 = rest_after_lvl1[consumed2:]

        # ---- Niveau 3
        lvl3_list = self.structure.get(lvl1, {}).get(lvl2, [])
        if not isinstance(lvl3_list, list) or not lvl3_list:
            return lvl1, lvl2, None

        lvl3_map = {sanitize_token_compact(k): k for k in lvl3_list}
        found_lvl3 = []

        max_take = min(len(rest_after_lvl2), 8)
        for start in range(len(rest_after_lvl2)):
            for size in range(max_take, 0, -1):
                if start + size > len(rest_after_lvl2):
                    continue
                candidate = "_".join(rest_after_lvl2[start:start + size])
                if candidate in lvl3_map:
                    val = lvl3_map[candidate]
                    if val not in found_lvl3:
                        found_lvl3.append(val)
                    break

        if len(found_lvl3) == 1:
            return lvl1, lvl2, found_lvl3[0]

        return lvl1, lvl2, None

    def _ensure_documentation_root_and_lvl1_lvl2_lvl3_dirs(self, base_parent: str) -> str:
        """
        Crée si besoin :
            base_parent/Documentation/
            base_parent/Documentation/<N1>/
            base_parent/Documentation/<N1>/<N2>/
            base_parent/Documentation/<N1>/<N2>/<N3>/
        Retourne le chemin du dossier Documentation.
        """
        doc_root = os.path.join(base_parent, "Documentation")
        os.makedirs(doc_root, exist_ok=True)
        apply_windows_folder_icon(doc_root)

        for n1, sub in self.structure.items():
            n1_dir = os.path.join(doc_root, sanitize_token_compact(n1))
            os.makedirs(n1_dir, exist_ok=True)

            if isinstance(sub, dict):
                for n2, lst3 in sub.items():
                    n2_dir = os.path.join(n1_dir, sanitize_token_compact(n2))
                    os.makedirs(n2_dir, exist_ok=True)

                    if isinstance(lst3, list):
                        for n3 in lst3:
                            n3_dir = os.path.join(n2_dir, sanitize_token_compact(n3))
                            os.makedirs(n3_dir, exist_ok=True)

        return doc_root

    def _ensure_existing_lvl1_lvl2_lvl3_dirs(self, doc_root: str):
        """
        Si l'utilisateur a déjà ses dossiers, on complète discrètement
        les dossiers N1 / N2 / N3 manquants.
        """
        os.makedirs(doc_root, exist_ok=True)
        apply_windows_folder_icon(doc_root)

        for n1, sub in self.structure.items():
            n1_dir = os.path.join(doc_root, sanitize_token_compact(n1))
            os.makedirs(n1_dir, exist_ok=True)

            if isinstance(sub, dict):
                for n2, lst3 in sub.items():
                    n2_dir = os.path.join(n1_dir, sanitize_token_compact(n2))
                    os.makedirs(n2_dir, exist_ok=True)

                    if isinstance(lst3, list):
                        for n3 in lst3:
                            n3_dir = os.path.join(n2_dir, sanitize_token_compact(n3))
                            os.makedirs(n3_dir, exist_ok=True)

    def _unique_destination_path(self, dst_path: str) -> str:
        """
        Si collision, ajoute _001, _002, etc.
        """
        if not os.path.exists(dst_path):
            return dst_path

        folder = os.path.dirname(dst_path)
        stem, ext = os.path.splitext(os.path.basename(dst_path))

        i = 1
        while True:
            candidate = os.path.join(folder, f"{stem}_{i:03d}{ext}")
            if not os.path.exists(candidate):
                return candidate
            i += 1

    def auto_sort_documentation_lvl3(self):
        if not self.workspace.can_modify():
            return
        """
        Rangement automatique DOCUMENTATION :
        - traite uniquement les fichiers commençant par DOCUMENTATION
        - détecte N1 puis N2 puis N3
        - range dans Documentation/N1/N2/N3 si un seul N3 est reconnu
        - sinon dans Documentation/N1/N2
        - si N2 n'est pas reconnu, range dans Documentation/N1
        """
        if not self.folder or not os.path.isdir(self.folder):
            messagebox.showinfo(tr('Rangement DOCUMENTATION'), tr('Choisis d’abord un dossier source.'))
            return

        source_folder_before_sort = self.folder
        current_item = self._current_item()
        current_file_before_sort = current_item.path if current_item else None
        current_idx_before_sort = self.idx

        files = self._iter_candidate_files_for_sort()
        if not files:
            messagebox.showinfo(tr('Rangement DOCUMENTATION'), tr('Aucun fichier trouvé dans le dossier sélectionné.'))
            return

        doc_files = []
        for p in files:
            fn = os.path.basename(p)
            if fn.startswith("DOCUMENTATION"):
                doc_files.append(p)

        if not doc_files:
            messagebox.showinfo(
                tr('Rangement DOCUMENTATION'),
                tr('Aucun fichier commençant par DOCUMENTATION n’a été trouvé.')
            )
            return

        has_existing = messagebox.askyesno(
            tr('Rangement DOCUMENTATION'),
            tr('As-tu déjà tes dossiers Documentation ?\n\nOui = tu sélectionnes un dossier Documentation existant.\nNon = on crée automatiquement Documentation + les dossiers Niveau 1 / Niveau 2 / Niveau 3.')
        )

        if has_existing:
            doc_root = filedialog.askdirectory(
                title=tr('Choisir le dossier Documentation existant')
            )
            if not doc_root:
                return
            self._ensure_existing_lvl1_lvl2_lvl3_dirs(doc_root)
        else:
            parent_dest = filedialog.askdirectory(
                title=tr('Choisir le dossier dans lequel créer le dossier Documentation')
            )
            if not parent_dest:
                return
            doc_root = self._ensure_documentation_root_and_lvl1_lvl2_lvl3_dirs(parent_dest)

        moved = 0
        skipped = 0
        unknown = []

        for src_path in doc_files:
            fn = os.path.basename(src_path)
            lvl1, lvl2, lvl3 = self._extract_lvl1_lvl2_lvl3_from_filename(fn)

            if not lvl1:
                skipped += 1
                unknown.append(fn)
                continue

            if lvl2 and lvl3:
                dst_dir = os.path.join(
                    doc_root,
                    sanitize_token_compact(lvl1),
                    sanitize_token_compact(lvl2),
                    sanitize_token_compact(lvl3)
                )
            elif lvl2:
                dst_dir = os.path.join(
                    doc_root,
                    sanitize_token_compact(lvl1),
                    sanitize_token_compact(lvl2)
                )
            else:
                dst_dir = os.path.join(
                    doc_root,
                    sanitize_token_compact(lvl1)
                )

            os.makedirs(dst_dir, exist_ok=True)

            dst_path = os.path.join(dst_dir, fn)
            if os.path.normcase(os.path.abspath(src_path)) == os.path.normcase(os.path.abspath(dst_path)):
                skipped += 1
                continue
            dst_path = self._unique_destination_path(dst_path)

            try:
                if os.path.abspath(src_path).lower() == os.path.abspath(dst_path).lower():
                    skipped += 1
                    continue

                self.workspace.relocate(src_path, dst_path, destination_root=doc_root)
                moved += 1
            except Exception:
                skipped += 1
                unknown.append(fn)

        msg = (
            trf('Rangement terminé.\n\nDéplacés : {0}\nIgnorés / non traités : {1}', moved, skipped)
        )

        if unknown:
            preview = "\n".join(unknown[:15])
            if len(unknown) > 15:
                preview += "\n..."
            msg += trf('\n\nFichiers à vérifier :\n{0}', preview)

        messagebox.showinfo(tr('Rangement DOCUMENTATION'), msg)
        if moved:
            self.root.after_idle(lambda: self.workspace.set_folder(doc_root))

        self.idx = current_idx_before_sort
        self._reload_current_folder_after_sort(
            previous_folder=source_folder_before_sort,
            previous_file_path=current_file_before_sort
        )


