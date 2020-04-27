
from XMLParser import XML_Parser
import sys

if __name__ == "__main__": 

    petri_net = XML_Parser.parseXML(sys.argv[1])

    petri_net.run_petri_net_for(int(sys.argv[2]))
