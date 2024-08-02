'''
Script to capture live feed over RTSP and record video for a specified duration.
BLOCKERS:
    1. The video is not saving to the specified directory.
'''


import os
import ctypes
import vlc
import threading
import time
import keyboard  # Import the keyboard module

# Set the path to the VLC installation directory
vlc_path = r'C:/Program Files/VideoLAN/VLC'
os.add_dll_directory(vlc_path)

# Set the full path to the libvlc.dll file
libvlc_dll = os.path.join(vlc_path, 'libvlc.dll')
ctypes.CDLL(libvlc_dll)

# Define RTSP streams
rtsp_streams = {
    'feed1': 'rtsp://UmZF6h:atAIz1ecLgC8@192.168.1.127:554/live/ch1',
    'feed2': 'rtsp://TK1Xnf:LbAiQiGLPvRd@192.168.1.174:554/live/ch1',
    'feed3': 'rtsp://4kkzxW:hDneHFEeidTc@192.168.1.123:554/live/ch1',
    'feed5': 'rtsp://Z6WjWa:H48qMg7phOQC@192.168.1.223:554/live/ch1',
    'feed6': 'rtsp://vm4fKG:9q9c0v1TFGT1@192.168.1.64:554/live/ch1'
}

instance = vlc.Instance()

# Create media players for each stream
media_players = {}
for key, url in rtsp_streams.items():
    media = instance.media_new(url)
    media_player = instance.media_player_new()
    media_player.set_media(media)
    media_players[key] = media_player
    media_player.play()

# Event to signal thread to stop
stop_event = threading.Event()

# Function to check if players are playing and record video
def check_playing_and_record(record=False, record_time=None):
    while not stop_event.is_set():
        for key, media_player in media_players.items():
            if not media_player.is_playing():
                media_player.play()

        if record and record_time:
            try:
                minutes = int(record_time[:-1])
                if record_time[-1] == 'm' and minutes > 0:
                    for key, media_player in media_players.items():
                        media = media_player.get_media()
                        if media:
                            output_file = os.path.join(base_directory, f"{key}_{time.strftime('%Y-%m-%d_%H-%M-%S')}.mp4")
                            options = f" --sout=file/mp4:{output_file}"
                            media_player.stop()
                            media_player.play()
                            print(f"Recording {key} for {minutes} minutes...")
                            time.sleep(minutes * 60)
                            media_player.stop()
                            media_player.play()
                            print(f"Recording of {key} complete.")
                else:
                    print("Invalid record time format. Recording skipped.")
            except ValueError:
                print("Invalid record time format. Recording skipped.")

        time.sleep(1)

# Create and start a thread for checking players' status
record = True
record_time = '2m'
check_thread = threading.Thread(target=check_playing_and_record, args=(record, record_time))
check_thread.start()

try:
    while True:
        if keyboard.is_pressed('q'):
            print("Stopping the program...")
            stop_event.set()
            break
        time.sleep(0.1)
except KeyboardInterrupt:
    stop_event.set()
finally:
    check_thread.join()
    for key, media_player in media_players.items():
        media_player.stop()

    # Optionally release the instance
    # instance.release()
