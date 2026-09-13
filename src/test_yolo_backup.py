from ultralytics import YOLO
import cv2

# Load YOLO model
model = YOLO("yolo26n.pt")

# Open input video
cap = cv2.VideoCapture("test_video.mp4")

# Get video properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Create output video
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(
    "sar_output.mp4",
    fourcc,
    fps,
    (width, height)
)

previous_count = 0

while True:

    # Read one frame
    ret, frame = cap.read()

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

    current_count = 0

    # Check detected people
    if results[0].boxes is not None:
        if results[0].boxes.id is not None:

            track_ids = results[0].boxes.id.int().cpu().tolist()
            current_count = len(track_ids)

    # Draw YOLO detections
    annotated_frame = results[0].plot()

    # Check if people count changed
    if current_count != previous_count:
        status = "SAR ALERT - COUNT CHANGED"
    else:
        status = "SAR MONITORING"

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

    # Save frame to output video
    out.write(annotated_frame)

    # Update previous count
    previous_count = current_count

# Release everything
cap.release()
out.release()

print("SMART SAR video created successfully!")