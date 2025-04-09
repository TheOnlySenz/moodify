@echo off
echo Creating standalone executable for Emotion-Based Music Player...
echo.

REM Create a single executable file with all dependencies bundled
pyinstaller --onefile --windowed --add-data "spotify_cache;." --name EmotionMusicPlayer emotion_music_player.py

echo.
echo Build complete! Executable is located in the "dist" folder.
echo You can find it at: dist\EmotionMusicPlayer.exe
echo.
pause
