"""
Simple test to verify NVIDIA API configuration
"""

import os
import sys

# Test 1: Check environment variable
print("Test 1: Checking NVIDIA_API_KEY...")
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")
if api_key:
    print(f"✓ NVIDIA_API_KEY found (length: {len(api_key)})")
else:
    print("✗ NVIDIA_API_KEY not found")
    sys.exit(1)

# Test 2: Import LLM configurations
print("\nTest 2: Loading LLM configurations...")
try:
    from config import (
        kimi_k2_thinking,
        phi_4_multimodal,
        deepseek_v3,
        qwen3_coder,
        llama_3_3_70b,
    )
    print("✓ All 5 LLM models loaded successfully")
    print(f"  - Chief Justice: {kimi_k2_thinking.model_name}")
    print(f"  - Biometric Specialist: {phi_4_multimodal.model_name}")
    print(f"  - Physics Analyst: {deepseek_v3.model_name}")
    print(f"  - Signal Expert: {qwen3_coder.model_name}")
    print(f"  - Audio Sync Expert: {llama_3_3_70b.model_name}")
except Exception as e:
    print(f"✗ Failed to load LLMs: {e}")
    sys.exit(1)

# Test 3: Import tools
print("\nTest 3: Loading analysis tools...")
try:
    from tools import (
        analyze_facial_landmarks,
        detect_blink_anomalies,
        detect_face_blending,
        analyze_head_pose_3d,
        detect_lighting_inconsistencies,
        analyze_frequency_domain,
        detect_gan_fingerprints,
        extract_audio_track,
        analyze_lip_sync,
        calculate_av_offset,
    )
    print("✓ All 10 analysis tools loaded successfully")
except Exception as e:
    print(f"✗ Failed to load tools: {e}")
    sys.exit(1)

# Test 4: Import agents
print("\nTest 4: Loading agents...")
try:
    from agents import create_agents
    agents = create_agents()
    print(f"✓ All {len(agents)} agents created successfully")
    for name, agent in agents.items():
        tool_count = len(agent.tools) if hasattr(agent, 'tools') and agent.tools else 0
        print(f"  - {name}: {tool_count} tools")
except Exception as e:
    print(f"✗ Failed to create agents: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("✓ ALL TESTS PASSED!")
print("="*50)
