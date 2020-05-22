import os
import face_recognition
import cv2


def split_faces(filepath):
    image = cv2.imread(filepath)
    rgb_image = image[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_image, number_of_times_to_upsample=1, model='cnn')
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations, num_jitters=1, model='large')

    sub_images = []
    for top, right, bottom, left in face_locations:
        sub_images.append(rgb_image[top:bottom, left:right, ::-1])

    return sub_images, face_encodings


dirpath = 'photos'

for basename in os.listdir(dirpath):
    filepath = os.path.join(dirpath, basename)
    print('Processing', filepath)
    sub_images, _ = split_faces(filepath)
    print('Found %d different faces in it!' % len(sub_images))

    for i, sub_image in enumerate(sub_images):
        name = "test/" + os.path.splitext(basename)[0] + '_' + str(i) + '.jpg'
        cv2.imwrite(name, sub_image)
