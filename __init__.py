from .noise import NODE_CLASS_MAPPINGS as noise_mappings
from .hijack import NODE_CLASS_MAPPINGS as hijack_mappings

NODE_CLASS_MAPPINGS = {}
for mappings in (
        noise_mappings,
        hijack_mappings, 
    ):
    for mapping in mappings:
        NODE_CLASS_MAPPINGS[mapping] = mappings[mapping]

WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "WEB_DIRECTORY"]

VERSION = "1.3"
