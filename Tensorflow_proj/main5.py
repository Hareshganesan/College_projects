import cv2
import torch

# Set device for running the model
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

# Load pre-trained YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.to(device)

# Initialize OpenCV video capture object
cap = cv2.VideoCapture(0)

# Initialize a list to store the detected bottle bounding boxes
previous_bottles = []

bottle_count = 0

while True:
    ret, frame = cap.read()

    # Perform object detection on the current frame
    results = model(frame)

    current_bottles = []
    for result in results.xyxy[0]:
        x1, y1, x2, y2, conf, cls = result
        if model.names[int(cls)] == 'bottle':  # Only detect bottles
            current_bottles.append((int(x1), int(y1), int(x2), int(y2)))

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"Bottle {conf:.2f}", (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Check for new bottles
    for current_bottle in current_bottles:
        overlap = False
        for previous_bottle in previous_bottles:
            if (current_bottle[0] < previous_bottle[2] and
                current_bottle[2] > previous_bottle[0] and
                current_bottle[1] < previous_bottle[3] and
                current_bottle[3] > previous_bottle[1]):
                overlap = True
                break
        if not overlap:
            bottle_count += 1

    # Update previous bottles
    previous_bottles = current_bottles

    # Display the resulting frame with bottle count
    cv2.putText(frame, f"Bottle Count: {bottle_count}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow('Real-time Bottle Detection', frame)

    # Exit on pressing 'q' key
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture object and close all windows
cap.release()
cv2.destroyAllWindows()