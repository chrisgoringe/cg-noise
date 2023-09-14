from .noise import NODE_CLASS_MAPPINGS as noise_mappings
from .hijack import NODE_CLASS_MAPPINGS as hijack_mappings

NODE_CLASS_MAPPINGS = {}
def add_mappings(mappings:dict):
    for mapping in mappings:
        NODE_CLASS_MAPPINGS[mapping] = noise_mappings[mapping]

for mappings in (noise_mappings, hijack_mappings):
    add_mappings(mappings)

__all__ = ['NODE_CLASS_MAPPINGS']

import os, shutil
import folder_paths

module_js_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")
application_root_directory = os.path.dirname(folder_paths.__file__)
application_web_extensions_directory = os.path.join(application_root_directory, "web", "extensions", "cg-nodes")

shutil.copytree(module_js_directory, application_web_extensions_directory, dirs_exist_ok=True)