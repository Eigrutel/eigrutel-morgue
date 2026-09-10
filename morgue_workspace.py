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

"""File/index coordination for Morgue. No Tk dependency in this service."""
from morgue_i18n import trf
import os
import shutil
import morgue_library as library


def is_inside(path, root):
    if not root:
        return False
    try:
        return os.path.commonpath([os.path.normcase(os.path.abspath(path)),
                                   os.path.normcase(os.path.abspath(root))]) == os.path.normcase(os.path.abspath(root))
    except ValueError:
        return False


def relocate_indexed_file(source, destination, active_root='', destination_root=None):
    """Move once, update all affected scopes, and restore source on SQL failure.

    The caller blocks this operation during background indexing. Existing flags
    on the new path are merged so an old saved favorite is not silently lost.
    """
    source, destination = os.path.abspath(source), os.path.abspath(destination)
    if os.path.normcase(source) == os.path.normcase(destination):
        return
    if os.path.exists(destination):
        raise FileExistsError(destination)
    if not os.path.isfile(source):
        raise FileNotFoundError(source)
    with library.db_lock:
        conn = library.db_connect()
        moved = False
        try:
            conn.execute('BEGIN IMMEDIATE')
            old_roots = {row[0] for row in conn.execute(
                'SELECT library_root FROM images WHERE path=? UNION SELECT library_root FROM user_flags WHERE path=?',
                (source, source))}
            flags = {row[0]: row[1:] for row in conn.execute(
                'SELECT library_root,favorite,collected FROM user_flags WHERE path=?', (source,))}
            target_roots = {}
            for root in old_roots:
                target = root if is_inside(destination, root) else (destination_root or active_root)
                if not is_inside(destination, target):
                    target = os.path.dirname(destination)
                target = library.normalize_library_root(target)
                previous = target_roots.get(target, (0, 0))
                current = flags.get(root, (0, 0))
                target_roots[target] = tuple(max(int(a or 0), int(b or 0)) for a, b in zip(previous, current))
            if (os.path.basename(destination).upper().startswith('DOCUMENTATION_')
                    and destination.lower().endswith(library.IMG_EXTS)):
                for root in (active_root, destination_root):
                    if root and is_inside(destination, root):
                        target_roots.setdefault(library.normalize_library_root(root), (0, 0))
            shutil.move(source, destination)
            moved = True
            stat = os.stat(destination)
            width, height = library.safe_image_size(destination)
            filename, folder = os.path.basename(destination), os.path.dirname(destination)
            conn.execute('DELETE FROM images WHERE path=?', (source,))
            conn.execute('DELETE FROM user_flags WHERE path=?', (source,))
            for root, (favorite, collected) in target_roots.items():
                conn.execute('''INSERT OR REPLACE INTO images
                    (library_root,path,filename,folder,norm_filename,norm_folder,width,height,mtime_ns,file_size)
                    VALUES (?,?,?,?,?,?,?,?,?,?)''', (root, destination, filename, folder,
                    library.normalize_search_text(filename), library.normalize_search_text(folder),
                    width, height, stat.st_mtime_ns, stat.st_size))
                conn.execute('INSERT OR IGNORE INTO user_flags (library_root,path,favorite,collected) VALUES (?,?,0,0)', (root,destination))
                conn.execute('''UPDATE user_flags SET favorite=MAX(COALESCE(favorite,0),?),
                    collected=MAX(COALESCE(collected,0),?) WHERE library_root=? AND path=?''',
                    (favorite,collected,root,destination))
            conn.commit()
        except Exception as error:
            conn.rollback()
            if moved:
                try:
                    if os.path.exists(source):
                        raise FileExistsError(source)
                    shutil.move(destination, source)
                except Exception as restore_error:
                    raise RuntimeError(trf('Index non mis à jour. Le fichier reste à vérifier : {0}. Restauration impossible : {1}', destination, restore_error)) from error
            raise
        finally:
            conn.close()
