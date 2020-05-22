class Person:

    id_counter = 0

    def __init__(self, name):
        self.name = name
        self.id = Person.id_counter
        Person.id_counter += 1

    def __str__(self):
        return f'{self.id}: {self.name}'

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, int):
            return self.id == other
        else:
            return self.id == other.id
