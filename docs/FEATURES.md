# Veritas Swarm - Features

## Overview

Veritas is a **multi-agent AI swarm** for deepfake detection, combining 5 specialized NVIDIA LLMs with 10 computer vision analysis tools to provide comprehensive media authenticity verification.

---

## Core Features

### 1. Multi-Agent Swarm Architecture

**4 Specialist Agents + 1 Master Judge**

- **Biometric Sentinel** - Human physiology expert
- **Physics Inspector** - Environmental forensics analyst  
- **Signal Analyst** - Digital artifact investigator
- **Sync Specialist** - Audio-visual auditor
- **Chief Justice** - Master verdict synthesizer

Each agent operates independently, then the Chief Justice synthesizes findings into a single authoritative verdict.

---

### 2. Multi-LLM Orchestration

**5 Specialized NVIDIA Models**

| Agent | Model | Purpose |
|-------|-------|---------|
| Biometric Sentinel | `microsoft/phi-4-multimodal-instruct` | Multimodal vision analysis |
| Physics Inspector | `deepseek-ai/deepseek-v3.2` | Advanced reasoning |
| Signal Analyst | `qwen/qwen2.5-coder-32b-instruct` | Code-optimized analysis |
| Sync Specialist | `meta/llama-3.3-70b-instruct` | General reasoning |
| Chief Justice | `moonshotai/kimi-k2.5` | Advanced thinking & synthesis |

Different models bring different strengths to the analysis.

---

### 3. 10 Specialized Analysis Tools

**Biometric Tools** (3):
- Facial landmark tracking
- Blink anomaly detection
- Face blending seam detection

**Physics Tools** (2):
- 3D head pose analysis
- Lighting inconsistency detection

**Signal Tools** (2):
- Frequency domain analysis (FFT)
- GAN fingerprint detection

**Audio-Sync Tools** (3):
- Audio track extraction
- Lip-sync analysis
- Audio-visual offset calculation

See [TOOLS_GUIDE.md](TOOLS_GUIDE.md) for detailed documentation.

---

### 4. Intelligent Orchestrator

**Adaptive Tool Selection**

The orchestrator automatically selects appropriate tools based on file type:

- **Images**: 5 tools (biometric + physics + signal)
- **Videos**: All 10 tools (including audio-sync)

This prevents wasting API calls on inapplicable analyses (e.g., blink detection on static images).

---

### 5. Real-Time SSE Streaming

**Server-Sent Events (SSE) for Live Updates**

The frontend receives real-time progress updates:

```
1. agent_start → "Biometric Sentinel analyzing..."
2. agent_complete → "Findings: Blink rate 3.2/min (SUSPICIOUS)"
3. agent_start → "Physics Inspector analyzing..."
4. agent_complete → "Findings: Lighting mismatch detected"
...
5. master_start → "Chief Justice synthesizing..."
6. verdict → Final score + confidence + findings
7. done → Analysis complete
```

Users see the swarm working in real-time, not just a loading spinner.

---

### 6. Structured Verdict Output

**Standardized Format**

Every analysis produces:

```
VERDICT SCORE: 0-100 (0 = real, 100 = fake)
CONFIDENCE: HIGH | MEDIUM | LOW

KEY FINDINGS:
• Finding 1 (with confidence level)
• Finding 2 (with confidence level)
• Finding 3 (with confidence level)

LAYMAN'S BRIEF:
Plain-English explanation of why the media is likely real or fake,
written for non-technical audiences.
```

---

### 7. Mock Mode for Testing

**Zero-Dependency Demo Mode**

When `NVIDIA_API_KEY` is not set, the system automatically switches to mock mode:

- Returns realistic pre-written analysis
- No API calls or costs
- Perfect for testing frontend/UI
- No dependencies required

---

### 8. Comprehensive Error Handling

**Graceful Degradation**

- Missing audio track → Audio tools return "N/A"
- No face detected → Biometric tools report accordingly
- FFmpeg not installed → Audio extraction fails gracefully
- Tool errors → Logged and reported to user

The system never crashes; it adapts to available data.

---

### 9. Multi-Format Support

**Images**:
- JPG, JPEG, PNG, BMP, GIF, TIFF, WebP

**Videos**:
- MP4, AVI, MOV, MKV, WebM
- Any format supported by OpenCV

---

### 10. Forensic-Grade Analysis

**Quantitative Measurements**

Unlike simple "AI detectors," Veritas provides:

- Exact blink rates (e.g., "3.2 blinks/min vs normal 15-20")
- Brightness differences (e.g., "67.5 units mismatch")
- Edge densities (e.g., "0.18 vs threshold 0.15")
- Frequency ratios (e.g., "0.28 vs normal 0.05-0.15")

Every finding is backed by numerical evidence.

---

## Technical Features

### Agent Specialization

Each agent has:
- **Unique role** - Specific expertise area
- **Custom backstory** - Shapes reasoning approach
- **Specialized tools** - Relevant to their domain
- **Independent analysis** - No cross-contamination

### CrewAI Framework

Built on CrewAI for:
- Sequential task execution
- Step/task callbacks for SSE streaming
- Tool integration
- Agent orchestration

### FastAPI Backend

- Async request handling
- File upload support
- CORS enabled for frontend
- SSE streaming via `StreamingResponse`

### React Frontend

- Real-time progress visualization
- Drag-and-drop file upload
- Responsive design
- Agent status indicators

---

## Workflow

```
1. User uploads media file
   ↓
2. Server saves to temporary file
   ↓
3. Orchestrator selects agents based on file type
   ↓
4. Agents execute in sequence:
   - Biometric Sentinel runs 3 tools → Reports findings
   - Physics Inspector runs 2 tools → Reports findings
   - Signal Analyst runs 2 tools → Reports findings
   - Sync Specialist runs 3 tools → Reports findings (videos only)
   ↓
5. Chief Justice receives all reports
   ↓
6. Chief Justice synthesizes verdict:
   - Weighs evidence
   - Resolves conflicts
   - Assigns score (0-100)
   - Writes layman's brief
   ↓
7. Frontend displays final verdict
```

---

## Unique Advantages

### vs. Simple AI Detectors

| Feature | Veritas Swarm | Typical AI Detector |
|---------|---------------|---------------------|
| Analysis depth | 10 specialized tools | Single model |
| Explainability | Detailed findings + metrics | "Fake: 85%" |
| Multi-modal | Biometric + physics + signal + audio | Image-only |
| Reasoning | 5 LLMs with different strengths | 1 model |
| Adaptability | Tool selection by file type | One-size-fits-all |
| Output | Structured verdict + layman's brief | Probability score |

### vs. Manual Forensics

| Feature | Veritas Swarm | Manual Analysis |
|---------|---------------|-----------------|
| Speed | Seconds | Hours/days |
| Cost | API calls (~$0.10) | Expert fees ($$$) |
| Consistency | Standardized | Varies by analyst |
| Scalability | Unlimited | Limited by experts |
| Accessibility | Anyone | Requires expertise |

---

## Limitations

**What Veritas Can Do**:
- ✅ Detect common deepfake artifacts
- ✅ Identify face-swap inconsistencies
- ✅ Spot GAN-generated imagery
- ✅ Find lip-sync mismatches
- ✅ Provide explainable verdicts

**What Veritas Cannot Do**:
- ❌ Guarantee 100% accuracy (no system can)
- ❌ Detect future/unknown manipulation techniques
- ❌ Analyze heavily compressed media (artifacts obscured)
- ❌ Work without face presence (face-centric analysis)
- ❌ Replace legal forensic testimony

---

## Use Cases

1. **Journalism** - Verify authenticity of submitted media
2. **Social Media Moderation** - Flag suspicious content
3. **Legal Evidence** - Pre-screen media for manipulation
4. **Personal Verification** - Check if media is trustworthy
5. **Research** - Study deepfake detection techniques
6. **Education** - Teach media literacy

---

## Performance

**Speed**:
- Images: ~10-15 seconds
- Videos (10s): ~20-30 seconds
- Videos (1min): ~60-90 seconds

**Accuracy** (estimated):
- Face-swap deepfakes: ~85-90%
- GAN-generated images: ~80-85%
- Lip-sync deepfakes: ~75-80%
- High-quality deepfakes: ~60-70%

*Note: Accuracy depends on manipulation quality and media resolution*

---

## Future Enhancements

Potential additions:
- [ ] GPU acceleration for faster processing
- [ ] Advanced lip-sync analysis (SyncNet integration)
- [ ] Deepfake generation detection (specific model fingerprints)
- [ ] Batch processing support
- [ ] Confidence calibration
- [ ] User feedback loop for model improvement

---

## Summary

Veritas Swarm combines:
- **5 specialized LLMs** for diverse reasoning
- **10 analysis tools** for comprehensive detection
- **4 detection categories** (biometric, physics, signal, audio)
- **Real-time streaming** for transparency
- **Structured output** for actionability

**Result**: A powerful, explainable, and accessible deepfake detection system.
