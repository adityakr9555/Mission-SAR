from ultralytics import YOLO
import cv2
from gps_tracker import get_gps_location
from datetime import datetime


# Load YOLO model
model = YOLO("yolo26n.pt")


# Open input video
cap = cv2.VideoCapture("videos/medium_test.mp4")


# Get video properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)


# Create output video
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

out = cv2.VideoWriter(
    "medium_test_output.mp4",
    fourcc,
    fps,
    (width, height)
)


# Previous stable people count
previous_count = 0

alert_count = 0

change_frames = 0

frame_number = 0


# Number of frames required before generating alert
REQUIRED_FRAMES = 5


while True:

    # Read one frame
    ret, frame = cap.read()
    frame_number += 1


    # Stop when video ends
    if not ret:
        break


    # Detect and track people
    results = model.track(
        frame,
        persist=True,
        conf=0.5,
        tracker="bytetrack.yaml",
        classes=[0],
        verbose=False
    )


    # Current number of people
    current_count = 0


    # Check whether detection boxes exist
    if results[0].boxes is not None:

        # Check whether tracking IDs exist
        if results[0].boxes.id is not None:

            track_ids = results[0].boxes.id.int().cpu().tolist()

            current_count = len(track_ids)


    # Draw YOLO boxes and tracking information
    annotated_frame = results[0].plot()


    # Check whether people count changed
    if current_count != previous_count:

        change_frames += 1

    else:

        change_frames = 0


    # Default status
    status = "SAR MONITORING"

    # Generate alert only after 5 consecutive changed frames
    if change_frames >= REQUIRED_FRAMES:

        status = "SAR ALERT - COUNT CHANGED"

        alert_count += 1
        latitude, longitude = get_gps_location()

        print(f"GPS Location: {latitude:.6f}, {longitude:.6f}")

        print("🚨 SAR ALERT TRIGGERED!")
        print(f"Previous people: {previous_count}")
        print(f"Current people: {current_count}")
        print(f"Total alerts: {alert_count}")
        print("------------------------")
        with open("sar_alerts.txt", "a") as log_file:

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            log_file.write(f"ALERT {alert_count}\n")
            log_file.write(f"Time: {current_time}\n")
            log_file.write(f"Frame: {frame_number}\n")
            log_file.write(f"Previous people: {previous_count}\n")
            log_file.write(f"Current people: {current_count}\n")
            log_file.write(f"GPS Latitude: {latitude:.6f}\n")
            log_file.write(f"GPS Longitude: {longitude:.6f}\n")
            log_file.write("------------------------\n")
        previous_count = current_count
        change_frames = 0


    # Display people count
    cv2.putText(
        annotated_frame,
        f"People: {current_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )


    # Display SAR status
    cv2.putText(
        annotated_frame,
        status,
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )


    # Display change frame counter
    cv2.putText(
        annotated_frame,
        f"Stable change frames: {change_frames}/{REQUIRED_FRAMES}",
        (20, 115),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 0),
        2
    )


    # Save processed frame
    out.write(annotated_frame)


    # Update previous count
    if change_frames >= REQUIRED_FRAMES:

        previous_count = current_count

        change_frames = 0


# Release video resources
cap.release()
out.release()


print("SMART SAR video created successfully!")