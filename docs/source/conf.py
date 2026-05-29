# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Añadir el directorio raíz del backend al path para que autodoc
# pueda importar los módulos directamente
sys.path.insert(0, os.path.abspath("../.."))

# ---------------------------------------------------------------------------
# Información del proyecto
# ---------------------------------------------------------------------------

project = "BrailleScript"
copyright = "2025, BrailleScript"
author = "BrailleScript"
release = "1.0.0"
version = "1.0"

# ---------------------------------------------------------------------------
# Extensiones
# ---------------------------------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",          # Genera docs desde docstrings
    "sphinx.ext.autosummary",      # Tablas-resumen de módulos/clases
    "sphinx.ext.viewcode",         # Enlace «[source]» a cada función
    "sphinx.ext.napoleon",         # Soporte para secciones Google/NumPy style
    "sphinx.ext.intersphinx",      # Referencias cruzadas a docs externas (Python, etc.)
    "sphinx_autodoc_typehints",    # Muestra type hints de forma limpia en los docs
]

# ---------------------------------------------------------------------------
# Configuración de autodoc
# ---------------------------------------------------------------------------

autodoc_default_options = {
    "members": True,               # Documentar todos los miembros públicos
    "undoc-members": False,        # Omitir miembros sin docstring
    "private-members": False,      # Omitir miembros privados (_xxx)
    "show-inheritance": True,      # Mostrar jerarquía de herencia
    "member-order": "bysource",    # Orden según aparición en el código fuente
}

autodoc_typehints = "description"  # Muestra los tipos en la sección de descripción
autodoc_typehints_format = "short" # Usa nombres cortos (str en vez de builtins.str)

# ---------------------------------------------------------------------------
# Configuración de Napoleon (secciones de docstrings)
# ---------------------------------------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True   # Enmarca los Examples en un bloque
napoleon_use_admonition_for_notes = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_attr_annotations = True

# ---------------------------------------------------------------------------
# Configuración de autosummary
# ---------------------------------------------------------------------------

autosummary_generate = True        # Genera los .rst de cada módulo automáticamente

# ---------------------------------------------------------------------------
# Intersphinx: referencias cruzadas a documentación externa
# ---------------------------------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pillow": ("https://pillow.readthedocs.io/en/stable/", None),
}

# ---------------------------------------------------------------------------
# Idioma y localización
# ---------------------------------------------------------------------------

language = "es"

# ---------------------------------------------------------------------------
# Rutas de plantillas y archivos estáticos
# ---------------------------------------------------------------------------

templates_path = ["_templates"]
exclude_patterns = []
html_static_path = ["_static"]

# ---------------------------------------------------------------------------
# Tema HTML: Furo (moderno, limpio, con modo claro/oscuro)
# ---------------------------------------------------------------------------

html_theme = "furo"

html_title = "BrailleScript — Documentación"
html_short_title = "BrailleScript"

html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "light_css_variables": {
        "color-brand-primary": "#5C6BC0",
        "color-brand-content": "#3949AB",
        "color-admonition-background": "rgba(92, 107, 192, 0.05)",
        "font-stack": "Inter, system-ui, -apple-system, sans-serif",
        "font-stack--monospace": "JetBrains Mono, Fira Code, monospace",
    },
    "dark_css_variables": {
        "color-brand-primary": "#7986CB",
        "color-brand-content": "#9FA8DA",
    },
    "footer_icons": [
        {
            "name": "BrailleScript",
            "url": "https://github.com",
            "html": "",
            "class": "",
        },
    ],
}

# ---------------------------------------------------------------------------
# Fuentes de Google Fonts (inyectadas vía CSS personalizado)
# ---------------------------------------------------------------------------

html_css_files = ["custom.css"]
