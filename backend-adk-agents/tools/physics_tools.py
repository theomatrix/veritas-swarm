"""
Physics Analysis Tools — Spatial & Lighting Validation
Detects lighting inconsistencies and physically impossible head movements.
"""

import cv2
import numpy as np
import os
from crewai.tools import tool
from typing import Dict, Any


def is_image_file(file_path: str) -> bool:
    """Check if file is an image based on extension."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    return os.path.splitext(file_path.lower())[1] in image_extensions


# Use OpenCV for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')



@tool("Analyze Head Pose 3D")
def analyze_head_pose_3d(file_path: str) -> Dict[str, Any]:
    """
    Tracks face position changes using OpenCV. For images, returns static analysis.
    For videos, analyzes movement patterns.
    
    Args:
        file_path: Path to the image or video file to analyze
        
    Returns:
        Dictionary with head movement analysis
    """
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Handle image files
    if is_image_file(file_path):
        frame = cv2.imread(file_path)
        if frame is None:
            return {'status': 'ERROR', 'details': 'Failed to load image file'}
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        return {
            'file_type': 'image',
            'status': 'N/A',
            'details': 'Head pose tracking requires video input. Static images cannot be analyzed for movement patterns.'
        }
    
    # Handle video files
    cap = cv2.VideoCapture(file_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    face_positions = []
    sudden_movements = 0
    
    frame_count = 0
    prev_center = None
    
    while cap.isOpened() and frame_count < 300:
        ret, frame = cap.read()
        if not ret:
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            (x, y, w, h) = faces[0]  # Use first face
            center_x = x + w // 2
            center_y = y + h // 2
            
            face_positions.append({
                'frame': frame_count,
                'center_x': center_x,
                'center_y': center_y,
                'width': w,
                'height': h
            })
            
            # Detect sudden movements (>100 pixels per frame)
            if prev_center is not None:
                distance = np.sqrt((center_x - prev_center[0])**2 + (center_y - prev_center[1])**2)
                if distance > 100:
                    sudden_movements += 1
            
            prev_center = (center_x, center_y)
        
        frame_count += 1
    
    cap.release()
    
    # Calculate movement statistics
    if len(face_positions) > 1:
        x_positions = [p['center_x'] for p in face_positions]
        y_positions = [p['center_y'] for p in face_positions]
        
        x_range = max(x_positions) - min(x_positions)
        y_range = max(y_positions) - min(y_positions)
    else:
        x_range = y_range = 0
    
    is_anomalous = sudden_movements > 5 or x_range > 500 or y_range > 500
    
    return {
        'frames_analyzed': frame_count,
        'faces_tracked': len(face_positions),
        'sudden_movements_detected': sudden_movements,
        'horizontal_movement_range': round(x_range, 2),
        'vertical_movement_range': round(y_range, 2),
        'anomaly_detected': is_anomalous,
        'anomaly_score': round(min(sudden_movements / 10, 1.0), 3),
        'status': 'SUSPICIOUS' if is_anomalous else 'NORMAL',
        'details': f"Detected {sudden_movements} sudden head movements. {'Unnatural movement patterns suggest synthetic manipulation' if is_anomalous else 'Head movements appear natural'}."
    }



@tool("Detect Lighting Inconsistencies")
def detect_lighting_inconsistencies(file_path: str) -> Dict[str, Any]:
    """
    Analyzes shadow direction and lighting consistency between face and background.
    Detects when face lighting doesn't match environmental lighting. Works on both images and videos.
    
    Args:
        file_path: Path to the image or video file to analyze
        
    Returns:
        Dictionary with lighting consistency analysis
    """
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Handle image files
    if is_image_file(file_path):
        frame = cv2.imread(file_path)
        if frame is None:
            return {'status': 'ERROR', 'details': 'Failed to load image file'}
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            face_region = frame[y:y+h, x:x+w]
            frame_h = frame.shape[0]
            bg_top = frame[0:frame_h//4, :]
            bg_bottom = frame[3*frame_h//4:frame_h, :]
            
            if face_region.size > 0 and bg_top.size > 0:
                face_brightness = np.mean(cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY))
                bg_top_brightness = np.mean(cv2.cvtColor(bg_top, cv2.COLOR_BGR2GRAY))
                bg_bottom_brightness = np.mean(cv2.cvtColor(bg_bottom, cv2.COLOR_BGR2GRAY))
                avg_bg_brightness = (bg_top_brightness + bg_bottom_brightness) / 2
                brightness_diff = abs(face_brightness - avg_bg_brightness)
                is_suspicious = brightness_diff > 50
                
                return {
                    'file_type': 'image',
                    'brightness_difference': round(brightness_diff, 2),
                    'anomaly_score': round(min(brightness_diff / 50, 1.0), 3),
                    'lighting_mismatch_detected': is_suspicious,
                    'status': 'SUSPICIOUS' if is_suspicious else 'NORMAL',
                    'details': f"Brightness difference: {brightness_diff:.2f}. {'Face lighting does not match environmental lighting' if is_suspicious else 'Lighting appears consistent'}."
                }
        return {'file_type': 'image', 'status': 'N/A', 'details': 'No face detected in image'}
    
    # Handle video files
    cap = cv2.VideoCapture(file_path)
    
    lighting_inconsistencies = 0
    frames_analyzed = 0
    
    while cap.isOpened() and frames_analyzed < 100:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frames_analyzed % 10 == 0:  # Every 10th frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                (x, y, w, h) = faces[0]  # Use first face
                
                # Extract face region
                face_region = frame[y:y+h, x:x+w]
                
                # Extract background regions (top and bottom strips)
                frame_h = frame.shape[0]
                bg_top = frame[0:frame_h//4, :]
                bg_bottom = frame[3*frame_h//4:frame_h, :]
                
                if face_region.size > 0 and bg_top.size > 0:
                    # Calculate average brightness
                    face_brightness = np.mean(cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY))
                    bg_top_brightness = np.mean(cv2.cvtColor(bg_top, cv2.COLOR_BGR2GRAY))
                    bg_bottom_brightness = np.mean(cv2.cvtColor(bg_bottom, cv2.COLOR_BGR2GRAY))
                    
                    avg_bg_brightness = (bg_top_brightness + bg_bottom_brightness) / 2
                    
                    # Check if face brightness is inconsistent with background
                    brightness_diff = abs(face_brightness - avg_bg_brightness)
                    
                    # Threshold: >50 brightness units difference is suspicious
                    if brightness_diff > 50:
                        lighting_inconsistencies += 1
        
        frames_analyzed += 1
    
    cap.release()
    
    inconsistency_rate = lighting_inconsistencies / (frames_analyzed // 10) if frames_analyzed > 0 else 0
    is_suspicious = inconsistency_rate > 0.3
    
    return {
        'frames_analyzed': frames_analyzed // 10,
        'lighting_inconsistencies_detected': lighting_inconsistencies,
        'inconsistency_rate': round(inconsistency_rate, 3),
        'anomaly_score': round(min(inconsistency_rate / 0.3, 1.0), 3),
        'lighting_mismatch_detected': is_suspicious,
        'status': 'SUSPICIOUS' if is_suspicious else 'NORMAL',
        'details': f"Lighting inconsistencies found in {inconsistency_rate*100:.1f}% of frames. {'Face lighting does not match environmental lighting' if is_suspicious else 'Lighting appears consistent'}."
    }

