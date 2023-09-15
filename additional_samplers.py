from .noise import variations_factory
NODE_CLASS_MAPPINGS = {}

try:
    from custom_nodes.ComfyUI_tinyterraNodes.tinyterraNodes import ttN_TSC_pipeKSampler, ttN_pipeKSamplerAdvanced, ttN_pipeKSamplerSDXL
    NODE_CLASS_MAPPINGS["pipeKSampler with Variations"] = variations_factory(ttN_TSC_pipeKSampler) 
    NODE_CLASS_MAPPINGS["pipeKSamplerAdvanced with Variations"] = variations_factory(ttN_pipeKSamplerAdvanced) 
    NODE_CLASS_MAPPINGS["pipeKSamplerSDXL with Variations"] = variations_factory(ttN_pipeKSamplerSDXL) 
except:
    pass