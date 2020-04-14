
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


class Transition(Node):

    def __init__(self, id):
        super().__init__(id)
        self.transition_inhibited = False

    def is_transition_node(self):
        return True

    def is_place_node(self):
        return False 

    def is_transition_enabled(self):
        for arc in self.incoming_arcs:
            if (not arc.is_arc_enabled()):
                return False
        return True

    def is_transition_eligible(self):
        if self.is_transition_inhibited(): return False 
        for arc in self.incoming_arcs:
            if (not arc.is_arc_enabled()) and (not arc.was_arc_disputed()):
                return False
        return True 

    def set_transition_inhibited(self):
        self.transition_inhibited = True 
    
    def reset_transition_inhibited(self):
        self.transition_inhibited = False 
    
    def is_transition_inhibited(self):
        return self.transition_inhibited

    def get_list_of_disputes(self):
        return [arc.get_previous().get_id() for arc in self.incoming_arcs if arc.was_arc_disputed()]

    
        
class Arc(object):

    def __init__(self, previous, next, weight = 1, id = ''):
        self.previous = previous
        self.next = next
        self.weight = 1
        self.id = id
        self.inhibitor = False
        self.is_enabled = False
        self.was_disputed = False 

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

    def set_was_disputed(self): 
        self.was_disputed = True 

    def reset_was_disputed(self):
        self.was_disputed = False

    def was_arc_disputed(self):
        return self.was_disputed 

    def is_arc_enabled(self):
        return self.is_enabled
    
    def get_weight_to_consume(self):
        return self.weight

class InhibitorArc(Arc):

    def __init__(self, previous, next, weight = 1, id = ''):
        if id is not None: 
            super().__init__(previous, next, weight=weight, id=id)
        else:
            super().__init__(previous, next, weight=weight)
        self.is_enabled = True

    def get_weight_to_consume(self):
        return 0

    def enable_arc(self):
        self.is_enabled = False 

    def reset_arc(self):
        self.is_enabled = True 

    def is_inhibitor(self):
        return True
    


class PetriNetSolver(object):


    def __init__(self, arcs, places, transitions):
        self.arcs = arcs
        self.places = places 
        self.transitions = transitions
        self.are_outgoing_arcs_enabled = False 
        self.aux_marks = {}

    def __enable_outgoing_arcs(self):
        if self.are_outgoing_arcs_enabled:
            return

        self.aux_marks = {key: place.get_marks() for key, place in self.places.items()}

        for _, place in self.places.items():
           self.__inhibit_transitions_from_place(place)
        
        for _, place in self.places.items():
           self.__enable_undisputed_arcs_for_place(place)

        transition_keys = random.sample(self.transitions.keys(), len(self.transitions))
        for key in transition_keys:
            self.__enable_disputed_arcs_from_transition(self.transitions[key])

        self.are_outgoing_arcs_enabled = True

    def __reset_outgoing_arcs(self):
        for arc in self.arcs:
            arc.reset_arc()
            arc.reset_was_disputed()
            if isinstance(arc.next, Transition):
                arc.next.reset_transition_inhibited()
        self.are_outgoing_arcs_enabled = False

    def __inhibit_transitions_from_place(self, place):
        for arc in place.get_outgoing_arcs():
            if arc.is_inhibitor() and place.get_marks() >= arc.get_weight():
                arc.enable_arc()
                arc.next.set_transition_inhibited()

    def __enable_disputed_arcs_from_transition(self, transition):
        if not transition.is_transition_eligible():
            for arc in transition.get_incoming_arcs():
                arc.reset_was_disputed()
            return 
        
        for arc in transition.get_incoming_arcs():
            if not arc.is_inhibitor() and self.aux_marks[arc.previous.get_id()] < arc.get_weight_to_consume():
                return 
        
        for arc in transition.get_incoming_arcs():
            if not arc.is_inhibitor():
                self.aux_marks[arc.previous.get_id()] -= arc.get_weight_to_consume()
                arc.enable_arc()

    def __enable_undisputed_arcs_for_place(self, place): 

        enabled_outgoing_arcs = [arc for arc in place.get_outgoing_arcs() if place.get_marks() >= arc.get_weight() and not arc.is_inhibitor() and not arc.next.is_transition_inhibited()]

        required_marks = sum([arc.get_weight_to_consume() for arc in enabled_outgoing_arcs])

        # enable undisputed arcs
        if (required_marks <= place.get_marks()):
            for arc in enabled_outgoing_arcs:
                arc.enable_arc()
            return 

        # set disputed arcs 
        for arc in enabled_outgoing_arcs:
            arc.set_was_disputed()

    def pre_process_for_print(self):
        self.__enable_outgoing_arcs()

    def evaluate(self):
        self.__enable_outgoing_arcs()

        transition_keys_to_evaluate = [key for key, transition in self.transitions.items() if transition.is_transition_enabled()]
        
        for key in transition_keys_to_evaluate:
            self.evaluate_transition(self.transitions[key])

        self.__reset_outgoing_arcs()

    def evaluate_transition(self, transition):
        if not transition.is_transition_enabled():
            return

        for arc in transition.get_incoming_arcs():
            if not arc.is_inhibitor():
                arc.previous.remove_mark(marks_to_remove = arc.get_weight())
        
        for arc in transition.get_outgoing_arcs():
            arc.next.add_mark(marks_to_add = arc.get_weight())


class PetriNet(object):

    def __init__(self, Petri_net_solver_class = PetriNetSolver):
        self.places = {}
        self.transitions = {}
        self.arcs = []
        self.are_outgoing_arcs_enabled = False
        self.solver = Petri_net_solver_class(self.arcs, self.places, self.transitions)
    
    def add_place(self, id, number_of_marks = 0):
        self.places[id] = Place(id, number_of_marks=number_of_marks)
    
    def set_number_of_marks_for_place(self, place_id, number_of_marks):
        self.places[place_id].set_marks(number_of_marks)

    def add_transition(self, id):
        self.transitions[id] = Transition(id)
    
    def connect_place_to_transition(self, place_id, transition_id, weight = 1):
        place = self.places[place_id]
        transition = self.transitions[transition_id]
        arc = Arc(place, transition, weight)
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

    def inhibit_transition_by_place(self, place_id, transition_id, weight = 1):
        place = self.places[place_id]
        transition = self.transitions[transition_id]
        arc = InhibitorArc(place, transition, weight = weight)
        transition.add_incoming_arc(arc)
        place.add_outgoing_arc(arc)
        self.arcs.append(arc)

    def evaluate(self):
        self.solver.evaluate()
    
    def get_state(self):

        self.solver.pre_process_for_print()

        print_matrix = {key: place.get_marks() for key, place in self.places.items()}
        list_separator = ', '
        for key, transition in self.transitions.items():
            list_of_disputes = transition.get_list_of_disputes()
            print_matrix[key] = f'{"S" if transition.is_transition_enabled() else "N"} {f"({list_separator.join(list_of_disputes)})" if len(list_of_disputes) > 0 else ""}'
        
        return print_matrix
        
    def run_petri_net_for(self, n = 1):
        
        net_states = []
        for i in range(n):
            net_states.append(self.get_state())
            self.evaluate()
        columns = [key for key in self.places.keys()]
        columns.extend(key for key in self.transitions.keys())

        pd.set_option('display.max_columns', None)

        output_dataframe = pd.DataFrame.from_records(net_states, columns=columns)
        print(output_dataframe)
        




