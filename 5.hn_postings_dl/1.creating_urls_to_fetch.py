import pandas as pd
from os.path import join
import pickle

# Declare variables
url_csv = join('1.postings', '1.posting_urls.csv')
save_folder = join('2.pickles', '1.urls_to_fetch')
url_df_filename = 'url_df.pkl'
url_list_filename = 'url_list.pkl'


# In[4]:

def create_url_df(file):
    """Create a dataframe with URLs to fetch"""
    # Specific to columns used in CSV file
    posting_urls = pd.read_csv(file, sep=";")
    posting_urls['days_ago'] = posting_urls['days_ago'].apply(lambda x: x[:len(x)-3])
    posting_urls['days_ago'] = posting_urls['days_ago'].astype(int)
    posting_urls['month'] = pd.to_datetime(posting_urls['month'], format='%b-%y')
    return posting_urls

def create_url_list(url_df):
    """Create a list of URLs to fetch from the URL dataframe """
    date_list = []
    urls_list = []
    
    for date in url_df['month'].values:
        date_list.append(date)
    
    for date in url_df['link'].values:
        urls_list.append(date)
    
    urls_list = list(zip(urls_list,date_list))
    return urls_list

print('Creating URL list objects and pickling them to ' + save_folder)

url_df = create_url_df(url_csv)
url_list = create_url_list(url_df)

pickle.dump(url_df, open(join(save_folder,
                              url_df_filename), 'wb'))

pickle.dump(url_list, open(join(save_folder,
                                url_list_filename), 'wb'))
print('URL list objects saved!')

