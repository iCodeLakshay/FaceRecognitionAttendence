import os
import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime

video_capture = cv2.VideoCapture(0)

# Helper to load an image and return its encoding (or None)
def load_encoding(path):
    if not os.path.exists(path):
        print(f"Warning: image not found: {path}")
        return None
    img = face_recognition.load_image_file(path)
    encs = face_recognition.face_encodings(img)
    if not encs:
        print(f"Warning: no face found in image: {path}")
        return None
    return encs[0]

# Prepare known faces (adjust paths to your workspace)
known_face_encodings = []
known_face_names = []

# Example: try to load some images from the faces/ subfolders
candidates = [
    (os.path.join("faces", "lakshay.jpg"), "Lakshay"),
    (os.path.join("faces", "mummy.png"), "Neeraj"),
    (os.path.join("faces", "ayush.png"), "Ayush"),
]

for path, name in candidates:
    enc = load_encoding(path)
    if enc is not None:
        known_face_encodings.append(enc)
        known_face_names.append(name)

if not known_face_encodings:
    print("Error: no known face encodings were loaded. Exiting.")
    video_capture.release()
    raise SystemExit(1)

# List of expected Students
students = known_face_names.copy()

face_locations = []
face_encodings = []

# Get the current date and time
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(f"{current_date}.csv", "w+", newline="")
writer = csv.writer(f)
writer.writerow(["Name", "Time"])  # header

try:
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame from camera")
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)

            best_match_index = np.argmin(face_distance)
            name = "Unknown"
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                # Record attendance once per student
                if name in students:
                    time_now = datetime.now().strftime("%H:%M:%S")
                    writer.writerow([name, time_now])
                    f.flush()
                    print(f"Marked {name} at {time_now}")
                    students.remove(name)

        cv2.imshow("Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    f.close()
    video_capture.release()
    cv2.destroyAllWindows()
