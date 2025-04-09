"""
Spotify Player Module - Demo Version
Simulates music selection based on detected emotions without requiring actual Spotify credentials.
"""

import random
import time

class SpotifyPlayer:
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None):
        """
        Initialize the demo Spotify player
        """
        print("Initializing Spotify player in DEMO MODE")
        print("Song selection will be simulated without actual playback")
        
        # Define emotion to playlist mapping
        self.playlist_names = {
            'happy': ['Happy Hits!', 'Feelin\' Good', 'Feel-Good Indie Rock'],
            'sad': ['Sad Hours', 'Down in the Dumps', 'Life Sucks'],
            'angry': ['Anger Management', 'Rock Hard', 'Adrenaline Workout'],
            'neutral': ['Peaceful Piano', 'Deep Focus', 'Instrumental Study'],
            'surprise': ['Dance Classics', 'Dance Party', 'Dance Rising']
        }
        
        # Keep track of current emotion and playlist
        self.current_emotion = None
        self.current_playlist = None
    
    def play_music_for_emotion(self, emotion):
        """
        Simulate playing music that matches the detected emotion
        
        Args:
            emotion (str): The detected emotion
        """
        # Skip if emotion is the same as current (to avoid restarting the same playlist)
        if emotion == self.current_emotion and self.current_playlist is not None:
            return
        
        # Update current emotion
        self.current_emotion = emotion
        
        # Get the list of playlists for this emotion, or use neutral if emotion not recognized
        playlist_names = self.playlist_names.get(emotion, self.playlist_names['neutral'])
        
        # Select a random playlist from the list
        self.current_playlist = random.choice(playlist_names)
        
        # Display what would be playing
        print(f"[DEMO] Now playing: {self.current_playlist} (Emotion: {emotion})")
        print(f"To enable actual Spotify playback, update the .env file with valid credentials")
