import xml.etree.ElementTree as ET 

def parseXML(xmlfile): 

	#Create element tree object 
	tree = ET.parse(xmlfile) 

	#Get root element 
	root = tree.getroot() 

	#Dict for places
	places = {}
	transitions = {}
	
	print('Places')
	#Create all places
	for place in root.findall('subnet/place'): 
		#Search attributes
		id =  place.find('id').text
		label = place.find('label').text
		tokens = place.find('tokens').text
		
		#Add places to dictionary
		places[int(id)] = label
				
		#Net
		#petri_net.add_place(label, tokens)
		print(places)
	
	print('Transitions')
	# create all transitions
	for transition in root.findall('subnet/transition'):
		#Search attributes
		id =  transition.find('id').text
		label = transition.find('label').text
		
		#Add places to dictionary
		transitions[int(id)] = label
				
		#Net
		#petri_net.add_transition(label)
		print(transitions)
		
	#Create all arcs
	print('Arcs')
	#Create all arcs
	for arc in root.findall('subnet/arc'): 
		#Search attributes
		sourceId =  arc.find('sourceId').text
		destinationId = arc.find('destinationId').text
		multiplicity = arc.find('multiplicity').text
		
		
		#Decision which method select
		if int(sourceId) in places:
			print(sourceId + '-' + destinationId + '-' + multiplicity + ' place_to_transition')
			#petri_net.connect_place_to_transition('places[sourceId]', 'places[destinationId]', multiplicity)
				
		if int(sourceId) in transitions:
			print(sourceId + '-' + destinationId + '-' + multiplicity + ' transition_to_place')
			#petri_net.connect_transition_to_place('places[sourceId]', 'places[destinationId]', multiplicity)
	
	

def main():

	#Parse xml file 
	parseXML('xml.xml')
	
	
if __name__ == "__main__": 

	# calling main function 
	main() 