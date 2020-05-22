# Train multiple images per person
# Find and recognize faces in an image using a SVC with scikit-learn

"""
Structure:
        <test_image>.jpg
        <train_dir>/
            <person_1>/
                <person_1_face-1>.jpg
                <person_1_face-2>.jpg
                .
                .
                <person_1_face-n>.jpg
           <person_2>/
                <person_2_face-1>.jpg
                <person_2_face-2>.jpg
                .
                .
                <person_2_face-n>.jpg
            .
            .
            <person_n>/
                <person_n_face-1>.jpg
                <person_n_face-2>.jpg
                .
                .
                <person_n_face-n>.jpg
"""

import face_recognition
from sklearn import svm
import os
import cv2

# Training the SVC classifier

# The training data would be all the face encodings from all the known images and the labels are their names
encodings = []
names = []

# Training directory
train_dir = os.listdir('train_dir/')

# Loop through each person in the training directory
for person in train_dir:
    pix = os.listdir("train_dir/" + person)

    # Loop through each training image for the current person
    for person_img in pix:
        # Get the face encodings for the face in each image file
        face = face_recognition.load_image_file("train_dir/" + person + "/" + person_img)
        face_bounding_boxes = face_recognition.face_locations(face)

        #If training image contains exactly one face
        if len(face_bounding_boxes) == 1:
            face_enc = face_recognition.face_encodings(face)[0]
            # Add face encoding for current image with corresponding label (name) to the training data
            encodings.append(face_enc)
            names.append(person)
        else:
            print(person + "/" + person_img + " was skipped and can't be used for training")

# Create and train the SVC classifier
clf = svm.SVC(gamma='scale')
clf.fit(encodings, names)

"""
# Load the test image with unknown faces into a numpy array

for basename in os.listdir('photos'):
    test_image = face_recognition.load_image_file('photos/' + basename)

    # Find all the faces in the test image using the default HOG-based model
    face_locations = face_recognition.face_locations(test_image)
    no = len(face_locations)
    print("Number of faces detected: ", no)

    # Predict all the faces in the test image using the trained classifier
    print("Found:")
    for i in range(no):
        test_image_enc = face_recognition.face_encodings(test_image)[i]
        name = clf.predict([test_image_enc])
        print("Found in", basename, *name)"""

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
    names = [clf.predict([face_encoding])[0] for face_encoding in face_encodings]
    """
    for face_encoding in face_encodings:

        matches = face_recognition.compare_faces(known_encodings, face_encoding)

        name = "Unkwown"

        distances = face_recognition.face_distance(known_encodings, face_encoding)

        name = clf.predict()
        
        best_match_index = np.argmin(distances)

        if matches[best_match_index]:
            name = known_names[best_match_index]

        names.append(name)"""

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
