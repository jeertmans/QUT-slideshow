import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import pickle
from people import Person
from pictures import Picture
from random import sample


class Network:

    def __init__(self):
        self.graph = nx.MultiGraph()
        self.pictures = defaultdict(Network.__init__dict__)

    @staticmethod
    def dummy(n_people, n_pictures, connectivity=0.15):
        network = Network()
        with open('data/first_names.txt', 'r') as f:
            names = f.readlines()
            people = [Person(name.strip()) for name in sample(names, n_people)]
            pictures = [Picture(name.strip()) for name in sample(names, n_pictures)]

        for picture in pictures:
            people_sample = sample(people, int(n_people * connectivity))

            for person in people_sample:
                network.add_person_to_picture(person, picture)

        return network

    @staticmethod
    def __init__dict__():
        return {'people': []}

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            network = pickle.load(f)

            # Import to set back the id counter to where it was !
            network.__reset__id__counter__()

            return network

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def __str__(self):
        return f'Network of {len(self.graph.nodes)} people linked by {len(self.pictures)} pictures'

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.graph) + hash(self.pictures)

    def __eq__(self, other):
        return (self.graph.nodes == other.graph.nodes) and (self.pictures.keys() == other.pictures.keys())

    def __getattribute__(self, item):
        if item == 'people':
            return self.graph.nodes
        else:
            return super(Network, self).__getattribute__(item)

    def __getitem__(self, item):
        if isinstance(item, int) or isinstance(item, Person):
            try:
                return next(person for person in self.people if person == item)
            except StopIteration:
                raise KeyError(f"This person or id is not in this network: {item}")
        elif isinstance(item, str) or isinstance(item, Picture):
            try:
                return self.pictures[item]
            except StopIteration:
                raise KeyError(f"This picture or filename is not in this network: {item}")
        else:
            raise KeyError(f"Unknown type of key: {item}")

    def __reset__id__counter__(self):
        Person.id_counter = max(person.id for person in self.people) + 1

    def add_relation(self, person_a, person_b):
        self.graph.add_edge(person_a, person_b)

    def add_person(self, person):
        self.graph.add_node(person)

    def add_person_to_picture(self, person, picture):

        for person_b in self.pictures[picture]['people']:
            self.add_relation(person, person_b)

        self.pictures[picture]['people'].append(person)

    def get_person(self, person):
        return self.graph[person]

    def get_people_in_picture(self, picture):
        return self.pictures[picture]['people']

    @staticmethod
    def sort_dict_by_len(d, reverse=True):
        return sorted(d.items(), key=lambda x: len(x[1]), reverse=reverse)

    def sorted_direct_neighbors(self, person, reverse=True):
        return Network.sort_dict_by_len(self.graph[person], reverse=reverse)

    def neighbors(self, person):
        # Auto casting to Person object
        person = self[person]

        neighbors = self.sorted_direct_neighbors(person)

        visited = {person}

        visited.update(neighbor for neighbor, _ in neighbors)

        while len(neighbors) != 0:

            temp = defaultdict(set)

            for neighbor, _ in neighbors:
                yield neighbor
                visited.add(neighbor)

                for candidate, edges in self.graph[neighbor].items():
                    if candidate not in visited:
                        temp[candidate].update(edges)
                        visited.add(candidate)

            neighbors = Network.sort_dict_by_len(temp)

    def traverse_all(self, person):
        candidates = set(self.graph.nodes)
        candidates.remove(person)

        neighbors = self.neighbors(person)

        while True:
            for neighbor in neighbors:
                yield neighbor
                candidates.remove(neighbor)

            if len(candidates) != 0:
                person = next(iter(candidates))
                yield person
                candidates.remove(person)
                neighbors = self.neighbors(person)
            else:
                break

    def show(self):
        nx.draw(self.graph, with_labels=True)
        plt.show()
