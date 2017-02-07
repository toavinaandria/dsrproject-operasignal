# coding: utf-8

import pickle
import pandas as pd
import numpy as np
import os
import re


# Change the below if files are moved
projectdir = '~/githubdata'
subfolderdir = '3.gh_users_filter'
picklesdir = '1.pickles'


# 1. Define folders from which to aggregate data
folder = os.path.join(projectdir,'2.gh_userinfo_dl','user_data')
folder2 = os.path.join(projectdir,'2.gh_userinfo_dl','user_data2')


# 2. Create list of json files to aggregate into the Pandas Dataframe
def return_list_json_in_folder(folder):
    """ Returns a numpy array with all the .json files in the relevant foldr"""
    return np.array([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f)) and '.json' in f])

file_list1 = return_list_json_in_folder(folder)
file_list2 = return_list_json_in_folder(folder2)

problem_files = []

# 3. Create an aggregate dataframe from the json files
def json_to_df(file,folder):
    """Transform a json file into a Pandas dataframe row"""
    row = pd.read_json(folder+'/'+ file,
    orient='index',
    typ='series',
    dtype=True).to_frame().transpose()
    return row

frames1 = [json_to_df(f,folder) for f in file_list1]
frames2 = [json_to_df(f,folder2) for f in file_list2]

df1 = pd.concat(frames1)
df2 = pd.concat(frames2)

# 4. Pickle the dataframes

pickle.dump(df1, open(os.path.join(projectdir,subfolderdir,picklesdir,'user_df1.pkl','wb')))
pickle.dump(df2, open(os.path.join(projectdir,subfolderdir,picklesdir,'user_df2.pkl','wb')))


# 5. Concatenating both dataframes and changing the index

agg_df = pd.concat([df1,df2])
agg_df.index = range(len(agg_df))


# 6. Pickle the dataframes

pickle.dump(agg_df, open(os.path.join(projectdir,subfolderdir,picklesdir,'agg_df.pkl','wb')))



# In[21]:

agg_df_w_names = agg_df[['name','location','bio','blog','company',
        'created_at','updated_at','email','followers',
       'following','hireable','login',
        'public_gists','public_repos',
       'site_admin', 'type']][~pd.isnull(agg_df['name'])]


# In[22]:

agg_df_w_names


# In[415]:

len(agg_df_w_names) / len(agg_df)


# ## Filter ideas

# * Remove users with only one name - DONE
# * Remove users with non-Latin characters - NOT DONE BUT UNNEEDED
# * Remove users with a number in their character - DONE
# * Remove users not in the US, Canada or Europe (Remove China and India, Shanghai, Beijing) - PARTIALLY DONE
# * Remove users with less than 5 characters overall in both names - DONE

# In[221]:

# location mask removing China, Inda, Shanghai or Beijing
location_mask = ~agg_df_w_names['location'].str.contains('China' or 'India'                                                          or 'Shanghai'                                                          or 'Beijing'                                                          or 'Delhi'                                                          or 'Hyderabad'                                                          or 'Russia', na=False)


# In[358]:

#Remove users with numerical characters and no space (i.e. one single word)
# re.search([0-9], agg_df_w_names.loc[3]['name'])

def filter_names(string):
    """returns True if want to remove certain conditions"""
    
    #Subfunctions to search for invalid names 
    
    # search for no space
    def no_space(string):
        if len(string.split(' ')) == 1:
            return True
        else:
            return False

    # filter for names that are too short
    def too_short(string):
        if len(string) < 6:
            return True
        else:
            return False
        
    too_short_search = too_short(string)
    no_space_search = no_space(string)
    # search for a number in the string
    num_search = re.search("\d",string)
    at_search = re.search("@",string)

    if num_search or at_search or no_space_search == True     or too_short_search == True:
        return False
    else:
        return True

name_mask = agg_df_w_names['name'].apply(filter_names)


# In[380]:

def filter_locations(string):
    # filter for certain locations
    try:
        unwanted_loc_search = re.search("(?i)Shanghai(?i)|(?i)Beijing(?i)|(?i)China(?i)|(?i)India(?i)|(?i)Delhi(?i)|(?i)Hyderabad(?i)|(?i)Bangalore(?i)|(?i)Russia(?i)|(?i)Xi'an(?i)|(?i)Xian(?i)|(?i)Brazil(?i)|(?i)Argentina(?i)|(?i)Rio(?i)|(?i)Brazil(?i)|(?i)Mexico(?i)|(?i)Nicaragua(?i)|(?i)Colombia(?i)|(?i)Uruguay(?i)|(?i)Ecuador(?i)|(?i)Chile(?i)|(?i)Peru(?i)|(?i)Palestine(?i)|(?i)Perú(?i)|(?i)Dominicana(?i)|(?i)Brasil(?i)|(?i)Korea(?i)|(?i)Japan(?i)", string)
        
        if unwanted_loc_search:
            return False
        else:
            return True
    except:
        return True


# In[377]:

words = ['Argentina','Brazil',
         'Mexico','Nicaragua',
         'Colombia','Uruguay',
         'Ecuador','Chile',
         'Peru']

for word in words:
    print("(?i)"+word+"(?i)|"+'\\')


# In[382]:

location_mask = agg_df_w_names['location'].apply(filter_locations)


# In[383]:

agg_df_w_names[location_mask][name_mask]

