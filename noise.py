import comfy.sample
from nodes import KSampler, KSamplerAdvanced

def get_mixed_noise_function(original_noise_function, variation_seed, variation_weight):
    def prepare_mixed_noise(latent_image, seed, batch_inds):
        different_noise = original_noise_function(latent_image, variation_seed, batch_inds)
        original_noise = original_noise_function(latent_image, seed, batch_inds)
        return original_noise * (1.0-variation_weight) + different_noise * (variation_weight) 
    return prepare_mixed_noise

def insert_variation_inputs(input_types):
    required = {}
    for rkey in input_types['required']:
        required[rkey] = input_types['required'][rkey]
        if rkey=="seed" or rkey=="noise_seed":
            required['variation_seed'] = ("INT", {"min": 0, "max": 0xffffffffffffffff})
            required['variation_weight'] = ("FLOAT", {"default": 0.001, "min": 0, "max": 1, "step": 0.001})
    input_types['required'] = required
    return input_types    

class Variations():
    CATEGORY = "sampling"
    FUNCTION = "func"
    clazz = None
    @classmethod
    def INPUT_TYPES(cls):
        return insert_variation_inputs(cls.clazz.INPUT_TYPES())
    
    def __init__(self):
        self.original_function_name = self.clazz.FUNCTION

    def func(self, **kwargs):
        variation_seed = kwargs.pop('variation_seed')
        variation_weight = kwargs.pop('variation_weight')
        original_noise_function = comfy.sample.prepare_noise
        comfy.sample.prepare_noise = get_mixed_noise_function(original_noise_function, variation_seed, variation_weight)
        results = getattr(self,self.clazz.FUNCTION)(**kwargs)
        comfy.sample.prepare_noise = original_noise_function
        return results    
    
class KSamplerVariations(Variations, KSampler):
    clazz = KSampler
    
class KSamplerAdvancedVariations(Variations, KSamplerAdvanced):
    clazz = KSamplerAdvanced

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
