#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import pickle
import numpy as np
from os.path import join
from os import listdir
from tqdm import tqdm
import re

# NOTE - This script manually cleans certain rows from the various dataframes and corrects some dates, saving the
# pickles and the aggregate datafram to be used by the next script


# In[629]:

print('Loading variables')
load_folder = join('2.pickles', '4.manually_cleaned_dataframes')
save_folder = join('2.pickles', '5.auto_cleaned_dataframes')
agg_df_save_folder = join('2.pickles', '6.aggregate_dataframe')

# In[310]:

# Load dataframes
print('Loading dataframes')
dfs = [pickle.load(open(join(load_folder, file), 'rb')) for file in listdir(load_folder) if '.pkl' in file]


# In[599]:

# Create a copy of dfs and remove errors
def remove_error_rows(df):
    df = df.reset_index().drop('index', axis=1)
    error_rows = []
    for row, text in enumerate(df['text'].values):
        try:
            dummy = str(text + '\n')
        except:
            error_rows.append(row)
    return df.drop(error_rows)


def clean_dates(df):
    """Removes date aberrations by converting those to the mode"""
    date_mode = df['date'].mode()[0]

    def fix_abnormal_dates(date, date_mode, delta_days=40):
        """Fixes abnormal dates in a column"""
        if np.datetime64(date) >= np.datetime64(date_mode) + delta_days or np.datetime64(date) <= np.datetime64(
                date_mode) - delta_days:
            date = date_mode
        return np.datetime64(date)

    df['date'] = df['date'].apply(fix_abnormal_dates, args=(date_mode, 40))

    return df


def clean_email(df):
    """Applies regex to contact strings to reveal emails users try to scramble"""

    def clean_email_strings(string):
        string = str(string)
        string = re.sub(r'\[(?i)at\]', '@', string)
        string = re.sub(r'[\s\S]\[(?i)at\][\s\S]', '@', string)
        string = re.sub(r'\((?i)at\)', '@', string)
        string = re.sub(r'[\s\S]\((?i)at\)[\s\S]', '@', string)
        string = re.sub(r'[\s\S]\((?i)at\)[\s\S]', '@', string)
        string = re.sub('\[@\]', '@', string)
        string = re.sub(r'[\s\S]\[(?i)dot\][\s\S]', '.', string)
        string = re.sub(r'[\s\S]\((?i)dot\)[\s\S]', '.', string)
        string = re.sub('\[\.\]', '.', string)
        string = re.sub(r'\[(?i)dot\]', '.', string)
        string = re.sub(' (?i)dot ', '.', string)
        string = re.sub('\s\[\.\]\s', '.', string)
        string = re.sub(' (?i)at ', '@', string)
        string = re.sub('\s\[@\]\s', '@', string)
        string = re.sub(' @ ', '@', string)
        string = re.sub(' . ', '.', string)
        string = re.sub("\s\'at ", '@', string)
        string = re.sub('(?i)mail$', 'mail.com', string)
        string = re.sub('(?i)mailto:', '', string)
        string = re.sub('\w+ com', '.com', string)
        string = re.sub('.com.com', '.com', string)

        string = re.sub('\s\(gmail\)', '@gmail.com', string)
        string = re.sub('\s\{(?i)at\}\s','@', string)
        string = re.sub('\s\[(?i)a]\s', '@', string)
        string = re.sub('gmail\[com\]', 'gmail.com', string)
        string = re.sub(' @{2,10}', '@', string)
        string = re.sub(' \{dot\} ', '.', string)
        string = re.sub(' \(google mail\)', '@gmail.com', string)

        string = re.sub(r'\] Chris@NorcoPhoenix.com', 'Chris@NorcoPhoenix.com', string)
        string = re.sub(r'\[olafthefrog `at` gmail.com\]', 'olafthefrog@gmail.com', string)
        string = re.sub('https\:\/\/github.com\/jammor\snormandiggs@gmail.com', 'normandiggs@gmail.com',
                        string)

        return string

    df['contact'] = df['contact'].apply(clean_email_strings)

    return df


def clean_df(df):
    """Applies all cleaning functions to the dataframe"""
    remove_error_rows(df)
    clean_dates(df)
    clean_email(df)
    return df


print('Cleaning dataframes')
clean_dfs = [clean_df(df) for df in dfs]

# In[628]:

# Dump the dataframes

print('Pickling the dataframes and saving them to ' + save_folder)
i = 0
for clean_df in tqdm(clean_dfs):
    pickle.dump(clean_df, open(join(save_folder, 'clean_df' + str(i) + '.pkl'), 'wb'))
    i += 1

# Dump the aggregate dataframe

print('Pickling the aggregate dataframe and saving it to ' + agg_df_save_folder)
agg_df = pd.concat(clean_dfs)
agg_df = agg_df.reset_index().drop('index', axis=1)
pickle.dump(agg_df, open(join(agg_df_save_folder, 'hn_posts_agg_df.pkl'), 'wb'))
