"""
Veritas Swarm — FastAPI Server
POST /api/analyze  →  SSE stream of agent events + final verdict.
GET  /api/health   →  health check.
"""

import asyncio
import json
import os
import tempfile
import threading
import time
import warnings

# Suppress non-critical warnings from LiteLLM
warnings.filterwarnings("ignore", message="Missing dependency.*apscheduler")

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

app = FastAPI(title="Veritas Swarm API")

# ── CORS for Vite dev server ────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Check if we should run in MOCK mode ─────────────────────────────────────
MOCK_MODE = not os.getenv("NVIDIA_API_KEY")

# ── Health check ────────────────────────────────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok", "mock": MOCK_MODE}


# ── Mock data for demo when API credits are exhausted ───────────────────────
MOCK_AGENTS = [
    {
        "name": "Biometric Sentinel",
        "findings": (
            "BIOMETRIC ANALYSIS REPORT\n\n"
            "• Blink Pattern: FAIL — No natural blink reflex detected across "
            "observable frames. Confidence: HIGH\n"
            "• Eye Glints: FAIL — Specular reflections in the left and right "
            "eyes show inconsistent positioning suggesting synthetic generation. "
            "Confidence: HIGH\n"
            "• Skin Micro-Texture: SUSPICIOUS — Pore detail appears artificially "
            "smoothed in the forehead and cheek regions. Confidence: MEDIUM\n"
            "• Pupil Boundaries: PASS — Iris-pupil boundary appears geometrically "
            "consistent. Confidence: LOW"
        ),
    },
    {
        "name": "Physics Inspector",
        "findings": (
            "PHYSICS & LIGHTING REPORT\n\n"
            "• Lighting Direction: FAIL — Primary light source on face appears to "
            "come from upper-left, while background shadows suggest upper-right "
            "illumination. Confidence: HIGH\n"
            "• Shadow Geometry: SUSPICIOUS — Nose shadow angle inconsistent with "
            "claimed light position. Confidence: MEDIUM\n"
            "• Specular Highlights: FAIL — Skin specular highlights show uniform "
            "intensity rather than natural Fresnel falloff. Confidence: HIGH\n"
            "• Color Temperature: PASS — Overall colour temperature is broadly "
            "consistent. Confidence: LOW"
        ),
    },
    {
        "name": "Signal Analyst",
        "findings": (
            "DIGITAL ARTIFACT REPORT\n\n"
            "• Blending Seams: FAIL — Detectable boundary artefact along the "
            "jawline where face region meets original background. Confidence: HIGH\n"
            "• Pixel Noise: SUSPICIOUS — Noise distribution in the face region "
            "differs statistically from the background (variance mismatch). "
            "Confidence: MEDIUM\n"
            "• Compression Ghosts: PASS — No obvious double-quantisation "
            "artefacts detected. Confidence: LOW\n"
            "• Frequency Domain: FAIL — DCT analysis reveals anomalous energy "
            "distribution typical of GAN-generated content. Confidence: HIGH"
        ),
    },
    {
        "name": "Sync Specialist",
        "findings": (
            "AUDIO-VISUAL SYNC REPORT\n\n"
            "• Lip Sync: NOT APPLICABLE — Input is a still image; no video "
            "frames or audio track to analyse.\n"
            "• Speech Cadence: NOT APPLICABLE\n"
            "• Room Acoustics: NOT APPLICABLE\n"
            "• TTS Artefacts: NOT APPLICABLE\n\n"
            "Note: Audio-visual analysis requires video input with an audio "
            "track. This analysis is limited to visual-only indicators."
        ),
    },
]

MOCK_VERDICT = {
    "score": 82,
    "confidence": "HIGH",
    "findings": [
        "Inconsistent lighting direction between face and background (HIGH confidence)",
        "Missing natural blink reflex in observable data (HIGH confidence)",
        "Detectable blending seam along jawline boundary (HIGH confidence)",
        "Anomalous DCT frequency distribution typical of GAN generation (HIGH confidence)",
        "Artificially smoothed skin micro-texture (MEDIUM confidence)",
    ],
    "laymans_brief": (
        "This image shows strong signs of being artificially generated or manipulated. "
        "The most telling sign — the 'Tell' — is that the lighting on the person's "
        "face doesn't match the lighting in the background, like someone cut out a "
        "face from one photo and pasted it onto another taken at a different time of "
        "day. Additionally, we found a visible seam along the jawline where the "
        "swapped face meets the original image, and the skin looks unnaturally smooth "
        "— almost like a video game character rather than a real person. The digital "
        "fingerprint of the image also matches patterns typically left behind by AI "
        "image generators. We rate this as 82/100 likely to be a deepfake."
    ),
    "raw": "",
}


# ── SSE Analyze endpoint ───────────────────────────────────────────────────
@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    """
    Accept a file upload, run the Veritas Swarm (or mock), and
    stream SSE events back to the frontend.
    """

    # Save uploaded file to temp dir
    suffix = os.path.splitext(file.filename or "upload")[1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    content = await file.read()
    tmp.write(content)
    tmp.flush()
    tmp_path = tmp.name
    tmp.close()

    async def event_stream():
        try:
            if MOCK_MODE:
                # ── Mock mode: simulate agent workflow ──────────────────
                for agent in MOCK_AGENTS:
                    yield f"data: {json.dumps({'type': 'agent_start', 'agent': agent['name'], 'status': 'analyzing'})}\n\n"
                    await asyncio.sleep(2.0)
                    yield f"data: {json.dumps({'type': 'agent_complete', 'agent': agent['name'], 'findings': agent['findings']})}\n\n"
                    await asyncio.sleep(0.5)

                yield f"data: {json.dumps({'type': 'master_start', 'status': 'synthesizing'})}\n\n"
                await asyncio.sleep(3.0)
                yield f"data: {json.dumps({'type': 'verdict', **MOCK_VERDICT})}\n\n"
                yield f"data: {json.dumps({'type': 'done'})}\n\n"

            else:
                # ── Real mode: run CrewAI with callbacks ────────────────
                from callbacks import AgentEventBridge
                from crew import VeritasCrew

                bridge = AgentEventBridge()
                crew = VeritasCrew(tmp_path)

                # Run the crew in a background thread
                def _run():
                    try:
                        crew.run(
                            step_callback=bridge.step_callback,
                            task_callback=bridge.task_callback,
                            event_bridge=bridge,
                        )
                    except Exception as e:
                        bridge.push_error(str(e))
                    finally:
                        bridge.push_done()

                thread = threading.Thread(target=_run, daemon=True)
                thread.start()

                # Stream events from the bridge queue
                while True:
                    try:
                        event = bridge.event_queue.get(timeout=0.5)
                        yield f"data: {event}\n\n"
                        parsed = json.loads(event)
                        if parsed.get("type") in ("done", "error"):
                            break
                    except Exception:
                        if not thread.is_alive():
                            break
                        continue

        finally:
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
