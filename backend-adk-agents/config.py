"""
Veritas Swarm — Multi-LLM Configuration
5 specialized models via NVIDIA API for different agent roles.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
if not NVIDIA_API_KEY:
    raise EnvironmentError(
        "NVIDIA_API_KEY is not set. "
        "Create a .env file from .env.example and add your key."
    )

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

# Set OPENAI env vars to NVIDIA credentials to ensure LiteLLM/CrewAI 
# uses them correctly even if it ignores the ChatOpenAI object attributes.
os.environ["OPENAI_API_KEY"] = NVIDIA_API_KEY
os.environ["OPENAI_API_BASE"] = NVIDIA_BASE_URL

# ── Chief Justice: Advanced reasoning model ────────────────────────────────
kimi_k2_thinking = ChatOpenAI(
    model="openai/moonshotai/kimi-k2.5",
    api_key=NVIDIA_API_KEY,
    base_url=NVIDIA_BASE_URL,
    temperature=0.1,
)

# ── Biometric Specialist: Multimodal vision model ──────────────────────────
phi_4_multimodal = ChatOpenAI(
    model="openai/microsoft/phi-4-multimodal-instruct",
    api_key=NVIDIA_API_KEY,
    base_url=NVIDIA_BASE_URL,
    temperature=0.2,
)

# ── Physics Analyst: Advanced reasoning model ──────────────────────────────
deepseek_v3 = ChatOpenAI(
    model="openai/deepseek-ai/deepseek-v3.2",
    api_key=NVIDIA_API_KEY,
    base_url=NVIDIA_BASE_URL,
    temperature=0.2,
)

# ── Signal Expert: Code-optimized reasoning model ──────────────────────────
qwen3_coder = ChatOpenAI(
    model="openai/qwen/qwen2.5-coder-32b-instruct",
    api_key=NVIDIA_API_KEY,
    base_url=NVIDIA_BASE_URL,
    temperature=0.2,
)

# ── Audio Sync Expert: General reasoning model ─────────────────────────────
llama_3_3_70b = ChatOpenAI(
    model="openai/meta/llama-3.3-70b-instruct",
    api_key=NVIDIA_API_KEY,
    base_url=NVIDIA_BASE_URL,
    temperature=0.2,
)
