# Function that writes a list to a text file.

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

