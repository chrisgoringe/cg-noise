from .noise_context import NoiseContext

class Hijack():
    CATEGORY = "noise/hijack"
    FUNCTION = "func"
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required" : {
                "latent": ("LATENT", {}), 
                "variation_seed":("INT", {"default": 42, "min": 0, "max": 0xffffffffffffffff}), 
                "variation_weight": ("FLOAT", {"default": 0.2, "min": 0, "max": 1, "step": 0.001}) 
            },
            "hidden" : { "id": "UNIQUE_ID" }
        }
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)

    _context = None
    _hijack_node_id = None

    def func(self, latent, variation_seed, variation_weight, id):
        if Hijack._context==None:
            Hijack._hijack_node_id = id
            Hijack._context = NoiseContext(variation_seed, variation_weight)
        else:
            print("In noise hijack, the noise function had already been hijacked - continuing, but this might be an error. Maybe you forgot to unhijack?")
            return (latent,)
        Hijack._context.hijack()
        return (latent, )

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
    OUTPUT_NODE = True

    def func(self,latent):
        if Hijack._context:
            Hijack._context.unhijack()
            Hijack._context = None
            return (latent,)
        else:
            print("In noise unhijack, the noise function wasn't hijacked - continuing, but this might be an error.")
            return (latent,)
    
NODE_CLASS_MAPPINGS = {
    "Hijack" : Hijack, 
    "UnHijack" : UnHijack, 
}
