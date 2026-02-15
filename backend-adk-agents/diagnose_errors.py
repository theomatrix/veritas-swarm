"""
Quick test to identify all errors in the backend
"""

import sys
import os

print("=" * 70)
print("BACKEND ERROR DIAGNOSTIC")
print("=" * 70)

# Test 1: Import all modules
print("\n1. Testing module imports...")
try:
    from config import (
        kimi_k2_thinking,
        phi_4_multimodal,
        deepseek_v3,
        qwen3_coder,
        llama_3_3_70b
    )
    print("✓ Config module loaded successfully")
    print(f"  - Chief Justice LLM: {kimi_k2_thinking.model}")
    print(f"  - Biometric LLM: {phi_4_multimodal.model}")
    print(f"  - Physics LLM: {deepseek_v3.model}")
    print(f"  - Signal LLM: {qwen3_coder.model}")
    print(f"  - Audio Sync LLM: {llama_3_3_70b.model}")
except Exception as e:
    print(f"✗ Config import failed: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Import tools
print("\n2. Testing tool imports...")
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
        calculate_av_offset
    )
    print("✓ All 10 tools imported successfully")
except Exception as e:
    print(f"✗ Tool import failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Import agents
print("\n3. Testing agent creation...")
try:
    from agents import create_agents
    agents = create_agents()
    print(f"✓ All {len(agents)} agents created successfully")
    for name, agent in agents.items():
        print(f"  - {name}: {agent.role}")
except Exception as e:
    print(f"✗ Agent creation failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Import crew
print("\n4. Testing crew import...")
try:
    from crew import VeritasCrew
    print("✓ VeritasCrew imported successfully")
except Exception as e:
    print(f"✗ Crew import failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)
