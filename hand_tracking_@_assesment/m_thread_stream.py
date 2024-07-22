import cv2
import mediapipe as mp
import time
import numpy as np
import threading

# Define dictionary with multiple RTSP stream URLs
rtsp_streams = {
    'feed1': 'rtsp://UmZF6h:atAIz1ecLgC8@192.168.1.127:554/live/ch1',
    'feed2': 'rtsp://TK1Xnf:LbAiQiGLPvRd@192.168.1.174:554/live/ch1',
    'feed3': 'rtsp://4kkzxW:hDneHFEeidTc@192.168.1.123:554/live/ch1'
}

# Initialize MediaPipe hands and drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Function to process frames from a single stream
def process_stream(key, url, prev_frame_time):
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print(f"Error: Unable to open stream {key}")
        return
    
    with mp_hands.Hands(
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as hands:
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print(f"Error: Unable to read frame from stream {key}")
                break
            
            # Calculate FPS
            new_frame_time = time.time()
            fps = 1 / (new_frame_time - prev_frame_time)
            prev_frame_time = new_frame_time

            # Process the frame
            image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Add FPS text
            fps_text = "FPS: " + str(int(fps))
            cv2.putText(image, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(image, f"feed: {key}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Display the frame
            cv2.imshow(f'Stream {key} with MediaPipe Hands', image)

            # Handle key events
            key_pressed = cv2.waitKey(1) & 0xFF
            if key_pressed == ord('q'):
                break

    cap.release()

# Create threads for each stream
threads = []
prev_frame_time = {key: time.time() for key in rtsp_streams.keys()}
for key, url in rtsp_streams.items():
    thread = threading.Thread(target=process_stream, args=(key, url, prev_frame_time[key]))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Clean up
cv2.destroyAllWindows()
