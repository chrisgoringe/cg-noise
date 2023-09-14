from noise import get_mixed_noise_function
import comfy.sample

class HijackException(Exception):
    pass

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
            }
        }
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    _original_noise_function = None
    @classmethod
    def func(cls, latent, variation_seed, variation_weight, trigger=None):
        if cls._original_noise_function==None:
            cls._original_noise_function = comfy.sample.prepare_noise
            comfy.sample.prepare_noise = get_mixed_noise_function(cls._original_noise_function, variation_seed, variation_weight)
        else:
            raise HijackException("comfy.sample.prepare_noise already replaced - perhaps you failed to UnHijack?")
        return (latent,)
    
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

    @classmethod
    def func(cls,latent):
        if Hijack._original_noise_function:
            comfy.sample.prepare_noise = Hijack._original_noise_function
            Hijack._original_noise_function = None
        return (latent,)
    
NODE_CLASS_MAPPINGS = {
    "Hijack" : Hijack, 
    "UnHijack" : UnHijack, 
}
