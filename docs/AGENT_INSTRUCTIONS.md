# Veritas Swarm - Agent Instructions

This document explains what each agent is instructed to do and why.

## Overview

Each agent receives a **task description** that tells them:
1. What to analyze
2. Which tools to use
3. What to look for
4. How to report findings

---

## Biometric Sentinel

### Role
"Human Signal Expert"

### Task Description

```
Analyse the following media file for biometric anomalies:
  File: {file_path}

CRITICAL: You MUST use your specialized analysis tools to perform comprehensive analysis.
Execute these tools in order:
1. analyze_facial_landmarks - Detect facial geometry anomalies and tracking consistency
2. detect_blink_anomalies - Measure blink rate and detect unnatural patterns
3. detect_face_blending - Scan for face-swap paste boundaries

Additional focus areas (if observable from tool outputs):
• Eye-glint consistency (position, shape, count)
• Remote PPG (rPPG) pulse signal presence
• Skin micro-texture under magnification
• Pupil dilation / iris boundary irregularities

Report each finding with a confidence tag: HIGH / MEDIUM / LOW.
Include specific metrics from tool outputs (e.g., 'Blink rate: 3.2/min, Normal: 15-20/min').
```

### Why These Instructions?

- **Tool execution order**: Ensures systematic analysis (presence → behavior → artifacts)
- **Specific metrics**: Forces quantitative reporting, not vague assessments
- **Confidence tags**: Helps Chief Justice weigh evidence
- **Additional focus areas**: Guides interpretation of tool outputs

### Expected Output

```
A structured forensic report listing each biometric indicator checked, 
whether it passed or failed, the confidence level, and a short justification 
for each finding.
```

---

## Physics Inspector

### Role
"Environmental Forensic Analyst"

### Task Description

```
Analyse the following media file for physics & lighting anomalies:
  File: {file_path}

CRITICAL: You MUST use your specialized analysis tools to perform comprehensive analysis.
Execute these tools in order:
1. analyze_head_pose_3d - Calculate 3D head rotation and detect unnatural movements
2. detect_lighting_inconsistencies - Analyze shadow vectors and lighting coherence

Additional focus areas (if observable from tool outputs):
• Shadow geometry and ground-truth plausibility
• Specular highlight coherence on skin, eyes, and glossy surfaces
• Reflection accuracy in eyes and mirrors
• Colour temperature consistency across the scene

Report each finding with a confidence tag: HIGH / MEDIUM / LOW.
Include specific metrics from tool outputs (e.g., 'Sudden movements: 12, Lighting inconsistencies: 35%').
```

### Why These Instructions?

- **Physics focus**: Catches face-swaps with mismatched lighting/shadows
- **Specific metrics**: Quantifies "physically impossible" claims
- **Specular highlights**: Often overlooked but telltale sign
- **Color temperature**: Detects faces from different lighting conditions

### Expected Output

```
A structured forensic report listing each physics/lighting indicator checked, 
whether it passed or failed, the confidence level, and a short justification 
for each finding.
```

---

## Signal Analyst

### Role
"Digital Artifact Investigator"

### Task Description

```
Analyse the following media file for digital manipulation artefacts:
  File: {file_path}

CRITICAL: You MUST use your specialized analysis tools to perform comprehensive analysis.
Execute these tools in order:
1. analyze_frequency_domain - Perform FFT analysis to detect high-frequency GAN fingerprints
2. detect_gan_fingerprints - Detect checkerboard artifacts from GAN upsampling

Additional focus areas (if observable from tool outputs):
• GAN-induced spatial warping or geometric distortion
• Blending seams between face region and background
• Abnormal pixel noise distribution patterns
• JPEG / H.264 re-compression ghosts or double-quantisation

Report each finding with a confidence tag: HIGH / MEDIUM / LOW.
Include specific metrics from tool outputs (e.g., 'High-freq ratio: 0.28, Normal: 0.05-0.15').
```

### Why These Instructions?

- **Frequency analysis**: Catches AI-generated content invisible to human eye
- **GAN fingerprints**: Detects specific generative model artifacts
- **Compression ghosts**: Finds evidence of post-processing
- **Specific metrics**: Provides numerical proof of manipulation

### Expected Output

```
A structured forensic report listing each digital-signal indicator checked, 
whether it passed or failed, the confidence level, and a short justification 
for each finding.
```

---

## Sync Specialist

### Role
"Audio-Visual Auditor"

### Task Description

```
Analyse the following media file for audio-visual sync anomalies:
  File: {file_path}

CRITICAL: You MUST use your specialized analysis tools to perform comprehensive analysis.
Execute these tools in order:
1. extract_audio_track - Extract audio from video for analysis
2. analyze_lip_sync - Track mouth movements and detect speech patterns
3. calculate_av_offset - Measure audio-visual synchronization offset

If the file is a still image with no audio, note that audio-visual sync checks 
are not applicable and report accordingly.

Additional focus areas (if observable from tool outputs):
• Natural speech cadence and rhythm
• Room acoustic fingerprint vs. visual environment
• TTS (text-to-speech) artefacts in the audio track

Report each finding with a confidence tag: HIGH / MEDIUM / LOW.
Include specific metrics from tool outputs (e.g., 'MAR variation: 0.008, Offset: 0ms').
```

### Why These Instructions?

- **Audio extraction first**: Prerequisite for other audio tools
- **Lip-sync analysis**: Catches voice cloning with mismatched video
- **TTS detection**: Identifies synthetic speech
- **Graceful handling**: Acknowledges when analysis isn't applicable

### Expected Output

```
A structured forensic report listing each audio-visual sync indicator checked, 
whether it passed or failed / was not applicable, the confidence level, and a 
short justification.
```

---

## Chief Justice

### Role
"Master Deepfake Verdict Agent"

### Task Description

```
You are the Chief Justice of the Veritas Swarm. You have received forensic reports 
from specialist agents who independently analysed the same media file. Your job:

1. Read ALL reports carefully.
2. Weigh the evidence — resolve any conflicting signals.
3. Produce a single VERDICT SCORE from 0 (certainly real) to 100 (certainly fake).
4. State your CONFIDENCE level: HIGH / MEDIUM / LOW.
5. List KEY FINDINGS as bullet points.
6. Write a LAYMAN'S BRIEF — a short, non-technical paragraph explaining the 'Tell' 
   (why it looks fake or real) so that any regular person can understand it.

Be decisive. Hedge only when the evidence is genuinely ambiguous.
```

### Why These Instructions?

- **Synthesis role**: Prevents redundant re-analysis
- **Conflict resolution**: Handles contradictory findings
- **Numerical score**: Provides quantifiable verdict
- **Layman's brief**: Makes findings accessible to non-experts
- **Decisiveness**: Avoids wishy-washy conclusions

### Expected Output

```
VERDICT SCORE: <0-100>
CONFIDENCE: <HIGH | MEDIUM | LOW>

KEY FINDINGS:
• <finding 1>
• <finding 2>
• ...

LAYMAN'S BRIEF:
<A plain-English paragraph explaining the 'Tell' — why the media is likely real 
or fake, written for a non-technical audience.>
```

---

## Instruction Design Principles

### 1. **Explicit Tool Execution**

"CRITICAL: You MUST use your specialized analysis tools"

**Why**: Without this, LLMs might try to analyze based on descriptions alone, which doesn't work.

### 2. **Ordered Tool Lists**

"Execute these tools in order: 1. ... 2. ... 3. ..."

**Why**: Ensures systematic analysis and proper dependencies (e.g., extract audio before analyzing lip-sync).

### 3. **Specific Metrics Required**

"Include specific metrics from tool outputs (e.g., 'Blink rate: 3.2/min')"

**Why**: Forces agents to cite numerical evidence, not make vague claims.

### 4. **Confidence Tags**

"Report each finding with a confidence tag: HIGH / MEDIUM / LOW"

**Why**: Helps Chief Justice weigh contradictory evidence.

### 5. **Additional Focus Areas**

Lists of secondary indicators to look for in tool outputs.

**Why**: Guides interpretation beyond raw numbers (e.g., what does "edge density 0.18" mean?).

### 6. **Structured Output Format**

Clear expectations for report structure.

**Why**: Ensures consistent, parseable output for frontend display.

---

## How Instructions Flow Through the System

```
1. User uploads media
   ↓
2. Orchestrator selects agents
   ↓
3. Task created with instructions:
   - File path injected
   - Tool list specified
   - Focus areas listed
   ↓
4. Agent receives task
   ↓
5. Agent executes tools in order
   ↓
6. Agent receives tool outputs (JSON)
   ↓
7. Agent interprets outputs per instructions
   ↓
8. Agent writes structured report
   ↓
9. Report sent to Chief Justice
```

---

## Example: Complete Agent Workflow

**Input**: `suspect_video.mp4`

**Biometric Sentinel receives**:
```
Task: Analyze suspect_video.mp4 for biometric anomalies
Tools: analyze_facial_landmarks, detect_blink_anomalies, detect_face_blending
```

**Biometric Sentinel executes tools**:
```python
result1 = analyze_facial_landmarks("suspect_video.mp4")
# Returns: {"detection_rate": 0.95, "status": "NORMAL"}

result2 = detect_blink_anomalies("suspect_video.mp4")
# Returns: {"blink_rate_per_minute": 3.2, "status": "SUSPICIOUS"}

result3 = detect_face_blending("suspect_video.mp4")
# Returns: {"edge_density": 0.18, "status": "SUSPICIOUS"}
```

**Biometric Sentinel writes report**:
```
BIOMETRIC ANALYSIS REPORT

1. Facial Landmarks: PASS (Confidence: HIGH)
   - Detection rate: 95% across 300 frames
   - Face tracking is consistent

2. Blink Anomalies: FAIL (Confidence: HIGH)
   - Blink rate: 3.2/min (Normal: 15-20/min)
   - Severely reduced blinking suggests synthetic face

3. Face Blending: FAIL (Confidence: MEDIUM)
   - Edge density: 0.18 (Threshold: 0.15)
   - Visible blending seam detected along jawline
```

**Chief Justice receives all 4 reports** → Synthesizes verdict

---

## Summary

| Agent | Tools | Primary Focus | Key Instruction |
|-------|-------|---------------|-----------------|
| Biometric Sentinel | 3 | Human physiology signals | "Detect unnatural blink patterns" |
| Physics Inspector | 2 | Environmental plausibility | "Verify lighting consistency" |
| Signal Analyst | 2 | Digital manipulation artifacts | "Hunt for GAN fingerprints" |
| Sync Specialist | 3 | Audio-visual coherence | "Evaluate lip-sync alignment" |
| Chief Justice | 0 | Evidence synthesis | "Produce authoritative verdict" |

**Total**: 10 tools across 4 specialist agents, synthesized by 1 master judge.
