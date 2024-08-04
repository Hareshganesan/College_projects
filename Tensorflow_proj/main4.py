import cv2
import torch

# Set device for running the model
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

# Load pre-trained YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.to(device)

# Initialize OpenCV video capture object
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    print(frame)

    # Perform object detection on the current frame
    results = model(frame)

    for result in results.xyxy[0]:
        x1, y1, x2, y2, conf, cls = result
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, f"{model.names[int(cls)]} {conf:.2f}", (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Real-time Object Detection', frame)

    # Exit on pressing 'q' key
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture object and close all windows
cap.release()
cv2.destroyAllWindows()