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
 
# When a Pandas dataframe contains object data types, this function
# quickly converts those to string. Use when exporting to formats that
# do not accept object data types.
def obj_to_string(df):
    for obj_col in list(df.select_dtypes(include=['object']).columns):
        df[obj_col] = df[obj_col].astype(str)
    return(df)




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
    
# Function for testing purposes.

def hello_world():
    print('Hello world')

