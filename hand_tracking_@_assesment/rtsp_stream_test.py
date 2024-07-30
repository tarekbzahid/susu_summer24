import os
import ctypes
import vlc
import time

def utils():
    # Set the path to the VLC installation directory
    vlc_path = r'C:/Program Files/VideoLAN/VLC'
    os.add_dll_directory(vlc_path)

    # Set the full path to the libvlc.dll file
    libvlc_dll = os.path.join(vlc_path, 'libvlc.dll')
    ctypes.CDLL(libvlc_dll)

def main():
    utils()  # Initialize VLC settings

    # Define RTSP stream for feed5
    rtsp_feed5 = 'rtsp://4kkzxW:hDneHFEeidTc@192.168.1.123:554/live/ch1'

    # Create a VLC instance and media player for the RTSP feed
    instance = vlc.Instance()
    media = instance.media_new(rtsp_feed5)
    player = instance.media_player_new()
    player.set_media(media)

    # Start streaming
    player.play()
    print("Streaming from feed...")

    try:
        # Keep the stream open
        while True:
            time.sleep(1)  # Sleep for a while to keep the script running
    except KeyboardInterrupt:
        print("Stopping the stream...")

    # Clean up
    player.stop()
    instance.release()
    print("Stream stopped.")

if __name__ == '__main__':
    main()
