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
    instance = vlc.Instance()

    print("Checking for active stream connections...")
    try:
        for key, url in rtsp_streams.items():
            media = instance.media_new(url)
            media_player = instance.media_player_new()
            media_player.set_media(media)

            # Try to play the media to check if the stream is active
            media_player.play()
            time.sleep(2)  # Wait for the stream to attempt to connect

            # Check if the stream is playing
            active_streams[key] = media_player.is_playing()
            media_player.stop()  # Stop the media player after checking

    finally:
        instance.release()  # Release the VLC instance

    print("Stream connections checked. Active streams:", active_streams)
    return active_streams

def create_stream_instance(active_streams):
    # Create parallel instances for each active stream
    media_players = {}
    for stream, is_active in active_streams.items():
        if is_active:
            instance = vlc.Instance()
            media = instance.media_new(rtsp_streams[stream])
            media_player = instance.media_player_new()
            media_player.set_media(media)
            media_player.play()
            media_players[stream] = media_player
            print(f"Connected to {stream}")
        else:
            print(f"Failed to connect to {stream}")
    return media_players

def record_stream(media_player, stream_name, record, record_time_min):
    if not record:
        print(f"Recording is disabled for {stream_name}.")
        return

    # Create a timestamp for the output file
    start_time_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_file = os.path.join("recordings", f"{stream_name}_{start_time_str}.mp4")

    # Set VLC options for recording
    options = f":sout=#file{{dst={output_file},mux=mp4}}"
    media = media_player.get_media()  # Get the current media

    # Set the modified media to the player
    media_player.set_media(media)
    media_player.play()
    print(f"Recording {stream_name} started...")

    # Record for a specific duration
    record_duration = record_time_min * 60  # Convert minutes to seconds
    start_time = time.time()

    while time.time() - start_time < record_duration:
        if keyboard.is_pressed('q'):
            print("Stopping recording...")
            media_player.stop()
            break
        time.sleep(1)

    if media_player.is_playing():
        media_player.stop()

    print(f"Recording of {stream_name} complete.")

def exit_program():
    while True:
        if keyboard.is_pressed('q'):
            print("Exiting the program...")
            os._exit(0)  # Exit the terminal cleanly
        time.sleep(0.1)

def main():
    utils()  # Initialize VLC settings

    record = True    # Set to True to enable recording
    record_time_min = 1  # Set the recording duration in minutes

    # Start a thread to monitor for 'q' key press
    exit_thread = threading.Thread(target=exit_program, daemon=True)
    exit_thread.start()

    while True:
        # Check which streams are active
        active_streams = check_stream_active()
        media_players = create_stream_instance(active_streams)

        # Record streams that are active
        record_threads = []
        for stream, player in media_players.items():
            record_thread = threading.Thread(target=record_stream, args=(player, stream, record, record_time_min))
            record_threads.append(record_thread)
            record_thread.start()

        # Wait for all recording threads to finish
        for thread in record_threads:
            thread.join()

if __name__ == '__main__':
    # Ensure the recordings directory exists
    if not os.path.exists("recordings"):
        os.makedirs("recordings")
    
    main()
