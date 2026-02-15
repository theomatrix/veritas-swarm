"""
Signal Analysis Tools — Frequency & GAN Noise Detection
Detects invisible AI generation fingerprints using frequency domain analysis.
"""

import cv2
import numpy as np
import os
from scipy import fft
from crewai.tools import tool
from typing import Dict, Any


def is_image_file(file_path: str) -> bool:
    """Check if file is an image based on extension."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    return os.path.splitext(file_path.lower())[1] in image_extensions


@tool("Analyze Frequency Domain")
def analyze_frequency_domain(file_path: str) -> Dict[str, Any]:
    """
    Uses FFT to convert frames to frequency domain and detect high-frequency noise patterns.
    AI-generated images leave specific frequency signatures invisible to the human eye.
    Works on both images and videos.
    
    Args:
        file_path: Path to the image or video file to analyze
        
    Returns:
        Dictionary with frequency domain analysis and GAN fingerprint detection
    """
    is_image = is_image_file(file_path)
    cap = cv2.VideoCapture(file_path)
    
    high_freq_anomalies = []
    frames_analyzed = 0
    
    while cap.isOpened() and frames_analyzed < 50:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frames_analyzed % 10 == 0:  # Every 10th frame
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply 2D FFT
            f_transform = fft.fft2(gray)
            f_shift = fft.fftshift(f_transform)
            
            # Calculate magnitude spectrum
            magnitude_spectrum = np.abs(f_shift)
            
            # Analyze high-frequency components
            h, w = magnitude_spectrum.shape
            center_y, center_x = h // 2, w // 2
            
            # Create mask for high-frequency region (outer 40%)
            y, x = np.ogrid[:h, :w]
            mask = ((x - center_x)**2 + (y - center_y)**2) > (min(h, w) * 0.3)**2
            
            # Calculate high-frequency energy
            high_freq_energy = np.sum(magnitude_spectrum[mask])
            total_energy = np.sum(magnitude_spectrum)
            
            high_freq_ratio = high_freq_energy / total_energy if total_energy > 0 else 0
            
            high_freq_anomalies.append(high_freq_ratio)
        
        frames_analyzed += 1
    
    cap.release()
    
    avg_high_freq_ratio = np.mean(high_freq_anomalies) if high_freq_anomalies else 0
    std_high_freq_ratio = np.std(high_freq_anomalies) if high_freq_anomalies else 0
    
    # GAN-generated images typically have higher high-frequency content
    # Natural images: 0.05-0.15, GAN images: 0.20-0.40
    is_suspicious = avg_high_freq_ratio > 0.20
    
    return {
        'file_type': 'image' if is_image else 'video',
        'frames_analyzed': int(len(high_freq_anomalies)),
        'avg_high_frequency_ratio': float(round(avg_high_freq_ratio, 4)),
        'std_high_frequency_ratio': float(round(std_high_freq_ratio, 4)),
        'normal_range': '0.05-0.15',
        'anomaly_score': float(round(min(avg_high_freq_ratio / 0.20, 1.0), 3)),
        'gan_fingerprint_detected': bool(is_suspicious),
        'status': 'SUSPICIOUS' if is_suspicious else 'NORMAL',
        'details': f"High-frequency energy ratio: {avg_high_freq_ratio:.4f}. {'Elevated high-frequency content suggests GAN-generated imagery' if is_suspicious else 'Frequency spectrum appears natural'}."
    }


@tool("Detect GAN Fingerprints")
def detect_gan_fingerprints(file_path: str) -> Dict[str, Any]:
    """
    Detects repeating grid patterns characteristic of GAN upsampling layers.
    GANs often leave checkerboard artifacts in the frequency domain.
    Works on both images and videos.
    
    Args:
        file_path: Path to the image or video file to analyze
        
    Returns:
        Dictionary with GAN-specific pattern detection results
    """
    is_image = is_image_file(file_path)
    cap = cv2.VideoCapture(file_path)
    
    checkerboard_scores = []
    frames_analyzed = 0
    
    while cap.isOpened() and frames_analyzed < 50:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frames_analyzed % 10 == 0:  # Every 10th frame
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Resize to standard size for consistent analysis
            gray = cv2.resize(gray, (512, 512))
            
            # Apply 2D FFT
            f_transform = fft.fft2(gray)
            f_shift = fft.fftshift(f_transform)
            magnitude_spectrum = np.abs(f_shift)
            
            # Log scale for better visualization
            magnitude_spectrum = np.log(magnitude_spectrum + 1)
            
            # Detect checkerboard pattern (peaks at specific frequencies)
            h, w = magnitude_spectrum.shape
            center_y, center_x = h // 2, w // 2
            
            # Check for peaks at quarter frequencies (characteristic of 2x upsampling)
            quarter_freq_positions = [
                (center_y + h//4, center_x),
                (center_y - h//4, center_x),
                (center_y, center_x + w//4),
                (center_y, center_x - w//4),
            ]
            
            # Sample magnitude at these positions
            quarter_freq_values = []
            for y, x in quarter_freq_positions:
                if 0 <= y < h and 0 <= x < w:
                    # Average in small neighborhood
                    neighborhood = magnitude_spectrum[max(0, y-2):min(h, y+3), max(0, x-2):min(w, x+3)]
                    quarter_freq_values.append(np.mean(neighborhood))
            
            avg_quarter_freq = np.mean(quarter_freq_values) if quarter_freq_values else 0
            
            # Compare to overall average
            overall_avg = np.mean(magnitude_spectrum)
            
            # Ratio > 1.5 indicates strong peaks at quarter frequencies
            checkerboard_ratio = avg_quarter_freq / overall_avg if overall_avg > 0 else 0
            checkerboard_scores.append(checkerboard_ratio)
        
        frames_analyzed += 1
    
    cap.release()
    
    avg_checkerboard_score = np.mean(checkerboard_scores) if checkerboard_scores else 0
    
    # Threshold: ratio > 1.3 is suspicious
    is_suspicious = avg_checkerboard_score > 1.3
    
    return {
        'file_type': 'image' if is_image else 'video',
        'frames_analyzed': int(len(checkerboard_scores)),
        'avg_checkerboard_score': float(round(avg_checkerboard_score, 3)),
        'threshold': 1.3,
        'anomaly_score': float(round(min(avg_checkerboard_score / 1.3, 1.0), 3)),
        'gan_upsampling_artifacts_detected': bool(is_suspicious),
        'status': 'SUSPICIOUS' if is_suspicious else 'NORMAL',
        'details': f"Checkerboard artifact score: {avg_checkerboard_score:.3f}. {'Strong frequency peaks at quarter-wavelengths indicate GAN upsampling artifacts' if is_suspicious else 'No GAN-specific frequency patterns detected'}."
    }
