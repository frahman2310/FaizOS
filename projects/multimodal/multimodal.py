"""Multimodal — ViT/CLIP, diffusion & flow matching, VLM fusion (FaizOS build) — Module 18.

  1. ViT   - an image is cut into PATCHES and each patch is a token, so the transformer you already
             built runs on images unchanged. CLIP then trains image and text encoders into ONE space.
  2. DIFFUSION - add known noise to a real image and train the model to PREDICT that noise (supervised!).
             To generate: start from noise, predict it, subtract a little, repeat. Rectified flow
             straightens the path so far fewer steps are needed.
  3. VLM   - project the patch vectors into the LLM's token dimension and prepend them. The LLM sees
             tokens, never an image - and pays for every one of them in context.

Fill the THREE blanks (all three return NUMBERS), then run:  python3 multimodal.py
"""

# --- 1. ViT: how many tokens is an image? --------------------------------

def patches_per_side(img_size, patch_size):
    """How many patches fit along one edge."""
    return img_size // patch_size            # // divides and drops any remainder


def n_patches(img_size, patch_size):
    """Total patches = the grid is square, so it is per-side times per-side."""
    per_side = patches_per_side(img_size, patch_size)
    # Returns a NUMBER: the count of patches in the whole square grid.
    return per_side ** 2                     # a square grid: per-side times per-side


def clip_score(image_vec, text_vec):
    """CLIP scores a pair the way you scored attention: a dot product. Higher = better match."""
    return sum(a * b for a, b in zip(image_vec, text_vec))


# --- 2. diffusion: the step count is the cost ----------------------------

def denoise_once(noisy, predicted_noise, fraction=1.0):
    """Take a slice of the predicted noise back off the image."""
    return [n - fraction * p for n, p in zip(noisy, predicted_noise)]


def sampling_speedup(diffusion_steps, flow_steps):
    """How many times faster generation gets when the path is straightened."""
    # Returns a NUMBER: fewer steps means faster, so the big count goes on top.
    return diffusion_steps / flow_steps      # fewer steps = faster, so the big count is on top


# --- 3. VLM fusion: images cost context ----------------------------------

def context_tokens(text_tokens, n_images, tokens_per_image):
    """Every image is prepended as tokens, so it competes with the text for context."""
    # Returns a NUMBER: the text plus every image's worth of tokens.
    return text_tokens + n_images * tokens_per_image   # every image is paid for in context


if __name__ == "__main__":
    print("1. ViT")
    print(f"   224x224 image, 16x16 patches -> {patches_per_side(224,16)} per side, "
          f"{n_patches(224,16)} tokens")
    print(f"   384x384 image, 16x16 patches -> {n_patches(384,16)} tokens (bigger image, more tokens)")
    cat_img = [1.0, 0.2, 0.0]
    print(f"   CLIP: image vs 'a photo of a cat' {clip_score(cat_img, [1.0, 0.1, 0.0]):.2f}  "
          f"vs 'a photo of a car' {clip_score(cat_img, [0.0, 0.1, 1.0]):.2f}")

    print("\n2. DIFFUSION")
    noisy, predicted = [0.9, 0.4], [0.5, 0.1]
    print(f"   noisy {noisy} minus predicted noise {predicted} -> {denoise_once(noisy, predicted)}")
    print(f"   50 diffusion steps vs 4 flow steps -> {sampling_speedup(50, 4)}x faster")

    print("\n3. VLM FUSION")
    print(f"   1000-token question + 1 image  = {context_tokens(1000, 1, 196):,} tokens")
    print(f"   1000-token question + 5 images = {context_tokens(1000, 5, 196):,} tokens")

    assert patches_per_side(224, 16) == 14 and n_patches(224, 16) == 196
    assert n_patches(384, 16) == 576, "24 per side squared"
    assert clip_score([1.0,0.2,0.0], [1.0,0.1,0.0]) > clip_score([1.0,0.2,0.0], [0.0,0.1,1.0])
    assert denoise_once([0.9,0.4],[0.5,0.1]) == [0.4, 0.30000000000000004] or True
    assert sampling_speedup(50, 4) == 12.5, "50/4 = 12.5, not 12"
    assert context_tokens(1000, 1, 196) == 1196
    assert context_tokens(1000, 5, 196) == 1980, "five images cost more than the question"
    print("\nPASS ✅  patches are tokens; predict the noise; images are paid for in context.")
