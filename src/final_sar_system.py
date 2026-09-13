from ultralytics import YOLO
import cv2
from gps_tracker import get_gps_location
from datetime import datetime


# Load YOLO model
model = YOLO("yolo26n.pt")


# Three videos
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


# Process all videos
for video_path in videos:

    print("\n==============================")
    print("Processing:", video_path)
    print("==============================")


    # Open video
    cap = cv2.VideoCapture(video_path)


    if not cap.isOpened():

        print("Could not open:", video_path)
        continue


    # Previous people count
    previous_count = 0

    # Count frames where people count changes
    change_frames = 0

    # Required stable frames
    REQUIRED_FRAMES = 5

    # Total SAR alerts
    alert_count = 0


    while True:

        # Read frame
        ret, frame = cap.read()


        if not ret:
            break


        # YOLO tracking
        results = model.track(
            frame,
            persist=True,
            conf=0.5,
            tracker="bytetrack.yaml",
            verbose=False
        )


        # -------------------------
        # PERSON DETECTION
        # -------------------------

        person_ids = []


        if results[0].boxes.id is not None:

            track_ids = results[0].boxes.id.int().cpu().tolist()
            classes = results[0].boxes.cls.int().cpu().tolist()


            for track_id, class_id in zip(track_ids, classes):

                if class_id == 0:

                    person_ids.append(track_id)


        current_count = len(set(person_ids))


        # -------------------------
        # SAR ALERT LOGIC
        # -------------------------

        if current_count != previous_count:

            change_frames += 1

        else:

            change_frames = 0


        if change_frames >= REQUIRED_FRAMES:

            alert_count += 1


            latitude, longitude = get_gps_location()


            current_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )


            print("\n🚨 SAR ALERT!")
            print("Video:", video_path)
            print("Time:", current_time)
            print("People:", current_count)
            print(
                f"GPS: {latitude:.6f}, {longitude:.6f}"
            )


            # Reset
            previous_count = current_count
            change_frames = 0


        # -------------------------
        # OBSTACLE DETECTION
        # -------------------------

        obstacle_status = "PATH CLEAR"
        direction = "NONE"
        proximity = "NONE"


        for box in results[0].boxes:

            class_id = int(box.cls[0])
            class_name = model.names[class_id]


            if class_name in obstacle_classes:

                obstacle_status = "OBSTACLE DETECTED"


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


                # Proximity
                if box_area > 150000:

                    proximity = "VERY CLOSE"

                elif box_area > 60000:

                    proximity = "NEAR"

                else:

                    proximity = "FAR"


                break


        # -------------------------
        # DRAW RESULTS
        # -------------------------

        annotated_frame = results[0].plot()


        # People count
        cv2.putText(
            annotated_frame,
            f"People: {current_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )


        # Obstacle status
        cv2.putText(
            annotated_frame,
            f"Obstacle: {obstacle_status}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )


        # Direction
        cv2.putText(
            annotated_frame,
            f"Direction: {direction}",
            (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )


        # Proximity
        cv2.putText(
            annotated_frame,
            f"Proximity: {proximity}",
            (20, 145),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )


        # Show video
        cv2.imshow(
            "Mission-SAR Final System",
            annotated_frame
        )


        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):

            cap.release()
            


    # Release current video
    cap.release()


cv2.destroyAllWindows()


print("\n================================")
print("MISSION-SAR FINAL SYSTEM COMPLETE")
print("All 3 videos processed!")
print("================================")