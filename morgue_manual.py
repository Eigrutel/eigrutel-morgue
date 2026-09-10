# Eigrutel Lab / Atelier d'outils libres pour la bande dessinée
# Programme conçu et développé par Simon Léturgie / Eigrutel BD Academy.
# Nom public : Morgue / Version : 3.1.12 / Date : 10-09-2026
# Code : GNU AGPL v3.0 ou version ultérieure.
# Documentation et ressources : CC BY-SA 4.0, sauf mention contraire.
# Marques et logos Eigrutel / Eigrutel Lab / Eigrutel BD Academy : réservés.
"""Open the bundled offline manual in the user's browser."""
from pathlib import Path
import hashlib
import os
import sys
import tempfile
import webbrowser

MANUAL_NAME = 'Manuel-Morgue.html'


def manual_path():
    # Prefer the bundled version, never a stale HTML beside an updated EXE.
    base = Path(sys._MEIPASS) if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
    source = base / MANUAL_NAME
    if not source.is_file():
        raise FileNotFoundError(str(source))
    if not getattr(sys, 'frozen', False):
        return source

    # PyInstaller deletes its extraction directory at exit. Keep the browser's
    # document outside it so delayed opening, reloading and printing still work.
    data = source.read_bytes()
    digest = hashlib.sha256(data).hexdigest()[:20]
    user_cache = Path(os.environ.get('LOCALAPPDATA') or (Path.home() / '.cache'))
    directory = user_cache / 'Morgue' / 'manuals'
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / f'Manuel-Morgue-{digest}.html'
    if destination.is_file() and destination.read_bytes() == data:
        return destination
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=directory, suffix='.tmp', delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(data)
        os.replace(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return destination


def open_manual(interface_language='fr'):
    lang = 'en' if interface_language == 'en' else 'fr'
    url = manual_path().resolve().as_uri() + f'#{lang}-01'
    if not webbrowser.open(url, new=2):
        raise OSError('No browser accepted the local manual: ' + url)
    return url
