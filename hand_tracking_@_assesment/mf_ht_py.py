import cv2
import mediapipe as mp
import time
import numpy as np

# Define dictionary with multiple RTSP stream URLs
rtsp_streams = {
    'feed1': 'rtsp://UmZF6h:atAIz1ecLgC8@192.168.1.127:554/live/ch1',
    'feed2': 'rtsp://TK1Xnf:LbAiQiGLPvRd@192.168.1.174:554/live/ch1',
    'feed3': 'rtsp://4kkzxW:hDneHFEeidTc@192.168.1.123:554/live/ch1'
}

# Initialize MediaPipe hands and drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Connect to the RTSP streams
caps = {key: cv2.VideoCapture(url) for key, url in rtsp_streams.items()}

if not all(cap.isOpened() for cap in caps.values()):
    print("Error: Unable to open one or more video streams")
    exit()

# Initialize variables for FPS calculation
prev_frame_time = 0
new_frame_time = 0

with mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7) as hands:
    
    while all(cap.isOpened() for cap in caps.values()):
        frames = {}
        for key, cap in caps.items():
            ret, frame = cap.read()
            if not ret:
                print(f"Error: Unable to read frame from feed {key}")
                break
            frames[key] = frame
        
        if len(frames) != len(caps):
            break

        # Calculate FPS
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time

        # Convert the FPS to an integer
        fps = int(fps)

        # Convert the frame rate to a string
        fps_text = "FPS: " + str(fps)

        processed_frames = []
        for key, image in frames.items():
            # Process the image
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            cv2.putText(image, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(image, f"feed: {key}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            processed_frames.append(image)

        # Ensure we have exactly 4 frames for the 2x2 grid
        blank_frame = np.zeros_like(processed_frames[0])
        while len(processed_frames) < 4:
            processed_frames.append(blank_frame)

        # Arrange frames in a 2x2 grid
        top_row = cv2.hconcat([processed_frames[0], processed_frames[1]])
        bottom_row = cv2.hconcat([processed_frames[2], processed_frames[3]])
        combined_image = cv2.vconcat([top_row, bottom_row])

        # Display the combined frame
        cv2.imshow('RTSP Streams with MediaPipe Hands and FPS', combined_image)

        # Handle key events
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

# Release all resources
for cap in caps.values():
    cap.release()
cv2.destroyAllWindows()
