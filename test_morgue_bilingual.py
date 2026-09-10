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

"""Bilingual regression tests; uses Tcl only, no display or user data."""
import ast
import copy
import json
from pathlib import Path
import string
import tempfile
import tkinter as tk
import unittest
from unittest.mock import Mock, patch
from types import SimpleNamespace
import EigrutelMorgue as app
import morgue_i18n as i18n
import morgue_library as library
import morgue_renamer as renamer
from morgue_translations import EN
from morgue_structure_en import STRUCTURE_EN


class BilingualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        i18n.install()
        cls.tcl = tk.Tcl()

    def setUp(self):
        i18n.set_language('fr')

    def tearDown(self):
        i18n.set_language('fr')

    def test_reused_message_uses_current_language(self):
        label = i18n.tr('Couleur')
        i18n.set_language('en')
        value = tk.StringVar(self.tcl, value=i18n.tr(label))
        self.assertEqual(value.get(), 'Color')
        i18n.set_language('fr')
        self.assertEqual(value.get(), 'Couleur')

    def test_catalogue_preserves_format_fields(self):
        def fields(s):
            return sorted((key, spec, conv) for _, key, spec, conv in string.Formatter().parse(s) if key is not None)
        for source, target in EN.items():
            with self.subTest(source=source):
                self.assertEqual(fields(source), fields(target))

    def test_all_explicit_messages_have_translations(self):
        for path in Path(__file__).parent.glob('*.py'):
            if path.name.startswith('test_'):
                continue
            for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ('tr','trf') and node.args and isinstance(node.args[0], ast.Constant):
                    self.assertIn(node.args[0].value, EN, f'{path.name}:{node.lineno}')

    def test_dynamic_tcl_variable_is_reversible(self):
        value = tk.StringVar(self.tcl, value=i18n.trf('{0} résultats', 12))
        self.assertEqual(value.get(), '12 résultats')
        i18n.set_language('en')
        self.assertEqual(value.get(), '12 results')
        i18n.set_language('fr')
        self.assertEqual(value.get(), '12 résultats')

    def test_user_data_is_never_translated_even_if_in_catalogue(self):
        value = tk.StringVar(self.tcl, value='Couleur')
        i18n.set_language('en')
        self.assertEqual(value.get(), 'Couleur')
        value.set(i18n.tr('Couleur'))
        value.set('Forme')
        i18n.set_language('fr')
        self.assertEqual(value.get(), 'Forme')

    def test_nested_count_and_filename_remain_correct(self):
        value = tk.StringVar(self.tcl, value=i18n.trf('{0} • favoris', i18n.trf('{0} résultats', 8)))
        filename = tk.StringVar(self.tcl, value=i18n.tr('Modifié : ') + 'DOCUMENTATION_Couleur.png')
        i18n.set_language('en')
        self.assertEqual(value.get(), '8 results • favorites')
        self.assertTrue(filename.get().endswith('DOCUMENTATION_Couleur.png'))
        self.assertTrue(filename.get().startswith('Modified'))

    def test_ui_switch_does_not_change_generated_names(self):
        view = renamer.DocumentationRenamer.__new__(renamer.DocumentationRenamer)
        view.naming_language = 'fr'
        view.selected_lvl1, view.selected_lvl2 = 'Animaux', 'Chevaux'
        view.lvl3_vars = {}
        view.insp_vars = {'Couleur': SimpleNamespace(get=lambda:1)}
        view.insp_type_vars = {'Dessin': SimpleNamespace(get=lambda:1)}
        view.precision_var = SimpleNamespace(get=lambda:'Mon_cheval')
        view.start_var = SimpleNamespace(get=lambda:'7')
        item = renamer.FileItem(path='original.png', rel='original.png')
        before = view._build_target_name_for_item(item)
        i18n.set_language('en')
        self.assertEqual(before, view._build_target_name_for_item(item))
        self.assertTrue(before.startswith('DOCUMENTATION_'))
        view.naming_language = 'en'
        after = view._build_target_name_for_item(item)
        self.assertIn('_DRAWING_Color_', after)
        self.assertIn('_Animaux_Chevaux_', after)
        self.assertTrue(after.endswith('_007.png'))
        self.assertTrue(after.startswith('DOCUMENTATION_'))

    def test_search_fields_work_in_both_languages(self):
        for fr,en in [('nom:cheval -dossier:chat','name:cheval -folder:chat'), ('dossier:horse ext:png','folder:horse ext:png')]:
            self.assertEqual(library.search_condition(fr), library.search_condition(en))

    def test_templates_are_independent(self):
        original = copy.deepcopy(renamer.STRUCTURE_BASE)
        self.assertIn('Horses', STRUCTURE_EN['Animals'])
        i18n.set_language('en')
        self.assertEqual(renamer.STRUCTURE_BASE, original)
        self.assertIsNot(STRUCTURE_EN, renamer.STRUCTURE_BASE)

    def test_save_profile_preserves_deletions_and_language(self):
        controller = app.Morgue.__new__(app.Morgue)
        controller.settings = {}
        controller.folder = 'my-library'
        controller.renamer = SimpleNamespace(naming_language='en',structure={'Custom': {'Only': []}})
        with tempfile.TemporaryDirectory() as temp, patch.object(app,'SETTINGS_FILE',str(Path(temp)/'settings.json')):
            controller.save_classification()
            controller.renamer.structure.clear()
            controller.save_classification()
            saved = json.loads(Path(app.SETTINGS_FILE).read_text())
            self.assertEqual(saved['classification_profiles']['my-library'],{'language':'en','structure':{}})

    def test_change_ui_preserves_selection_and_saves_preference(self):
        controller = app.Morgue.__new__(app.Morgue)
        controller.language_var = SimpleNamespace(get=lambda:'EN')
        controller.settings = {}
        controller.tabs = Mock()
        controller.library_page, controller.rename_page = 'lib', 'rename'
        controller.library = Mock()
        controller.library.current_idx = 42
        controller.renamer = SimpleNamespace(naming_language='fr', structure={'Chevaux':{}})
        with patch.object(app,'save_json') as save:
            controller.change_language()
        self.assertEqual(controller.library.current_idx,42)
        controller.library.run_search.assert_not_called()
        self.assertEqual(controller.renamer.structure,{'Chevaux':{}})
        self.assertEqual(controller.renamer.naming_language,'fr')
        self.assertEqual(controller.settings['language'],'en')
        save.assert_called_once()


if __name__ == '__main__':
    unittest.main()
