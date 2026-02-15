"""
Veritas Swarm — Analysis Tools Package
Specialized deepfake detection tools for each agent.
"""

from .biometric_tools import (
    analyze_facial_landmarks,
    detect_blink_anomalies,
    detect_face_blending,
)
from .physics_tools import (
    analyze_head_pose_3d,
    detect_lighting_inconsistencies,
)
from .signal_tools import (
    analyze_frequency_domain,
    detect_gan_fingerprints,
)
from .audio_sync_tools import (
    extract_audio_track,
    analyze_lip_sync,
    calculate_av_offset,
)

__all__ = [
    # Biometric tools
    "analyze_facial_landmarks",
    "detect_blink_anomalies",
    "detect_face_blending",
    # Physics tools
    "analyze_head_pose_3d",
    "detect_lighting_inconsistencies",
    # Signal tools
    "analyze_frequency_domain",
    "detect_gan_fingerprints",
    # Audio sync tools
    "extract_audio_track",
    "analyze_lip_sync",
    "calculate_av_offset",
]
