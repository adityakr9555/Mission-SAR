from ultralytics import YOLO
import cv2


# Load YOLO model
model = YOLO("yolo26n.pt")


# Three input videos
videos = [
    "test_video.mp4",
    "videos/easy_test.mp4",
    "videos/medium_test.mp4"
]


# Obstacle classes
obstacle_classes = [
    "bicycle",
    "car",
    "motorcycle",
    "bus",
    "truck",
    "chair",
    "bench",
    "suitcase"
]


# Process videos one by one
for video_path in videos:

    print("--------------------------------")
    print("Processing:", video_path)
    print("--------------------------------")


    # Open video
    cap = cv2.VideoCapture(video_path)


    # Check video
    if not cap.isOpened():

        print("Could not open:", video_path)
        continue


    while True:

        # Read frame
        ret, frame = cap.read()


        # Stop when video ends
        if not ret:
            break


        # Detect objects
        results = model(
            frame,
            conf=0.5,
            verbose=False
        )


        # Default values
        status = "PATH CLEAR"
        direction = "NONE"
        proximity = "NONE"


        # Check detected objects
        for box in results[0].boxes:

            class_id = int(box.cls[0])
            class_name = model.names[class_id]


            if class_name in obstacle_classes:

                status = "OBSTACLE DETECTED"


                # Bounding box
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()


                # Obstacle center
                obstacle_center_x = (x1 + x2) / 2


                # Frame width
                frame_width = frame.shape[1]


                # Direction
                if obstacle_center_x < frame_width / 3:

                    direction = "LEFT"

                elif obstacle_center_x < (frame_width * 2 / 3):

                    direction = "CENTER"

                else:

                    direction = "RIGHT"


                # Obstacle size
                box_width = x2 - x1
                box_height = y2 - y1

                box_area = box_width * box_height


                # Proximity estimate
                if box_area > 150000:

                    proximity = "VERY CLOSE"

                elif box_area > 60000:

                    proximity = "NEAR"

                else:

                    proximity = "FAR"


                break


        # Draw detections
        annotated_frame = results[0].plot()


        # Display status
        cv2.putText(
            annotated_frame,
            f"Status: {status}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )


        # Display direction
        cv2.putText(
            annotated_frame,
            f"Direction: {direction}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )


        # Display proximity
        cv2.putText(
            annotated_frame,
            f"Proximity: {proximity}",
            (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )


        # Show video
        cv2.imshow(
            "Mission-SAR Obstacle Detection",
            annotated_frame
        )


        # Q = quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


    # Close current video
    cap.release()


# Close everything
cv2.destroyAllWindows()


print("================================")
print("All 3 videos processed!")
print("================================")