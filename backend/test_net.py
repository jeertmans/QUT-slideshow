from networks import Network
import networkx as nx
from people import Person
from pictures import Picture

def dummy_network():
    n = Network()
    pic1 = Picture('famille.png')
    pic2 = Picture('annif.png')
    pic3 = Picture('fete.png')
    pic4 = Picture('soiree')

    per1 = Person('Jesus')
    per2 = Person('Juda')
    per3 = Person('Moise')
    per4 = Person('Charlie')
    per5 = Person('Antoine')

    n.add_person_to_picture(per1, pic1)
    n.add_person_to_picture(per2, pic1)
    n.add_person_to_picture(per3, pic1)

    n.add_person_to_picture(per3, pic2)
    n.add_person_to_picture(per4, pic2)
    n.add_person_to_picture(per5, pic2)

    n.add_person_to_picture(per1, pic3)
    n.add_person_to_picture(per5, pic3)

    n.add_person_to_picture(per1, pic4)
    n.add_person_to_picture(per5, pic4)

    return n


#n = dummy_network()

#print("Dummy network:", n)

#Network.save(n, 'test.p')

#n_load = Network.load('test.p')

n_load = Network.dummy(150, 500)

print(n_load.people)

source = list(n_load.people)[0]

#n_load.show()

print('source', source)

for neighbor in n_load.neighbors(source):
    print(neighbor)

print('Now traversing all')

for neighbor in n_load.traverse_all(source):
    print(neighbor)
