"""
Spotify Emotion-Based Player - Simplified Test Version
Tests playing music based on selected emotions without using the camera.
"""

import os
import time
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Get Spotify credentials
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    
    # Verify credentials are available
    if not all([client_id, client_secret, redirect_uri]):
        print("ERROR: Spotify credentials not found in .env file")
        return
    
    print("=== Spotify Emotion-Based Player ===")
    print(f"Using redirect URI: {redirect_uri}")
    
    # Emotion playlists
    emotion_playlists = {
        'happy': [
            'spotify:playlist:37i9dQZF1DXdPec7aLTmlC',  # Happy Hits!
            'spotify:playlist:37i9dQZF1DX9XIFQuFvzM4',  # Feelin' Good
        ],
        'sad': [
            'spotify:playlist:37i9dQZF1DX7qK8ma5wgG1',  # Sad Hours
            'spotify:playlist:37i9dQZF1DX889U0CL85jj',  # Down in the Dumps
        ],
        'angry': [
            'spotify:playlist:37i9dQZF1DX1tyCD9QhIWF',  # Anger Management
            'spotify:playlist:37i9dQZF1DX4eRPd9frC1m',  # Rock Hard
        ],
        'neutral': [
            'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',  # Peaceful Piano
            'spotify:playlist:37i9dQZF1DWZeKCadgRdKQ',  # Deep Focus
        ],
        'surprise': [
            'spotify:playlist:37i9dQZF1DX5Vy6DFOcx00',  # Dance Classics
            'spotify:playlist:37i9dQZF1DX0BcQWzuB7ZO',  # Dance Party
        ]
    }
    
    # Connect to Spotify
    try:
        print("\nConnecting to Spotify...")
        scope = "user-read-playback-state,user-modify-playback-state"
        
        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            open_browser=True,
            show_dialog=True
        )
        
        sp = spotipy.Spotify(auth_manager=auth_manager)
        user = sp.current_user()
        print(f"Connected as: {user['display_name']}")
        
        # Check for active devices
        print("\nChecking for active Spotify devices...")
        devices = sp.devices()
        
        if not devices['devices']:
            print("No active Spotify devices found!")
            print("Please open Spotify on your phone or computer and play/pause a song")
            print("Then run this script again")
            return
        
        print(f"Found {len(devices['devices'])} device(s):")
        for i, device in enumerate(devices['devices']):
            print(f"  {i+1}. {device['name']} ({device['type']})")
        
        device_id = devices['devices'][0]['id']
        
        # Main loop - simulate emotion changes
        print("\n=== Emotion Music Player Started ===")
        print("Press Ctrl+C to exit")
        
        emotions = list(emotion_playlists.keys())
        
        try:
            while True:
                # Select a random emotion
                emotion = random.choice(emotions)
                print(f"\nDetected emotion: {emotion}")
                
                # Get playlist for this emotion
                playlists = emotion_playlists[emotion]
                playlist_uri = random.choice(playlists)
                
                # Play the playlist
                try:
                    sp.start_playback(device_id=device_id, context_uri=playlist_uri)
                    playlist_info = sp.playlist(playlist_uri)
                    print(f"Now playing: {playlist_info['name']} (Emotion: {emotion})")
                    
                    # Wait before changing emotion
                    for i in range(15, 0, -1):
                        print(f"Changing emotion in {i} seconds...", end="\r")
                        time.sleep(1)
                    print(" " * 40, end="\r")  # Clear the line
                    
                except spotipy.exceptions.SpotifyException as e:
                    print(f"Spotify error: {e}")
                    if "NO_ACTIVE_DEVICE" in str(e):
                        print("Please open Spotify on your device and play/pause a song to activate it")
                        break
                    elif "PREMIUM_REQUIRED" in str(e):
                        print("This feature requires Spotify Premium")
                        break
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            
    except Exception as e:
        print(f"\nError: {e}")
        print("\nPossible issues:")
        print("1. Incorrect redirect URI in Spotify Developer Dashboard")
        print("2. Invalid client credentials")
        print("3. Network connectivity issues")
    
    print("\nDone!")

if __name__ == "__main__":
    main()
