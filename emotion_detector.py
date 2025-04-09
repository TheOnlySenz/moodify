"""
Emotion Detector Module
Uses OpenCV to detect faces and basic emotion cues from webcam input.
"""

import cv2
import numpy as np
import random
import time

class EmotionDetector:
    def __init__(self, camera_index=0):
        """
        Initialize the emotion detector with camera feed
        
        Args:
            camera_index (int): Index of the camera to use (default: 0 for built-in webcam)
        """
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise ValueError("Could not open camera. Please check your webcam connection.")
        
        # Load the face cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Mapping of emotions to display colors (BGR format)
        self.emotion_colors = {
            'happy': (0, 255, 255),     # Yellow
            'sad': (255, 0, 0),         # Blue
            'angry': (0, 0, 255),       # Red
            'neutral': (255, 255, 255), # White
            'surprise': (0, 165, 255)   # Orange
        }
        
        # Available emotions
        self.emotions = list(self.emotion_colors.keys())
        
        # For the simplified version, we'll use time-based emotion changes
        self.last_emotion_time = time.time()
        self.emotion_change_interval = 15  # seconds
        self.current_emotion = 'neutral'
        
        # Print initialization message
        print("Emotion detector initialized. Accessing camera feed...")
    
    def detect_emotion(self):
        """
        Capture a frame from the webcam and simulate emotion detection
        
        Returns:
            tuple: (frame, emotion) - The captured frame and the simulated emotion
        """
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture frame from camera")
            return None, None
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # For demo purposes, change the emotion every few seconds
        current_time = time.time()
        if current_time - self.last_emotion_time > self.emotion_change_interval:
            self.current_emotion = random.choice(self.emotions)
            self.last_emotion_time = current_time
            print(f"Emotion changed to: {self.current_emotion}")
        
        # If at least one face is detected
        if len(faces) > 0:
            # Use the largest face for visualization
            largest_face = max(faces, key=lambda face: face[2] * face[3])
            x, y, w, h = largest_face
            
            # Draw a rectangle around the face
            color = self.emotion_colors.get(self.current_emotion, (255, 255, 255))
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            return frame, self.current_emotion
        
        return frame, None
    
    def display_emotion(self, frame, emotion):
        """
        Display the detected emotion text on the frame
        
        Args:
            frame: The frame to display the emotion on
            emotion (str): The detected emotion
        """
        if frame is not None and emotion is not None:
            # Display the emotion text
            color = self.emotion_colors.get(emotion, (255, 255, 255))
            cv2.putText(frame, f"Emotion: {emotion}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    
    def show_frame(self, frame):
        """
        Display the frame
        
        Args:
            frame: The frame to display
        """
        if frame is not None:
            cv2.imshow('Emotion-Based Music Player', frame)
    
    def should_quit(self):
        """
        Check if the user wants to quit the application
        
        Returns:
            bool: True if the user pressed 'q', False otherwise
        """
        return cv2.waitKey(1) & 0xFF == ord('q')
    
    def release(self):
        """
        Release the camera and close all windows
        """
        self.cap.release()
        cv2.destroyAllWindows()
        print("Camera released and windows closed")
