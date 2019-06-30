# This function cleans a string so that only letters a-z and digits
# 0-9 will remain. Also removes spaces. Use to prepare pandas 
# dataframe columns for export in formats that do not accept special 
# characters in variable names.
def clean_word(word, *, case='lower'):
    import re
    if case == 'lower':
        return(''.join(re.findall(r'[a-z|A-Z|0-9]', word.lower())))
    elif case == 'upper':
        return(''.join(re.findall(r'[a-z|A-Z|0-9]', word.upper())))
    elif case == 'asis':
        return(''.join(re.findall(r'[a-z|A-Z|0-9]', word)))
    else:
        raise Exception('Argument (case) incorrectly specified. \
                        Default is "lower" Alternate options \
                        are "upper" and "asis".')

# This funciton cleans a list of column names so that only letters
# a-z and digits 0-9 will remain. Also removes spaces. Also makes
# sure each column name is unique. Use to prepare pandas dataframe
# columns for export in formats that do not accept special
# characters, spaces, or duplicates among variable names.
def clean_cols(clst, *, case='lower'):
    import warnings
    newcols = []
    for col in clst:
        newcols.append(clean_word(col, case=case))
    if len(clst) != len(set(newcols)):
        warnings.warn('\nDuplicates in column list. \
                      \nDuplicates appended with location.')
        newestcols = []
        suffix = 0
        for i in newcols:
            if newcols.count(i) > 1:
                newestcols.append(i + str(suffix))
            else:
                newestcols.append(i)
            suffix += 1
        return(newestcols)
    else:
        return(newcols)


# This function prepares Pandas dataframes for export to Stata.
def prep_for_stata(df, log_out=True):
   obj_cols = list(df.select_dtypes(include=['object']).columns)
   if log_out:
       print('Found {} object type columns. Including:'.format(len(obj_cols)))
       print(obj_cols)
   # Convert object data types to string.
   df = obj_to_string(df)
   # Remove special (unicode) characters.
   for obj_col in obj_cols:
       df[obj_col] = df[obj_col].apply(fix_char_ct)
   return(df)


# When a Pandas dataframe contains object data types, this function
# quickly converts those to string. Use when exporting to formats that
# do not accept object data types.
def obj_to_string(df):
    for obj_col in list(df.select_dtypes(include=['object']).columns):
        df[obj_col] = df[obj_col].astype(str)
    return(df)

# This function gets a list of variables in a pandas dataframe that need
# to be saved as Strl format in Stata.
def get_strl(df, max_len=244):
    strl_list = []
    for obj_col in list(df.select_dtypes(include=['object']).columns):
        if df[obj_col].map(lambda x: len(x)).max() > max_len:
            strl_list.append(obj_col)
    return(strl_list)

# Define function that finds and replaces offensive characters.
def fix_char_ct(bad_text):
    ret_txt = ''
    for item in bad_text:
        ret_txt += item if len(item.encode(encoding='utf_8')) == 1 else ''
    return(ret_txt)


# Function that writes a list to a text file.
# Useful when using a list to log events.
def write_log_file(write_list, dir='', descriptive_text=''):
    # Save a list to a log file.
    import datetime
    import os

    write_log = write_list.copy()

    if descriptive_text != '':
        write_log.insert(0, '')
        write_log.insert(0, descriptive_text)
        write_log.insert(0, '')
    else:
        write_log.insert(0, descriptive_text)

    dirpath = os.path.join(dir, 'log_{}.txt'.format(
            str(datetime.datetime.now()).replace(" ", "-").replace(":","")))

    with open(dirpath, mode='w') as logfile:
                print('This is the write log file from {}'.format(str(datetime.datetime.now())), file = logfile)
                for write_lines in write_log:
                    print(write_lines, file = logfile)
    logfile.close

# This Function merges csv files into a single pandas dataframe.
def combine_csv_files(path='.'):
    import os
    import pandas as pd
    full_file_list = os.listdir(path)
    csvs_file_list = []
    for i in full_file_list:
        if i[-4:] == '.csv':
            csvs_file_list.append(i)
    df = pd.read_csv(os.path.join(path, csvs_file_list.pop(0)))
    for filename in csvs_file_list:
        df = pd.concat([df, pd.read_csv(os.path.join(path, filename))])
    return(df)
    
    
# Function for testing purposes.

def hello_world():
    print('Hello world')

