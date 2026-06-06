import cv2  # webcam aur image ke liye
import face_recognition  # face detect aur recognize karne ke liye
import numpy as np  # comparison ke liye
import csv  # attendance save karne ke liye
import os
from datetime import datetime  # date aur time ke liye

# known faces ka folder
KNOWN_FACES_DIR = "known_faces"
ATTENDANCE_FILE = "attendance.csv"

print("--- Facial Recognition Attendance System ---")

# known faces load karne ka function
def load_faces():
    encodings = []
    names = []
    
    # folder nahi hai toh bana do
    if not os.path.exists(KNOWN_FACES_DIR):
        os.makedirs(KNOWN_FACES_DIR)
        print(f"'{KNOWN_FACES_DIR}' folder banaya!")
        print("Isme student photos daalo aur restart karo.")
        return encodings, names
    
    print("Known faces load ho rahe hain...")
    
    for file in os.listdir(KNOWN_FACES_DIR):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(KNOWN_FACES_DIR, file)
            
            img = face_recognition.load_image_file(path)
            enc = face_recognition.face_encodings(img)
            
            if enc:
                encodings.append(enc[0])
                name = os.path.splitext(file)[0]  # filename hi naam hai
                names.append(name)
                print(f"Loaded: {name}")
            else:
                print(f"Face nahi mila: {file}")
    
    print(f"\nTotal {len(names)} faces loaded!\n")
    return encodings, names

# attendance mark karne ka function
def mark_attendance(name):
    today = datetime.now().strftime("%Y-%m-%d")
    time_now = datetime.now().strftime("%H:%M:%S")
    
    # pehle check karo aaj already mark hua hai ya nahi
    already_marked = set()
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2 and row[1] == today:
                    already_marked.add(row[0])
    
    # agar already mark nahi hua toh mark karo
    if name not in already_marked:
        with open(ATTENDANCE_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            
            # pehli baar file hai toh header likho
            if not os.path.exists(ATTENDANCE_FILE) or os.path.getsize(ATTENDANCE_FILE) == 0:
                writer.writerow(["Name", "Date", "Time"])
            
            writer.writerow([name, today, time_now])
        
        print(f"Attendance marked: {name} at {time_now}")
        return True
    
    return False  # already marked

# webcam se attendance lene ka function
def start_attendance(known_encodings, known_names):
    if not known_encodings:
        print("Pehle known_faces folder mein photos daalo!")
        return
    
    # webcam open karo
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Camera nahi mila!")
        return
    
    print("Camera on hai. Q dabao band karne ke liye.\n")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # frame chhota karo - fast processing ke liye
        small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)  # BGR to RGB
        
        # frame mein faces dhundo
        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)
        
        for encoding, location in zip(encodings, locations):
            # known faces se compare karo
            matches = face_recognition.compare_faces(known_encodings, encoding)
            distances = face_recognition.face_distance(known_encodings, encoding)
            
            name = "Unknown"
            color = (0, 0, 255)  # red for unknown
            
            if True in matches:
                # sabse close match lo
                best = np.argmin(distances)
                if matches[best]:
                    name = known_names[best]
                    color = (0, 255, 0)  # green for recognized
                    mark_attendance(name)
            
            # coordinates scale back karo
            top, right, bottom, left = location
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            # face ke around box banao
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # naam dikhao
            cv2.rectangle(frame, (left, bottom - 30), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 5, bottom - 8),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        cv2.imshow("Attendance System - Q to Quit", frame)
        
        # Q dabane pe band ho
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Camera band ho gaya.")

# attendance records dikhane ka function
def view_attendance():
    if not os.path.exists(ATTENDANCE_FILE):
        print("Koi attendance record nahi mila!")
        return
    
    print("\n--- Attendance Records ---")
    with open(ATTENDANCE_FILE, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                print("  |  ".join(row))
    print("--------------------------")

# faces load karo
known_encodings, known_names = load_faces()

# main menu
while True:
    print("\n1. Start Attendance (Webcam)")
    print("2. View Attendance Records")
    print("3. Exit")
    
    choice = input("Enter choice: ")
    
    if choice == "1":
        start_attendance(known_encodings, known_names)
        
    elif choice == "2":
        view_attendance()
        
    elif choice == "3":
        print("Bye!")
        break
    else:
        print("Invalid choice!")
