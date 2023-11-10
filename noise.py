from .noise_context import NoiseContext
from nodes import KSampler, KSamplerAdvanced

def insert_variation_inputs(input_types):
    required = {}
    for rkey in input_types['required']:
        required[rkey] = input_types['required'][rkey]
        if rkey=="seed" or rkey=="noise_seed":
            required['variation_seed'] = ("INT", {"default": 42, "min": 0, "max": 0xffffffffffffffff})
            required['variation_weight'] = ("FLOAT", {"default": 0.200, "min": 0, "max": 1, "step": 0.001})
    if (not 'variation_seed' in required):
        required['variation_seed'] = ("INT", {"default": 42, "min": 0, "max": 0xffffffffffffffff})
        required['variation_weight'] = ("FLOAT", {"default": 0.200, "min": 0, "max": 1, "step": 0.001})
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
        with NoiseContext(variation_seed, variation_weight):
            return getattr(self,self.clazz.FUNCTION)(**kwargs)
    
def variations_factory(original_class:type, name=None) -> type:
    name = name or original_class.__name__+"Variations"
    return type(name, (Variations, original_class), {'clazz':original_class})

NODE_CLASS_MAPPINGS = {
    "KSampler with Variations" : variations_factory(KSampler), 
    "KSampler Advanced with Variations" : variations_factory(KSamplerAdvanced), 
}
