import xml.etree.ElementTree as ET 
from graph_objects import PetriNet
import sys

class XML_Parser(object):

    @staticmethod
    def parseXML(xmlfile): 

        #Create element tree object 
        tree = ET.parse(xmlfile) 

        #Get root element 
        root = tree.getroot() 

        #Dict for places
        places = {}
        transitions = {}

        petri_net = PetriNet()
        
        #Create all places
        for place in root.findall('subnet/place'): 
            #Search attributes
            id =  place.find('id').text
            label = place.find('label').text
            tokens = int(place.find('tokens').text)
            
            #Add places to dictionary
            places[int(id)] = label
                    
            #Net
            petri_net.add_place(label, tokens)
            
        # create all transitions
        for transition in root.findall('subnet/transition'):
            #Search attributes
            id =  transition.find('id').text
            label = transition.find('label').text
            
            #Add places to dictionary
            transitions[int(id)] = label
                    
            #Net
            petri_net.add_transition(label)
            
        #Create all arcs
        for arc in root.findall('subnet/arc'): 
            #Search attributes
            sourceId =  int(arc.find('sourceId').text)
            destinationId = int(arc.find('destinationId').text)
            multiplicity = int(arc.find('multiplicity').text)
            arc_type = arc.find('type').text
            
            #Decision which method select
            if int(sourceId) in places:
                if arc_type == 'regular':
                    petri_net.connect_place_to_transition(places[sourceId], transitions[destinationId], multiplicity)
                elif arc_type == 'inhibitor':
                    petri_net.inhibit_transition_by_place(places[sourceId], transitions[destinationId], multiplicity)
            elif int(sourceId) in transitions:
                petri_net.connect_transition_to_place(transitions[sourceId], places[destinationId], multiplicity)
        
        return petri_net
    
    
    
if __name__ == "__main__": 

    petri_net = XML_Parser.parseXML(sys.argv[1])

    petri_net.run_petri_net_for(5)