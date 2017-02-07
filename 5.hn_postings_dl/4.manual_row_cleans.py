#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import pickle
import numpy as np
from os.path import join
from os import listdir
from tqdm import tqdm
import re

# NOTE - This script manually cleans certain rows from the various dataframes


# In[629]:

print('Loading variables')
load_folder = join('2.pickles', '3.posts_dataframes')
save_folder = join('2.pickles', '4.manually_cleaned_dataframes')

# Load dataframes
print('Loading dataframes')

df0 = pickle.load(open(join(load_folder, 'df0.pkl'), 'rb'))
df1 = pickle.load(open(join(load_folder, 'df1.pkl'), 'rb'))
df2 = pickle.load(open(join(load_folder, 'df2.pkl'), 'rb'))
df3 = pickle.load(open(join(load_folder, 'df3.pkl'), 'rb'))
df4 = pickle.load(open(join(load_folder, 'df4.pkl'), 'rb'))
df5 = pickle.load(open(join(load_folder, 'df5.pkl'), 'rb'))
df6 = pickle.load(open(join(load_folder, 'df6.pkl'), 'rb'))
df7 = pickle.load(open(join(load_folder, 'df7.pkl'), 'rb'))
df8 = pickle.load(open(join(load_folder, 'df8.pkl'), 'rb'))
df9 = pickle.load(open(join(load_folder, 'df9.pkl'), 'rb'))
df10 = pickle.load(open(join(load_folder, 'df10.pkl'), 'rb'))

df11 = pickle.load(open(join(load_folder, 'df11.pkl'), 'rb'))
df12 = pickle.load(open(join(load_folder, 'df12.pkl'), 'rb'))
df13 = pickle.load(open(join(load_folder, 'df13.pkl'), 'rb'))
df14 = pickle.load(open(join(load_folder, 'df14.pkl'), 'rb'))
df15 = pickle.load(open(join(load_folder, 'df15.pkl'), 'rb'))
df16 = pickle.load(open(join(load_folder, 'df16.pkl'), 'rb'))
df17 = pickle.load(open(join(load_folder, 'df17.pkl'), 'rb'))
df18 = pickle.load(open(join(load_folder, 'df18.pkl'), 'rb'))
df19 = pickle.load(open(join(load_folder, 'df19.pkl'), 'rb'))
df20 = pickle.load(open(join(load_folder, 'df20.pkl'), 'rb'))

df21 = pickle.load(open(join(load_folder, 'df21.pkl'), 'rb'))
df22 = pickle.load(open(join(load_folder, 'df22.pkl'), 'rb'))
df23 = pickle.load(open(join(load_folder, 'df23.pkl'), 'rb'))
df24 = pickle.load(open(join(load_folder, 'df24.pkl'), 'rb'))
df25 = pickle.load(open(join(load_folder, 'df25.pkl'), 'rb'))
df26 = pickle.load(open(join(load_folder, 'df26.pkl'), 'rb'))
df27 = pickle.load(open(join(load_folder, 'df27.pkl'), 'rb'))
df28 = pickle.load(open(join(load_folder, 'df28.pkl'), 'rb'))
df29 = pickle.load(open(join(load_folder, 'df29.pkl'), 'rb'))
df30 = pickle.load(open(join(load_folder, 'df30.pkl'), 'rb'))


print('Resetting indices for dataframes')

df0.reset_index(inplace=True)
df0.drop('index', axis=1, inplace=True)

df1.reset_index(inplace=True)
df1.drop('index', axis=1, inplace=True)

df2.reset_index(inplace=True)
df2.drop('index', axis=1, inplace=True)

df3.reset_index(inplace=True)
df3.drop('index', axis=1, inplace=True)

df4.reset_index(inplace=True)
df4.drop('index', axis=1, inplace=True)

df5.reset_index(inplace=True)
df5.drop('index', axis=1, inplace=True)

df6.reset_index(inplace=True)
df6.drop('index', axis=1, inplace=True)

df7.reset_index(inplace=True)
df7.drop('index', axis=1, inplace=True)

df8.reset_index(inplace=True)
df8.drop('index', axis=1, inplace=True)

df9.reset_index(inplace=True)
df9.drop('index', axis=1, inplace=True)

df10.reset_index(inplace=True)
df10.drop('index', axis=1, inplace=True)

df11.reset_index(inplace=True)
df11.drop('index', axis=1, inplace=True)

df12.reset_index(inplace=True)
df12.drop('index', axis=1, inplace=True)

df13.reset_index(inplace=True)
df13.drop('index', axis=1, inplace=True)

df14.reset_index(inplace=True)
df14.drop('index', axis=1, inplace=True)

df15.reset_index(inplace=True)
df15.drop('index', axis=1, inplace=True)

df16.reset_index(inplace=True)
df16.drop('index', axis=1, inplace=True)

df17.reset_index(inplace=True)
df17.drop('index', axis=1, inplace=True)

df18.reset_index(inplace=True)
df18.drop('index', axis=1, inplace=True)

df19.reset_index(inplace=True)
df19.drop('index', axis=1, inplace=True)

df20.reset_index(inplace=True)
df20.drop('index', axis=1, inplace=True)

df21.reset_index(inplace=True)
df21.drop('index', axis=1, inplace=True)

df22.reset_index(inplace=True)
df22.drop('index', axis=1, inplace=True)

df23.reset_index(inplace=True)
df23.drop('index', axis=1, inplace=True)

df24.reset_index(inplace=True)
df24.drop('index', axis=1, inplace=True)

df25.reset_index(inplace=True)
df25.drop('index', axis=1, inplace=True)

df26.reset_index(inplace=True)
df26.drop('index', axis=1, inplace=True)

df27.reset_index(inplace=True)
df27.drop('index', axis=1, inplace=True)

df28.reset_index(inplace=True)
df28.drop('index', axis=1, inplace=True)

df29.reset_index(inplace=True)
df29.drop('index', axis=1, inplace=True)

df30.reset_index(inplace=True)
df30.drop('index', axis=1, inplace=True)


# in df0.pkl —————————————————— DONE

df0_rows_to_delete = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 23, 24, 25, 27, 29, 30, 31, 32,
                      33, 34, 39, 42, 46, 47, 48,
                      51, 52, 54, 55, 59, 62, 70, 78, 97, 103, 107, 108, 109, 111, 136, 137, 139, 142, 143, 148, 151,
                      171, 172, 185, 193, 195,
                      196, 197, 198, 199, 200, 219, 220, 221, 233, 252, 265, 271, 294, 295, 301, 326, 351, 352, 354,
                      366, 367, 368, 369]
df0_custom_jobs = [17, 21, 50, 66, 208, 225, 360]

# in df1.pkl —————————————————— DONE

df1_rows_to_delete = [3, 12]
df1_custom_jobs = []

# df2.pkl--------- DONE

df2_rows_to_delete = [2, 3, 4, 43, 134, 194, 209]
df2_custom_jobs = [92]

# df3.pkl--------- DONE

df3_rows_to_delete = [4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 21, 22, 58, 76, 81, 96, 98, 118, 137, 144, 145, 183, 184, 189,
                      194, 246, 254, 255,
                      293, 298, 328, 334, 335, 337]
df3_custom_jobs = [102]

# df4.pkl--------- DONE

df4_rows_to_delete = [16, 217]
df4_custom_jobs = [220, 223]

# df5.pkl--------- DONE

df5_rows_to_delete = [3, 10, 25, 137]
df5_custom_jobs = []

# df6.pkl--------- DONE

df6_rows_to_delete = [37, 38, 39, 57, 141, 142, 146]
df6_custom_jobs = []

# df7.pkl--------- DONE

df7_rows_to_delete = [11, 29]
df7_custom_jobs = []

# df8.pkl--------- DONE

df8_rows_to_delete = [30, 35]
df8_custom_jobs = []

# df9.pkl--------- DONE

df9_rows_to_delete = [3, 159]
df9_custom_jobs = []

# df10.pkl--------- DONE

df10_rows_to_delete = []
df10_custom_jobs = []

# df11.pkl--------- DONE

df11_rows_to_delete = [75, 76, 80, 104, 105, 132, 133]
df11_custom_jobs = []

# df12.pkl--------- DONE

df12_rows_to_delete = [19, 94]
df12_custom_jobs = []

# df13.pkl--------- DONE

df13_rows_to_delete = [102, 264, 264, 268, 269, 270, 271, 272]
df13_custom_jobs = []

# df14.pkl--------- DONE

df14_rows_to_delete = []
df14_custom_jobs = []

# df15.pkl--------- DONE

df15_rows_to_delete = [49, 50, 119]
df15_custom_jobs = []

# df16.pkl--------- DONE

df16_rows_to_delete = [1, 2, 15, 37, 87, 169, 189]
df16_custom_jobs = []

# df17.pkl--------- DONE

df17_rows_to_delete = [12, 13, 14, 99, 100]
df17_custom_jobs = []

# df18.pkl--------- DONE

df18_rows_to_delete = [2, 3, 4, 5, 6]
df18_custom_jobs = []

# df19.pkl--------- DONE

df19_rows_to_delete = [45]
df19_custom_jobs = []

# df20.pkl--------- DONE

df20_rows_to_delete = []
df20_custom_jobs = []

# df21.pkl--------- DONE

df21_rows_to_delete = [41, 59]
df21_custom_jobs = []

# df22.pkl--------- DONE

df22_rows_to_delete = [6, 51, 52, 53, 158, 199]
df22_custom_jobs = []

# df23.pkl--------- DONE

df23_rows_to_delete = [34, 118, 209, 266, 277, 279, 280, 281]
df23_custom_jobs = []

# df24.pkl--------- DONE

df24_rows_to_delete = [78, 106]
df24_custom_jobs = []

# df25.pkl--------- DONE

df25_rows_to_delete = [3, 5, 6, 9, 64, 227, 228, 236]
df25_custom_jobs = []

# df26.pkl--------- DONE

df26_rows_to_delete = [202, 203, 204, 205, 208]
df26_custom_jobs = []

# df27.pkl--------- DONE

df27_rows_to_delete = []
df27_custom_jobs = []

# df28.pkl--------- DONE

df28_rows_to_delete = []
df28_custom_jobs = []

# df29.pkl--------- DONE

df29_rows_to_delete = [30, 33, 59, 60, 90, 96, 97, 117, 233, 234, 257, 259, 260]
df29_custom_jobs = []

# df30.pkl--------- DONE

df30_rows_to_delete = [48, 49, 50, 245, 250]
df30_custom_jobs = [189]

##### Manually run each row deletion job - NOTE - Custom jobs are ignored, could be refined with more time

print('Deleting non-post rows')
df0 = df0.drop(df0_rows_to_delete)
df1 = df1.drop(df1_rows_to_delete)
df2 = df2.drop(df2_rows_to_delete)
df3 = df3.drop(df3_rows_to_delete)
df4 = df4.drop(df4_rows_to_delete)
df5 = df5.drop(df5_rows_to_delete)
df6 = df6.drop(df6_rows_to_delete)
df7 = df7.drop(df7_rows_to_delete)
df8 = df8.drop(df8_rows_to_delete)
df9 = df9.drop(df9_rows_to_delete)
df10 = df10.drop(df10_rows_to_delete)

df11 = df11.drop(df11_rows_to_delete)
df12 = df12.drop(df12_rows_to_delete)
df13 = df13.drop(df13_rows_to_delete)
df14 = df14.drop(df14_rows_to_delete)
df15 = df15.drop(df15_rows_to_delete)
df16 = df16.drop(df16_rows_to_delete)
df17 = df17.drop(df17_rows_to_delete)
df18 = df18.drop(df18_rows_to_delete)
df19 = df19.drop(df19_rows_to_delete)
df20 = df20.drop(df20_rows_to_delete)

df21 = df21.drop(df21_rows_to_delete)
df22 = df22.drop(df22_rows_to_delete)
df23 = df23.drop(df23_rows_to_delete)
df24 = df24.drop(df24_rows_to_delete)
df25 = df25.drop(df25_rows_to_delete)
df26 = df26.drop(df26_rows_to_delete)
df27 = df27.drop(df27_rows_to_delete)
df28 = df28.drop(df28_rows_to_delete)
df29 = df29.drop(df29_rows_to_delete)
df30 = df30.drop(df30_rows_to_delete)

# Save the dataframes
print('Pickling the dataframes and saving them to '+ save_folder)

pickle.dump(df0, open(join(save_folder, 'df0' + '.pkl'), 'wb'))
pickle.dump(df1, open(join(save_folder, 'df1' + '.pkl'), 'wb'))
pickle.dump(df2, open(join(save_folder, 'df2' + '.pkl'), 'wb'))
pickle.dump(df3, open(join(save_folder, 'df3' + '.pkl'), 'wb'))
pickle.dump(df4, open(join(save_folder, 'df4' + '.pkl'), 'wb'))
pickle.dump(df5, open(join(save_folder, 'df5' + '.pkl'), 'wb'))
pickle.dump(df6, open(join(save_folder, 'df6' + '.pkl'), 'wb'))
pickle.dump(df7, open(join(save_folder, 'df7' + '.pkl'), 'wb'))
pickle.dump(df8, open(join(save_folder, 'df8' + '.pkl'), 'wb'))
pickle.dump(df9, open(join(save_folder, 'df9' + '.pkl'), 'wb'))
pickle.dump(df10, open(join(save_folder, 'df10' + '.pkl'), 'wb'))

pickle.dump(df11, open(join(save_folder, 'df11' + '.pkl'), 'wb'))
pickle.dump(df12, open(join(save_folder, 'df12' + '.pkl'), 'wb'))
pickle.dump(df13, open(join(save_folder, 'df13' + '.pkl'), 'wb'))
pickle.dump(df14, open(join(save_folder, 'df14' + '.pkl'), 'wb'))
pickle.dump(df15, open(join(save_folder, 'df15' + '.pkl'), 'wb'))
pickle.dump(df16, open(join(save_folder, 'df16' + '.pkl'), 'wb'))
pickle.dump(df17, open(join(save_folder, 'df17' + '.pkl'), 'wb'))
pickle.dump(df18, open(join(save_folder, 'df18' + '.pkl'), 'wb'))
pickle.dump(df19, open(join(save_folder, 'df19' + '.pkl'), 'wb'))
pickle.dump(df20, open(join(save_folder, 'df20' + '.pkl'), 'wb'))

pickle.dump(df21, open(join(save_folder, 'df21' + '.pkl'), 'wb'))
pickle.dump(df22, open(join(save_folder, 'df22' + '.pkl'), 'wb'))
pickle.dump(df23, open(join(save_folder, 'df23' + '.pkl'), 'wb'))
pickle.dump(df24, open(join(save_folder, 'df24' + '.pkl'), 'wb'))
pickle.dump(df25, open(join(save_folder, 'df25' + '.pkl'), 'wb'))
pickle.dump(df26, open(join(save_folder, 'df26' + '.pkl'), 'wb'))
pickle.dump(df27, open(join(save_folder, 'df27' + '.pkl'), 'wb'))
pickle.dump(df28, open(join(save_folder, 'df28' + '.pkl'), 'wb'))
pickle.dump(df29, open(join(save_folder, 'df29' + '.pkl'), 'wb'))
pickle.dump(df30, open(join(save_folder, 'df30' + '.pkl'), 'wb'))
