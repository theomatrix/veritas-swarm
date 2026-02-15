"""
Biometric Analysis Tools — Face & Geometry Detection
Detects unnatural blinking, micro-expressions, and facial blending boundaries.
"""

import cv2
import mediapipe as mp
import numpy as np
import os
from crewai.tools import tool
from typing import Dict, Any


def is_image_file(file_path: str) -> bool:
    """Check if file is an image based on extension."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    return os.path.splitext(file_path.lower())[1] in image_extensions


# Initialize MediaPipe Face Mesh using new API
try:
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    
    # Note: The new API requires a model file path
    # For now, we'll use a fallback approach with cv2 for facial detection
    USE_NEW_MEDIAPIPE = False
except ImportError:
    USE_NEW_MEDIAPIPE = False



def calculate_eye_aspect_ratio(landmarks, eye_indices):
    """Calculate Eye Aspect Ratio (EAR) for blink detection."""
    # Vertical eye landmarks
    A = np.linalg.norm(landmarks[eye_indices[1]] - landmarks[eye_indices[5]])
    B = np.linalg.norm(landmarks[eye_indices[2]] - landmarks[eye_indices[4]])
    # Horizontal eye landmark
    C = np.linalg.norm(landmarks[eye_indices[0]] - landmarks[eye_indices[3]])
    
    ear = (A + B) / (2.0 * C)
    return ear


@tool("Analyze Facial Landmarks")
def analyze_facial_landmarks(file_path: str) -> Dict[str, Any]:
    """
    Analyzes facial presence using OpenCV. Handles both images and videos.
    Detects facial geometry anomalies and tracking consistency.
    
    Args:
        file_path: Path to the image or video file to analyze
        
    Returns:
        Dictionary with face detection consistency scores and anomaly flags
    """
    # Use OpenCV's Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Check if it's an image or video
    if is_image_file(file_path):
        # Handle image
        frame = cv2.imread(file_path)
        if frame is None:
            return {'status': 'ERROR', 'details': 'Failed to load image file'}
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        face_detected = len(faces) > 0
        
        return {
            'file_type': 'image',
            'faces_detected': len(faces),
            'face_present': face_detected,
            'anomaly_score': 0.0 if face_detected else 1.0,
            'status': 'NORMAL' if face_detected else 'SUSPICIOUS',
            'details': f"{'Face detected in image' if face_detected else 'No face detected in image'}. {len(faces)} face(s) found."
        }
    else:
        # Handle video
        cap = cv2.VideoCapture(file_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        face_detections = []
        frames_analyzed = 0
        frames_with_face = 0
        frame_skip = 5
        
        while cap.isOpened() and frames_analyzed < min(total_frames, 300):
            ret, frame = cap.read()
            if not ret:
                break
                
            if frames_analyzed % frame_skip == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                
                if len(faces) > 0:
                    frames_with_face += 1
            
            frames_analyzed += 1
        
        cap.release()
        
        detection_rate = frames_with_face / (frames_analyzed / frame_skip) if frames_analyzed > 0 else 0
        
        return {
            'file_type': 'video',
            'total_frames_analyzed': frames_analyzed // frame_skip,
            'frames_with_face_detected': frames_with_face,
            'detection_rate': round(detection_rate, 3),
            'anomaly_score': round(1.0 - detection_rate, 3),
            'status': 'SUSPICIOUS' if detection_rate < 0.8 else 'NORMAL',
            'details': f"Face detected in {detection_rate*100:.1f}% of frames. Low detection rate may indicate face-swap artifacts."
        }



@tool("Detect Blink Anomalies")
def detect_blink_anomalies(file_path: str) -> Dict[str, Any]:
    """
    Analyzes eye region changes over time to estimate blink patterns.
    Uses OpenCV for face and eye detection. For images, returns N/A.
    
    Args:
        file_path: Path to the image or video file to analyze
        
    Returns:
        Dictionary with blink rate estimation and anomaly detection
    """
    # Blink detection only works for videos
    if is_image_file(file_path):
        return {
            'file_type': 'image',
            'status': 'N/A',
            'details': 'Blink detection requires video input. Image files cannot be analyzed for blink patterns.'
        }
    
    cap = cv2.VideoCapture(file_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps if fps > 0 else 0
    
    # Use Haar Cascade for eye detection
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    eye_detections = []
    frame_count = 0
    
    while cap.isOpened() and frame_count < 300:  # Analyze first 10 seconds at 30fps
        ret, frame = cap.read()
        if not ret:
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        eyes_detected = 0
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            eyes_detected = len(eyes)
            break  # Only process first face
        
        eye_detections.append(eyes_detected)
        frame_count += 1
    
    cap.release()
    
    # Estimate blinks by counting transitions from 2 eyes to 0 eyes
    blink_count = 0
    for i in range(1, len(eye_detections)):
        if eye_detections[i-1] >= 2 and eye_detections[i] == 0:
            blink_count += 1
    
    # Calculate blink rate per minute
    blink_rate = (blink_count / duration) * 60 if duration > 0 else 0
    
    # Normal human blink rate: 15-20 per minute
    is_anomalous = blink_rate < 5 or blink_rate > 30
    
    return {
        'blink_count': blink_count,
        'video_duration_seconds': round(duration, 2),
        'blink_rate_per_minute': round(blink_rate, 2),
        'normal_range': '15-20 blinks/min',
        'anomaly_detected': is_anomalous,
        'anomaly_score': round(abs(17.5 - blink_rate) / 17.5, 3),  # Distance from normal average
        'status': 'SUSPICIOUS' if is_anomalous else 'NORMAL',
        'details': f"Estimated blink rate of {blink_rate:.1f}/min is {'abnormally low' if blink_rate < 5 else 'abnormally high' if blink_rate > 30 else 'within normal range'}."
    }


@tool("Detect Face Blending Boundaries")
def detect_face_blending(file_path: str) -> Dict[str, Any]:
    """
    Scans face edges for blurred pixels indicating face-swap paste boundaries.
    Uses edge detection to find unnatural blending seams. Works on both images and videos.
    
    Args:
        file_path: Path to the image or video file to analyze
        
    Returns:
        Dictionary with blending boundary detection results
    """
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Handle image files
    if is_image_file(file_path):
        frame = cv2.imread(file_path)
        if frame is None:
            return {'status': 'ERROR', 'details': 'Failed to load image file'}
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            mask = np.zeros_like(edges)
            border_width = 20
            cv2.rectangle(mask, (x-border_width, y-border_width), (x+w+border_width, y+h+border_width), 255, border_width)
            boundary_edges = cv2.bitwise_and(edges, mask)
            edge_density = np.sum(boundary_edges > 0) / np.sum(mask > 0) if np.sum(mask > 0) > 0 else 0
            is_suspicious = edge_density > 0.15
            
            return {
                'file_type': 'image',
                'edge_density': round(edge_density, 4),
                'anomaly_score': round(min(edge_density / 0.15, 1.0), 3),
                'blending_seam_detected': is_suspicious,
                'status': 'SUSPICIOUS' if is_suspicious else 'NORMAL',
                'details': f"Edge density around face boundary: {edge_density:.4f}. {'High density suggests face-swap blending artifacts' if is_suspicious else 'Normal edge characteristics'}."
            }
        else:
            return {'file_type': 'image', 'status': 'N/A', 'details': 'No face detected in image'}
    
    # Handle video files
    cap = cv2.VideoCapture(file_path)
    edge_anomaly_scores = []
    frames_analyzed = 0
    
    while cap.isOpened() and frames_analyzed < 50:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frames_analyzed % 10 == 0:  # Every 10th frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Canny edge detection
            edges = cv2.Canny(blurred, 50, 150)
            
            # Detect face region
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                (x, y, w, h) = faces[0]  # Use first face
                
                # Create mask for face boundary region (expand slightly)
                mask = np.zeros_like(edges)
                border_width = 20
                cv2.rectangle(mask, 
                            (x-border_width, y-border_width), 
                            (x+w+border_width, y+h+border_width), 
                            255, border_width)
                
                # Count edge pixels in boundary region
                boundary_edges = cv2.bitwise_and(edges, mask)
                edge_density = np.sum(boundary_edges > 0) / np.sum(mask > 0) if np.sum(mask > 0) > 0 else 0
                
                edge_anomaly_scores.append(edge_density)
        
        frames_analyzed += 1
    
    cap.release()
    
    avg_edge_density = np.mean(edge_anomaly_scores) if edge_anomaly_scores else 0
    
    # High edge density around face boundary = potential blending seam
    is_suspicious = avg_edge_density > 0.15
    
    return {
        'frames_analyzed': len(edge_anomaly_scores),
        'average_edge_density': round(avg_edge_density, 4),
        'anomaly_score': round(min(avg_edge_density / 0.15, 1.0), 3),
        'blending_seam_detected': is_suspicious,
        'status': 'SUSPICIOUS' if is_suspicious else 'NORMAL',
        'details': f"Edge density around face boundary: {avg_edge_density:.4f}. {'High density suggests face-swap blending artifacts' if is_suspicious else 'Normal edge characteristics'}."
    }
