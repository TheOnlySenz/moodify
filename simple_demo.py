"""
Simple Emotion-Based Music Recommender - Demo Version
This simplified application uses OpenCV to detect faces and simulate emotions,
then recommends music that would match the mood without actually playing it.
"""

import cv2
import random
import time

class SimpleEmotionMusicRecommender:
    def __init__(self):
        # Initialize the camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise ValueError("Could not open camera. Please check your webcam connection.")
        
        # Load the face cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Emotion colors (BGR format)
        self.emotion_colors = {
            'happy': (0, 255, 255),     # Yellow
            'sad': (255, 0, 0),         # Blue
            'angry': (0, 0, 255),       # Red
            'neutral': (255, 255, 255), # White
            'surprise': (0, 165, 255)   # Orange
        }
        
        # List of emotions to cycle through
        self.emotions = list(self.emotion_colors.keys())
        
        # Music recommendations for each emotion
        self.playlists = {
            'happy': ['Happy Hits!', 'Feelin\' Good', 'Feel-Good Indie Rock'],
            'sad': ['Sad Hours', 'Down in the Dumps', 'Life Sucks'],
            'angry': ['Anger Management', 'Rock Hard', 'Adrenaline Workout'],
            'neutral': ['Peaceful Piano', 'Deep Focus', 'Instrumental Study'],
            'surprise': ['Dance Classics', 'Dance Party', 'Dance Rising']
        }
        
        # For demo purposes - emotion changes
        self.last_emotion_time = time.time()
        self.emotion_change_interval = 10  # seconds
        self.current_emotion = 'neutral'
        self.current_playlist = None
        
        print("Emotion-Music recommender initialized successfully")
        print("Camera is working properly")
    
    def run(self):
        """Main application loop"""
        print("Starting Emotion-Based Music Recommender Demo")
        print("Press 'q' to quit")
        
        while True:
            # Capture frame from webcam
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame from camera")
                break
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # For demo purposes, change emotion every few seconds
            current_time = time.time()
            if current_time - self.last_emotion_time > self.emotion_change_interval:
                self.current_emotion = random.choice(self.emotions)
                self.last_emotion_time = current_time
                self.recommend_music(self.current_emotion)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            # Draw faces and display emotion
            if len(faces) > 0:
                # Use the largest face
                largest_face = max(faces, key=lambda face: face[2] * face[3])
                x, y, w, h = largest_face
                
                # Draw rectangle around face
                color = self.emotion_colors.get(self.current_emotion, (255, 255, 255))
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
                
                # Display emotion text
                cv2.putText(frame, f"Emotion: {self.current_emotion}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
                
                # Display playlist info if available
                if self.current_playlist:
                    cv2.putText(frame, f"Playlist: {self.current_playlist}", (10, 70), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)
            
            # Display the frame
            cv2.imshow('Emotion-Based Music Recommender', frame)
            
            # Check if user wants to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release resources
        self.cap.release()
        cv2.destroyAllWindows()
        print("Application closed")
    
    def recommend_music(self, emotion):
        """Recommend music based on the detected emotion"""
        # Get playlist choices for this emotion
        playlist_options = self.playlists.get(emotion, self.playlists['neutral'])
        
        # Select a random playlist
        self.current_playlist = random.choice(playlist_options)
        print(f"Detected emotion: {emotion}")
        print(f"Recommended playlist: {self.current_playlist}")
        print("(In a full version, this would play music from Spotify)")
        print("-" * 40)

if __name__ == "__main__":
    try:
        app = SimpleEmotionMusicRecommender()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")
