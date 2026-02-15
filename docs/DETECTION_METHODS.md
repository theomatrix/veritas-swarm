# Veritas Swarm - Detection Methods

This document explains **WHY** we detect specific signals and **HOW** we detect them technically.

## 1. Biometric Signals

### Blink Patterns
**Why:** Generative models (GANs) often fail to reproduce the natural autonomic nervous system functions. Early Deepfakes (e.g., DeepFakes 1.0) completely lacked blinking. Modern ones may blink, but often at unnatural rates (too fast/slow) or with irregular patterns (fluttering without full closure).
**How:**
- **Eye Aspect Ratio (EAR):** We calculate the ratio of eye height to eye width using 6 facial landmarks per eye.
- **Thresholding:** When EAR falls below ~0.2, it counts as a closed eye.
- **Rate Calculation:** We count closure events over time to determine blinks per minute (BPM).
- **Metric:** Normal human blink rate is 15-30 BPM. <10 or >50 is suspicious.

### Eye Glints (Specular Reflections)
**Why:** The cornea is reflective. In a real photo, the reflection of the light source (glint) should be consistent in both eyes (same location, shape, number). In synthetic faces, these are often generated independently or muddled, leading to mismatched reflections.
**How:**
- **Iris Isolation:** We isolate the iris region using facial landmarks.
- **Highlight Detection:** We use adaptive thresholding to find the brightest pixels (specular highlights) within the iris.
- **Consistency Check:** We compare the geometric vector of the highlight center relative to the pupil center for both eyes.

### Face Blending Seams
**Why:** Face-swapping often involves pasting a generated face onto a target head. This creates a boundary or "mask line" usually around the jawline and forehead where the texture resolution or noise pattern changes abruptly.
**How:**
- **Edge Detection:** We use Canny Edge Detection specifically along the convex hull of the face landmarks (jawline).
- **Gradient Analysis:** We look for sharp discontinuities or "blur striping" (feathering used to hide the seam) that doesn't match the surrounding skin texture.

## 2. Physics & Lighting

### Head Pose Consistency (3D)
**Why:** In 2D-based face swaps, extreme head rotations often result in warping or "face slipping" because the model cannot infer the occluded side of the face. The 2D facial features might appear to "slide" across the 3D head geometry.
**How:**
- **PnP (Perspective-n-Point):** We solve the PnP problem using 2D facial landmarks and a generic 3D face model to estimate pitch, yaw, and roll.
- **Temporal derivative:** We check the rate of change. Instantaneous 90-degree turns or "jittery" rotation values are flagged.

### Lighting Consistency
**Why:** The face source and the target video often have different lighting environments. If a face lit from the left is swapped into a scene lit from the right, the shadows will be wrong.
**How:**
- **Global vs. Local Illumination:** We estimate the primary light source direction on the face (using nose shadow and forehead shading) and compare it to the background or body lighting.
- **Brightness Histogram:** We compare the histogram distribution of the face skin tones vs. the neck/body skin tones. Significant deviation (>2 SD) suggests a mismatch.

## 3. Signal Analysis ("Digital Fingerprints")

### Frequency Domain Analysis (FFT)
**Why:** GANs (Generative Adversarial Networks) generate images by upsampling noise. This upsampling process leaves periodic artifacts in the frequency domain that are invisible to the naked eye but obvious in a spectrum plot.
**How:**
- **Fast Fourier Transform (FFT):** We convert the image from spatial domain (pixels) to frequency domain.
- **Azimuthal Integration:** We average the power spectrum radially.
- **High-Frequency Anomalies:** Real cameras have a natural drop-off (1/f) in high frequencies. GANs often show spikes or "fingerprints" in the high-frequency band.

### GAN Grid Artifacts
**Why:** Transposed convolution layers in GANs often create a checkerboard pattern of pixel correlations.
**How:**
- **Pixel Correlation:** We look for repeating 4x4 or 8x8 pixel patterns that indicate block-based generation.
- **Noise Analysis:** We subtract a denoised version of the image from the original to get the "noise residual" and analyze it for grid patterns.

## 4. Audio-Visual Sync

### Lip Sync (Visemes vs. Phonemes)
**Why:** In "Lip Sync" deepfakes (e.g., Wav2Lip), the mouth is modified to match a new audio track. The synchronization is rarely perfect at the millisecond level, especially for plosive sounds (B, P) and fricatives (F, V).
**How:**
- **Mouth Aspect Ratio (MAR):** Similar to EAR, we track mouth opening height/width.
- **Audio Envelope:** We extract the amplitude envelope of the audio track.
- **Correlation:** We compute the cross-correlation between the MAR signal and the audio amplitude. A lag > 100ms indicates desynchronization.

### Audio consistency
**Why:** Voice cloning algorithms often generate "clean" studio-like audio that lacks the background noise or reverb of the video's environment.
**How:**
- **Noise Floor Analysis:** We measure the background noise level in silent parts of the audio.
- **Spectral Continuity:** We check for sudden cut-offs in the spectrogram which indicate spliced audio.

---

## Summary of Detection Confidence

| Method | Reliability | Works Best On | Weakness |
|:---|:---|:---|:---|
| **Blink Analysis** | High | DeepFakes 1.0, Long videos | Short clips, non-human blinkers |
| **Frequency Analysis** | Very High | GAN Images (StyleGAN) | Heavily compressed JPEGs |
| **Bending Seams** | Medium | Face Swaps | High-quality post-processing |
| **Lip Sync** | High | Dubbing/Re-enactment | Silent videos |
| **Lighting** | Medium | Poor quality swaps | Controlled studio lighting |
