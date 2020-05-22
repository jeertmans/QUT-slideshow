class Picture:

    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return f'{self.filename}'

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, str):
            return self.filename == other
        else:
            return self.filename == other.filename
