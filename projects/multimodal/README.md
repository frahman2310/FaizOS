# Multimodal — ViT/CLIP, diffusion & flow matching, VLM fusion

**1. ViT & CLIP.** An image is cut into PATCHES; each patch is a token; the transformer runs unchanged. 224x224 with 16x16 patches -> 14 per side -> 196 tokens (384px -> 576: quadratic in image size). CLIP trains an image encoder and a text encoder so matching pairs have a high DOT PRODUCT — the same scoring from Module 7 — putting images and text in ONE space, which is what makes zero-shot classification work. SigLIP swaps the batch softmax for a per-pair sigmoid.

**2. Diffusion & rectified flow.** Turn generation back into a SUPERVISED problem: add known noise to a real image, train the model to predict that noise. To generate, start from noise, predict it, subtract a little, repeat. The path is curved so it needs many steps; RECTIFIED FLOW trains it straight — 50 steps -> 4, a 12.5x speedup.

**3. VLM fusion.** The LLM only understands tokens, so: image -> ViT -> 196 patch vectors -> a projection into the LLM's token dimension -> prepended like text. The LLM never sees an image. Cost: `text + n_images * tokens_per_image`. A 1000-token question + 5 images = 1,980 tokens — the images outweigh the question. (Cross-attention, as in Flamingo, avoids the context cost at the price of complexity.)

Run: `python3 multimodal.py` -> PASS. Module 18 skills `vit-clip-siglip`, `diffusion-flow-matching`, `vlm-fusion`. Completes Module 18.
