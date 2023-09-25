from .noise import get_mixed_noise_function
from custom_nodes.cg_custom_core.ui_decorator import ui_signal

import comfy.sample

@ui_signal('set_title_color')
class Hijack():
    CATEGORY = "noise/hijack"
    FUNCTION = "func"
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required" : {
                "latent": ("LATENT", {}), 
                "variation_seed":("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}), 
                "variation_weight": ("FLOAT", {"default": 0.001, "min": 0, "max": 1, "step": 0.001}) 
            },
            "hidden" : { "id": "UNIQUE_ID" }
        }
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    _original_noise_function = None
    _hijack_node_id = None

    def func(self, latent, variation_seed, variation_weight, id):
        if self._original_noise_function==None:
            self._original_noise_function = comfy.sample.prepare_noise
        else:
            print("In noise hijack, the noise function had already been hijacked - continuing, but this might be an error. Maybe you forgot to unhijack?")
        comfy.sample.prepare_noise = get_mixed_noise_function(self._original_noise_function, variation_seed, variation_weight)
        Hijack._hijack_node_id = id
        return (latent, (f"id={Hijack._hijack_node_id}", "red"))

@ui_signal('set_title_color')  
class UnHijack():
    CATEGORY = "noise/hijack"
    FUNCTION = "func"
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required" : {
                "latent": ("LATENT", {}), 
            },
        }
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)

    def func(slef,latent):
        if Hijack._original_noise_function:
            comfy.sample.prepare_noise = Hijack._original_noise_function
            Hijack._original_noise_function = None
        return (latent,(f"id={Hijack._hijack_node_id}","reset"))
    
NODE_CLASS_MAPPINGS = {
    "Hijack" : Hijack, 
    "UnHijack" : UnHijack, 
}
