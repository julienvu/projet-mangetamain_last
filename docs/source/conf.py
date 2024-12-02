# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Mangetamain_last"
copyright = "2024, Julien Vu"
author = "Julien Vu"
release = "Version 1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc"]
html_static_path = []
templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
#html_static_path = ["_static"]

import os
import sys
import warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

autodoc_mock_imports = ["data_loader", "log_config", "main"]
warnings.filterwarnings("ignore", category=DeprecationWarning)
suppress_warnings = ['autodoc.import_object']
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode'
]


autodoc_mock_imports = ['streamlit', 'pandas', 'numpy']
sys.path.insert(0, os.path.abspath('../../src')) 
