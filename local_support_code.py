# Test if running in notebook
def is_running_from_ipython():
    from IPython import get_ipython
    return get_ipython() is not None     

# A conditional print / display option
def printmd(string, mkdn=True):
    from IPython.display import Markdown
    if is_running_from_ipython() & mkdn:
        display(Markdown(string))
    else:
        print(string)

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
def prep_for_stata(df, log_out=False):
    from tqdm import tqdm, tqdm_notebook
    obj_cols = list(df.select_dtypes(include=['object']).columns)
    if log_out:
        print('Found {} object type columns. Including:'.format(len(obj_cols)))
        print(obj_cols)
    # Convert object data types to string.
    df = obj_to_string(df)
    # Remove special (unicode) characters.
    for obj_col in tqdm(obj_cols, desc='Fix Char Ct'):
        df[obj_col] = df[obj_col].apply(fix_char_ct)
    return(df)

# When a Pandas dataframe contains object data types, this function
# quickly converts those to string. Use when exporting to formats that
# do not accept object data types.
def obj_to_string(df):
    from tqdm import tqdm, tqdm_notebook
    obj_cols = list(df.select_dtypes(include=['object']).columns)
    for obj_col in tqdm(obj_cols, desc='Obj To Text'):
        df[obj_col] = df[obj_col].astype(str)
    return(df)

def get_strl(df, max_len=244):
    from tqdm import tqdm, tqdm_notebook
    obj_cols = list(df.select_dtypes(include=['object']).columns)
    strl_list = []
    for obj_col in tqdm(obj_cols, desc='Get Strl List'):
        if df[obj_col].fillna('').map(lambda x: len(str(x))).max() > max_len:
            strl_list.append(obj_col)
    return(strl_list)

# Define function that finds and replaces offensive characters.
def fix_char_ct(bad_text):
    ret_txt = ''
    for item in bad_text:
        ret_txt += item if len(item.encode(encoding='utf_8')) == 1 else ''
    return(ret_txt)

def parallelize_dataframe(df, func, n_cores=4):
    import pandas as pd 
    from multiprocessing import  Pool
    import numpy as np
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

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

# Prints iterable more neatly.
def neat_list(thelist, width=4):
    if type(thelist) == dict:
        thelist = [(k,v) for k,v in thelist.items()]
    for i in range(0,len(thelist)):
        if i%width > 0:
            print('"{}" '.format(thelist[i]), end='')
        elif i%width == 0:
            print('"{}" '.format(thelist[i]))

# Prints iterable more neatly in dataframe format.
def neat_list_df(ilist, max_cols=4, sort=False, reverse=False):
    # Sort of sort specified True
    if sort == True:
        ilist = sorted(ilist, reverse=reverse, key=str.lower)
    
    # Make the list evenly divisble by number of columns
    ilist = list(ilist) + [''] * int(len(ilist)%max_cols)
    
    # Calculate the number of rows
    nrows = int(len(ilist)/max_cols)
    
    # Declare dictionary for the data & starting row
    neat_data = {}
    startrow = 0
    
    for i in range(0,max_cols):
        # Iteratively add each row
        neat_data[i] = ilist[startrow:startrow+nrows]
        # Increment the starting row.
        startrow = startrow + nrows
        
    # Return a dataframe
    return(pd.DataFrame(neat_data))

# Test if an item is in a list.
# Inspired by Stata's inlist command.
def inlist(list_to_test, item=''):
    isinlist = False
    for i in list_to_test:
        if i == item:
            isinlist = True
    return(isinlist)

def SigStrObs(df, rounder=4, prounder=3, sigval=.05, frame=True, lower=False):
    '''
    Returns a correlation matrix with p-values.
    
    Arguments:
        df - A dataframe.
        
        rounder - Default = 4. Number of decimal places to display coefficients.
        
        prounder - Default = 3. Number of decimanl places to display p-values.
        
        sigval - Default = .05. Statistical significance threshold.
                                Stars placed by p-values below threshold.
                                
        frame - Default = True. When False the return will be a dictionary.
        
        lower - Default = False. When true will reverse display of coefficients.
    '''
    from scipy.stats import pearsonr
    if rounder > 6:
        print('NOTE: Some results reported to a maximum of six decimal places.')
    df.dropna(inplace=True)    
    corrs = df.corr()
    pvals = pd.DataFrame([[pearsonr(df[c], df[y])[1] for y in df.columns] for c in df.columns],
                         columns=df.columns, index=df.columns)
    
    if not lower:
        itr1 = 0
        itr2 = 1
    
    if lower:
        itr1 = 0
        itr2 = len(corrs.columns)
    
    result = {}
    for c in corrs.columns:
        result[c] = []
        for r in corrs.columns[itr1:itr2]:

            # Write the correlation coefficient.
            result[c].append(round(corrs[c][r], rounder))
            # Adjust display of coefficient if on the diagonal
            if result[c][-1] == 1:
                result[c][-1] = '1.' + '0' * rounder

            # Write the p-value for the correlation.
            result[c].append(round(pvals[c][r], prounder))
            result[c][-1] = str(result[c][-1])
            if len(result[c][-1]) < 2 + prounder:
                result[c][-1] = result[c][-1] + '0' * (2 + prounder - len(result[c][-1]))
            if result[c][-1].find('e') > -1:
                result[c][-1] = '0.0000' + result[c][-1][0]
            # Add parens to the p-value output
            result[c][-1] = '({})'.format(result[c][-1])
            
            # Add star for significance
            if float(result[c][-1][4:6]) / 1000 < sigval:
                result[c][-1] = result[c][-1] + '*'

            # TODO: Implement pairwise counts of cases.
            # Add observation counts TODO: Needs testing.
            # result[c].append(str(len(df[[c,r]].dropna())))

            # Remove p-values & obs for the diagonal
            if df[[c]].columns == df[[r]].columns:
                # Remove the p-value
                result[c][-1] = ''
                # Not yet implemented. See related TODO above.
                # Remove the observation count
                # result[c][-2] = ''
        
        if not lower:
            result[c] = result[c] + [''] * 2 * (len(corrs.columns) - itr2)
            itr2 += 1
            
        if lower:
            result[c] = [''] * 2 * itr1 + result[c]
            itr1 += 1
    
    outer = np.array(corrs.columns).repeat(2).tolist()
    inner = ['coef','pval'] * len(corrs.columns)
    if frame:
        return(pd.DataFrame(result, index=[outer, inner]))
    else:
        return(result)

    
# Function for testing purposes.
def hello_world():
    print('Hello world')

