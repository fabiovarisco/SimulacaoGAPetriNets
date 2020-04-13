

from graph_objects import PetriNet

print(__name__)

if __name__ == '__main__':

    print('Starting Petri Net')

    petri_net = PetriNet()
    petri_net.add_place('P1', 5)
    petri_net.add_place('P2', 3)
    petri_net.add_place('P3', 0)
    petri_net.add_place('P4', 0)
    petri_net.add_place('P5', 0)
    petri_net.add_transition('T1')
    petri_net.add_transition('T2')
    petri_net.add_transition('T3')
    petri_net.connect_place_to_transition('P1', 'T1')
    petri_net.connect_place_to_transition('P2', 'T1')
    petri_net.connect_transition_to_place('T1', 'P3')
    petri_net.connect_place_to_transition('P3', 'T2')
    petri_net.connect_transition_to_place('T2', 'P4')
    petri_net.connect_place_to_transition('P3', 'T3')
    petri_net.connect_transition_to_place('T3', 'P5')

    petri_net.run_petri_net_for(6)