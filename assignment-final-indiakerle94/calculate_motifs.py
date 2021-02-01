from datetime import datetime, timedelta

def get_cheaters_at_the_time(cheaters, killers):
    """Takes as input 1) the formatted cheaters list and 
    2) the formatted killers list and returns a subset of 
    the killers list where the killer was a cheater at 
    time of event."""
    
    cheaters_at_the_time = []
    for cheat_kill in killers:
        for cheater in cheaters:
            if cheat_kill[1] == cheater[0]:
                if cheater[1] < cheat_kill[3] < cheater[2]:
                    cheaters_at_the_time.append(cheat_kill)
                    
    return cheaters_at_the_time

def get_victim_cheater_motifs(cheaters_at_the_time, cheaters):
    """Takes as input 1) cheater_at_the_time list and 2) formatted
    cheaters list and returns the number of individuals who were 
    killed by cheaters then went on to cheat themselves within 5 days."""
      
    
    number_of_victim_cheater_motifs = []
    for player_record in cheaters_at_the_time:
        victim = player_record[2]
        cheater_record_for_victim = [x for x in cheaters if x[0] == victim]
        if len(cheater_record_for_victim) > 0:
            cheater_record_for_victim = cheater_record_for_victim[0]
            start_cheating = cheater_record_for_victim[1]
            killed_time = player_record[3]
            if start_cheating > killed_time:
                if start_cheating < (killed_time + timedelta(5)):
                    number_of_victim_cheater_motifs.append(player_record)
                    
    return len(number_of_victim_cheater_motifs)

def calc_victim_cheater_motifs(cheaters, killers):
    """Takes as input 1) the formatted cheaters list and
    2) the formatted killers list and returns the number 
    of individuals who were killed by cheaters then went on 
    to cheat themselves within 5 days."""
    
    cheaters_at_the_time = get_cheaters_at_the_time(cheaters, killers)
    num_of_victim_cheater_motifs = get_victim_cheater_motifs(cheaters_at_the_time, cheaters)
    
    return num_of_victim_cheater_motifs

