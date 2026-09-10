# Morgue / User manual

**A library for organizing and studying visual references**

Manual for Morgue 3.1.12 / Edition dated 10 September 2026.

Designed and developed by Simon Léturgie as part of Eigrutel BD Academy. Eigrutel Lab / Open tools workshop for comics.

This manual covers the Python desktop application and its Windows executable. It can be read independently of the program. The HTML edition contains both French and English, a contents panel, search and a print layout. It works offline; its language selector does not change the language of Morgue itself.

## 1. Understanding Morgue

Morgue brings the former Documentation Renamer and Index Documentation programs together in one application. Prepare your references, find them and use them for drawing without launching two separate programs.

Two workspaces share the same window and working folder: **Library**, with a dark blue toolbar, and **Organize / Rename**, with a dark red toolbar. **Studio**, available from the Library, opens a separate window for observation and timed drawing practice.

The documentation system relies on **filenames and folder paths**. Morgue does not automatically identify what an image depicts, translate its subject or perform AI visual searches. A horse photograph called `IMG_4582.jpg` will not be found by searching for “horse” unless that word appears in the information being searched.

The common prefix **`DOCUMENTATION_`** tells the Library which images to index. It stays the same in French and English. Your images remain ordinary files on your drive; the index is a catalogue for finding them, not a copy of the images.

## 2. Installing and launching

### Using the Windows executable

Place `Morgue-3.1.12.exe` in a folder you can write to, then open it. Python is not required to use an executable that has already been built. The application modules and resources are bundled inside the executable; working data and settings are saved alongside it.

The application folder and your image folder have different roles: the first contains the software and its operating data; the second contains the references you want to browse and organize. Select the latter inside Morgue.

### Using the Python sources

Keep all files from the program archive together. With Python 3.10 or later and Tkinter available, open a terminal in that folder and run:

```text
py -3 -m pip install -r requirements.txt
py -3 EigrutelMorgue.py
```

To build the executable on Windows, run **Construire_Morgue.cmd**. The first build downloads its dependencies; the result is `dist/Morgue-3.1.12.exe`. Editing a Python file does not update an executable that has already been built.

### Supported formats

Morgue recognizes `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tif` and `.tiff` images. PDFs, videos, text documents and Photoshop files are not part of this workflow. A supported extension does not guarantee that a damaged file can be read.

The Library also requires the `DOCUMENTATION_` prefix. Organize / Rename accepts supported images before they have been renamed. Studio can open an external file or folder without requiring this prefix.

## 3. Getting started

### Your images have not been prepared yet

1. Open **Organize / Rename**, then **Choose folder**.
2. Enable **Include subfolders** if the images are spread across several folders.
3. Choose classification levels, useful tags and optional details.
4. Check the **Target name** and click **RENAME (Enter)**. The program moves on to the next image.
5. To organize the actual folders as well, use **Sort DOCUMENTATION**, explained in chapter 12.
6. Switch to **Library**, check the chosen folder and run **Index / Reindex** to establish the initial catalogue of your collection.

### Your images already have DOCUMENTATION_ names

1. In the Library, click **Load DOCUMENTATION** and choose the root of your reference library.
2. Click **Index / Reindex**. Subfolders are included in indexing.
3. Wait for completion, then enter a word found in a filename or folder.
4. Click a thumbnail to inspect the image. Mark it as a favorite or add it to the collection if it is useful.

You do not need to reindex after every rename made inside Morgue: internal changes are synchronized with the index. Reindexing is still useful for discovering an existing collection or changes made outside Morgue.

## 4. Navigation, languages and help

The **Morgue** label occupies the same position in both toolbars. Navigation buttons also indicate their destination through color: red for Organize / Rename, dark blue for Library. Clicking the workspace that is already active does not restart your browsing session.

From Library, **Organize / Rename** carries over the selected image and the currently loaded search results. The renamer’s Previous and Next buttons then browse that set. To process an entire folder, use **Choose folder** in the renamer. Do not confuse this results-based browsing set with automatic sorting, which examines the source folder according to the subfolder option.

**FR / EN** immediately changes controls and help text. Your choice is saved, but filenames, categories and search terms are not translated. **Classification…**, in Organize / Rename, separately selects the category template and the vocabulary used in future filenames. See chapter 11.

The **i in the toolbar** opens help for the current workspace and the **About** page, with clickable contents. The **Complete manual** button at the bottom opens this manual in your browser, offline and in Morgue’s current language. It is available from both workspaces and from the Help and About pages. The manual is bundled inside the executable; the page remains available after Morgue closes. The **Show tooltips** checkbox enables or disables hover help throughout the application. This preference is remembered between launches. The **small i below the renamer preview** shows file metadata and serves a different purpose.

On compatible Windows versions, the title bar adopts the color of the active workspace. If this customization is unsupported, Windows keeps its usual appearance.

## 5. Library: indexing and browsing

The Library places thumbnails on the left, a large preview in the center, and search, collection and Studio controls on the right. The indexed-image count describes the catalogue; the result count depends on your current search.

**Index / Reindex** scans the chosen folder and its subfolders. The old index is kept until the new indexing operation succeeds. Press **Esc** to interrupt the operation. While it is running, Morgue blocks renaming, sorting and folder changes to avoid inconsistent paths.

Results load in **groups of 500**. A count such as `500 / 9491` means that 500 of 9,491 matches are loaded. Use the additional-results button at the bottom of the grid to continue. Collecting all results and using Studio’s “Current search” source operate on the loaded results only.

| Gesture or command | Effect |
| --- | --- |
| Click a thumbnail | Select the image and show it in the center. |
| Double-click a thumbnail | Open the file in its associated system application. |
| Mouse wheel over results | Scroll the thumbnails. |
| Previous / Next | Browse the loaded results. |
| Open image | Open the current image in your usual viewer. |
| Open folder | Access its location on your drive. |

Below the preview, the filename and folder identify the actual file. The displayed image is a preview; displaying it does not alter the source file.

## 6. Searching effectively

Search ignores case and accents and accepts word fragments. All entered terms must match, possibly in different parts of the filename and path. A short delay starts the search as you type; **Enter** starts it immediately.

| Query | What it searches for |
| --- | --- |
| `horse` | This fragment in the filename or path. |
| `horse red` | Both terms. |
| `horse -running` | Horse, excluding matches that contain running. |
| `-cat` | An exclusion without requiring a positive term. |
| `"street scene"` | A group of words together in the normalized text. |
| `name:horse` | Search the filename only. |
| `folder:costume` | Search the folder path only. |
| `ext:jpg` | The jpg extension; jpeg is a separate extension. |
| `folder:costume -name:test` | A folder containing costume, without test in the filename. |

The French aliases **`nom:`** and **`dossier:`** also work when the interface is in English. English aliases work in French. However, `horse` and `cheval` are not translated into each other: use the words actually present in your documentation.

Underscores in names are also treated as word separators during search. Thus, `"street scene"` can match `street_scene`. Without quotation marks, `street scene` requires both terms without requiring them to be adjacent.

The **Composition, Form, Silhouette, Color, Light, Values, Scale** checkboxes add their words to the query. They do not analyze the image. Selecting several checkboxes combines the criteria. The inserted words follow the classification language, which may differ from the interface language.

**Favorites** and **Collection** restrict the search to marked images. When both are selected, images belonging to either group are included, while still matching the other search terms. The toolbar’s **=★** and **=☑** buttons activate these filters; they do not mark the current image.

**Reset search** clears the query and disables the filters. It does not delete files, favorites or collection membership. In the Search field, the up and down arrows recall query history; right-click to access the command for clearing it.

Start with a simple term. If there are too many results, add a visual-use tag, a folder or an exclusion. If nothing is found, remove the filters before concluding that an image is missing.

## 7. Favorites, collection and export

A **favorite** identifies a reference you want to find again over time. The **collection** gathers a working selection, for example for a scene or an album. These flags are independent and saved per library; closing Morgue does not clear the collection.

| Command | Effect |
| --- | --- |
| Star below the preview | Add or remove the current image’s favorite flag. |
| Small square on a thumbnail | Add or remove that image from the collection. |
| Square below the preview / Image button | Add or remove the current image from the collection. |
| All results | Add the currently loaded results to the collection. |
| Show collection | Display the collection and clear the current text query. |
| Clear collection | Remove all collection flags after confirmation. Images stay on your drive. |
| Export collection | Copy collected images into a folder you choose. |

Export includes the active library’s entire indexed collection even when not all its thumbnails are loaded. Copies are gathered in the chosen folder without reproducing the original folder hierarchy. Existing names receive a suffix to prevent overwriting. Copy errors are reported; originals remain in place.

A useful approach is to collect broadly for a project, then mark the clearest references as favorites. The **Prime** filename tag is a separate concept: selecting Prime in the renamer does not automatically create a favorite flag in the database. This tag is called Master in French classification.

## 8. Correcting a filename in the Library

Select the image, edit the field below the preview and click **Rename**, or press **Ctrl+Enter in that field**. This command renames the actual file in its folder and updates the index.

Keep the original extension. If you omit it, Morgue adds it back; if you try to change it, the program refuses. Empty names, characters forbidden by Windows and name collisions are rejected. Changing a filename does not convert the image format.

Also keep the `DOCUMENTATION_` prefix so the document remains eligible for indexing. A renamed file may no longer match the current query and can therefore disappear from the results without being deleted.

To build a filename from levels, types and visual-use tags, switch to **Organize / Rename**.

## 9. Organize / Rename: building filenames

The left side contains the image, **Current name**, **Target name** and navigation controls. The right side contains types, visual-use tags, the level structure and naming settings.

**Choose folder** loads supported images. **Include subfolders** extends browsing into descendant folders; changing this option reloads the list. The `x / y` indicator shows your position among loaded images, not the number of successfully renamed files.

### From general to specific

Select a **Level 1**, then a **Level 2** belonging to it. If needed, select one or more **Level 3** items in that branch. For example, a personal structure might contain `Animals > Horses > Profile`. This is an illustration of the method; create any terms missing from your template.

Changing a parent refreshes the available child levels. The small menus beside the level headings open a more spacious selection window. Lists can be scrolled when their contents do not fit on screen.

### Types and visual uses

| Tag | Documentary purpose |
| --- | --- |
| PHOTO / Drawing | Identify the nature of the reference. |
| Prime | Flag an especially useful or exemplary reference. |
| Composition | Arrangement of masses, framing and eye flow. |
| Form / Silhouette | Volumes, outlines and readability of a pose. |
| Color | Harmonies, dominant colors and color relationships. |
| Light / Values | Lighting and the distribution of light and dark. |
| Scale | Size relationships and dimensional clues. |
| Walk / Run / Fight | Support, movement and storytelling through gesture. |

Levels describe the subject; tags also describe its usefulness for drawing. Choose the uses that matter, rather than giving every image every tag. The ten visible visual-use checkboxes in this version are the ones in the table; “Jump,” mentioned in older help text, is not offered as a checkbox in this panel.

### Automatic filename order

```text
DOCUMENTATION_L1_L2_L3_Type_Inspiration_Details_001.jpg
```

Unfilled parts are omitted. Several Level 3 items, types or visual-use tags may appear in sequence. Example using a custom template:

```text
DOCUMENTATION_Animals_Horses_Profile_PHOTO_Values_backlit_001.jpg
```

Automatic naming elements are cleaned: accents are removed, spaces become `_`, forbidden characters are removed and each element is limited to 80 characters. This per-element limit does not guarantee that the entire path will be short enough. The original extension is preserved.

The **Counter** adds a number with at least three digits (`001`, `002`, then `1000` when needed). It increases after a successful rename. An empty field adds no numeric suffix. **Details** adds free text before the number. The small crosses clear their respective fields.

### Applying the name and continuing

Always check the Target name, then click **RENAME (Enter)**. The file is renamed on your drive and the next image appears. A collision is refused: change the details or counter. Naming choices remain available for processing a series; check which ones no longer apply to the next image.

**Current name** and **Naming rules** switch between two methods. Current name copies the existing filename into the target field for manual correction. Typing directly in that field also enables manual mode. Naming rules restores automatic construction from the current choices; it does not undo the last rename.

**Open file**, **Folder**, **Previous**, **Next** and the small **i** complete the workflow. Metadata includes the path, file size, modification date and image dimensions when available.

## 10. Finding and editing levels

**Search levels** searches the entire hierarchy without case or accent sensitivity. Enter several terms to locate a branch. Typing alone does not replace your current choices: review the suggestion, use **up / down** to browse suggestions, then press **Enter**. In this field, Enter selects the suggestion instead of renaming the file. The cross clears the search.

The **L1**, **L2** and **L3** fields at the bottom modify the structure:

| Action | Procedure |
| --- | --- |
| Add a Level 1 | Enter its name in L1, then click +. |
| Add a Level 2 | Select its parent Level 1 first, enter L2, then click +. |
| Add a Level 3 | Select Levels 1 and 2, enter L3, then click +. |
| Delete a Level 1 or 2 | Select the category, use its - button and confirm. |
| Delete Level 3 items | Check the relevant items, use - and confirm. |
| Delete directly from a list | Right-click the relevant entry. |

Deleting a category changes the structure, and deleting a parent removes its branch. It does not delete or rename files that used those words. Those files can still be searched by name, but automatic sorting may no longer recognize their former category.

The add fields do not replace selections: typing a word in L2 without clicking + does not create a category.

## 11. Structure and classification language

**Save structure** exports the hierarchy to a `.docarch.json` file along with the classification language. **Load structure** replaces the current structure with an exported one. This file contains categories, not your images, favorites or collections.

**Reset**, in the structure controls, restores the original template for the classification language after confirmation. Do not confuse it with Reset search in the Library. Save your custom categories before replacing or resetting them.

**Classification…** offers a French or English template. This choice governs categories and tags used in future filenames, independently of the interface’s FR / EN selector. For example:

| French classification | English classification |
| --- | --- |
| `DOCUMENTATION_Animaux_Chevaux_001.jpg` | `DOCUMENTATION_Animals_Horses_001.jpg` |
| Couleur tag | Color tag |
| Master tag | Prime tag |

This change does not translate files already renamed or details you typed yourself. It replaces the structure after confirmation. A library containing both French and English filenames can still be browsed, but queries must use the appropriate words; sorting also depends on the active template’s categories.

Morgue remembers a structure and classification language for each working folder, including categories you deleted. When an older structure file does not specify a language, importing it keeps the current classification language.

## 12. Sorting files into folders

**Rename** changes a filename in its current folder. **Sort DOCUMENTATION** moves files into a hierarchy based on the levels recognized in their names. These are separate operations.

1. Check the source folder and **Include subfolders** option. Sorting covers that scope, not just the displayed image or results passed over by the Library.
2. Check that the active structure matches your filenames.
3. Click **Sort DOCUMENTATION**.
4. Select an existing Documentation root or the location where you want to create one.
5. Read the report of moved and unrecognized files.

| Recognized levels | Destination within the chosen root |
| --- | --- |
| L1, L2 and exactly one L3 | `L1/L2/L3` |
| L1 and L2, without a unique L3 or with several L3 items | `L1/L2` |
| L1 only | `L1` |
| No recognized L1 | File skipped and reported. |

Sorting examines names beginning with `DOCUMENTATION`. For Library indexing, use the full naming convention with `DOCUMENTATION_`. Names already present at the destination receive a suffix; existing files are not overwritten.

Moves performed within Morgue update the index and preserve favorite and collection flags. If the destination is another library, it becomes the working folder after sorting. There is no general command to undo an entire sorting operation: keep a backup of your images before a major reorganization.

## 13. Studio: preparing a session

In the Library, click **Studio**. The panel offers five sources: **Current search** results, **Favorites**, **Collection**, an **external file** or an **external folder**. External folders are scanned with their subfolders and do not require the documentation prefix.

Current search uses only loaded results. Favorites and Collection use their indexed sets in the active library, independently of that display limit.

Choose a time per image: **30 seconds, 1, 2, 5, 10 or 30 minutes**. **Custom time** accepts a duration in minutes; it does not mean an untimed session. To observe without a countdown, pause the session.

Next choose **Normal** or **Random** order, all images or a limit, and a **Dark**, **White** or **Neutral** background. When using random order with a limit, the images are shuffled before the requested number is selected.

Click **Start**. The session opens in its own window, advancing automatically when each image’s time expires. It ends after the last image, and you may also leave earlier.

## 14. Studio: observing and analyzing

Session tools change the display only. They do not rewrite your original files or export edited images.

| Tool | Use |
| --- | --- |
| Normal | See the original colors. |
| Grayscale | Read the image without differences in hue. |
| Black and white | Examine a strong separation between light and dark. |
| Three values / Five values | Simplify the tonal arrangement. |
| Blur | Observe large masses while reducing detail. |
| Composition | Overlay guides for thirds and diagonals. |
| Grid / Measuring grid | Compare proportions using a grid with adjustable size and horizontal and vertical offsets. |
| Grid color | Choose a more readable contrast against the image. |
| Horizontal and vertical flips | Refresh your perception of shapes and imbalances. |
| Rotation | Change the viewing orientation. |
| Dark, white or neutral background | Compare how the surroundings affect your reading of values. |

Right-click within the session to open display commands. Previous and Next change the reference; **Space** pauses or resumes the countdown. **Esc** first closes the grid settings window if it is open, and otherwise lets you leave the session.

For silhouette practice, choose poses, set 30 seconds and focus on support and overall direction. For composition study, choose a longer duration, then compare normal view, blur and three values. These are suggested exercises, not additional automatic modes.

## 15. Keyboard shortcuts

Commands depend on the active workspace. Letter shortcuts and the Library’s navigation arrows are distinct from typing in a text field.

### Library

| Shortcut | Action |
| --- | --- |
| Ctrl+O | Choose the library folder. |
| Ctrl+L / Ctrl+N | Focus search / the filename field. |
| Enter in Search | Run the search. |
| Up / Down in Search | Browse query history. |
| Ctrl+Enter in the filename | Apply quick renaming. |
| Left / Right outside text entry | Previous / next image. |
| f / k | Toggle the current image’s favorite / collection flag. |
| Shift+K | Add loaded results to the collection. |
| Ctrl+K / Ctrl+Shift+K | Show / clear the collection. |
| Alt+K | Export the collection. |
| F6 or a / Shift+F6 | Show the Studio panel / start the session. |
| F1 | Open help. |
| Esc | Close the Studio panel or interrupt indexing. |

### Organize / Rename

| Shortcut | Action |
| --- | --- |
| Ctrl+O | Choose the folder to process. |
| Ctrl+Shift+O / Ctrl+Shift+F | Open the image / its folder. |
| Ctrl+I / Ctrl+R | Insert the current name / restore automatic naming. |
| Left / Right outside text entry | Previous / next image. |
| Enter | Rename and continue; in Search levels, select the suggestion. |
| Up / Down in Search levels | Browse suggestions. |

### Studio session window

| Shortcut | Action |
| --- | --- |
| Left / Right | Previous / next reference. |
| Space | Pause / resume. |
| 1 / 2 / 3 | Normal / grayscale / black and white. |
| 4 / 5 / 6 | Three values / five values / blur. |
| 7 / 8 / 9 | Composition / grid color / show or hide the grid. |
| m / p / r | Horizontal flip / vertical flip / rotation. |
| Esc | Close grid settings or leave the session. |

The numeric keypad is also recognized during sessions. If a shortcut does nothing, click within the relevant window and check whether a text field or dialog has focus.

## 16. Settings, backup and relocation

Morgue works locally. It does not provide an online account or remote synchronization of your documentation. Automatically saved settings support continuity, but they do not replace image backups.

| Item | Contents or purpose |
| --- | --- |
| Your documentation folder | The actual image files. |
| `morgue_settings.json` | Shared folder, interface language, tooltips, structures and classification languages per library. |
| `index_documentation.db` | Catalogue and favorite and collection flags. |
| `index_documentation_settings.json` | Library preferences, query history and Studio settings. |
| `settings.json` | Renamer preferences, including folder, counter, details and selections. |
| `documentation_structure_user.json` | Historical structure data retained for continuity with earlier versions. |
| `index_documentation_thumbs` | Thumbnail cache, which can be rebuilt. |
| `logs` | Diagnostic logs; they are not an undo command. |
| Exported `.docarch.json` files | Independent copies of your structures. |

For a full backup, close Morgue, then copy **the application folder with its data and your image folder** to your backup destination. A structure export does not preserve favorites; a collection export contains only the selected images.

When updating, keep the data files and replace the software. If using the executable, place the new version in the folder containing your existing data. Avoid running the old standalone programs and Morgue simultaneously on the same files.

Paths play a role in the index and flags. Copying a library elsewhere with File Explorer and then reindexing does not guarantee recovery of the favorites and collection associated with the old paths. Moves made through **Sort DOCUMENTATION** benefit from internal synchronization. When migrating to another computer or drive, keep backups before reorganizing anything and check your flags afterwards.

## 17. Troubleshooting

| Situation | Check and action |
| --- | --- |
| No images in the Library | Check the root, extensions and `DOCUMENTATION_` prefix, then index and reset the search. |
| Images appear in the renamer but not in Library | The renamer accepts raw filenames; Library requires documentary naming. |
| An English query cannot find a French filename | Interface language does not translate files. Search words from their names or folders. |
| Only 500 results are visible | Load the next group at the bottom of the thumbnails. |
| A renamed file disappears from results | Check whether it still matches the query and retains the prefix. |
| Naming choices no longer change the Target name | Click Naming rules to leave manual mode. |
| A collision prevents renaming | Choose details or a counter that produces an unused filename. |
| Sorting does not recognize my names | Check the active structure’s language and categories. Read the skipped-file report. |
| External changes are not visible | Reindex after changes made in File Explorer or another program. |
| Some commands are blocked | Check whether indexing is running; wait or interrupt it with Esc. |
| Tooltips have disappeared | Open i and enable Show tooltips. |
| Bottom fields are off screen | Enlarge the window and scroll the level lists within their own areas. Also check display scaling. |
| The old icon or design still appears | Launch the newly rebuilt executable and replace shortcuts pinned to the old version. |
| An image will not open | Check that it still exists and try Open image in the system viewer. |

## 18. Terms and credits

**Structure**: the hierarchy of category levels. **Index**: the file catalogue. **Naming rules**: the rules used to construct filenames. **Favorite**: a saved flag identifying a preferred reference. **Collection**: an exportable working selection. **Studio**: the observation and practice workspace. **Working folder**: the active documentation root shared by both workspaces.

Morgue / Eigrutel Lab. Designed and developed by **Simon Léturgie** as part of **Eigrutel BD Academy**.

Source code and compiled program: **GNU AGPL v3.0 or later**. Documentation and resources: **CC BY-SA 4.0 unless otherwise stated**. Third-party libraries retain their respective licenses. Eigrutel / Eigrutel Lab / Eigrutel BD Academy trademarks, logos and distinctive signs: **reserved**.

The licenses for the software and this manual do not change the rights attached to the images you organize. This manual was prepared from the earlier manuals and the Morgue 3.1.12 source code. The labels and functions described refer to that version.
