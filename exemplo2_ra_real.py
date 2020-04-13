

from graph_objects import PetriNet

print(__name__)

if __name__ == '__main__':

    print('Starting Petri Net')

    petri_net = PetriNet()
    petri_net.add_place('ra_castelo', number_of_marks=1)
    petri_net.add_place('ra_acorda', number_of_marks=0)
    petri_net.add_place('ra_dorme', number_of_marks=0)
    petri_net.add_place('ra_margem', number_of_marks=0)
    petri_net.add_place('margem', number_of_marks=5)
    petri_net.add_place('ponte', number_of_marks=0)
    petri_net.add_place('lugar_na_ponte', number_of_marks=1)
    petri_net.add_place('rio', number_of_marks=0)
    petri_net.add_place('saida_rio', number_of_marks=0)
    petri_net.add_place('lugar_no_rio', number_of_marks=1)
    petri_net.add_transition('ra_castelo_p_margem')
    petri_net.add_transition('ra_margem_p_castelo')
    petri_net.add_transition('ra_beijando')
    petri_net.add_transition('margem_p_ponte')
    petri_net.add_transition('ponte_p_rio')
    petri_net.add_transition('saindo_do_rio')
    petri_net.add_transition('saida_p_margem')
    petri_net.connect_place_to_transition('ra_castelo', 'ra_castelo_p_margem')
    petri_net.connect_place_to_transition('ra_acorda', 'ra_castelo_p_margem')
    petri_net.connect_place_to_transition('ra_dorme', 'ra_margem_p_castelo')
    petri_net.connect_place_to_transition('ra_margem', 'ra_beijando')
    petri_net.connect_place_to_transition('ra_margem', 'ra_margem_p_castelo')
    petri_net.connect_place_to_transition('margem', 'margem_p_ponte')
    petri_net.connect_place_to_transition('lugar_na_ponte', 'margem_p_ponte')
    petri_net.connect_place_to_transition('ponte', 'ponte_p_rio')
    petri_net.connect_place_to_transition('lugar_no_rio', 'ponte_p_rio')
    petri_net.connect_place_to_transition('rio', 'saindo_do_rio')
    petri_net.connect_place_to_transition('saida_rio', 'saida_p_margem')
    petri_net.connect_place_to_transition('saida_rio', 'ra_beijando')
    petri_net.connect_transition_to_place('ra_margem_p_castelo', 'ra_castelo')
    petri_net.connect_transition_to_place('ra_castelo_p_margem', 'ra_margem')
    petri_net.connect_transition_to_place('margem_p_ponte', 'ponte')
    petri_net.connect_transition_to_place('ponte_p_rio', 'lugar_na_ponte')
    petri_net.connect_transition_to_place('ponte_p_rio', 'rio')
    petri_net.connect_transition_to_place('saindo_do_rio', 'saida_rio')
    petri_net.connect_transition_to_place('saindo_do_rio', 'lugar_no_rio')
    petri_net.connect_transition_to_place('saida_p_margem', 'margem')
    petri_net.connect_transition_to_place('ra_beijando', 'ra_margem')
    petri_net.connect_transition_to_place('ra_beijando', 'margem')
    petri_net.inhibit_transition_by_place('ra_margem', 'saida_p_margem')

    petri_net.run_petri_net_for(5)

    petri_net.set_number_of_marks_for_place('ra_acorda', 1)

    petri_net.run_petri_net_for(5)

    petri_net.set_number_of_marks_for_place('ra_dorme', 1)

    petri_net.run_petri_net_for(5)
