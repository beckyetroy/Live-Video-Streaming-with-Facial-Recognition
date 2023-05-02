from flask import Flask, render_template, Response
import cv2
import face_recognition
import numpy as np
app=Flask(__name__)
camera = cv2.VideoCapture(0)
# Load picture of person 1 and learn how to recognise it.
becky_image = face_recognition.load_image_file("Becky/Becky.jpeg")
becky_face_encoding = face_recognition.face_encodings(becky_image)[0]

# Load picture of person 2 and learn how to recognise it.
adam_image = face_recognition.load_image_file("Adam/Adam.jpeg")
adam_face_encoding = face_recognition.face_encodings(adam_image)[0]

# Load picture of person 3 and learn how to recognise it.
pedro_image = face_recognition.load_image_file("Pedro/Pedro.jpg")
pedro_face_encoding = face_recognition.face_encodings(pedro_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    becky_face_encoding,
    adam_face_encoding,
    pedro_face_encoding
]
known_face_names = [
    "Becky",
    "Adam",
    "Pedro"
]
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # Skip every other frame
            if process_this_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]
            
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)

                green = (0, 153, 51)
                white = (255, 255, 255)
                font = cv2.FONT_HERSHEY_SIMPLEX
                # Display the results
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    # Calculate the size of the text
                    name_size, _ = cv2.getTextSize(name, font, 1.0, 2)
                    match_size, _ = cv2.getTextSize('100% Match', font, 0.7, 2)

                    # Calculate the position of the name and match text
                    name_pos = ((left + right - name_size[0]) // 2, bottom)
                    match_pos = (left + 2, bottom + 25)

                    # Draw a box around the face
                    cv2.rectangle(frame, (left, top), (right, bottom + 30), green, 2)

                    # Draw the name and match text
                    cv2.rectangle(frame, (left, bottom - 10 - match_size[1]), (right, bottom + 35), green, cv2.FILLED)
                    cv2.putText(frame, name, name_pos, font, 1.0, white, 2)
                    if name != 'Unknown':
                        cv2.putText(frame, '100% Match', match_pos, font, 0.7, white, 2)

                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            process_this_frame = not process_this_frame

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=='__main__':
    app.run(debug=True)