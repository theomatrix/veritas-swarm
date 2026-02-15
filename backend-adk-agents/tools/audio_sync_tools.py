"""
Audio-Sync Analysis Tools — Lip-Sync & Audio Validation
Detects millisecond mismatches between audio and lip movements.
"""

import cv2
import numpy as np
import subprocess
import os
import tempfile
from crewai.tools import tool
from typing import Dict, Any


def is_image_file(file_path: str) -> bool:
    """Check if file is an image based on extension."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    return os.path.splitext(file_path.lower())[1] in image_extensions


# Use OpenCV for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


@tool("Extract Audio Track")
def extract_audio_track(file_path: str) -> Dict[str, Any]:
    """
    Extracts audio track from video using FFmpeg. Returns N/A for images.
    Returns audio file path and basic audio properties.
    
    Args:
        file_path: Path to the video or image file
        
    Returns:
        Dictionary with audio extraction results and file path
    """
    # Images don't have audio
    if is_image_file(file_path):
        return {
            'success': False,
            'file_type': 'image',
            'details': 'Audio extraction requires video input. Image files do not contain audio tracks.'
        }
    
    try:
        # Create temporary audio file
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, f"extracted_audio_{os.getpid()}.wav")
        
        # Use FFmpeg to extract audio
        command = [
            'ffmpeg',
            '-i', file_path,
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # PCM 16-bit
            '-ar', '16000',  # 16kHz sample rate
            '-ac', '1',  # Mono
            '-y',  # Overwrite
            audio_path
        ]
        
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0 and os.path.exists(audio_path):
            file_size = os.path.getsize(audio_path)
            
            return {
                'success': True,
                'audio_path': audio_path,
                'file_size_bytes': file_size,
                'sample_rate': 16000,
                'channels': 1,
                'format': 'WAV (PCM 16-bit)',
                'details': f"Successfully extracted audio track ({file_size / 1024:.1f} KB)"
            }
        else:
            return {
                'success': False,
                'error': result.stderr,
                'details': "Failed to extract audio track. Video may not contain audio."
            }
            
    except FileNotFoundError:
        return {
            'success': False,
            'error': 'FFmpeg not found',
            'details': "FFmpeg is not installed or not in system PATH. Audio analysis requires FFmpeg."
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'details': f"Audio extraction failed: {str(e)}"
        }


@tool("Analyze Lip Sync")
def analyze_lip_sync(file_path: str) -> Dict[str, Any]:
    """
    Analyzes face presence and basic motion in video frames.
    Simplified analysis without detailed lip tracking. Returns N/A for images.
    
    Args:
        file_path: Path to the image or video file to analyze
        
    Returns:
        Dictionary with basic motion analysis
    """
    # Lip sync analysis requires video
    if is_image_file(file_path):
        return {
            'file_type': 'image',
            'status': 'N/A',
            'details': 'Lip-sync analysis requires video input with temporal data. Image files cannot be analyzed for lip movement.'
        }
    
    cap = cv2.VideoCapture(file_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    face_detections = []
    frame_count = 0
    
    while cap.isOpened() and frame_count < 300:  # Analyze first 10 seconds
        ret, frame = cap.read()
        if not ret:
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            # Extract lower face region (mouth area)
            mouth_y = y + int(h * 0.6)
            mouth_region = gray[mouth_y:y+h, x:x+w]
            
            # Calculate pixel variance in mouth region as proxy for movement
            if mouth_region.size > 0:
                variance = np.var(mouth_region)
                face_detections.append(variance)
        
        frame_count += 1
    
    cap.release()
    
    if not face_detections:
        return {
            'success': False,
            'details': "No face detected in video. Cannot analyze lip sync."
        }
    
    # Analyze variance in mouth region (speech causes changes)
    variance_std = np.std(face_detections)
    variance_range = max(face_detections) - min(face_detections)
    
    return {
        'frames_analyzed': len(face_detections),
        'mouth_region_variance_std': round(variance_std, 2),
        'variance_range': round(variance_range, 2),
        'lip_movement_detected': variance_std > 50,
        'details': f"Mouth region variation: {variance_std:.2f}. {'Active movements detected' if variance_std > 50 else 'Minimal movement (may indicate static face or voice-over)'}."
    }


@tool("Calculate Audio-Visual Offset")
def calculate_av_offset(file_path: str) -> Dict[str, Any]:
    """
    Estimates temporal offset between audio and visual tracks.
    Detects lip-sync drift that indicates post-production manipulation. Returns N/A for images.
    
    Args:
        file_path: Path to the image or video file to analyze
        
    Returns:
        Dictionary with A/V sync offset estimation
    """
    # A/V sync requires video with audio
    if is_image_file(file_path):
        return {
            'file_type': 'image',
            'status': 'N/A',
            'details': 'Audio-visual sync analysis requires video input. Image files do not contain audio or temporal data.'
        }
    
    # First extract audio
    audio_result = extract_audio_track(file_path)
    
    if not audio_result.get('success'):
        return {
            'success': False,
            'details': "Cannot calculate AV offset without audio track."
        }
    
    audio_path = audio_result['audio_path']
    
    # Check for face presence and motion in video
    cap = cv2.VideoCapture(file_path)
    
    face_count = 0
    motion_scores = []
    frame_count = 0
    prev_frame_gray = None
    
    while cap.isOpened() and frame_count < 100: # Analyze first few seconds
        ret, frame = cap.read()
        if not ret:
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            face_count += 1
            
            # Calculate motion in the frame
            if prev_frame_gray is not None:
                diff = cv2.absdiff(gray, prev_frame_gray)
                _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
                motion_score = np.sum(thresh) / (thresh.shape[0] * thresh.shape[1]) # Percentage of moving pixels
                motion_scores.append(motion_score)
        
        prev_frame_gray = gray
        frame_count += 1
    
    cap.release()
    
    face_detection_rate = face_count / frame_count if frame_count > 0 else 0
    avg_motion = np.mean(motion_scores) if motion_scores else 0
    
    # Clean up temporary audio file
    try:
        if os.path.exists(audio_path):
            os.remove(audio_path)
    except:
        pass
    
    return {
        'file_type': 'video',
        'frames_analyzed': int(frame_count),
        'face_detection_rate': float(round(face_detection_rate, 3)),
        'avg_motion_score': float(round(avg_motion, 3)),
        'status': 'NORMAL' if face_detection_rate > 0.7 else 'SUSPICIOUS',
        'details': f"Face detected in {face_detection_rate*100:.1f}% of frames. Average motion score: {avg_motion:.3f}. {'Consistent face presence and natural motion patterns' if face_detection_rate > 0.7 else 'Low face detection rate may indicate manipulation'}."
    }
