# Emotion-Based Music Player

This application uses facial emotion detection with OpenCV to play music from Spotify that matches your detected mood.

## Features

- Real-time facial emotion detection using OpenCV and DeepFace
- Automatic Spotify playlist selection based on detected emotions
- Visual feedback of detected emotions
- Simple keyboard controls

## Requirements

- Python 3.7+
- Webcam
- Spotify account (Premium required for playback control)
- Spotify Developer API credentials

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/emotion-music-player.git
   cd emotion-music-player
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up Spotify API credentials:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Create a new application
   - Set the Redirect URI to `http://localhost:8888/callback`
   - Create a `.env` file in the project root with your Spotify credentials:
     ```
     SPOTIFY_CLIENT_ID=your_client_id_here
     SPOTIFY_CLIENT_SECRET=your_client_secret_here
     SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
     ```

## Usage

1. Start the application:
   ```
   python main.py
   ```

2. On first run, you'll need to authorize the application with your Spotify account.
   - A browser will open asking you to login to Spotify
   - After logging in, you'll be redirected to the callback URL
   - Copy the entire URL and paste it into the terminal if prompted

3. Make sure Spotify is open on one of your devices before running the application.

4. Look at the camera and the application will detect your emotion and play music accordingly.

5. Press 'q' to quit the application.

## Emotion-Music Mapping

The application maps detected emotions to curated Spotify playlists:

- **Happy**: Upbeat, cheerful music
- **Sad**: Melancholic, slow-tempo songs
- **Angry**: High-energy, intense music
- **Neutral**: Calm, instrumental music
- **Fear**: Confidence-boosting, positive music
- **Disgust**: Soothing, relaxing music
- **Surprise**: Energetic, dance music

## Troubleshooting

- **No device found**: Make sure Spotify is open on your computer or phone. Play and pause any song to activate the device.
- **Playback doesn't start**: Spotify Premium is required for the API playback functionality.
- **Camera not detected**: Check your webcam connection and permissions.
- **Face not detected**: Make sure you're in a well-lit environment and facing the camera directly.

## License

MIT
