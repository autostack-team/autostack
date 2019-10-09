'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/09/2019
Overview:
'''

def create_pipe(path):
    '''
    Creates a named pipe at the specified path. If the fifo already exists,
    the function throws an error. This function will recursively create the
    full file path.

    Parameter {string}: the full path to the fifo.
    '''

    leaf_dir_path = path.split('/')[:-1].join('')

    if (os.path.exists(path)):
        raise Error('The fifo already exists.')
    elif not os.path.exists(leaf_dir_path):
        os.mkdirs(leaf_dir_path)
    else:
        os.mkfifo(path)
