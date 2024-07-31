import os
import ctypes
import vlc
import threading
import time
import keyboard  # Import the keyboard module
from datetime import datetime  # Import datetime

def utils():
    # Set the path to the VLC installation directory
    vlc_path = r'C:/Program Files/VideoLAN/VLC'
    os.add_dll_directory(vlc_path)

    # Set the full path to the libvlc.dll file
    libvlc_dll = os.path.join(vlc_path, 'libvlc.dll')
    ctypes.CDLL(libvlc_dll)

# Define RTSP stream for feed3
rtsp_feed3 = 'rtsp://4kkzxW:hDneHFEeidTc@192.168.1.123:554/live/ch1'

def record_stream(media_player, output_path):
    # Create a timestamp for the output file
    start_time_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_file = os.path.join(output_path, f"feed3_{start_time_str}.mp4")

    # Set VLC options for recording
    options = f":sout=#transcode{{vcodec=h264,acodec=mp3}}:file{{dst={output_file},mux=mp4}}"
    media = media_player.get_media()  # Get the current media
    media.add_options(options)  # Add options for recording

    # Set the modified media to the player and start it
    media_player.set_media(media)
    media_player.play()
    print(f"Recording started for feed3...")

    # Record until 'q' is pressed
    while True:
        if keyboard.is_pressed('q'):
            print("Stopping recording...")
            media_player.stop()
            break
        time.sleep(1)

def main():
    utils()  # Initialize VLC settings

    output_path = "C:/Users/MSI/Documents/GitHub/susu_summer24/hand_tracking_@_assesment/recordings"

    # Ensure the recordings directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Create a VLC instance for playback
    playback_instance = vlc.Instance()
    playback_media = playback_instance.media_new(rtsp_feed3)
    playback_player = playback_instance.media_player_new()
    playback_player.set_media(playback_media)
    playback_player.play()  # Start playback for feed3
    print("Playback started for feed3.")

    # Start a separate thread to record the stream
    record_thread = threading.Thread(target=record_stream, args=(playback_player, output_path))
    record_thread.start()  # Start recording in a separate thread

    # Wait for the recording thread to finish
    record_thread.join()

    # Clean up
    playback_player.stop()
    playback_instance.release()
    print("Playback stopped.")

if __name__ == '__main__':
    main()
