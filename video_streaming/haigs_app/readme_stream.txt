# README: RTSP Stream Script

This script streams video feeds from RTSP URLs specified in a text file. It checks the connection status of each feed and displays the results.

## How to Add Feeds

1. **Modify the Feeds File**:
   - Open a text editor (like Notepad).
   - Add your camera feeds in this format:
     stream_name:rtsp://username:password@ip_address:port/live/channel
   - **Example**:
     first_floor_camera:rtsp://UmZF6h:atAIz1ecLgC8@192.168.1.127:554/live/ch1
   - Save the file as `feeds`.

2. **Place the Files in the Same Directory**:
   - Ensure that both `feeds` and `stream.py` are in the following directory:
     C:\Users\MSI\Desktop\haigs_app

## How to Run the Script

1. **Open PowerShell**:
   - Press `Win + X` and select "Windows PowerShell".

2. **Navigate to the Directory**:
   - Type the following command and press Enter:

     cd C:\Users\MSI\Desktop\haigs_app

3. **Run the Script**:
   - Execute the following command:

     python stream.py --refresh_time_min 10 --feeds_file feeds

   - The `--refresh_time_min` option specifies how often (in minutes) the script checks the connection status of each stream. For example, setting it to `10` means the script will check every 10 minutes.

## Stopping the Program

- To exit the program, press the `q` key on your keyboard.

## Troubleshooting

- **Connection Issues**: If the script cannot connect to a stream, verify the RTSP URL and ensure the camera is powered on and connected to the network.
- **No Output**: Ensure VLC is installed and properly configured.
