"""Hover cancellation, bilingual semantics, preferences and title colors."""
import unittest
from unittest.mock import Mock, patch
from types import SimpleNamespace
import EigrutelMorgue as application
from morgue_tooltips import Tooltips, describe
from morgue_windows_icon import colorref


class TooltipTests(unittest.TestCase):
    def manager(self,enabled):
        tip=Tooltips.__new__(Tooltips)
        tip.root=Mock()
        tip.root.after.return_value='scheduled'
        tip.enabled=SimpleNamespace(get=lambda:enabled)
        tip.pending=tip.tip=tip.target=None
        tip.on_change=Mock()
        return tip

    def test_disabled_does_not_schedule(self):
        tip=self.manager(False)
        tip.enter(SimpleNamespace(widget=object()))
        tip.root.after.assert_not_called()

    def test_leaving_cancels_delayed_display(self):
        tip=self.manager(True)
        widget=object()
        tip.enter(SimpleNamespace(widget=widget))
        tip.root.after.assert_called_once_with(550,tip.show)
        tip.leave(SimpleNamespace(widget=widget))
        tip.root.after_cancel.assert_called_once_with('scheduled')
        self.assertIsNone(tip.target)

    def test_disabling_hides_visible_tip_and_saves_preference(self):
        tip=self.manager(False)
        window=Mock()
        tip.tip=window
        tip._changed()
        window.destroy.assert_called_once()
        tip.on_change.assert_called_once_with(False)

    def test_same_symbol_has_contextual_bilingual_help(self):
        self.assertIn('fichier',describe('i','123open_metadata_dialog'))
        self.assertIn('file',describe('i','123open_metadata_dialog',True))
        self.assertIn('crédits',describe('i','123open_info_dialog'))
        self.assertIn('without deleting',describe('Purger collecte','123clear_collected',True))

    def test_tooltip_preference_is_persisted(self):
        controller=application.Morgue.__new__(application.Morgue)
        controller.settings={}
        with patch.object(application,'save_json') as save:
            controller.set_tooltips_enabled(False)
        self.assertIs(controller.settings['tooltips_enabled'],False)
        save.assert_called_once_with(application.SETTINGS_FILE,controller.settings)

    def test_windows_title_colors_and_active_workspace(self):
        self.assertEqual(colorref('#1F3A44'),0x443A1F)
        self.assertEqual(colorref('#7F2D30'),0x302D7F)
        controller=application.Morgue.__new__(application.Morgue)
        controller.root=object()
        controller.library=object()
        controller.renamer=object()
        with patch('morgue_windows_icon.set_caption_color') as color:
            controller.active_view=controller.library
            controller.update_title_color()
            color.assert_called_with(controller.root,'#1F3A44')
            controller.active_view=controller.renamer
            controller.update_title_color()
            color.assert_called_with(controller.root,'#7F2D30')


if __name__=='__main__':
    unittest.main()
