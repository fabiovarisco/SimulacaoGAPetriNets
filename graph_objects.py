
from abc import ABC, abstractmethod

class Node(ABC):

    def __init__(self, id):
        super().__init__()
        self.id = id

    @abstractmethod
    def is_transition_node(self):
        pass 
    
    @abstractmethod
    def is_place_node(self):
        pass 

    def get_id(self):
        return self.id 

class Place(Node):
    
    def __init__(self, id):
        super().__init__(id)
        self.marks = 0

    def is_transition_node(self):
        return False

    def is_place_node(self):
        return True

    def add_mark(marks_to_add = 1):
        self.marks += marks_to_add

    def remove_mark(marks_to_remove = 1):
        self.marks -= marks_to_remove

    def get_marks():
        return self.marks

class Transition(Node):

    def __init__(self, id):
        super().__init__(id)
        self.outgoing_arcs = []
        self.incoming_arcs = []

    def is_transition_node(self):
        return True

    def is_place_node(self):
        return False 
    
    def add_outgoing_arc(self, arc):
        self.outgoing_arcs.append(arc)
    
    def get_outgoing_arcs(self):
        return self.outgoing_arcs
    
    def add_incoming_arc(self, arc):
        self.incoming_arcs.append(arc)

    def get_incoming_arcs(self):
        return self.incoming_arcs

    def is_transition_enabled(self):
        for arc in incoming_arcs:
            if arc.weight > arc.previous.get_marks():
                return False
        return True

    def evaluate(self):
        if not self.is_transition_enabled():
            return
        for arc in incoming_arcs:
            arc.previous.remove_mark(marks_to_remove = arc.get_weight())
        
        for arc in outgoing_arcs:
            arc.next.add_mark(marks_to_add = arc.get_weight())

        
class Arc(object):

    def __init__(self, previous, next, weight = 1, id = ''):
        self.previous = previous
        self.next = next
        self.weight = 1
        self.id = id
        self.inhibitor = False

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



    
