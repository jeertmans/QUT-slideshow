import face_recognition
import numpy as np
import os
import cv2
from PIL import Image

# https://github.com/ageitgey/face_recognition/blob/master/examples/face_recognition_svm.py
# https://github.com/ageitgey/face_recognition

def load_knowns(dirpath):
    names = []
    encodings = []
    for basename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, basename)
        name = os.path.splitext(basename)[0]
        names.append(name)
        image = face_recognition.load_image_file(filepath)
        encoding = face_recognition.face_encodings(image)[0]
        encodings.append(encoding)

    return names, encodings

print("Loading known people... ", end='')
known_names, known_encodings = load_knowns('known')
print("Done !")

dirpath = 'photos'

for basename in os.listdir(dirpath):
    print('Processing photo ', basename)

    filepath = os.path.join(dirpath, basename)

    image = cv2.imread(filepath)

    bgr_small_image = cv2.resize(image, (0, 0), fx=.25, fy=.25)
    rgb_small_image = bgr_small_image[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_image, model='cnn')
    face_encodings = face_recognition.face_encodings(rgb_small_image, face_locations)

    names = []

    for face_encoding in face_encodings:

        matches = face_recognition.compare_faces(known_encodings, face_encoding)

        name = "Unkwown"

        distances = face_recognition.face_distance(known_encodings, face_encoding)

        best_match_index = np.argmin(distances)

        if matches[best_match_index]:
            name = known_names[best_match_index]

        names.append(name)

    print(names)
    for (top, right, bottom, left), name in zip(face_locations, names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        try:
            # Draw a box around the face
            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image, name, (left + 6, bottom - 6), font, 1, (255, 255, 255), 1)
        except:
            pass

        # Display the resulting image
    cv2.imwrite('outputs/'+basename, image)
