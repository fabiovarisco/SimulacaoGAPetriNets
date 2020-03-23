
from abc import ABC, abstractmethod
import pandas as pd
import random

class Node(ABC):

    def __init__(self, id):
        super().__init__()
        self.id = id
        self.outgoing_arcs = []
        self.incoming_arcs = []

    @abstractmethod
    def is_transition_node(self):
        pass 
    
    @abstractmethod
    def is_place_node(self):
        pass 

    def get_id(self):
        return self.id 

    def add_outgoing_arc(self, arc):
        self.outgoing_arcs.append(arc)
    
    def get_outgoing_arcs(self):
        return self.outgoing_arcs
    
    def add_incoming_arc(self, arc):
        self.incoming_arcs.append(arc)

    def get_incoming_arcs(self):
        return self.incoming_arcs

class Place(Node):
    
    def __init__(self, id, number_of_marks = 0):
        super().__init__(id)
        self.marks = number_of_marks

    def is_transition_node(self):
        return False

    def is_place_node(self):
        return True

    def set_marks(self, number_of_marks):
        self.marks = number_of_marks

    def add_mark(self, marks_to_add = 1):
        self.marks += marks_to_add

    def remove_mark(self, marks_to_remove = 1):
        self.marks -= marks_to_remove

    def get_marks(self):
        return self.marks

    def enable_outgoing_arcs(self): 
        enabled_outgoing_arcs = [arc for arc in self.get_outgoing_arcs() if self.marks >= arc.get_weight()]

        marks_left_to_consume = self.marks

        while (marks_left_to_consume > 0 and len(enabled_outgoing_arcs) > 0):
            chosen_arc = random.randint(0, len(enabled_outgoing_arcs) - 1)
            if marks_left_to_consume >= enabled_outgoing_arcs[chosen_arc].get_weight():
                enabled_outgoing_arcs[chosen_arc].enable_arc()
                marks_left_to_consume -= enabled_outgoing_arcs[chosen_arc].get_weight()

            del enabled_outgoing_arcs[chosen_arc]  

class Transition(Node):

    def __init__(self, id):
        super().__init__(id)

    def is_transition_node(self):
        return True

    def is_place_node(self):
        return False 

    def is_transition_enabled(self):
        for arc in self.incoming_arcs:
            if (not arc.is_arc_enabled()):
                return False
        return True

    def evaluate(self):
        if not self.is_transition_enabled():
            return
        for arc in self.incoming_arcs:
            arc.previous.remove_mark(marks_to_remove = arc.get_weight())
        
        for arc in self.outgoing_arcs:
            arc.next.add_mark(marks_to_add = arc.get_weight())

        
class Arc(object):

    def __init__(self, previous, next, weight = 1, id = ''):
        self.previous = previous
        self.next = next
        self.weight = 1
        self.id = id
        self.inhibitor = False
        self.is_enabled = False

    def get_next(self):
        return self.next

    def get_previous(self):
        return self.previous 
    
    def get_weight(self):
        return self.weight 

    def get_id(self):
        return self.id 

    def is_inhibitor(self):
        return False

    def enable_arc(self):
        self.is_enabled = True 

    def reset_arc(self):
        self.is_enabled = False 

    def is_arc_enabled(self):
        return self.is_enabled

class InhibitorArc(Arc):

    def __init__(self, previous, next, weight = 1, id = ''):
        if id is not None: 
            super().__init__(previous, next, weight=weight, id=id)
        else:
            super().__init__(previous, next, weight=weight)
        self.is_inhibitor = True

    def enable_arc(self):
        self.is_enabled = False 

    def reset_arc(self):
        self.is_enabled = True 

    def is_arc_enabled(self):
        return self.is_enabled
    

class PetriNet(object):

    def __init__(self):
        self.places = {}
        self.transitions = {}
        self.arcs = []
        self.are_outgoing_arcs_enabled = False
    
    def add_place(self, id, number_of_marks = 0):
        self.places[id] = Place(id, number_of_marks=number_of_marks)
    
    def set_number_of_marks_for_place(self, place_id, number_of_marks):
        self.places[place_id].set_marks(number_of_marks)

    def add_transition(self, id):
        self.transitions[id] = Transition(id)
    
    def connect_place_to_transition(self, place_id, transition_id, weight = 1):
        place = self.places[place_id]
        transition = self.transitions[transition_id]
        arc = Arc(place, transition, weight = weight)
        transition.add_incoming_arc(arc)
        place.add_outgoing_arc(arc)
        self.arcs.append(arc)
    
    def connect_transition_to_place(self, transition_id, place_id, weight = 1):
        place = self.places[place_id]
        transition = self.transitions[transition_id]
        arc = Arc(transition, place, weight = weight)
        transition.add_outgoing_arc(arc)
        place.add_incoming_arc(arc)
        self.arcs.append(arc)

    def evaluate(self):
        self._enable_outgoing_arcs()

        transition_keys_to_evaluate = [key for key, transition in self.transitions.items() if transition.is_transition_enabled()]
        
        for key in transition_keys_to_evaluate:
            self.transitions[key].evaluate()

        self._reset_outgoing_arcs()
    
    def print_state(self):

        self._enable_outgoing_arcs()

        print_matrix = {key: place.get_marks() for key, place in self.places.items()}
        print_matrix = dict(print_matrix, **{key: transition.is_transition_enabled() for key, transition in self.transitions.items()})

        output = pd.DataFrame.from_records([print_matrix])
        print(output)
        
    def _enable_outgoing_arcs(self):
        if self.are_outgoing_arcs_enabled:
            return
        
        for _, place in self.places.items():
            place.enable_outgoing_arcs()

        self.are_outgoing_arcs_enabled = True

    def _reset_outgoing_arcs(self):
        for arc in self.arcs:
            arc.reset_arc()
        self.are_outgoing_arcs_enabled = False
        





    
