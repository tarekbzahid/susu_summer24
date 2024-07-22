import vlc
import threading
import time

# Define dictionary with multiple RTSP stream URLs
rtsp_streams = {
    'feed1': 'rtsp://UmZF6h:atAIz1ecLgC8@192.168.1.127:554/live/ch1',
    'feed2': 'rtsp://TK1Xnf:LbAiQiGLPvRd@192.168.1.174:554/live/ch1',
    'feed3': 'rtsp://4kkzxW:hDneHFEeidTc@192.168.1.123:554/live/ch1',
    'feed5': 'rtsp://Z6WjWa:H48qMg7phOQC@192.168.1.223:554/live/ch1',
    'feed6': 'rtsp://vm4fKG:9q9c0v1TFGT1@192.168.1.64:554/live/ch1'
}

# Initialize VLC instance
instance = vlc.Instance()

# Create media objects for each stream
media_players = {}
for key, url in rtsp_streams.items():
    media = instance.media_new(url)
    media_player = instance.media_player_new()
    media_player.set_media(media)
    media_players[key] = media_player

    # Optional: Adjust options like volume, etc.
    # media_player.audio_set_volume(50)

    # Start playing each stream
    media_player.play()

# Function to continuously check if players are playing
def check_playing():
    while True:
        for key, media_player in media_players.items():
            if not media_player.is_playing():
                # Restart the player if it's not playing
                media_player.play()
        time.sleep(1)

# Create a thread for checking players' status
check_thread = threading.Thread(target=check_playing)
check_thread.start()

# Optionally, wait for the thread to complete if needed
# check_thread.join()

# Keep the main thread running (you can add other logic here)
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break

# Clean up
for key, media_player in media_players.items():
    media_player.stop()

# Optionally release the instance
# instance.release()
