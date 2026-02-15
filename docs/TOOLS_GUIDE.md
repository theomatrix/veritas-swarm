# Veritas Swarm - Analysis Tools Guide

This document provides a comprehensive explanation of all 10 deepfake detection tools used by the Veritas Swarm agents.

## Overview

The Veritas Swarm uses **10 specialized analysis tools** across 4 categories:
- **Biometric Tools** (3) - Detect unnatural human physiology signals
- **Physics Tools** (2) - Verify physical plausibility of scenes
- **Signal Tools** (2) - Hunt for digital manipulation fingerprints
- **Audio-Sync Tools** (3) - Validate temporal coherence

Each tool uses computer vision (OpenCV), signal processing, or audio analysis to extract **quantitative measurements** that LLMs then interpret.

---

## Biometric Tools

### 1. Analyze Facial Landmarks

**What it does**: Detects faces and tracks facial geometry consistency across frames.

**How it works**:
- Uses OpenCV's Haar Cascade classifier for face detection
- For images: Checks if a face is present
- For videos: Tracks face detection rate across frames

**What it detects**:
- Missing faces (no detection)
- Inconsistent face tracking (face appears/disappears)
- Face-swap artifacts that break detection

**Technical Details**:
```python
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
faces = face_cascade.detectMultiScale(gray, 1.1, 4)
```

**Output Format**:
```json
{
  "file_type": "video",
  "total_frames_analyzed": 60,
  "frames_with_face_detected": 58,
  "detection_rate": 0.967,
  "anomaly_score": 0.033,
  "status": "NORMAL"
}
```

**Interpretation**:
- Detection rate > 0.8 = NORMAL
- Detection rate < 0.8 = SUSPICIOUS (face-swap artifacts)

---

### 2. Detect Blink Anomalies

**What it does**: Analyzes eye region changes to estimate natural blinking patterns.

**How it works**:
- Uses Haar Cascade for eye detection within face regions
- Counts transitions from "2 eyes detected" → "0 eyes detected"
- Calculates blink rate per minute

**What it detects**:
- Missing blink reflex (common in GAN-generated faces)
- Abnormally high blink rates (poor face-swap alignment)
- Unnatural eye behavior

**Technical Details**:
```python
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
eyes = eye_cascade.detectMultiScale(roi_gray)
# Count blinks: transitions from 2+ eyes to 0 eyes
```

**Output Format**:
```json
{
  "blink_count": 12,
  "video_duration_seconds": 10.5,
  "blink_rate_per_minute": 68.6,
  "normal_range": "15-20 blinks/min",
  "anomaly_detected": true,
  "status": "SUSPICIOUS"
}
```

**Interpretation**:
- Normal: 15-20 blinks/min
- < 5 blinks/min = SUSPICIOUS (missing blink reflex)
- > 30 blinks/min = SUSPICIOUS (tracking errors)

**Note**: Only works on videos (N/A for images)

---

### 3. Detect Face Blending

**What it does**: Scans face edges for blurred pixels indicating face-swap paste boundaries.

**How it works**:
- Detects face region using Haar Cascade
- Applies Canny edge detection
- Creates mask around face boundary (20px border)
- Measures edge density in boundary region

**What it detects**:
- Blending seams where swapped face meets original background
- Unnatural edge artifacts
- Face-swap paste boundaries

**Technical Details**:
```python
edges = cv2.Canny(blurred, 50, 150)
# Create boundary mask
mask = cv2.rectangle(mask, (x-20, y-20), (x+w+20, y+h+20), 255, 20)
boundary_edges = cv2.bitwise_and(edges, mask)
edge_density = np.sum(boundary_edges > 0) / np.sum(mask > 0)
```

**Output Format**:
```json
{
  "file_type": "image",
  "edge_density": 0.1823,
  "anomaly_score": 1.0,
  "blending_seam_detected": true,
  "status": "SUSPICIOUS"
}
```

**Interpretation**:
- Edge density > 0.15 = SUSPICIOUS (blending seam detected)
- Edge density < 0.15 = NORMAL

---

## Physics Tools

### 4. Analyze Head Pose 3D

**What it does**: Tracks face position changes to detect unnatural head movements.

**How it works**:
- Tracks face center coordinates across video frames
- Calculates movement distance between consecutive frames
- Detects sudden jumps (> 100 pixels per frame)

**What it detects**:
- Unnatural head movements (teleporting, jittering)
- Physically impossible rotations
- Face-swap tracking failures

**Technical Details**:
```python
center_x = x + w // 2
center_y = y + h // 2
distance = np.sqrt((center_x - prev_x)**2 + (center_y - prev_y)**2)
if distance > 100:
    sudden_movements += 1
```

**Output Format**:
```json
{
  "frames_analyzed": 300,
  "faces_tracked": 285,
  "sudden_movements_detected": 12,
  "horizontal_movement_range": 245.5,
  "vertical_movement_range": 180.3,
  "anomaly_detected": true,
  "status": "SUSPICIOUS"
}
```

**Interpretation**:
- Sudden movements > 5 = SUSPICIOUS
- Movement range > 500px = SUSPICIOUS (unnatural)

**Note**: Only works on videos (N/A for images)

---

### 5. Detect Lighting Inconsistencies

**What it does**: Analyzes shadow direction and lighting consistency between face and background.

**How it works**:
- Extracts face region and background regions (top/bottom strips)
- Calculates average brightness for each region
- Compares face brightness to background brightness

**What it detects**:
- Mismatched lighting (face from different scene)
- Inconsistent shadow direction
- Face-swap lighting errors

**Technical Details**:
```python
face_brightness = np.mean(cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY))
bg_brightness = (bg_top_brightness + bg_bottom_brightness) / 2
brightness_diff = abs(face_brightness - bg_brightness)
```

**Output Format**:
```json
{
  "file_type": "image",
  "brightness_difference": 67.5,
  "anomaly_score": 1.0,
  "lighting_mismatch_detected": true,
  "status": "SUSPICIOUS"
}
```

**Interpretation**:
- Brightness difference > 50 = SUSPICIOUS (lighting mismatch)
- Brightness difference < 50 = NORMAL

---

## Signal Tools

### 6. Analyze Frequency Domain

**What it does**: Uses FFT to convert frames to frequency domain and detect high-frequency noise patterns.

**How it works**:
- Applies 2D Fast Fourier Transform (FFT) to grayscale frames
- Calculates magnitude spectrum
- Measures high-frequency energy ratio (outer 40% of spectrum)

**What it detects**:
- GAN-specific frequency signatures
- Unnatural high-frequency content
- AI generation fingerprints

**Technical Details**:
```python
f_transform = fft.fft2(gray)
f_shift = fft.fftshift(f_transform)
magnitude_spectrum = np.abs(f_shift)
# Measure high-frequency energy (outer 40%)
high_freq_ratio = high_freq_energy / total_energy
```

**Output Format**:
```json
{
  "frames_analyzed": 5,
  "avg_high_frequency_ratio": 0.2845,
  "normal_range": "0.05-0.15",
  "anomaly_score": 1.0,
  "gan_fingerprint_detected": true,
  "status": "SUSPICIOUS"
}
```

**Interpretation**:
- Natural images: 0.05-0.15
- GAN images: 0.20-0.40
- Ratio > 0.20 = SUSPICIOUS

---

### 7. Detect GAN Fingerprints

**What it does**: Detects repeating grid patterns characteristic of GAN upsampling layers.

**How it works**:
- Applies FFT to detect checkerboard artifacts
- Checks for peaks at quarter frequencies (2x upsampling signature)
- Compares quarter-frequency magnitude to overall average

**What it detects**:
- Checkerboard patterns from GAN upsampling
- StyleGAN/ProGAN artifacts
- AI-generated image signatures

**Technical Details**:
```python
# Check for peaks at quarter frequencies
quarter_freq_positions = [
    (center_y + h//4, center_x),
    (center_y - h//4, center_x),
    (center_y, center_x + w//4),
    (center_y, center_x - w//4)
]
checkerboard_ratio = avg_quarter_freq / overall_avg
```

**Output Format**:
```json
{
  "frames_analyzed": 5,
  "avg_checkerboard_score": 1.52,
  "threshold": 1.3,
  "anomaly_score": 1.0,
  "gan_upsampling_artifacts_detected": true,
  "status": "SUSPICIOUS"
}
```

**Interpretation**:
- Ratio > 1.3 = SUSPICIOUS (GAN artifacts detected)
- Ratio < 1.3 = NORMAL

---

## Audio-Sync Tools

### 8. Extract Audio Track

**What it does**: Extracts audio track from video using FFmpeg.

**How it works**:
- Uses FFmpeg subprocess to extract audio
- Converts to WAV format (PCM 16-bit, 16kHz, mono)
- Returns temporary audio file path

**What it detects**:
- Presence/absence of audio track
- Audio extraction success/failure

**Technical Details**:
```python
command = [
    'ffmpeg', '-i', file_path,
    '-vn',  # No video
    '-acodec', 'pcm_s16le',
    '-ar', '16000',  # 16kHz
    '-ac', '1',  # Mono
    audio_path
]
subprocess.run(command)
```

**Output Format**:
```json
{
  "success": true,
  "audio_path": "/tmp/extracted_audio_12345.wav",
  "file_size_bytes": 256000,
  "sample_rate": 16000,
  "channels": 1,
  "format": "WAV (PCM 16-bit)"
}
```

**Note**: Only works on videos (N/A for images). Requires FFmpeg installed.

---

### 9. Analyze Lip Sync

**What it does**: Analyzes mouth region variance to detect lip movements.

**How it works**:
- Detects face and extracts lower face region (mouth area)
- Calculates pixel variance in mouth region across frames
- High variance = active speech, low variance = static/voice-over

**What it detects**:
- Lip movement presence/absence
- Static faces with voice-over
- Potential lip-sync issues

**Technical Details**:
```python
mouth_y = y + int(h * 0.6)  # Lower 40% of face
mouth_region = gray[mouth_y:y+h, x:x+w]
variance = np.var(mouth_region)
variance_std = np.std(all_variances)
```

**Output Format**:
```json
{
  "frames_analyzed": 300,
  "mouth_region_variance_std": 125.8,
  "variance_range": 450.2,
  "lip_movement_detected": true,
  "details": "Active movements detected"
}
```

**Interpretation**:
- Variance std > 50 = Active lip movement
- Variance std < 50 = Minimal movement (suspicious)

**Note**: Only works on videos (N/A for images)

---

### 10. Calculate Audio-Visual Offset

**What it does**: Estimates temporal offset between audio and visual tracks.

**How it works**:
- Extracts audio track using tool #8
- Analyzes face detection rate in video
- Calculates frame-to-frame motion scores
- Correlates audio presence with visual motion

**What it detects**:
- Lip-sync drift
- Post-production audio replacement
- Voice cloning with mismatched video

**Technical Details**:
```python
diff = cv2.absdiff(gray, prev_frame_gray)
_, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
motion_score = np.sum(thresh) / (thresh.shape[0] * thresh.shape[1])
```

**Output Format**:
```json
{
  "frames_analyzed": 100,
  "face_detection_rate": 0.95,
  "avg_motion_score": 0.082,
  "status": "NORMAL"
}
```

**Interpretation**:
- Face detection rate > 0.7 = NORMAL
- Face detection rate < 0.7 = SUSPICIOUS (manipulation)

**Note**: Only works on videos with audio (N/A for images)

---

## Tool Selection by File Type

The **Orchestrator** intelligently selects tools based on file type:

### Images
- ✅ Analyze Facial Landmarks
- ✅ Detect Face Blending
- ✅ Detect Lighting Inconsistencies
- ✅ Analyze Frequency Domain
- ✅ Detect GAN Fingerprints
- ❌ Blink Anomalies (N/A)
- ❌ Head Pose 3D (N/A)
- ❌ Audio tools (N/A)

### Videos
- ✅ All 10 tools available

---

## Dependencies

All tools require:
- `opencv-python` - Face detection, image processing
- `numpy` - Numerical computations
- `scipy` - FFT analysis
- `mediapipe` - Advanced face mesh (optional)

Audio tools additionally require:
- `ffmpeg-python` - Audio extraction
- `ffmpeg` binary installed on system

---

## How Tools Communicate with LLMs

**Critical Understanding**: LLMs **never see the actual images/videos**. Here's the flow:

```
1. User uploads media file → Server saves to /tmp/file.jpg

2. Agent receives task: "Analyze /tmp/file.jpg for blink anomalies"

3. Agent calls tool: detect_blink_anomalies("/tmp/file.jpg")

4. Tool (Python code) executes:
   - cv2.imread() reads actual image pixels
   - OpenCV analyzes the image
   - Returns JSON: {"blink_rate": 0.12, "status": "FAIL"}

5. LLM receives only the JSON data:
   "Based on the tool output, the blink rate of 0.12 is suspicious..."

6. LLM writes analysis interpreting the numbers
```

**The tool sees the pixels, the LLM sees only the numbers.**

---

## Example: Complete Tool Output

Here's what an agent receives from running all biometric tools on a video:

```json
{
  "analyze_facial_landmarks": {
    "detection_rate": 0.95,
    "status": "NORMAL"
  },
  "detect_blink_anomalies": {
    "blink_rate_per_minute": 3.2,
    "normal_range": "15-20 blinks/min",
    "status": "SUSPICIOUS"
  },
  "detect_face_blending": {
    "edge_density": 0.18,
    "blending_seam_detected": true,
    "status": "SUSPICIOUS"
  }
}
```

The LLM then interprets: *"The facial landmark detection is normal (95% detection rate), but the blink rate of 3.2/min is far below the normal 15-20/min range, and edge density of 0.18 indicates a blending seam. This suggests a face-swap deepfake."*

---

## Summary

| Tool | Category | Works On | Primary Detection |
|------|----------|----------|-------------------|
| Analyze Facial Landmarks | Biometric | Images, Videos | Face presence consistency |
| Detect Blink Anomalies | Biometric | Videos only | Missing blink reflex |
| Detect Face Blending | Biometric | Images, Videos | Face-swap seams |
| Analyze Head Pose 3D | Physics | Videos only | Unnatural movements |
| Detect Lighting Inconsistencies | Physics | Images, Videos | Lighting mismatch |
| Analyze Frequency Domain | Signal | Images, Videos | GAN frequency signatures |
| Detect GAN Fingerprints | Signal | Images, Videos | Checkerboard artifacts |
| Extract Audio Track | Audio-Sync | Videos only | Audio presence |
| Analyze Lip Sync | Audio-Sync | Videos only | Lip movement detection |
| Calculate A/V Offset | Audio-Sync | Videos only | Sync drift |

**Total**: 10 tools, 4 categories, covering biometric, physics, signal, and audio-visual analysis.
