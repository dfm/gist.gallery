#!/usr/bin/env python
# -*- coding: utf-8 -*-


extensions = [
    "sphinx.ext.mathjax",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://docs.scipy.org/doc/numpy/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
    "astropy": ("http://docs.astropy.org/en/stable/", None),
}

# templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"

# General information about the project.
project = "gist.gallery"
author = "Dan Foreman-Mackey"
copyright = "2020 " + author

version = "0.1"
release = "0.1"

exclude_patterns = ["_build", "env"]
pygments_style = "sphinx"

# HTML theme
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
