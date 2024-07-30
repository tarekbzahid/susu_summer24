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
            time.sleep(5)  # Increase wait time for the stream to attempt to connect

            # Check if the stream is playing
            is_playing = media_player.is_playing()
            active_streams[key] = is_playing
            print(f"Stream {key} playing: {is_playing}")

            media_player.stop()  # Stop the media player after checking

    except Exception as e:
        print(f"Error checking streams: {e}")
    finally:
        instance.release()  # Release the VLC instance

    print("Stream connections checked. Active streams:", active_streams)
    return active_streams

def stream_and_record(stream_name, url, record_time_min, output_path):
    # Create a timestamp for the output file
    start_time_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_file = os.path.join(output_path, f"{stream_name}_{start_time_str}.mp4")

    # Create a new VLC instance for streaming
    instance = vlc.Instance()
    media = instance.media_new(url)
    media_player = instance.media_player_new()
    media_player.set_media(media)
    
    # Start streaming
    media_player.play()
    print(f"Streaming {stream_name}...")

    # Set VLC options for recording
    options = f":sout=#transcode{{vcodec=h264,acodec=mp3}}:file{{dst={output_file},mux=mp4}}"
    media.add_options(options)
    
    # Start recording
    media_player.set_media(media)
    media_player.play()
    print(f"Recording {stream_name} started...")

    # Record for a specific duration
    record_duration = record_time_min * 60  # Convert minutes to seconds
    start_time = time.time()

    while time.time() - start_time < record_duration:
        if keyboard.is_pressed('q'):
            print(f"Stopping {stream_name} recording...")
            media_player.stop()
            break
        time.sleep(1)

    if media_player.is_playing():
        media_player.stop()
    
    print(f"Recording of {stream_name} complete.")
    instance.release()  # Release the VLC instance after recording

def exit_program():
    while True:
        if keyboard.is_pressed('q'):
            print("Exiting the program...")
            os._exit(0)  # Exit the terminal cleanly
        time.sleep(0.1)

def main():
    utils()  # Initialize VLC settings

    record_time_min = 1  # Set the recording duration in minutes
    output_path = "C:/Users/MSI/Documents/GitHub/susu_summer24/hand_tracking_@_assesment/recordings"

    # Ensure the recordings directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Start a thread to monitor for 'q' key press
    exit_thread = threading.Thread(target=exit_program, daemon=True)
    exit_thread.start()

    while True:
        # Check which streams are active
        active_streams = check_stream_active()
        
        # Create threads for streaming and recording for each active stream
        stream_threads = []
        for stream, is_active in active_streams.items():
            if is_active:
                url = rtsp_streams[stream]
                thread = threading.Thread(target=stream_and_record, args=(stream, url, record_time_min, output_path))
                stream_threads.append(thread)
                thread.start()

        # Wait for all stream threads to finish
        for thread in stream_threads:
            thread.join()

if __name__ == '__main__':
    main()
