import os, yaml
module_root_directory_noise = os.path.dirname(os.path.realpath(__file__))
    
class Base_noise:
    def __init__(self):
        pass
    FUNCTION = "func"
    CATEGORY = "noise"
    REQUIRED = {}
    OPTIONAL = None
    HIDDEN = None
    @classmethod    
    def INPUT_TYPES(s):
        types = {"required": s.REQUIRED}
        if s.OPTIONAL:
            types["optional"] = s.OPTIONAL
        if s.HIDDEN:
            types["hidden"] = s.HIDDEN
        return types
    RETURN_TYPES = ()
    RETURN_NAMES = ()
    
