from sklearn.svm import SVC
import pickle


class Model:

    def __init__(self):
        self.__model__ = SVC(gamma='auto')

    def save(self, filename):
        pickle.dump(self.__model__, open(filename, 'wb'))

    def load(self, filename):
        self.__model__ = pickle.loads(open(filename, 'rb'))

    def fit(self, X, y, sample_weight=None):
        return self.__model__.fit(X, y, sample_weight=sample_weight)

    def predict(self, X):
        return self.__model__.predict(X)
