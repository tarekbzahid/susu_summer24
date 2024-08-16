'''
This script processes all videos in a specified input folder to extract hand landmarks (XYZ coordinates)
using MediaPipe. The extracted landmarks are saved in CSV files within a local folder named 'landmark_extracts'.
The script supports detecting up to two hands in each video, and it includes the hand index in the output 
to differentiate between the two hands.

Usage:
    python extract_hand_landmarks.py /path/to/input/folder

The output CSV files will be saved in the 'landmark_extracts' folder in the same directory where the script is run.
'''

import cv2
import mediapipe as mp
import os
import argparse

def process_video(video_path, output_folder):
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,
                           max_num_hands=2,  # Limit to 2 hands
                           min_detection_confidence=0.5,
                           min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video source: {video_path}")
        return

    file_name = os.path.splitext(os.path.basename(video_path))[0]
    output_file = os.path.join(output_folder, f'hand_landmarks_{file_name}.csv')

    with open(output_file, 'w') as f:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print(f"Finished processing {video_path}")
                break

            # Convert the BGR image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame with MediaPipe Hands
            result = hands.process(rgb_frame)

            # Extract hand landmarks
            if result.multi_hand_landmarks:
                for hand_index, hand_landmarks in enumerate(result.multi_hand_landmarks):
                    for idx, landmark in enumerate(hand_landmarks.landmark):
                        # Get landmark coordinates
                        landmark_x = int(landmark.x * frame.shape[1])
                        landmark_y = int(landmark.y * frame.shape[0])
                        landmark_z = landmark.z  # Z-coordinate (depth)

                        # Write coordinates to the CSV file
                        f.write(f"hand_{hand_index},landmark_{idx},{landmark_x},{landmark_y},{landmark_z}\n")

    cap.release()
    hands.close()

def main():
    parser = argparse.ArgumentParser(description="Process videos to extract hand landmark XYZ values.")
    parser.add_argument('input_folder', type=str, help="Path to the folder containing videos")
    args = parser.parse_args()

    # Set output folder to 'landmark_extracts'
    output_folder = 'landmark_extracts'
    os.makedirs(output_folder, exist_ok=True)

    # Process all videos in the input folder
    for video_file in os.listdir(args.input_folder):
        if video_file.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            video_path = os.path.join(args.input_folder, video_file)
            process_video(video_path, output_folder)

if __name__ == "__main__":
    main()
