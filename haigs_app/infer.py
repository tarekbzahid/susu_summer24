import cv2
from ultralytics import YOLO
import matplotlib.pyplot as plt
import argparse

# Function to perform inference on a single image
def infer_single_image(model, image_path):
    # Load the image using OpenCV
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Unable to read image '{image_path}'")
        return
    
    # Perform inference
    results = model(img)
    
    # Iterate through each result in the list
    for result in results[0].boxes:
        x1, y1, x2, y2 = map(int, result.xyxy[0])  # Extract the bounding box coordinates
        conf = result.conf.item()  # Convert tensor to float
        cls = result.cls.item()  # Convert tensor to int

        # Draw the bounding box
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue box with thickness 2
        cv2.putText(img, f'{model.names[int(cls)]} {conf:.2f}', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)  # Label with confidence
    
    # Display the annotated image
    cv2.imshow('Annotated Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    plt.imshow(img)
    plt.axis('off')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="YOLO Inference on a Single Image")
    parser.add_argument('model_path', type=str, help='Path to the YOLO model weights')
    parser.add_argument('image_path', type=str, help='Path to the input image')

    args = parser.parse_args()

    # Load the trained YOLO model
    model = YOLO(args.model_path)

    # Perform inference
    infer_single_image(model, args.image_path)

if __name__ == '__main__':
    main()
