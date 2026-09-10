# Morgue 3.1.12 / Bilingual library and renamer

Eigrutel Lab / Open tools workshop for comics.
Program designed and developed by Simon Léturgie as part of Eigrutel BD Academy.

## Start the application

Extract the entire ZIP into one folder. Keep all Python modules together and launch only **EigrutelMorgue.py**. Python 3.10 or later, Tkinter and Pillow are required. On Windows, open a terminal in the extracted folder and run:

```text
py -3 -m pip install -r requirements.txt
py -3 EigrutelMorgue.py
```

The application combines **Library**, **Organize / Rename**, and the **Atelier** drawing session window. Both tabs share the working folder. Library indexes image filenames beginning with `DOCUMENTATION_`; the renamer can also process images that do not yet follow this convention.

## Navigation bar

Each workspace now has a single toolbar: atelier blue for Library and dark red for Organize / Rename. Integrated tabs replace the old switch buttons, with a colored active tab. FR / EN uses two compact buttons in the same bar. Both toolbars have the same height, adjusted for Windows display scaling.

The three level lists resize within the available space above the L1, L2 and L3 editing fields. Each list has a scrollbar. Switching to the renamer carries over the selected reference; clicking the already active tab does not reload it.

The matching warm-paper “i” buttons open contextual help and an About page in one window, with clickable contents and structured headings. The classification template selector now sits beside the renamer’s structure controls. Colors follow the [Eigrutel palette](https://www.stripmee.com/design/).

## Interface language and naming language

Select **EN** at the top of the main window for the English interface. Switch back to **FR** at any time without restarting. Help and the Atelier interface follow this choice. The choice is saved; filenames, categories, search text and image selection stay intact.

Use **Classification: FR / EN** separately to choose a category template for the current working folder. The English template uses categories such as `Animals / Horses` and naming tokens such as `DRAWING`, `Color`, and `Light`. Template replacement asks for confirmation: export your custom structure first if you want to retain it. Applying a template does not rename existing images or folders.

The filename prefix stays **`DOCUMENTATION_`** in both languages. Personal descriptions remain exactly as entered, subject to the usual filename sanitization. Each working folder retains its complete category tree and classification language, including category deletions. Structure exports include the classification language; older imports without that field retain the current classification language.

Search supports `name:horse`, `folder:animals`, `ext:jpg`, quoted phrases and exclusions such as `horse -red`. French aliases `nom:` and `dossier:` also work in either interface language. Search ignores case and accents, but does not translate words or recognize visual image content. Searching `cheval` does not automatically find `horse`.

Returning to Library reuses the loaded images when nothing has changed. After renaming, the toolbar is displayed before refreshing results; valid cached thumbnails are retained. The light action buttons and information buttons use warm-paper backgrounds, dark-red text and white hover states. The information window uses the same warm-paper accent.

## Existing data

Close previous versions first. For your initial trial, use a copy of your application folder and image collection. Existing database, preferences, thumbnails and custom structures remain supported. Keep `index_documentation.db`, `index_documentation_settings.json`, `settings.json`, `documentation_structure_user.json` and existing cache folders when upgrading.

The shared folder, interface language and classification profiles are saved in `morgue_settings.json`. Data stays alongside the source application or executable, so use a writable folder.

Renaming and organizing within Morgue update the index and preserve favorites and collection flags. Destination collisions are rejected. If an index update fails after a move, Morgue attempts to restore the original file location. File changes made outside Morgue require reindexing. Avoid concurrent edits from older applications.

## Build Morgue-3.1.12.exe on Windows

With Python installed, double-click **Construire_Morgue.cmd**. This Windows command script creates a `.venv`, installs the build dependencies, and runs the executable builder. The first build needs Internet access to download dependencies. It pauses at the end so you can read the result.

The resulting executable is **dist/Morgue-3.1.12.exe**. Place it in your writable Morgue data folder and launch it. Python modules are bundled inside the executable. The included `Morgue.ico` brands the executable; `Morgue.ico` and `Morgue.png` are also bundled for window icons. The ICO contains nine sizes, from 16 to 256 pixels. Rebuild the executable to replace its icon. An optional existing `DOC.ico` remains separate and is used for Windows folder icons.

**This archive contains source code and the builder, not a precompiled Windows executable.** Windows compilation has not been performed in this environment.

## Integrated complete manual

In either workspace, open **i**, then click **Complete manual** at the bottom. The button remains available on the Help and About pages. It opens the offline manual in your browser, using Morgue’s interface language at the time you click.

`Manuel-Morgue.html` is supplied in this archive and bundled by the Windows build. Keep it in place before building. Markdown sources are in `docs`. The finished executable does not need a separate HTML file alongside it: a reading copy is kept in `%LOCALAPPDATA%\Morgue\manuals`, so the page remains available after the application closes. Updated manual content uses a new cached copy.

## Verification

Python compilation and 49 automated tests passed: 18 integration and navigation tests, 11 bilingual tests, 7 icon tests, 6 tooltip and title bar tests, and 7 integrated manual tests. Run them from the extracted directory:

```text
py -3 -m unittest -v test_morgue_fusion test_morgue_bilingual test_morgue_icons test_morgue_tooltips test_morgue_manual
```

Translated variables were verified using Tcl. Graphical layout, real keyboard interaction and executable startup still need testing on Windows. Check both tabs, an open Atelier session and FR / EN switching before using the new version for your main collection.

## Licenses

Source code and compiled program: GNU AGPL v3.0 or later.
Documentation and resources: CC BY-SA 4.0 unless otherwise stated.
Third-party libraries retain their respective licenses.
Eigrutel / Eigrutel Lab / Eigrutel BD Academy trademarks, logos and distinctive signs: reserved.

## Windows icon correction (3.1.12)

The ICO now contains bitmap images. Windows receives an explicit window icon, with PNG fallback. Failed icon loading is recorded in `logs/morgue-icons.log`. The builder verifies the actual icon resources in the EXE. Run `dist/Morgue-3.1.12.exe`; old shortcuts still point to the old program and should be replaced. Windows compilation and display remain untested here.

## Taskbar icon (3.1.12)

The small and large native Windows window icons are set after the window is mapped and reapplied on remapping. Morgue uses a dedicated Windows application identity. Rebuild and run `Morgue-3.1.12.exe` directly. Replace any old pinned shortcut with the new executable. Visual confirmation on Windows is still required.

## Tooltips and title bar (3.1.12)

Hover over a button for 550 ms to read its French or English help. Tips close on leave, click, typing or workspace/language changes. Open the “i” information panel and toggle **Show tooltips** in its footer to disable hover help globally. The preference is saved across restarts.

On Windows 11 the native title bar uses dark blue for Library and dark red for Organize / Rename, with light text. System window controls are preserved; unsupported systems retain their standard title bar. Display on Windows still requires local verification.

## Toolbar seam and text cleanup (3.1.12)

The Windows border is suppressed where supported, and a flat workspace container uses the active toolbar color to remove the gray seam below the caption. Native window controls remain available. Visual confirmation on Windows is still needed. Long dashes in supplied interface text and documentation have been replaced with slashes or simple hyphens; user data is unchanged.

## Renamer layout (3.1.12)

The Organize / Rename panels start directly below the toolbar. Spacing is kept inside the light content container, matching the Library and avoiding the theme’s beige outer frame.
