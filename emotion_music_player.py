"""
Emotion-Based Music Player - Global Version
This version combines all components into a single file and stores Spotify credentials
within the application to make it portable.
"""

import os
import sys
import time
import random
import cv2
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# --- Configuration ---
# Spotify credentials - can be embedded for global distribution
DEFAULT_CLIENT_ID = "166cc0811c77480e8e7f46adc9e25987"
DEFAULT_CLIENT_SECRET = "85df3a86219440c4ba14e6252f5af295"
DEFAULT_REDIRECT_URI = "http://127.0.0.1:8888/callback"

class EmotionMusicPlayer:
    def __init__(self):
        # Load credentials
        load_dotenv()  # Try to load from .env file first
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID", DEFAULT_CLIENT_ID)
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", DEFAULT_CLIENT_SECRET)
        self.redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", DEFAULT_REDIRECT_URI)

        # Camera and face detection properties
        self.camera_index = 0
        self.cap = None
        self.face_cascade = None
        
        # Emotion properties
        self.current_emotion = "neutral"
        self.last_emotion_time = time.time()
        self.emotion_change_interval = 15  # seconds
        
        # Emotion colors (BGR format)
        self.emotion_colors = {
            'happy': (0, 255, 255),     # Yellow
            'sad': (255, 0, 0),         # Blue
            'angry': (0, 0, 255),       # Red
            'neutral': (255, 255, 255), # White
            'surprise': (0, 165, 255)   # Orange
        }
        
        # Available emotions to cycle through
        self.emotions = list(self.emotion_colors.keys())
        
        # Spotify properties
        self.sp = None
        self.current_playlist = None
        self.device_id = None
        self.demo_mode = False
        
        # Emotion playlists
        self.emotion_playlists = {
            'happy': [
                'spotify:playlist:37i9dQZF1DXdPec7aLTmlC',  # Happy Hits!
                'spotify:playlist:37i9dQZF1DX9XIFQuFvzM4',  # Feelin' Good
                'spotify:playlist:37i9dQZF1DX2sUQwD7tbmL'   # Feel-Good Indie Rock
            ],
            'sad': [
                'spotify:playlist:37i9dQZF1DX7qK8ma5wgG1',  # Sad Hours
                'spotify:playlist:37i9dQZF1DX889U0CL85jj',  # Down in the Dumps
                'spotify:playlist:37i9dQZF1DX3YSRoSdA634'   # Life Sucks
            ],
            'angry': [
                'spotify:playlist:37i9dQZF1DX1tyCD9QhIWF',  # Anger Management
                'spotify:playlist:37i9dQZF1DX4eRPd9frC1m',  # Rock Hard
                'spotify:playlist:37i9dQZF1DWXIcbzpLauPS'   # Adrenaline Workout
            ],
            'neutral': [
                'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',  # Peaceful Piano
                'spotify:playlist:37i9dQZF1DWZeKCadgRdKQ',  # Deep Focus
                'spotify:playlist:37i9dQZF1DWZqd5JICZI0u'   # Instrumental Study
            ],
            'surprise': [
                'spotify:playlist:37i9dQZF1DX5Vy6DFOcx00',  # Dance Classics
                'spotify:playlist:37i9dQZF1DX0BcQWzuB7ZO',  # Dance Party
                'spotify:playlist:37i9dQZF1DX8tZsk68tuDw'   # Dance Rising
            ]
        }
        
    def init_camera(self):
        """Initialize the camera and face detection"""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                print("Warning: Could not open camera. Running in demo mode without camera.")
                self.cap = None
                return False
                
            # Load the face cascade for face detection
            face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(face_cascade_path)
            
            print("Camera initialized successfully")
            return True
        except Exception as e:
            print(f"Camera initialization error: {e}")
            self.cap = None
            return False
    
    def init_spotify(self):
        """Initialize Spotify connection"""
        try:
            print("Connecting to Spotify...")
            
            # Authentication scope
            scope = "user-read-playback-state,user-modify-playback-state"
            
            # Create the OAuth manager
            auth_manager = SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope=scope,
                open_browser=True,
                show_dialog=True,
                cache_path=".spotify_cache"
            )
            
            # Create the Spotify client
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            
            # Check user info
            user = self.sp.current_user()
            print(f"Connected to Spotify as: {user['display_name']}")
            
            # Check for active devices
            self._check_devices()
            
            return True
        except Exception as e:
            print(f"Spotify connection error: {e}")
            print("Running in demo mode without Spotify.")
            self.demo_mode = True
            return False
    
    def _check_devices(self):
        """Check for active Spotify devices"""
        if self.demo_mode:
            return
            
        try:
            # Check for active devices
            devices = self.sp.devices()
            
            if not devices['devices']:
                print("No active Spotify devices found.")
                print("Please open Spotify on your phone or computer and play/pause a song.")
                print("Waiting for an active device...")
                
                # Wait for device to become available
                for i in range(3):
                    print(f"Checking for devices (attempt {i+1}/3)...")
                    time.sleep(2)
                    devices = self.sp.devices()
                    if devices['devices']:
                        break
                
                if not devices['devices']:
                    print("No Spotify devices found. Running in demo mode.")
                    self.demo_mode = True
                    return
            
            # Use the first available device
            self.device_id = devices['devices'][0]['id']
            device_name = devices['devices'][0]['name']
            print(f"Using Spotify device: {device_name}")
            
        except Exception as e:
            print(f"Error checking for Spotify devices: {e}")
            self.demo_mode = True
    
    def detect_face_and_emotion(self):
        """Detect face and simulate emotion detection"""
        if self.cap is None:
            # In demo mode without camera
            current_time = time.time()
            if current_time - self.last_emotion_time > self.emotion_change_interval:
                self.current_emotion = random.choice(self.emotions)
                self.last_emotion_time = current_time
                print(f"Detected emotion: {self.current_emotion}")
                
            return None, self.current_emotion
            
        # Read frame from camera
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture frame from camera")
            return None, None
            
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # For demo purposes, change emotion every few seconds
        current_time = time.time()
        if current_time - self.last_emotion_time > self.emotion_change_interval:
            self.current_emotion = random.choice(self.emotions)
            self.last_emotion_time = current_time
            print(f"Detected emotion: {self.current_emotion}")
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # If faces detected, show on frame
        if len(faces) > 0:
            # Use the largest face
            largest_face = max(faces, key=lambda face: face[2] * face[3])
            x, y, w, h = largest_face
            
            # Draw rectangle around face
            color = self.emotion_colors.get(self.current_emotion, (255, 255, 255))
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Display emotion text
            cv2.putText(frame, f"Emotion: {self.current_emotion}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
                        
            return frame, self.current_emotion
        
        return frame, None
    
    def play_music_for_emotion(self, emotion):
        """Play music based on the detected emotion"""
        if emotion is None:
            return
            
        if self.demo_mode:
            # Demo mode - just show what would be played
            playlist_names = {
                'happy': ['Happy Hits!', 'Feelin\' Good', 'Feel-Good Indie Rock'],
                'sad': ['Sad Hours', 'Down in the Dumps', 'Life Sucks'],
                'angry': ['Anger Management', 'Rock Hard', 'Adrenaline Workout'],
                'neutral': ['Peaceful Piano', 'Deep Focus', 'Instrumental Study'],
                'surprise': ['Dance Classics', 'Dance Party', 'Dance Rising']
            }
            
            names = playlist_names.get(emotion, playlist_names['neutral'])
            playlist_name = random.choice(names)
            print(f"[DEMO] Would play: {playlist_name} (Emotion: {emotion})")
            return
            
        # Skip if emotion hasn't changed
        if emotion == self.current_emotion and self.current_playlist is not None:
            return
            
        try:
            # Get playlists for this emotion
            playlists = self.emotion_playlists.get(emotion, self.emotion_playlists['neutral'])
            
            # Select a random playlist
            playlist_uri = random.choice(playlists)
            
            # Play the playlist
            self.sp.start_playback(device_id=self.device_id, context_uri=playlist_uri)
            
            # Get playlist info
            playlist_info = self.sp.playlist(playlist_uri)
            print(f"Now playing: {playlist_info['name']} (Emotion: {emotion})")
            
            # Update current playlist
            self.current_playlist = playlist_uri
            
        except spotipy.exceptions.SpotifyException as e:
            print(f"Spotify playback error: {e}")
            if "NO_ACTIVE_DEVICE" in str(e):
                print("Please open Spotify on your device and play/pause a song to activate it.")
                self._check_devices()
            elif "PREMIUM_REQUIRED" in str(e):
                print("This feature requires Spotify Premium.")
                self.demo_mode = True
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.demo_mode = True
    
    def run(self):
        """Main application loop"""
        print("Starting Emotion-Based Music Player...")
        print("Press 'q' to quit")
        
        camera_available = self.init_camera()
        spotify_available = self.init_spotify()
        
        if not camera_available:
            print("Running without camera in demo mode.")
        
        if not spotify_available:
            print("Running without Spotify in demo mode.")
            
        try:
            while True:
                # Detect face and emotion
                frame, emotion = self.detect_face_and_emotion()
                
                # Play music for detected emotion
                if emotion:
                    self.play_music_for_emotion(emotion)
                
                # Display the frame if camera is available
                if frame is not None:
                    cv2.imshow('Emotion-Based Music Player', frame)
                    
                    # Check for quit
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    # If no camera, just wait for interval
                    time.sleep(1)
                    
                    # Allow quitting with keyboard interrupt
                    print("Press Ctrl+C to quit", end="\r")
        
        except KeyboardInterrupt:
            print("\nApplication stopped by user")
            
        finally:
            # Clean up
            if self.cap is not None:
                self.cap.release()
            cv2.destroyAllWindows()
            print("Application closed")

if __name__ == "__main__":
    app = EmotionMusicPlayer()
    app.run()
