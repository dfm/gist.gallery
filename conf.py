#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import sphinx_typlog_theme


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

# # HTML theme
# # html_favicon = "_static/logo.png"
# html_theme = "sphinx_typlog_theme"
# html_theme_path = ["_themes", sphinx_typlog_theme.get_path()]
# # html_theme_options = {"logo": "logo.png"}
# # html_sidebars = {
# #     "**": ["logo.html", "globaltoc.html", "relations.html", "searchbox.html"]
# # }
# html_static_path = ["_static"]

# # Get the git branch name
# html_context = dict(
#     this_branch="master",
#     this_version=os.environ.get("READTHEDOCS_VERSION", "latest"),
# )
