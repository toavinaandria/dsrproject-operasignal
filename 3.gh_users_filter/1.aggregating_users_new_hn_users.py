#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd
import numpy as np
import os
from joblib import Parallel, delayed

# Change the below if files are moved
projectdir = '/Users/Toavina/githubdata'
subfolderdir = '3.gh_users_filter'
picklesdir = '1.pickles'
save_name = 'hn_users_df.pkl'


# 1. Define folders from which to aggregate data
folder = os.path.join(projectdir,'2.gh_userinfo_dl','1.data','hn_users_data_to_dl')


# 2. Create list of json files to aggregate into the Pandas Dataframe
def return_list_json_in_folder(folder):
    """ Returns a numpy array with all the .json files in the relevant foldr"""
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f)) and '.json' in f]

print('Creating list of files in user data folder')
file_list1 = return_list_json_in_folder(folder)

# problem_files = []

# 3. Create an aggregate dataframe from the json files
def json_to_df(file,folder):
    """Transform a json file into a Pandas dataframe row"""
    row = pd.read_json(folder+'/'+ file,
    orient='index',
    typ='series',
    dtype=True).to_frame().transpose()
    return row

print('Creating a list of jsons to concatenate')

def create_frames(f, folder):
    return json_to_df(f,folder)
    
frames1 = Parallel(n_jobs=7)(delayed(create_frames)(f, folder) for f in file_list1)

print('\nConcatenating frames')
df1 = pd.concat(frames1)

# 4. Pickle the dataframes

print('Pickling the dataframe to '+ os.path.join(projectdir,subfolderdir,picklesdir,save_name))
pickle.dump(df1, open(os.path.join(projectdir,subfolderdir,picklesdir,save_name),'wb'))
print('\nPickling finished!')

