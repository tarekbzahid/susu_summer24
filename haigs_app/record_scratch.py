import os
import ctypes
import vlc
import threading
import time
import keyboard
from datetime import datetime, time as dt_time
import argparse
import sys

def utils():
    # Set the path to the VLC installation directory
    vlc_path = r'C:/Program Files/VideoLAN/VLC'
    os.add_dll_directory(vlc_path)

    # Set the full path to the libvlc.dll file
    libvlc_dll = os.path.join(vlc_path, 'libvlc.dll')
    ctypes.CDLL(libvlc_dll)

def read_rtsp_streams(file_path):
    rtsp_streams = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                name, url = line.strip().split(':', 1)
                rtsp_streams[name] = url
    return rtsp_streams

def check_stream_active(rtsp_streams):
    active_streams = {}
    instance = vlc.Instance()

    print("Checking for active stream connections...")
    try:
        for key, url in rtsp_streams.items():
            media = instance.media_new(url)
            media_player = instance.media_player_new()
            media_player.set_media(media)

            # Redirect stderr to suppress VLC error messages
            with open(os.devnull, 'w') as devnull:
                stderr_fd = os.dup(2)
                os.dup2(devnull.fileno(), 2)
                try:
                    # Try to play the media to check if the stream is active
                    media_player.play()
                    time.sleep(1)  # Wait for the stream to attempt to connect

                    # Check if the stream is playing
                    active_streams[key] = media_player.is_playing()
                finally:
                    os.dup2(stderr_fd, 2)
                    os.close(stderr_fd)
                media_player.stop()  # Stop the media player after checking

    finally:
        instance.release()  # Release the VLC instance

    print("Stream connections checked. Active streams:", active_streams)
    return active_streams

def create_stream_instance(active_streams, rtsp_streams):
    # Create parallel instances for each active stream
    media_players = {}
    for stream, is_active in active_streams.items():
        if is_active:
            instance = vlc.Instance()
            media = instance.media_new(rtsp_streams[stream])
            media_player = instance.media_player_new()
            media_player.set_media(media)
            media_player.play()
            time.sleep(2)
            media_players[stream] = media_player
            print(f"Connected to {stream}")
        else:
            print(f"Failed to connect to {stream}")
    return media_players

def record_stream(media_player, stream_name, record, record_time_min, output_path):
    if not record:
        print(f"Recording is disabled for {stream_name}.")
        return

    # Create a timestamp for the output file
    start_time_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_file = os.path.join(output_path, f"{stream_name}_{start_time_str}.mp4")

    # Set VLC options for recording
    options = f":sout=#transcode{{acodec=mp3}}:file{{dst={output_file},mux=mp4}}"
    media = media_player.get_media()  # Get the current media
    media.add_options(options)  # Add options for recording

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

def is_within_non_recording_period(current_time, non_record_start, non_record_end):
    """ Check if the current time is within the non-recording period """
    if non_record_end < non_record_start:  # Non-recording period spans midnight
        return (current_time.time() >= non_record_start) or (current_time.time() <= non_record_end)
    return non_record_start <= current_time.time() <= non_record_end

def main():
    parser = argparse.ArgumentParser(description="RTSP Stream Recorder")
    parser.add_argument('--feeds_file', type=str, default='feeds.txt', help='Path to the file containing RTSP feeds')
    parser.add_argument('--record_time_min', type=int, default=1, help='Duration to record each stream in minutes')
    parser.add_argument('--record_max_time_min', type=int, default=100, help='Maximum duration before the recording session ends')
    parser.add_argument('--non_record_start', type=str, default='11:19', help='Start time of non-recording period in HH:MM format')
    parser.add_argument('--non_record_end', type=str, default='11:20', help='End time of non-recording period in HH:MM format')

    args = parser.parse_args()
  
    utils()  # Initialize VLC settings

    record = True  # Set to True to enable recording

    # Ensure the recordings directory exists in the current working directory
    output_path = os.path.join(os.getcwd(), "recordings")
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Start a thread to monitor for 'q' key press
    exit_thread = threading.Thread(target=exit_program, daemon=True)
    exit_thread.start()

    rtsp_streams = read_rtsp_streams(args.feeds_file)

    # Parse non-recording period times
    non_record_start = dt_time.fromisoformat(args.non_record_start)
    non_record_end = dt_time.fromisoformat(args.non_record_end)

    # Track the overall session start time
    session_start_time = time.time()
    max_record_duration = args.record_max_time_min * 60  # Convert minutes to seconds

    while True:
        # Check if the overall session time has exceeded the max duration
        if time.time() - session_start_time >= max_record_duration:
            print("Maximum recording session time reached. Stopping all recordings.")
            break

        current_time = datetime.now()
        if is_within_non_recording_period(current_time, non_record_start, non_record_end):
            print(f"Current time {current_time.time()} is within non-recording period.")
            time.sleep(60)  # Wait before re-checking
            continue

        # Check which streams are active
        active_streams = check_stream_active(rtsp_streams)
        media_players = create_stream_instance(active_streams, rtsp_streams)

        # Record streams that are active
        record_threads = []
        for stream, player in media_players.items():
            record_thread = threading.Thread(target=record_stream, args=(player, stream, record, args.record_time_min, output_path))
            record_threads.append(record_thread)
            record_thread.start()

        # Wait for all recording threads to finish
        for thread in record_threads:
            thread.join()

if __name__ == '__main__':
    main()
