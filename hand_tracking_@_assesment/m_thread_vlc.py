# import argeparse 
import os
import ctypes 

# Set the path to the VLC installation directory
vlc_path = r'C:\Program Files (x86)\VideoLAN\VLC'
os.add_dll_directory(vlc_path)

# Set the full path to the libvlc.dll file
libvlc_dll = os.path.join(vlc_path, 'libvlc.dll')
ctypes.CDLL(libvlc_dll)


import vlc
import threading
import time
import os  # Import os module for path operations

current_directory = os.path.dirname(os.path.abspath(__file__))
base_directory = os.path.join(current_directory, "susu_summer24")

os.makedirs(base_directory, exist_ok=True)

# Define dictionary with multiple RTSP stream URLs
rtsp_streams = {
    'feed1': 'rtsp://UmZF6h:atAIz1ecLgC8@192.168.1.127:554/live/ch1',
    'feed2': 'rtsp://TK1Xnf:LbAiQiGLPvRd@192.168.1.174:554/live/ch1',
    'feed3': 'rtsp://4kkzxW:hDneHFEeidTc@192.168.1.123:554/live/ch1',
    'feed5': 'rtsp://Z6WjWa:H48qMg7phOQC@192.168.1.223:554/live/ch1',
    'feed6': 'rtsp://vm4fKG:9q9c0v1TFGT1@192.168.1.64:554/live/ch1'
}
instance = vlc.Instance()

# Create media objects for each stream
media_players = {}
for key, url in rtsp_streams.items():
    media = instance.media_new(url)
    media_player = instance.media_player_new()
    media_player.set_media(media)
    media_players[key] = media_player

    # Start playing each stream
    media_player.play()

    # media player title
    #media_player.video_set_title(f"Factory Floor - Feed {key[-1]}")



# Function to continuously check if players are playing and record video
def check_playing_and_record(record=False, record_time=None):
    while True:
        for key, media_player in media_players.items():
            if not media_player.is_playing():
                # Restart the player if it's not playing
                media_player.play()

        # Record video if specified
        if record and record_time:
            try:
                minutes = int(record_time[:-1])
                if record_time[-1] == 'm' and minutes > 0:
                    # Start recording each stream
                    for key, media_player in media_players.items():
                        media = media_player.get_media()
                        if media:
                            # Define output file path relative to the base_directory
                            output_file = os.path.join(base_directory, f"{key}_{time.strftime('%Y-%m-%d_%H-%M-%S')}.mp4")
                            # Define VLC options for recording
                            options = f" --sout=file/mp4:{output_file}"
                            # Stop playback
                            media_player.stop()
                            # Start recording
                            media_player.play()
                            print(f"Recording {key} for {minutes} minutes...")
                            time.sleep(minutes * 60)  # Record for specified minutes
                            # Stop recording
                            media_player.stop()
                            # Resume playback
                            media_player.play()
                            print(f"Recording of {key} complete.")
                else:
                    print("Invalid record time format. Recording skipped.")
            except ValueError:
                print("Invalid record time format. Recording skipped.")

        time.sleep(1)

# Create a thread for checking players' status and optionally recording time
record = True  # Set to True to enable recording
record_time = '2m'  # Specify the recording duration ('Xm' format)
check_thread = threading.Thread(target=check_playing_and_record, args=(record, record_time))
check_thread.start()

# Keep the main thread running (you can add other logic here)
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

# Clean up
for key, media_player in media_players.items():
    media_player.stop()

# Optionally release the instance
# instance.release()
