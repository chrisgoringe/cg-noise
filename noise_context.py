import comfy.sample
import torch

class NoiseContext():
    original_noise_function = comfy.sample.prepare_noise

    def __init__(self, variation_seed, variation_weight):
        self.variation_seed = variation_seed
        self.variation_weight = variation_weight    
        
    def get_mixed_noise_function(cls, variation_seed, variation_weight):
        def prepare_mixed_noise(latent_image:torch.Tensor, seed, batch_inds):
            single_image_latent = latent_image[0].unsqueeze_(0)
            different_noise = NoiseContext.original_noise_function(single_image_latent, variation_seed, batch_inds)
            original_noise = NoiseContext.original_noise_function(single_image_latent, seed, batch_inds)
            if latent_image.shape[0]==1:
                mixed_noise = original_noise * (1.0-variation_weight) + different_noise * (variation_weight)
            else:
                mixed_noise = torch.empty_like(latent_image)
                for i in range(latent_image.shape[0]):
                    mixed_noise[i] = original_noise * (1.0-variation_weight*i) + different_noise * (variation_weight*i)
            return mixed_noise
        return prepare_mixed_noise
    
    def hijack(self):
        comfy.sample.prepare_noise = self.get_mixed_noise_function(self.variation_seed, self.variation_weight)

    def unhijack(self):
        comfy.sample.prepare_noise = NoiseContext.original_noise_function

    def __enter__(self):
        self.hijack()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.unhijack()
        