import os
import ctypes
import vlc
import threading
import time
import keyboard
import argparse

def utils():
    vlc_path = r'C:/Program Files/VideoLAN/VLC'
    os.add_dll_directory(vlc_path)
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

def create_stream_instance(active_streams, rtsp_streams):
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

def calculate_frame_rate(media_player, stream_name):
    start_time = time.time()
    frame_count = 0

    while media_player.is_playing():
        frame_count += 1
        time.sleep(1)  # Adjust the sleep time if needed

        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            frame_rate = frame_count / elapsed_time
            print(f"Stream {stream_name}: Frame rate = {frame_rate:.2f} fps")

def exit_program():
    while True:
        if keyboard.is_pressed('q'):
            print("Exiting the program...")
            os._exit(0)
        time.sleep(0.1)

def main():
    parser = argparse.ArgumentParser(description="RTSP Stream Checker and Frame Rate Calculator")
    parser.add_argument('--refresh_time_min', type=int, default=10, help='Refresh time in minutes')
    parser.add_argument('--feeds_file', type=str, required=True, help='Path to the file containing RTSP feeds')

    args = parser.parse_args()

    rtsp_streams = read_rtsp_streams(args.feeds_file)
    refresh_time_min = args.refresh_time_min

    utils()

    exit_thread = threading.Thread(target=exit_program, daemon=True)
    exit_thread.start()

    while True:
        active_streams = check_stream_active(rtsp_streams)
        media_players = create_stream_instance(active_streams, rtsp_streams)

        frame_rate_threads = []
        for stream, player in media_players.items():
            frame_rate_thread = threading.Thread(target=calculate_frame_rate, args=(player, stream))
            frame_rate_threads.append(frame_rate_thread)
            frame_rate_thread.start()

        for thread in frame_rate_threads:
            thread.join()

        time.sleep(refresh_time_min * 60)  # Refresh the streams after the specified duration

if __name__ == '__main__':
    main()
