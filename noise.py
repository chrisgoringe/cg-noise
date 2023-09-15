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
            required['variation_weight'] = ("FLOAT", {"default": 0.000, "min": 0, "max": 1, "step": 0.001})
    if (not 'variation_seed' in required):
        required['variation_seed'] = ("INT", {"min": 0, "max": 0xffffffffffffffff})
        required['variation_weight'] = ("FLOAT", {"default": 0.000, "min": 0, "max": 1, "step": 0.001})
    input_types['required'] = required
    return input_types    

class Variations():
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
    
def variations_factory(original_class:type, name=None) -> type:
    name = name or original_class.__name__+"Variations"
    return type(name, (Variations, original_class), {'clazz':original_class})

NODE_CLASS_MAPPINGS = {
    "KSampler with Variations" : variations_factory(KSampler), 
    "KSampler Advanced with Variations" : variations_factory(KSamplerAdvanced), 
}


