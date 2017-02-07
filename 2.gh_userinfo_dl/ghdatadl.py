#!/usr/bin/env python

import pickle
import time
import requests
import json
from requests.auth import HTTPBasicAuth
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import numpy as np
import sys
from calendar import timegm

# Checks that the script is run with an argument
if len(sys.argv) == 1 or len(sys.argv) > 2:
    print('Please use a pickled list as the only argument to the script, quitting')
    time.sleep(1)
    sys.exit()

userlist = pickle.load(open(sys.argv[1], "rb"))
GH_username = ''
GH_password = ''
iter_timer = 3600 # timer between download rate limit resets in seconds


class GHUserDownloader(object):

    def __init__(self, userlist, GH_username='',GH_password='',save_folder='1.data/hn_users_data_to_dl'):
        """Initialise the object and relevant variables
        userlist is a python list from which to download files
        """
        self.userlist = userlist
        self.GH_username = GH_username
        self.GH_password = GH_password
        self.save_folder = save_folder
        self.timer = self.get_timer() - timegm(time.gmtime()) + 10
        self.delay_iter = self.delay_to_next_iter()
        self.remaining_requests = self.get_ratelimit()
        # NB - Below only works for file extensions with 4 characters (5 including ".")
        self.onlyfiles = np.asarray([f[:len(f)-5] for f in listdir(self.save_folder) if \
                                     isfile(join(self.save_folder, f))])

        print(str(self.onlyfiles.size), " users already downloaded")
        print("The opening user list has "+str(len(self.userlist))+" files to download")

        self.print_ratelimit()

        print("Removing users already downloaded")

        self.userlist = np.setdiff1d(np.asarray(self.userlist), self.onlyfiles,assume_unique=True)
        print('There are '+str(len(self.userlist))+' users still to be downloaded')

        print("Saving list of remaining users to download")
        pickle.dump(self.userlist.tolist(), open('2.pickles/updateduserlist.pkl', 'wb'))

    def get_userdata(self):
        """ Downloads user data for users in the list"""
        if self.userlist.size == 0:
            print('Either all users have been downloaded or there is no userlist')
        else:
            print('Remaining requests: ' + str(self.remaining_requests))
            print('Remaining users to download ' + str(self.userlist.size))
            if self.remaining_requests == 0:
                self.prepare_next_iter()
            else:
                print('Starting download if possible of ' + str(self.remaining_requests) + ' users.')
                for user in tqdm(self.userlist[:self.remaining_requests]):
                    try:
                        requested_info = requests.get('https://api.github.com/users/'+user,
                                                      auth=HTTPBasicAuth(self.GH_username,
                                                                         self.GH_password))
                        data = requested_info.json()
                        with open(join(self.save_folder, user+'.json'), 'w') as f:
                            json.dump(data, f)

                    except:
                        # Accounts for users that deleted their accounts or failed download
                        with open(join(self.save_folder, user+'.fail'), 'w') as f:
                            f.write('Failed DL')
                        continue

                self.prepare_next_iter()

    def prepare_next_iter(self):
            print('Reached limit of download for this timeframe.')
            print('Updating list of users to download.')
            self.onlyfiles = np.asarray([f[:len(f)-5] for f in listdir(self.save_folder) if \
                                         isfile(join(self.save_folder, f))])
            print('You have now downloaded ' + str(self.onlyfiles.size) + ' users')
            self.userlist = np.setdiff1d(np.asarray(self.userlist), self.onlyfiles, assume_unique=True)
            pickle.dump(self.userlist.tolist(), open('2.pickles/updateduserlist.pkl', 'wb'))
            # Todo - Create variable of where to store latest userlist
            print('Cleaned up user list to download and saved it to disk as 2./pickles/updateduserlist.pkl')
            self.timer = self.get_timer() - timegm(time.gmtime()) + 10
            self.delay_iter = self.delay_to_next_iter()
            print('Starting again in '+str(self.delay_to_next_iter())+' seconds.')
            time.sleep(self.delay_to_next_iter())
            print('Starting next iteration')
            self.remaining_requests = self.get_ratelimit()
            self.get_userdata()


    def get_length_userlist(self):
        original_length = len(self.userlist)
        return original_length

    def get_ratelimit(self):
        """ Gets the rate limit for the logged_in user"""
        get_limit = requests.get('https://api.github.com/rate_limit',
                                 auth=HTTPBasicAuth(self.GH_username,
                                                    self.GH_password))
        data = get_limit.json()
        limit = data['rate']['remaining']
        return limit

    def get_timer(self):
        """Gets the countdown timer until next iteration for the logged_in user in seconds"""
        get_limit = requests.get('https://api.github.com/rate_limit',
                                 auth=HTTPBasicAuth(self.GH_username,
                                                    self.GH_password))
        data = get_limit.json()
        reset = data['rate']['reset']
        return reset

    def print_ratelimit(self):
        print('You have ' + str(self.remaining_requests) + ' requests remaining')

    def delay_to_next_iter(self):
        """ Sets delay before next action where time determines pause in seconds
        """
        if self.timer >= iter_timer:
            delay = 10
        else:
            delay = self.timer + 10
        return delay

    def delay_iter(self):
        """ Sets delay before next action where time determines pause in seconds
        """
        time.sleep(self.delay_iter)


downloader = GHUserDownloader(userlist, GH_username, GH_password)

downloader.get_userdata()
