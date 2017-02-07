#!/usr/bin/env python

# coding: utf-8

import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np
import pickle
from os import listdir
from os.path import join
from tqdm import tqdm


# README - This script creates dataframes with posting data from each thread by using regular expressions

# Declare loading variables

print('Loading objects to process...')

load_folder = join('2.pickles', '2.threads')
pickle_list = [join(load_folder,f) for f in listdir(load_folder)]
thread_list = [pickle.load(open(f, 'rb')) for f in pickle_list]
save_folder = join('2.pickles','3.posts_dataframes')

# IMPORTANT - Replace below with pickle if using that from previous file, or change the date to the time when
# threads were downloaded
download_date = np.datetime64('2016-11-29')


soups = [BeautifulSoup(o, 'lxml') for o in thread_list]


def replace_with_newlines(element):
    """Replaces breaks and new paragraphs with new lines for use with regex"""
    text = ''
    for elem in element.recursiveChildGenerator():
        if isinstance(elem, str):
            text += elem.strip()
        elif elem.name == 'br' or elem.name == 'p':
            text += '\n'
    return text



# * The first three requests have following format:
#     - [Location], [Remote | Relocation], [Full Time | Contract | Part Time]
#     - Stack: [Comma delimited list of technologies]
#     - Resume: [Link to resume]
#     - Contact: [Email address or other means of contact]
#     
# * Then up to October 2014:
#     - Location:
#     - Remote:
#     - Willing to relocate:
#     - Technologies:
#     - Resume: 
#     - Email:
#    
# * Then from November 2014 onwards:
#     - Location:
#     - Remote:
#     - Willing to relocate:
#     - Technologies:
#     - Résumé/CV: 
#     - Email:
#   

# # 2. Testing getting information from one URL

# In[23]:



# In[241]:

def create_frame(post):
    """Returns a dataframe with the relevant information from each post"""
    # Create dictionary to store values and temporary information ------------------------------------------
    posting = {}
    
    # Get key information ----------------------------------------------------------------------------------
    
    # Get user for the post
    try:
        posting['user'] = post.find_all('a', class_="hnuser")[0].get_text()
    except:
        posting['user'] = None

    # Get main post body
    try:
        posting['body'] = post.find_all('span', class_="c00")[0]
    except:
        posting['body'] = None

    # Get main_text
    try:
        posting['text'] = replace_with_newlines(post.find_all('span', class_="c00")[0])
    except:
        posting['text'] = None

    # Get any links
    try:
        posting['links'] = str(posting['body'].find_all('a'))
    except:
        posting['links'] = None
    
    
    # Define regex functions ------------------------------------------------------------------------------
    
    def create_re(regex_str,content_name):
        """Creates regex to search for a regex_str with a colon to find relevant content"""
        return re.search('(?i)'+ regex_str + ':(?P<' + content_name + '>.+)', replace_with_newlines(post))
    
    def find_word(regex_str):
        """Creates regex to find a word, no need to return content"""
        return re.search('(?i)'+ regex_str , replace_with_newlines(post))
    
    
    # Get location-related fields --------------------------------------------------------------------------
    
    # Find the location
    if create_re('location', 'location_content'):
        posting['location'] = create_re('location', 'location_content').group('location_content')
        location_found = True
    else:
        posting['location'] = None
        location_found = False
    
    if location_found == False:
        if re.search(r'<span class="c00">(?P<loc_content>.+[\w.])<p>',str(post)):
        # Returns the first line if there is no location: found in posts (for first versions of thread)
            posting['location'] = re.search(r'<span class="c00">(?P<loc_content>.+[\w.])<p>',
                                            str(post)).group('loc_content')
            
    
    # Find the remote tag
    if create_re('remote', 'remote_content'):
        posting['remote'] = create_re('remote', 'remote_content').group('remote_content')
    else:
        posting['remote'] = None
        
    # Find the willing to relocate tag
    if create_re('willing to relocate', 'relocation_content'):
        posting['can_relocate'] = create_re('willing to relocate',
                                            'relocation_content').group('relocation_content')
    else:
        posting['can_relocate'] = None
    
    # Get stack -------------------------------------------------------------------------------------------
    
    # Find the stack - Case where Stack: is used
    if create_re('stack','stack_content'):
        posting['stack'] = create_re('stack','stack_content').group('stack_content')
        stack_found = True
    else:
        posting['stack'] = None
        stack_found = False
    
    # Case where Technologies: is used
    if stack_found == False:
        if create_re('technologies','tech_content'):
            posting['stack'] = create_re('technologies','tech_content').group('tech_content')
    
    
    # Find the CV -----------------------------------------------------------------------------------
    
    # Case when only Resume: is used
    if create_re('r[ée]sum[ée]','cv_content'):
        posting['resume'] = create_re('r[ée]sum[ée]','cv_content').group('cv_content')
        resume_found = True
    else:
        posting['resume'] = None
        resume_found = False
        
    # Case when Resume/CV: is used
    
    if resume_found == False:
        if create_re('r[ée]sum[ée]/CV', 'cv_content'):
            posting['resume'] = create_re('r[ée]sum[ée]/CV', 'cv_content').group('cv_content')
            resume_found = True
    
    # Case when only CV: is used
            
    if resume_found == False:
        if create_re('cv', 'cv_content'):
            posting['resume'] = create_re('cv', 'cv_content').group('cv_content')

    
    # Find the contact -----------------------------------------------------------------------------
    
    # Case when Contact: is used
    if create_re('contact','contact_content'):
        posting['contact'] = create_re('contact','contact_content').group('contact_content')
        contact_found = True
    else:
        posting['contact'] = None
        contact_found = False
    
    # Case when email is used for contact
    if contact_found == False:
        if create_re('email', 'email_address'):
            posting['contact'] = create_re('email', 'email_address').group('email_address')
    
    
    # Find Github and LinkedIn mentions -------------------------------------------------------------
    
    # Find Github
    if create_re('github','github_content'):
        posting['github_account'] = create_re('github','github_content').group('github_content')
    else:
        posting['github_account'] = None
    
    # Find LinkedIn
    if create_re('linkedin','linkedin_content'):
        posting['linkedin_account'] = create_re('linkedin','linkedin_content').group('linkedin_content')
    else:
        posting['linkedin_account'] = None
    
    # See if Github mentioned
    if find_word('github'):
        posting['github_mention'] = True
    else:
        posting['github_mention'] = False
        
        
    # See if LinkedIn mentioned
    if find_word('linkedin'):
        posting['linkedin_mention'] = True
    else:
        posting['linkedin_mention'] = False
    
    
    # Get the date --------------------------------------------------------------------------------------
    
    # Get date
    posting['days_ago'] = int(re.search('(?P<num_days_ago>\d+) days ago', 
                                        replace_with_newlines(post)).group('num_days_ago'))
    
    posting['date'] = download_date - posting['days_ago']



    # Make BS4 objects strings so they can be pickled
    try:
        posting['body'] = str(post.find_all('span', class_="c00")[0])
    except:
        posting['body'] = None

    # Get main_text
    try:
        posting['text'] = str(replace_with_newlines(post.find_all('span', class_="c00")[0]))
    except:
        posting['text'] = None

    # # Get any links
    # try:
    #     posting['links'] = str(posting['body'].find_all('a'))
    # except:
    #     posting['links'] = None

    
    # Create the dataframe from the dictionary ---------------------------------------------------------
    
    row = pd.DataFrame(pd.Series(posting)).transpose()
    
    ordered_row = row[['date','user','contact','github_account',
                       'linkedin_account' ,'location','linkedin_mention',
                       'github_mention','remote','can_relocate','stack',
                       'resume','links','text','body','days_ago']]

    return ordered_row


# Execute loops to create the relevant dataframes

print('Creating dataframes that will be pickled in folder ' + save_folder)

i = 0

for soup in tqdm(soups):

    posts = soup.find_all('tr', class_="athing comtr ")

    frames = [create_frame(post) for post in posts]

    df = pd.concat(frames)

    pickle.dump(df, open(join(save_folder, 'df'+str(i)+'.pkl'), 'wb'))

    i += 1

print('Dataframes saved!')



