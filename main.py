"""
Emotion-Based Music Player
This application uses facial emotion detection to play music from Spotify that matches the detected emotion.
"""

import os
import time
from dotenv import load_dotenv
from emotion_detector import EmotionDetector
from spotify_player import SpotifyPlayer

# Load environment variables from .env file
load_dotenv()

def main():
    print("Starting Emotion-Based Music Player...")
    print("Press 'q' to quit")
    
    # Initialize the emotion detector
    emotion_detector = EmotionDetector()
    
    # Initialize the Spotify player (in demo mode)
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    
    if not all([client_id, client_secret, redirect_uri]) or any(x.startswith('your_') for x in [client_id, client_secret]):
        print("Note: Using demo mode since valid Spotify credentials are not configured")
        print("To use actual Spotify playback, update the .env file with your credentials")
    
    spotify_player = SpotifyPlayer(client_id, client_secret, redirect_uri)
    
    current_emotion = None
    last_emotion_change = 0
    emotion_cooldown = 10  # Seconds to wait before changing songs
    
    try:
        # Start the emotion detection loop
        while True:
            frame, emotion = emotion_detector.detect_emotion()
            
            # Display the current emotion
            if emotion:
                if emotion != current_emotion and time.time() - last_emotion_change > emotion_cooldown:
                    print(f"Detected emotion: {emotion}")
                    spotify_player.play_music_for_emotion(emotion)
                    current_emotion = emotion
                    last_emotion_change = time.time()
                
                # Display emotion on frame
                emotion_detector.display_emotion(frame, emotion)
            
            # Display the frame
            emotion_detector.show_frame(frame)
            
            # Check if user wants to quit
            if emotion_detector.should_quit():
                break
                
    except KeyboardInterrupt:
        print("Application stopped by user")
    finally:
        # Clean up
        emotion_detector.release()
        print("Application closed")

if __name__ == "__main__":
    main()
