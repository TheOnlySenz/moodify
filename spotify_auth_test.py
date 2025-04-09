"""
Spotify Authentication Test Script
This script tests Spotify authentication and checks if an active device is available.
"""

import os
import sys
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def test_spotify_auth():
    """Test Spotify authentication and device availability"""
    # Load environment variables
    load_dotenv()
    
    # Get Spotify credentials
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    
    # Verify credentials are available
    if not all([client_id, client_secret, redirect_uri]):
        print("ERROR: Spotify credentials not found in .env file")
        return False
    
    print(f"Testing Spotify authentication with:")
    print(f"Client ID: {client_id[:5]}...")
    print(f"Client Secret: {client_secret[:5]}...")
    print(f"Redirect URI: {redirect_uri}")
    
    # Authentication scope
    scope = "user-read-playback-state,user-modify-playback-state"
    
    try:
        print("\nInitializing Spotify authentication...")
        print("A browser window should open for you to log in to Spotify")
        print("After login, you may be redirected to a URL - copy and paste that URL here if prompted")
        
        # Initialize Spotify client with verbose output
        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            open_browser=True,
            show_dialog=True,
            cache_path=".spotify_cache"
        )
        
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        # Test authorization by getting current user
        user = sp.current_user()
        print(f"\nAuthentication successful!")
        print(f"Logged in as: {user['display_name']} (ID: {user['id']})")
        
        # Check for active devices
        print("\nChecking for active Spotify devices...")
        devices = sp.devices()
        
        if not devices['devices']:
            print("No active Spotify devices found!")
            print("Please open Spotify on your phone or computer and play/pause a song")
            print("then run this test again")
            return False
        
        print(f"Found {len(devices['devices'])} active device(s):")
        for i, device in enumerate(devices['devices']):
            print(f"  {i+1}. {device['name']} ({device['type']}) - {'Active' if device['is_active'] else 'Inactive'}")
        
        # Test playlist access
        print("\nTesting playlist access...")
        playlists = sp.current_user_playlists(limit=5)
        if playlists['items']:
            print(f"Successfully accessed your playlists. Examples:")
            for i, playlist in enumerate(playlists['items']):
                print(f"  {i+1}. {playlist['name']} ({playlist['tracks']['total']} tracks)")
        else:
            print("No playlists found in your account")
        
        print("\nAll tests PASSED! Your Spotify integration should work correctly.")
        return True
    
    except Exception as e:
        print(f"\nERROR during Spotify authentication: {e}")
        print("\nPossible issues and solutions:")
        print("1. Redirect URI mismatch - Make sure the redirect URI in your")
        print("   Spotify Developer Dashboard EXACTLY matches: " + redirect_uri)
        print("2. Invalid client credentials - Double-check your client ID and secret")
        print("3. Spotify account issues - Ensure you're using the correct Spotify account")
        print("4. Network issues - Check your internet connection")
        print("5. Ensure you have a Spotify Premium account for full playback control")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("SPOTIFY AUTHENTICATION TEST")
    print("=" * 60)
    success = test_spotify_auth()
    print("\nTest result:", "SUCCESS" if success else "FAILED")
    print("=" * 60)
    
    if not success:
        print("\nWould you like to see detailed troubleshooting steps? (y/n)")
        if input().lower() == 'y':
            print("\nSpotify Authentication Troubleshooting:")
            print("1. Check your Spotify Developer Dashboard at https://developer.spotify.com/dashboard/")
            print("2. Find your app and click 'Edit Settings'")
            print("3. Add EXACTLY this Redirect URI: http://localhost:8888/callback")
            print("4. Save the settings")
            print("5. Make sure your .env file has the correct credentials")
            print("6. Open Spotify on your phone or computer before running the test")
            print("7. You must have a Spotify Premium account for playback control")
    
    print("\nPress Enter to exit...")
    input()
