from bs4 import BeautifulSoup
import urllib
import numpy as np
import pickle
from os.path import join
from tqdm import tqdm

# README - This scripts takes the URLs from the list in the previous script and dumps them as strings of BeautifulSoup
# objects to be analysed by the next script.
# IMPORTANT NOTE - As the BeautifulSoup objects cannot be pickled, they are transformed into strings and should be
# re-converted into soup objects by the next script

# Declare variables
load_folder = join('2.pickles', '1.urls_to_fetch')
url_df_pickle_path = join(load_folder, 'url_df.pkl')
url_list_filename_path = join(load_folder, 'url_list.pkl')
threads_save_folder = join('2.pickles', '2.threads')

print('Loading URLs to fetch')
url_df = pickle.load(open(url_df_pickle_path, 'rb'))
url_list = pickle.load(open(url_list_filename_path, 'rb'))


print('Pickling threads from URLs to ' + threads_save_folder)

for url,month in tqdm(url_list):
    # 1. fetch the url
    hnews_page = urllib.request.urlopen(url).read()

    # 2. save as soup object
    soup = BeautifulSoup(hnews_page, 'lxml')

    # IMPORTANT NOTE - BeautifulSoup objects cannot be pickled - the soups are thus transformed as strings to be
    # read again as BeautifulSoup objects by the next script
    soup_str = str(soup)

    # 3. dump soup object as pkl with relevant date
    date_string = str(np.datetime64(month, 'M'))
    
    pickle.dump(soup_str, open(join(threads_save_folder,'hn_thread' + date_string + '.pkl'), 'wb'))
    
print('Threads saved!')

print('Saving date when threads were downloaded - used to determine thread dates')
download_date = np.datetime64('today')

pickle.dump(download_date, open(join(threads_save_folder, 'download_date.pkl'), 'wb'))

