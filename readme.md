# Noise Hijack

[Index of all my custom nodes](https://github.com/chrisgoringe/cg-nodes-index)

Custom nodes that replace `KSampler` and `KSampler Advanced` and allow you to generate small variations in the initial noise.

Conceptually, `noise = random_based_on(seed)` is replaced with `noise = random_based_on(variation_seed) * x + random_based_on(seed) * (1-x)` for some weight `x`. `x=0` generates an identical image to the normal nodes, small values of `x` generate similar images.

|Original|x=0.1|
|-|-|
|![Original](docs/variation_000.png)|![Variation](docs/variation_010.png)|

## Usage

The new nodes are then found under *sampling* as `KSampler with Variations` and `KSampler Advanced with Variations` (for use with other KSamplers, see below). Use them just like you use the original KSampler nodes, with

- `seed` is the seed for the original image
- `control_after_generated` is set to `fixed` by default
- `variation_seed` is the alternative seed
- `variation_weight` is the weight - typically quite small (try 0.1)

## Installation

```
cd [Comfy Install]/custom_nodes
git clone https://github.com/chrisgoringe/cg-noise.git
```
Then restart ComfyUI and reload the webpage.

## Update

```
cd [Comfy Install]/custom_nodes/cg-noise
git pull
```
Then restart ComfyUI and reload the webpage.

## Other Ksamplers

If you use a different KSampler, the following will *probably* work (it won't if the KSampler uses a non-standard noise generation routine - in which case raise an issue on the GitHub and I might look at it).

There are two custonm nodes under noise/hijack. Place the `Hijack` node directly before your KSampler, and the `Unhijack` node directly after it. Set *control_after_generate* to *fixed*. Like this, but with your KSampler:

![hijack](docs/hijack.png)

## Example

|||||
|-|-|-|-|
|x=0|x=0.005|x=0.01|x=0.02|
|![Original](docs/variation_000.png)|![x=0.005](docs/variation_005.png)|![x=0.010](docs/variation_010.png)|![x=0.2](docs/variation_020.png)|
|x=0.1|x=0.25|x=0.5|x=1|
|![x=0.1](docs/variation_100.png)|![x=0.25](docs/variation_250.png)|![x=05](docs/variation_500.png)|![x=1](docs/variation_1000.png)|

## Change Log

### 15 Sept 2023

- Added hijack nodes