from ultralytics import YOLO
import cv2
from gps_tracker import get_gps_location
from datetime import datetime


# Load YOLO model
model = YOLO("yolo26n.pt")


# Fresh mission log for the current run
log_file = "sar_alerts.txt"

with open(log_file, "w", encoding="utf-8") as file:
    file.write("MISSION-SAR ALERT LOG\n")
    file.write("=====================\n\n")


# Global alert counter
total_alerts = 0


# Three test videos
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

    print()
    print("======================================")
    print("Processing:", video_path)
    print("======================================")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video:", video_path)
        continue


    # Get video information
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)


    if fps == 0:
        fps = 30


    # Create output filename
    if video_path == "test_video.mp4":
        output_path = "sar_output.mp4"
    elif video_path == "videos/easy_test.mp4":
        output_path = "easy_test_output.mp4"
    else:
        output_path = "medium_test_output.mp4"


    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    out = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (frame_width, frame_height)
    )


    # SAR alert variables
    previous_count = 0
    change_frames = 0
    REQUIRED_FRAMES = 5
    frame_number = 0


    while True:

        ret, frame = cap.read()

        if not ret:
            break


        frame_number += 1


        # YOLO person tracking
        results = model.track(
            frame,
            persist=True,
            conf=0.5,
            tracker="bytetrack.yaml",
            verbose=False
        )


        # Store person tracking IDs
        person_ids = []


        if results[0].boxes.id is not None:

            track_ids = results[0].boxes.id.int().cpu().tolist()
            classes = results[0].boxes.cls.int().cpu().tolist()


            for track_id, class_id in zip(track_ids, classes):

                if class_id == 0:
                    person_ids.append(track_id)


        # Count unique people
        current_count = len(set(person_ids))


        # Detect potential obstacles
        obstacle_detected = False
        direction = "NONE"


        for box in results[0].boxes:

            class_id = int(box.cls[0])
            class_name = model.names[class_id]


            if class_name in obstacle_classes:

                obstacle_detected = True


                # Get obstacle bounding box
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()


                # Find obstacle center
                obstacle_center_x = (x1 + x2) / 2


                # Divide frame into three zones
                if obstacle_center_x < frame_width / 3:
                    direction = "LEFT"

                elif obstacle_center_x < (frame_width * 2 / 3):
                    direction = "CENTER"

                else:
                    direction = "RIGHT"


                break


        # Check for people count change
        if current_count != previous_count:
            change_frames += 1
        else:
            change_frames = 0


        # Create SAR alert after 5 consecutive changed frames
        if change_frames >= REQUIRED_FRAMES:

            total_alerts += 1


            # Get simulated GPS location
            latitude, longitude = get_gps_location()


            # Get current time
            current_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )


            # Print alert
            print()
            print("🚨 SAR ALERT!")
            print("Video:", video_path)
            print("Time:", current_time)
            print("Frame:", frame_number)
            print("People:", current_count)
            print(
                f"GPS: {latitude:.6f}, {longitude:.6f}"
            )


            # Save alert to log file
            with open(log_file, "a", encoding="utf-8") as file:

                file.write(f"ALERT {total_alerts}\n")
                file.write(f"Video: {video_path}\n")
                file.write(f"Time: {current_time}\n")
                file.write(f"Frame: {frame_number}\n")
                file.write(
                    f"Previous people: {previous_count}\n"
                )
                file.write(
                    f"Current people: {current_count}\n"
                )
                file.write(
                    f"GPS Latitude: {latitude:.6f}\n"
                )
                file.write(
                    f"GPS Longitude: {longitude:.6f}\n"
                )
                file.write("------------------------\n")


            # Reset alert condition
            previous_count = current_count
            change_frames = 0


        # Annotated frame
        annotated_frame = results[0].plot()


        # Show people count
        cv2.putText(
            annotated_frame,
            f"People: {current_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )


        # Show obstacle status
        if obstacle_detected:
            obstacle_text = "OBSTACLE DETECTED"
        else:
            obstacle_text = "PATH CLEAR"


        cv2.putText(
            annotated_frame,
            obstacle_text,
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )


        # Show direction
        cv2.putText(
            annotated_frame,
            f"Direction: {direction}",
            (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )


        # Write frame to output video
        out.write(annotated_frame)


    # Release video resources
    cap.release()
    out.release()


    print("Output created:", output_path)


print()
print("======================================")
print("MISSION-SAR FINAL SYSTEM COMPLETE")
print("All 3 videos processed!")
print("Total SAR Alerts:", total_alerts)
print("======================================")