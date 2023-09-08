import sys, os
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))
from .noise import *

NODE_CLASS_MAPPINGS = { "Hijack" : Hijack, "UnHijack" : UnHijack  }

__all__ = ['NODE_CLASS_MAPPINGS']

