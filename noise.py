from custom_nodes.cg_custom_core.base import BaseNode, TorchSeedContext
import comfy.sample
    
class Hijack(BaseNode):
    CATEGORY = "noise/hijack"
    REQUIRED = {"latent": ("LATENT", {}), 
                "variation":("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}), 
                "weight": ("FLOAT", {"default": 0.01, "min": 0, "max": 1, "step": 0.01}) }
    OPTIONAL = {"trigger": ("*",{})}
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    _original_noise_function = None
    def func(self, latent, variation, weight, trigger=None):
        if Hijack._original_noise_function==None:
            Hijack._original_noise_function = comfy.sample.prepare_noise
            def prepare_mixed_noise(latent_image, seed, batch_inds):
                original_noise = Hijack._original_noise_function(latent_image, seed, batch_inds)
                with TorchSeedContext(variation):
                    different_noise = Hijack._original_noise_function(latent_image, variation, batch_inds)
                return original_noise * (1.0-weight) + different_noise * (weight) 
            comfy.sample.prepare_noise = prepare_mixed_noise
        return (latent,)
    
class UnHijack(BaseNode):
    CATEGORY = "noise/hijack"
    REQUIRED = {"latent": ("LATENT", {}) }
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    def func(self,latent):
        if Hijack._original_noise_function:
            comfy.sample.prepare_noise = Hijack._original_noise_function
            Hijack._original_noise_function = None
        return (latent,)
