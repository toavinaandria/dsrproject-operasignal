from tqdm import tqdm
import os
import shutil
import pickle


def copy_files_to_dir( list reference_list,
                        str target_folder,
                        str folder1,
                        str folder2):
    """ Copy files within reference list and relevant extensions from folders 1 and 2 to the target folder"""

    cdef str user, fail_ext, json_ext, user_dl_failed
    cdef list failed_filelist, usr_w_problems

    fail_ext = '.fail'
    json_ext = '.json'
    failed_folder = 'user_dl_failed'
    failed_filelist = os.listdir(failed_folder)

    usr_w_problems = [] # Stores users for which there was a problem downloading the data


    for user in tqdm(reference_list):

        try:
            if user + fail_ext in failed_filelist:
                continue

            elif user + json_ext in os.listdir(folder1):
                shutil.copy(folder1 + user + json_ext, target_folder + user + json_ext)

            else:
                shutil.copy(folder2 + user + json_ext, target_folder + user + json_ext)

        except:
            usr_w_problems.append(user)

    pickle.dump(usr_w_problems, open('usr_w_problems.pkl', 'wb'))
