import face_recognition
from sklearn.naive_bayes import MultinomialNB

# https://scikit-learn.org/0.15/modules/scaling_strategies.html


class FaceClassifier:

    def __init__(self, classifier=MultinomialNB()):
        self.classifier = classifier

    def partial_fit(self, encodings, names):
        self.classifier.partial_fit(encodings, names)

    def fit(self, encodings, names):
        self.classifier.partial_fit(encodings, names)

    def predict(self, encoding):
        return self.classifier.predict(encoding)

    @staticmethod
    def split_faces(image_rgb):
        #face_locations = face_recognition.face_locations(image_rgb, number_of_times_to_upsample=1, model='cnn')
        #face_encodings = face_recognition.face_encodings(image_rgb, face_locations, num_jitters=1, model='large')
        face_locations = face_recognition.face_locations(image_rgb)
        face_encodings = face_recognition.face_encodings(image_rgb, face_locations)

        sub_images = []
        for top, right, bottom, left in face_locations:
            sub_images.append(image_rgb[top:bottom, left:right, :])

        return sub_images, face_encodings, face_locations
