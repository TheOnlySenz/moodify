"""
Spotify Player Module
Handles Spotify authentication and playing music based on detected emotions.
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import time

class SpotifyPlayer:
    def __init__(self, client_id, client_secret, redirect_uri):
        """
        Initialize the Spotify player with developer credentials
        
        Args:
            client_id (str): Spotify Developer Client ID
            client_secret (str): Spotify Developer Client Secret
            redirect_uri (str): Redirect URI set in Spotify Developer Dashboard
        """
        self.scope = "user-read-playback-state,user-modify-playback-state"
        try:
            print(f"Authenticating with Spotify: {client_id[:5]}...")
            print(f"Using redirect URI: {redirect_uri}")
            print("Opening browser for authentication - please login and authorize the app")
            
            # Initialize auth manager - more tolerant of redirect URI differences
            auth_manager = SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=self.scope,
                open_browser=True,
                show_dialog=True
            )
            
            # Create Spotify client
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            print("Authentication successful!")
            
        except Exception as e:
            print(f"Spotify authentication error: {e}")
            print("Falling back to demo mode...")
            # Create a demo mode indicator
            self.demo_mode = True
            self.emotion_playlists = {}
            return
        
        # Check if the user has an active device
        self._check_devices()
        
        # Define emotion to playlist mapping
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
            'fear': [
                'spotify:playlist:37i9dQZF1DX6SZazidEqln',  # Confidence Boost
                'spotify:playlist:37i9dQZF1DX4fpCWaHOned',  # Positive Vibes
                'spotify:playlist:37i9dQZF1DX9XIFQuFvzM4'   # Feelin' Good
            ],
            'disgust': [
                'spotify:playlist:37i9dQZF1DWZMCPjHG57Sq',  # Soothing Relaxation
                'spotify:playlist:37i9dQZF1DXcF6B6QPhFDv',  # Mindful Moments
                'spotify:playlist:37i9dQZF1DWYoYGBbGKurt'   # Ambient Relaxation
            ],
            'surprise': [
                'spotify:playlist:37i9dQZF1DX5Vy6DFOcx00',  # Dance Classics
                'spotify:playlist:37i9dQZF1DX0BcQWzuB7ZO',  # Dance Party
                'spotify:playlist:37i9dQZF1DX8tZsk68tuDw'   # Dance Rising
            ]
        }
        
        # Keep track of current emotion and playlist
        self.current_emotion = None
        self.current_playlist = None
        
        print("Spotify player initialized.")
    
    def _check_devices(self):
        """
        Check if there are any active Spotify devices
        If not, notify the user
        """
        try:
            # Check if we're in demo mode (set after an authentication error)
            if hasattr(self, 'demo_mode') and self.demo_mode:
                print("Running in demo mode - device check skipped")
                return
                
            devices = self.sp.devices()
            if not devices['devices']:
                print("WARNING: No active Spotify devices found!")
                print("Please open Spotify on your computer or phone and start playing any song")
                print("Then pause it and return to this application")
                print("Waiting for an active device...")
                
                # Wait until a device is available
                attempts = 0
                while attempts < 3:
                    time.sleep(5)
                    devices = self.sp.devices()
                    if devices['devices']:
                        print(f"Found active device: {devices['devices'][0]['name']}")
                        return
                    attempts += 1
                
                print("No devices found after waiting. Music playback may not work.")
                print("Please ensure Spotify is open on at least one of your devices.")
                
                # Switch to demo mode if no devices are found
                self.demo_mode = True
                print("Switching to demo mode due to no available devices")
        except Exception as e:
            print(f"Error checking for devices: {e}")
            self.demo_mode = True
            print("Switching to demo mode due to error")
    
    def play_music_for_emotion(self, emotion):
        """
        Play music that matches the detected emotion
        
        Args:
            emotion (str): The detected emotion
        """
        # Check if we're in demo mode after an authentication error
        if hasattr(self, 'demo_mode') and self.demo_mode:
            # Demo mode playlist names
            playlist_names = {
                'happy': ['Happy Hits!', 'Feelin\'Good', 'Feel-Good Indie Rock'],
                'sad': ['Sad Hours', 'Down in the Dumps', 'Life Sucks'],
                'angry': ['Anger Management', 'Rock Hard', 'Adrenaline Workout'],
                'neutral': ['Peaceful Piano', 'Deep Focus', 'Instrumental Study'],
                'surprise': ['Dance Classics', 'Dance Party', 'Dance Rising']
            }
            
            # Get playlists for this emotion or use neutral if not found
            names = playlist_names.get(emotion, playlist_names['neutral'])
            playlist_name = random.choice(names)
            print(f"[DEMO] Would play: {playlist_name} (Emotion: {emotion})")
            return
            
        # Real Spotify integration
        try:
            # Skip if emotion is the same as current (to avoid restarting the same playlist)
            if emotion == self.current_emotion and self.current_playlist is not None:
                return
            
            # Update current emotion
            self.current_emotion = emotion
            
            # Get the list of playlists for this emotion, or use neutral if emotion not recognized
            playlists = self.emotion_playlists.get(emotion, self.emotion_playlists['neutral'])
            
            # Select a random playlist from the list
            self.current_playlist = random.choice(playlists)
            
            # Check available devices again in case the active device changed
            devices = self.sp.devices()
            if not devices['devices']:
                print("No active Spotify devices found. Please open Spotify on a device.")
                # Switch to demo mode
                self.demo_mode = True
                print("Switching to demo mode - no devices available")
                self.play_music_for_emotion(emotion)  # Retry in demo mode
                return
            
            # Get the active device id
            device_id = devices['devices'][0]['id']
            
            # Start playing the selected playlist
            self.sp.start_playback(device_id=device_id, context_uri=self.current_playlist)
            
            # Get the playlist details to display to the user
            playlist_info = self.sp.playlist(self.current_playlist)
            print(f"Now playing: {playlist_info['name']} (Emotion: {emotion})")
            
        except spotipy.exceptions.SpotifyException as e:
            print(f"Spotify error: {e}")
            if "NO_ACTIVE_DEVICE" in str(e):
                print("Please open Spotify on your device and play/pause a song to activate it.")
            elif "PREMIUM_REQUIRED" in str(e):
                print("This feature requires Spotify Premium.")
            
            # Switch to demo mode
            self.demo_mode = True
            print("Switching to demo mode due to Spotify error")
            self.play_music_for_emotion(emotion)  # Retry in demo mode
            
        except Exception as e:
            print(f"Unexpected error: {e}")
            # Switch to demo mode
            self.demo_mode = True
            print("Switching to demo mode due to unexpected error")
            self.play_music_for_emotion(emotion)  # Retry in demo mode
