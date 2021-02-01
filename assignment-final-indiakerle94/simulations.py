import random
import pickle

def get_all_cheater_ids(cheaters):
    """Takes as input 1) the formatted cheaters list
    and returns a list of cheater ids."""
    
    all_cheaters_ids = list(set([i[0] for i in cheaters]))
    
    return all_cheaters_ids

def check_if_player_is_a_cheater_at_this_time(player_id, some_time, cheaters):
    """Takes as input 1) single player id as a string 2) some time as
    a single datetime and 3) a formatted cheaters list and returns 
    a boolean if that player was a cheater at the some time."""
    
    time_this_player_became_cheater = [x[1] for x in cheaters if x[0] == player_id]
    if len(time_this_player_became_cheater) > 0:
        if some_time > time_this_player_became_cheater[0]:
            return True
        else:
            return False 
    else:
        return False 

def get_matches_with_cheaters(killers, cheaters, all_cheaters_id):
    """Takes as input 1) the formatted killers list 2) the
    formatted cheaters list and 3) a list of cheater ids and
    returns a list of match ids with cheaters."""

    match = []
    for i in range(len(killers)):
        if (killers[i][1] in all_cheaters_id):
            if check_if_player_is_a_cheater_at_this_time(killers[i][1], killers[i][3], cheaters) == True:
                match.append(killers[i][0])
        if (killers[i][2] in all_cheaters_id):
            if check_if_player_is_a_cheater_at_this_time(killers[i][2], killers[i][3], cheaters) == True:
                match.append(killers[i][0])          
    match_with_cheaters = list(set(match))
    return match_with_cheaters


def get_player_replacement_dict(match_records, all_cheaters_id, cheaters):
    """Takes as input 1) a list of all records associated to a match
    2) a list of cheater ids and 3) a formatted cheaters list and returns 
    a dictionary of shuffled non cheating players while keeping the timing and 
    structure of interactions the same."""
  
    replacement_dict = {}
    all_players, all_cheating_players, all_non_cheating_players = get_all_players_match(match_records,cheaters)
    players_list = all_non_cheating_players.copy()
    for original_player in all_non_cheating_players:
        replacement_player = random.sample(players_list, 1)[0]
        players_list.remove(replacement_player)
        replacement_dict[original_player] = replacement_player

    for cheating_player in all_cheating_players:
        replacement_dict[cheating_player] = cheating_player
    
    return replacement_dict

def get_all_players_match(match_records, cheaters):
    """Takes as input 1) a list of all records associated to a match
    and 2) a formatted cheaters list and returns three lists: all players,
    all non cheating players and all cheating plays within the match."""
    
    all_players = []
    for record in match_records:
        all_players.append(record[1])
        all_players.append(record[2])
    all_players = list(set(list(all_players)))
    
    cheaters_in_match = []
    for player in all_players:
        for time_field in [1,2]:
            time_point_in_match = [x[3] for x in match_records if x[time_field] == player]
            if len(time_point_in_match) > 0:
                time_point_in_match = time_point_in_match[0]
                if check_if_player_is_a_cheater_at_this_time(player, time_point_in_match, cheaters):
                    cheaters_in_match.append(player)
    cheaters_in_match = list(set(cheaters_in_match))
    
    all_non_cheating_players = list(set([x for x in all_players if x not in cheaters_in_match]))
    all_cheating_players = list(set([x for x in all_players if x in cheaters_in_match]))
 
    return all_players, all_cheating_players, all_non_cheating_players

def get_simulated_match_records(match_records, replacement_dict):
    """Takes as input 1) a list of all records associated to a single match and
    2) a replacement dictionary and returns a simulated killers list
    for records of that match where non cheating players are shuffled.""" 
    
    simulated_match_records = []
    for index, record in enumerate(match_records):
        killer_id = record[1]
        victim_id = record[2]

        replacement_killer_id = replacement_dict[killer_id]
        replacement_victim_id = replacement_dict[victim_id]

        simulated_match_records.append([record[0], replacement_killer_id, replacement_victim_id, record[3]])
    
    return simulated_match_records

def run_single_simulation(match_with_cheaters, killers, cheaters, all_cheaters_id):
    """Takes as input 1) a list of match ids with cheaters, 2) a formatted
    killers list, 3 )a formatted cheaters list and 4) a list of cheater ids
    and returns a simulated killers for all records of matches with cheaters
    where non cheating players are shuffled."""
    
    all_match_sims_list = []
    total_records = 0
    match_with_cheaters_list = match_with_cheaters
    for index, match_id in enumerate(match_with_cheaters_list):
        match_records = [x for x in killers if x[0] == match_id]
        replacement_players_dict = get_player_replacement_dict(match_records,all_cheaters_id,cheaters)
        simulated_match_records = get_simulated_match_records(match_records,replacement_players_dict)
        all_match_sims_list = all_match_sims_list + simulated_match_records 
        total_records += len(match_records)
    
    return all_match_sims_list

def run_simulation(killers, cheaters, sim_num = 10):
    """Takes as input 1) a formatted killers list 2) a formatted cheaters 
    list and 3) the number of simulations. It runs run_single_simulation
    x number of times and pickles each simulation.""" 
    
    all_cheaters_id = get_all_cheater_ids(cheaters)
    match_with_cheaters = get_matches_with_cheaters(killers, cheaters, all_cheaters_id)
    for n in range(sim_num):
        sim_name = str(n)
        print(f'running simulation...{sim_name}')
        all_match_sims = run_single_simulation(match_with_cheaters, killers, cheaters, all_cheaters_id)
        with open(f'simulation_{sim_name}.pickle', 'wb') as f:
            pickle.dump(all_match_sims, f)

