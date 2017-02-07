
import pyximport; pyximport.install()
from file_mover import copy_files_to_dir
import pickle

relevant_DL_users = list(pickle.load(open('latestusersalreadydownloaded.pkl', 'rb')))

copy_files_to_dir(relevant_DL_users,
                  'agg_user_data',
                  'user_data',
                  'user_data 2')