"""Offline manual opening and Windows packaging contract, without a GUI."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest
import morgue_manual as manual
import build_windows as build


class ManualTests(unittest.TestCase):
    def test_source_paths_with_spaces_accents_and_hash_and_language(self):
        with TemporaryDirectory(prefix='Morgue é # ') as directory:
            root = Path(directory)
            (root / manual.MANUAL_NAME).write_text('<html>Manual</html>')
            with patch.object(manual, '__file__', str(root/'morgue_manual.py')), \
                 patch.object(manual.sys, 'frozen', False, create=True), \
                 patch.object(manual.webbrowser, 'open', return_value=True) as browser:
                for lang in ('fr', 'en'):
                    url = manual.open_manual(lang)
                    self.assertEqual(url, (root/manual.MANUAL_NAME).as_uri()+f'#{lang}-01')
                    browser.assert_called_with(url, new=2)

    def test_missing_manual_is_reported_without_launching_browser(self):
        with TemporaryDirectory() as directory, \
             patch.object(manual, '__file__', str(Path(directory)/'manual.py')), \
             patch.object(manual.sys, 'frozen', False, create=True), \
             patch.object(manual.webbrowser, 'open') as browser:
            with self.assertRaises(FileNotFoundError):
                manual.open_manual()
            browser.assert_not_called()

    def test_frozen_manual_survives_extraction_cleanup_and_updates(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = root/'bundle'; bundle.mkdir()
            source = bundle/manual.MANUAL_NAME
            source.write_bytes(b'first manual')
            with patch.object(manual.sys, 'frozen', True, create=True), \
                 patch.object(manual.sys, '_MEIPASS', str(bundle), create=True), \
                 patch.dict(manual.os.environ, {'LOCALAPPDATA': str(root/'cache')}):
                first = manual.manual_path()
                self.assertEqual(first, manual.manual_path())
                first.write_bytes(b'broken cache')
                self.assertEqual(manual.manual_path().read_bytes(), b'first manual')
                source.write_bytes(b'new manual')
                second = manual.manual_path()
                self.assertNotEqual(first, second)
                source.unlink(); bundle.rmdir()
                self.assertEqual(second.read_bytes(), b'new manual')

    def test_browser_refusal_is_reported(self):
        with patch.object(manual, 'manual_path', return_value=Path(__file__).resolve()), \
             patch.object(manual.webbrowser, 'open', return_value=False):
            with self.assertRaises(OSError):
                manual.open_manual('en')

    def test_windows_build_includes_required_manual(self):
        with patch.object(build.sys, 'platform', 'win32'), \
             patch.object(build.subprocess, 'run') as run, \
             patch.object(build, 'verify_executable_icon'):
            build.main()
            args = run.call_args.args[0]
            asset = str(Path(build.__file__).resolve().parent/manual.MANUAL_NAME)+':.'
            self.assertIn(asset, args)
            self.assertEqual(args[args.index(asset)-1], '--add-data')

    def test_build_stops_if_manual_missing(self):
        with TemporaryDirectory() as directory:
            root = Path(directory); (root/'Morgue.ico').touch()
            with patch.object(build, '__file__', str(root/'build_windows.py')), \
                 patch.object(build.sys, 'platform', 'win32'), \
                 patch.object(build.subprocess, 'run') as run:
                with self.assertRaises(SystemExit):
                    build.main()
                run.assert_not_called()

    def test_both_entry_anchors_exist_in_shipped_document(self):
        content = (Path(__file__).parent/manual.MANUAL_NAME).read_text(encoding='utf-8')
        self.assertIn('id="fr-01"', content)
        self.assertIn('id="en-01"', content)
        self.assertIn('Manuel complet', content)
        self.assertIn('Complete manual', content)


if __name__ == '__main__':
    unittest.main()
