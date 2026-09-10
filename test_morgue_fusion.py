"""Regression tests on temporary files. Run: python -m unittest -v test_morgue_fusion"""
import os
from pathlib import Path
import sqlite3
import tempfile
import threading
import types
import unittest
from unittest.mock import patch, Mock
from PIL import Image
import morgue_library as library
import morgue_renamer as renamer
import morgue_workspace as workspace
import EigrutelMorgue as application


class FusionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.root = self.base / 'documentation'
        self.root.mkdir()
        self.db_patch = patch.object(library, 'DB_FILE', str(self.base/'index.db'))
        self.db_patch.start()
        library.init_db()
        self.source = self.root/'DOCUMENTATION_chat.png'
        Image.new('RGB', (24, 36)).save(self.source)
        library.rebuild_index(str(self.root), threading.Event(), lambda *args: None)
        library.set_favorite(str(self.root), str(self.source), True)
        library.set_collected(str(self.root), str(self.source), True)

    def tearDown(self):
        self.db_patch.stop()
        self.temp.cleanup()

    def test_rename_keeps_flags_and_updates_search(self):
        target = self.root/'DOCUMENTATION_cheval.png'
        workspace.relocate_indexed_file(str(self.source),str(target),str(self.root))
        rows = library.search_images(str(self.root),'cheval')
        self.assertEqual(len(rows),1)
        self.assertEqual((rows[0]['favorite'],rows[0]['collected']),(1,1))
        self.assertEqual(library.search_images(str(self.root),'chat'),[])
        self.assertFalse(self.source.exists())
        self.assertTrue(target.exists())

    def test_move_to_subfolder(self):
        folder=self.root/'Animaux';folder.mkdir();target=folder/self.source.name
        workspace.relocate_indexed_file(str(self.source),str(target),str(self.root))
        self.assertEqual(library.search_images(str(self.root),'dossier:animaux')[0]['favorite'],1)

    def test_move_to_new_library(self):
        folder=self.base/'sorted';folder.mkdir();target=folder/self.source.name
        workspace.relocate_indexed_file(str(self.source),str(target),str(self.root),str(folder))
        self.assertEqual(library.search_images(str(self.root),''),[])
        self.assertEqual(library.search_images(str(folder),'')[0]['collected'],1)

    def test_sql_error_restores_file_and_old_index(self):
        target=self.root/'DOCUMENTATION_new.png'
        conn=sqlite3.connect(library.DB_FILE)
        conn.execute("CREATE TRIGGER fail BEFORE INSERT ON images BEGIN SELECT RAISE(ABORT,'test'); END;")
        conn.commit();conn.close()
        with self.assertRaises(sqlite3.IntegrityError):
            workspace.relocate_indexed_file(str(self.source),str(target),str(self.root))
        self.assertTrue(self.source.exists());self.assertFalse(target.exists())
        self.assertEqual(library.search_images(str(self.root),'chat')[0]['favorite'],1)

    def test_collision_never_overwrites_target(self):
        target=self.root/'DOCUMENTATION_new.png';target.write_bytes(b'original')
        with self.assertRaises(FileExistsError):
            workspace.relocate_indexed_file(str(self.source),str(target),str(self.root))
        self.assertEqual(target.read_bytes(),b'original');self.assertTrue(self.source.exists())

    def test_unindexed_image_enters_index_after_naming(self):
        raw=self.root/'photo.png';Image.new('RGB',(10,10)).save(raw)
        target=self.root/'DOCUMENTATION_maison.png'
        workspace.relocate_indexed_file(str(raw),str(target),str(self.root))
        self.assertEqual(len(library.search_images(str(self.root),'maison')),1)

    def test_non_image_is_not_indexed(self):
        raw=self.root/'raw.txt';raw.write_text('test');target=self.root/'DOCUMENTATION_test.txt'
        workspace.relocate_indexed_file(str(raw),str(target),str(self.root))
        self.assertEqual(len(library.search_images(str(self.root),'')),1)

    def test_multiple_roots_are_updated(self):
        library.rebuild_index(str(self.base),threading.Event(),lambda *args:None)
        target=self.root/'DOCUMENTATION_new.png'
        workspace.relocate_indexed_file(str(self.source),str(target),str(self.root))
        self.assertEqual(library.search_images(str(self.root),'new')[0]['favorite'],1)
        self.assertEqual(library.search_images(str(self.base),'new')[0]['favorite'],0)

    def test_saved_destination_flags_are_merged(self):
        target=self.root/'DOCUMENTATION_new.png'
        library.set_favorite(str(self.root),str(target),True)
        workspace.relocate_indexed_file(str(self.source),str(target),str(self.root))
        self.assertEqual(library.search_images(str(self.root),'new')[0]['collected'],1)

    def test_reindex_after_rename_keeps_flags(self):
        target=self.root/'DOCUMENTATION_new.png'
        workspace.relocate_indexed_file(str(self.source),str(target),str(self.root))
        library.rebuild_index(str(self.root),threading.Event(),lambda *args:None)
        self.assertEqual(library.search_images(str(self.root),'')[0]['favorite'],1)

    def test_bindings_only_run_in_active_main_view(self):
        for cls in (library.MorgueApp,renamer.DocumentationRenamer):
            callbacks=[];called=[]
            root=types.SimpleNamespace(bind=lambda seq,callback,add:callbacks.append(callback))
            view=types.SimpleNamespace(root=root,workspace=types.SimpleNamespace(active_view=None))
            cls._bind_scoped(view,'<Return>',lambda e:called.append(True))
            event=types.SimpleNamespace(widget=types.SimpleNamespace(winfo_toplevel=lambda:root))
            callbacks[0](event);self.assertEqual(called,[])
            view.workspace.active_view=view;callbacks[0](event);self.assertEqual(called,[True])
            event.widget.winfo_toplevel=lambda:object();callbacks[0](event);self.assertEqual(called,[True])

    def test_controller_updates_both_views(self):
        target=self.root/'DOCUMENTATION_new.png';queued=[]
        row=library.search_images(str(self.root),'')[0]
        file=renamer.FileItem(path=str(self.source),rel=self.source.name)
        app=types.SimpleNamespace(library=types.SimpleNamespace(indexing=False,results=[row]),
            renamer=types.SimpleNamespace(files=[file]),folder=str(self.root),refresh_pending=False,
            root=types.SimpleNamespace(after_idle=lambda callback:queued.append(callback)),refresh_library=lambda:None)
        application.Morgue.relocate(app,str(self.source),str(target))
        self.assertEqual(row['path'],str(target));self.assertEqual(file.path,str(target));self.assertEqual(len(queued),1)

    def test_controller_refuses_move_during_indexing(self):
        app=types.SimpleNamespace(library=types.SimpleNamespace(indexing=True))
        with self.assertRaises(RuntimeError):
            application.Morgue.relocate(app,str(self.source),str(self.root/'new.png'))
        self.assertTrue(self.source.exists())

    def test_root_boundaries(self):
        self.assertTrue(workspace.is_inside(str(self.source),str(self.root)))
        self.assertFalse(workspace.is_inside(str(self.base/'documentation2'/'a.png'),str(self.root)))


class NavigationRefreshTests(unittest.TestCase):
    def controller(self):
        controller = application.Morgue.__new__(application.Morgue)
        controller.root = Mock()
        controller.tabs = Mock()
        controller.navigation_var = Mock()
        controller.library_page = 'library-page'
        controller.library = Mock()
        controller.renamer = Mock()
        controller.active_view = controller.renamer
        controller.refresh_pending = False
        return controller

    def test_unchanged_return_does_not_reload(self):
        controller = self.controller()
        controller.show_library()
        controller.tabs.select.assert_called_once_with('library-page')
        controller.library.run_search.assert_not_called()
        controller.root.after_idle.assert_not_called()

    def test_changed_return_defers_work_until_after_display(self):
        controller = self.controller()
        controller.refresh_pending = True
        controller.show_library()
        controller.library.run_search.assert_not_called()
        callback = controller.root.after_idle.call_args.args[0]
        callback()
        controller.root.after.assert_called_once_with(20, controller.refresh_library)
        controller.root.after.call_args.args[1]()
        controller.library.run_search.assert_called_once()

    def test_hidden_library_keeps_changes_pending(self):
        controller = self.controller()
        controller.refresh_pending = True
        controller.refresh_library()
        self.assertTrue(controller.refresh_pending)
        controller.library.run_search.assert_not_called()

    def test_refresh_reuses_cache_and_coalesces_callbacks(self):
        controller = self.controller()
        controller.active_view = controller.library
        cached = object()
        controller.library.thumb_photo_cache = {'existing': cached}
        controller.refresh_pending = True
        controller.refresh_library()
        controller.refresh_library()
        controller.library.run_search.assert_called_once()
        self.assertIs(controller.library.thumb_photo_cache['existing'], cached)


if __name__=='__main__':
    unittest.main()
