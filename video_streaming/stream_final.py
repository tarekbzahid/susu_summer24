import os
import ctypes
import vlc
import threading
import time
import keyboard
from datetime import datetime

def utils():
    vlc_path = r'C:/Program Files/VideoLAN/VLC'
    os.add_dll_directory(vlc_path)
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

def check_stream_active():
    active_streams = {}
    instance = vlc.Instance(['--quiet', '--logfile=vlc-log.txt', '--verbose=2'])

    print("Checking for active stream connections...")
    try:
        for key, url in rtsp_streams.items():
            media = instance.media_new(url)
            media_player = instance.media_player_new()
            media_player.set_media(media)

            media_player.play()
            time.sleep(2)

            active_streams[key] = media_player.is_playing()
            media_player.stop()
    finally:
        instance.release()

    print("Stream connections checked. Active streams:", active_streams)
    return active_streams

def create_stream_instance(active_streams):
    media_players = {}
    for stream, is_active in active_streams.items():
        if is_active:
            instance = vlc.Instance(['--quiet', '--logfile=vlc-log.txt', '--verbose=2'])
            media = instance.media_new(rtsp_streams[stream])
            media_player = instance.media_player_new()
            media_player.set_media(media)
            media_player.play()
            media_players[stream] = media_player
            print(f"Connected to {stream}")
        else:
            print(f"Failed to connect to {stream}")
    return media_players

def exit_program():
    while True:
        if keyboard.is_pressed('q'):
            print("Exiting the program...")
            os._exit(0)
        time.sleep(0.1)

def main():
    utils()

    refresh_time_min = 10  # Set the refresh duration in minutes

    exit_thread = threading.Thread(target=exit_program, daemon=True)
    exit_thread.start()

    while True:
        active_streams = check_stream_active()
        media_players = create_stream_instance(active_streams)

        time.sleep(refresh_time_min * 60)  # Refresh the streams after the specified duration

if __name__ == '__main__':
    main()
