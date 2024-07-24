# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from datetime import date

sys.path.append(os.path.abspath("./_ext"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'RCJ-OnStage'
copyright = str(date.today().year) + ', Christian Häußler'
author = 'Christian Häußler'
release = 'v0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_toolbox.collapse",
    "sphinx_new_tab_link",
    'populate_team_data'
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
html_logo = "_static/images/logo_onstage.png"
html_title = "RoboCupJunior OnStage"
html_favicon = "_static/images/onstage_favicon.png"
html_css_files = [
    'custom.css',
]

html_theme_options = {
    "repository_url": "https://github.com/robocup-junior/onstage",
    "use_repository_button": True
}

# -- new_tab_link options --------------------------------------------------
# https://pypi.org/project/sphinx-new-tab-link/

new_tab_link_show_external_link_icon = True