from .common import Base_noise
import comfy.sample
    
class Hijack(Base_noise):
    REQUIRED = {"latent": ("LATENT", {}), 
                "variation":("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}), 
                "weight": ("FLOAT", {"default": 0.01, "min": 0, "max": 1, "step": 0.01}) }
    OPTIONAL = {"trigger": ("*",{})}
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    STOLEN = None
    def func(self, latent, variation, weight,trigger=None):
        if Hijack.STOLEN==None:
            Hijack.STOLEN = comfy.sample.prepare_noise
            def prepare_mixed_noise(latent_image, seed, batch_inds):
                return Hijack.STOLEN(latent_image, seed, batch_inds) * (1.0-weight) +\
                    Hijack.STOLEN(latent_image, variation, batch_inds) * (weight) 
            comfy.sample.prepare_noise = prepare_mixed_noise
        return (latent,)
    
class UnHijack(Base_noise):
    REQUIRED = {"latent": ("LATENT", {}) }
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    def func(self,latent):
        if Hijack.STOLEN:
            comfy.sample.prepare_noise = Hijack.STOLEN
            Hijack.STOLEN = None
        return (latent,)
