import cv2
import mediapipe as mp
import time
import threading
import logging

# Define dictionary with multiple RTSP stream URLs
rtsp_streams = {
    'feed1': 'rtsp://UmZF6h:atAIz1ecLgC8@192.168.1.127:554/live/ch1',
    'feed2': 'rtsp://TK1Xnf:LbAiQiGLPvRd@192.168.1.174:554/live/ch1',
    'feed3': 'rtsp://4kkzxW:hDneHFEeidTc@192.168.1.123:554/live/ch1',
    #'feed4': 'rtsp://eg20N4:qSaBHlWuRnDM@192.168.1.174:554/live/ch1',
    'feed5': 'rtsp://Z6WjWa:H48qMg7phOQC@192.168.1.223:554/live/ch1',
    'feed6': 'rtsp://vm4fKG:9q9c0v1TFGT1@192.168.1.64:554/live/ch1'
}

# Initialize MediaPipe hands and drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def process_stream(key, url, logging_enabled=True):
    # Setup logging to a text file if logging is enabled
    if logging_enabled:
        log_filename = f'streamlog_{key[-1]}.txt'  # e.g., streamlog_1.txt for feed1
        logging.info(f"#### Log time: {time.strftime('%H:%M:%S')} - Start logging hand landmarks")
        with open(log_filename, 'a') as file:
            file.write(f"#### Log time: {time.strftime('%H:%M:%S')} - Start logging hand landmarks\n")
    
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        logging.error(f"Error: Unable to open stream {key}")
        return
    
    window_title = f"Factory Floor - Feed {key[-1]}"  # e.g., Factory Floor - Feed 1

    with mp_hands.Hands(
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as hands:
        
        while True:
            ret, frame = cap.read()
            if not ret:
                logging.error(f"Error: Unable to read frame from stream {key}")
                break
            
            # Process the frame
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    # Log hand landmarks detection if logging is enabled
                    if logging_enabled:
                        logging.info(f"Hand landmarks detected in stream {key}")

            # Display the frame with the custom window title
            cv2.imshow(window_title, image)

            # Handle key events
            key_pressed = cv2.waitKey(1) & 0xFF
            if key_pressed == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

    if logging_enabled:
        logging.info(f"#### Log time: {time.strftime('%H:%M:%S')} - End logging hand landmarks")
        with open(log_filename, 'a') as file:
            file.write(f"#### Log time: {time.strftime('%H:%M:%S')} - End logging hand landmarks\n")

# Create threads for each stream
threads = []
for key, url in rtsp_streams.items():
    thread = threading.Thread(target=process_stream, args=(key, url))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()
