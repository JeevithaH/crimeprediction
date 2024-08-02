from ultralytics import YOLO
import cv2

def live_weapon_detection():
    # Load YOLO model
    model = YOLO(r"D:\crime_03_16 (1)\crime_03_16\best.pt")

    # Capture video from source 0 (webcam)
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # Perform object detection
        results = model(frame)

        # Check if there are any detections
        if isinstance(results, list) and len(results) > 0:
            first_result = results[0]

            # Check if this result has the expected attribute (e.g., xyxy)
            if hasattr(first_result, 'xyxy') and first_result.xyxy.shape[0] > 0:
                # Iterate through each detection
                for pred in first_result.xyxy:
                    label = int(pred[5])
                    conf = pred[4]
                    if conf > 0.5:  # Set a confidence threshold
                        xmin, ymin, xmax, ymax = map(int, pred[:4])
                        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                        cv2.putText(frame, f"Class: {label}, Conf: {conf:.2f}", (xmin, ymin - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame with bounding boxes
        cv2.imshow('Object Detection', frame)

        # Check for the 'q' key to exit the loop
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q') or cv2.getWindowProperty('Object Detection', cv2.WND_PROP_VISIBLE) < 1:
            break

    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


live_weapon_detection()