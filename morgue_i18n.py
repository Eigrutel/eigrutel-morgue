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

"""Explicit UI translations. User data never passes through the catalogue."""
import weakref
from morgue_translations import EN

_language = 'fr'
_tracked = weakref.WeakValueDictionary()
_installed = False


def language():
    return _language


def rendered(value):
    return value.render() if isinstance(value, LocalText) else value


class LocalText(str):
    def __new__(cls, source, args=(), kwargs=None, pieces=None):
        obj = super().__new__(cls, cls._render(source, args, kwargs or {}, pieces))
        obj.source, obj.args, obj.kwargs, obj.pieces = source, args, kwargs or {}, pieces
        return obj

    @staticmethod
    def _render(source, args, kwargs, pieces):
        if pieces is not None:
            return ''.join(str(rendered(p)) for p in pieces)
        text = EN.get(source, source) if _language == 'en' else source
        if args or kwargs:
            return text.format(*(rendered(v) for v in args), **{k:rendered(v) for k,v in kwargs.items()})
        return text

    def render(self):
        return self._render(self.source, self.args, self.kwargs, self.pieces)

    def format(self, *args, **kwargs):
        return LocalText(self.source, args, kwargs)

    def __add__(self, other):
        return LocalText('', pieces=(self, other))

    def __radd__(self, other):
        return LocalText('', pieces=(other, self))


def tr(source):
    return source if isinstance(source, LocalText) else LocalText(source)


def trf(source, *args, **kwargs):
    return LocalText(source, args, kwargs)


def set_language(value):
    global _language
    _language = 'en' if value == 'en' else 'fr'
    for obj in list(_tracked.values()):
        try:
            obj._refresh_language()
        except Exception as error:
            import tkinter as tk
            if not isinstance(error, tk.TclError):
                raise


def watch(widget, callback):
    widget._refresh_language = callback
    _tracked[id(widget)] = widget


def install():
    """Observe only explicitly marked strings, never names or category labels."""
    global _installed
    if _installed:
        return
    _installed = True
    import tkinter as tk
    from tkinter import ttk

    class WidgetMixin:
        def __init__(self, *args, **kwargs):
            self._local_text = kwargs.get('text') if isinstance(kwargs.get('text'), LocalText) else None
            if self._local_text is not None:
                kwargs['text'] = self._local_text.render()
            super().__init__(*args, **kwargs)
            _tracked[id(self)] = self

        def configure(self, cnf=None, **kwargs):
            options = dict(cnf) if isinstance(cnf, dict) else {}
            options.update(kwargs)
            if 'text' in options:
                self._local_text = options['text'] if isinstance(options['text'], LocalText) else None
            if self._local_text is not None and 'text' in options:
                options['text'] = self._local_text.render()
                return super().configure(options)
            return super().configure(cnf, **kwargs)

        config = configure

        def _refresh_language(self):
            if self._local_text is not None and self.winfo_exists():
                super().configure(text=self._local_text.render())

    for module in (tk, ttk):
        for name in ('Label','Button','Checkbutton','Radiobutton','LabelFrame','Labelframe'):
            original = getattr(module, name, None)
            if original is not None:
                setattr(module, name, type(name, (WidgetMixin, original), {}))

    OriginalVar = tk.StringVar
    class LocalVar(OriginalVar):
        def __init__(self, master=None, value=None, name=None):
            self._local_value = value if isinstance(value, LocalText) else None
            super().__init__(master, rendered(value), name)
            self._local_value = value if isinstance(value, LocalText) else None
            _tracked[id(self)] = self
        def set(self, value):
            self._local_value = value if isinstance(value, LocalText) else None
            return super().set(rendered(value))
        initialize = set
        def _refresh_language(self):
            if self._local_value is not None:
                super().set(self._local_value.render())
    tk.StringVar = LocalVar

    OriginalMenu = tk.Menu
    class LocalMenu(OriginalMenu):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._local_labels = {}
            _tracked[id(self)] = self
        def add(self, itemType, cnf=None, **kwargs):
            options = dict(cnf or {});options.update(kwargs)
            render_options = dict(options)
            if 'label' in render_options:
                render_options['label'] = rendered(render_options['label'])
            result = super().add(itemType, render_options)
            if isinstance(options.get('label'), LocalText):
                self._local_labels[self.index('end')] = options['label']
            return result
        def _refresh_language(self):
            for index, value in self._local_labels.items():
                self.entryconfigure(index, label=value.render())
    tk.Menu = LocalMenu

    OriginalTop = tk.Toplevel
    class LocalTop(OriginalTop):
        def __init__(self, *args, **kwargs):
            self._local_title = None
            super().__init__(*args, **kwargs)
            _tracked[id(self)] = self
        def title(self, value=None):
            if value is not None:
                self._local_title = value if isinstance(value, LocalText) else None
            return super().title(rendered(value))
        wm_title = title
        def _refresh_language(self):
            if self._local_title is not None:
                super().title(self._local_title.render())
    tk.Toplevel = LocalTop
