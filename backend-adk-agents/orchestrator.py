"""
Orchestrator — Intelligent Agent Routing
Routes agents based on file type to optimize analysis and reduce costs.
"""

import os


def is_image_file(file_path: str) -> bool:
    """Check if file is an image based on extension."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    return os.path.splitext(file_path.lower())[1] in image_extensions


def get_agents_for_file(file_path: str, all_agents: dict) -> dict:
    """
    Returns only the agents needed for this file type.
    
    Images: biometric + signal + chief_justice (skip physics + audio)
    Videos: all 5 agents
    
    Args:
        file_path: Path to the media file to analyze
        all_agents: Dictionary of all available agents
        
    Returns:
        Dictionary of agents appropriate for the file type
    """
    if is_image_file(file_path):
        # Images: Skip physics (no 3D motion) and audio (no sound)
        return {
            "biometric_sentinel": all_agents["biometric_sentinel"],
            "signal_analyst": all_agents["signal_analyst"],
            "chief_justice": all_agents["chief_justice"],
        }
    else:
        # Videos: Use all agents
        return all_agents
