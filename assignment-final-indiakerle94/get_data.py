import os
from datetime import datetime
import pickle

def get_cheater_data(filedir = "../assignment-final-data/cheaters.txt"):
    """ Takes as input raw cheaters.txt and outputs data as formatted
    list."""
    
    with open(filedir) as inp:
        raw_cheater_data =  list(zip(*(line.strip().split('\t') for line in inp))) 

    account_ids = raw_cheater_data[0]
    started_cheating_raw = raw_cheater_data[1]
    started_cheating_datetime = [datetime.strptime(x, '%Y-%m-%d') for x in started_cheating_raw]
    banned_date_raw = raw_cheater_data[2]
    banned_date_datetime = [datetime.strptime(x, '%Y-%m-%d') for x in banned_date_raw]

    cheater_data = []
    for index, x in enumerate(account_ids):
        cheater_data.append([x, started_cheating_datetime[index], banned_date_datetime[index]])
        
    return cheater_data

def get_killers_data(filedir = "../assignment-final-data/kills.txt"):
    """ Takes as input raw kills.txt and outputs data as formatted
    list."""
    
    with open(filedir) as inp:
        raw_killer_data =  list(zip(*(line.strip().split('\t') for line in inp)))  

    match_ids = raw_killer_data[0]
    killer_account_ids = raw_killer_data[1]
    victim_account_ids = raw_killer_data[2]
    time_of_killers_raw = raw_killer_data[3]
    time_of_killers_datetime = [datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f') for x in time_of_killers_raw]

    killers_data = []
    for index,x in enumerate(match_ids):
        killers_data.append([x,killer_account_ids[index],victim_account_ids[index],time_of_killers_datetime[index]])
                     
    return killers_data

def get_simulations_from_pickle_files(sim_file_ending = ".pickle", sim_file_start = "simulation_"):
    """Takes as input simulation file name ending and returns a list
    of simulations as formatted lists."""
    
    all_files = os.listdir(".")
    all_sim_files = [x for x in all_files if x.endswith(sim_file_ending)]
    all_sim_files = [x for x in all_sim_files if x.startswith(sim_file_start)]    
    simx_data_list = []
    for sim_num in range(0,len(all_sim_files)):
        simx_data = pickle.load( open(all_sim_files[sim_num], "rb" ) )
        simx_data_list.append(simx_data)

    return simx_data_list
