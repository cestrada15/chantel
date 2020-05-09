"""
Airline Dataset Loader
---------------------------
Handles the data operation on airlines dataset.

Usage:
import data_handler

# load a single dataframe
df = data_handler.read_as_dataframe()

# load dataframe in chunks
df_chunks_list = data_handler.read_as_dataframe_chunks()
"""

# standard packages
import glob
import pprint
import functools

# other packages
import pandas as pd


def read_as_dataframe(num_of_files=8):
    """
    Read all files into one single dataframe.
    
    Notes:
    This function will work only if you have a large amount of RAM
    on your computer. For example, anything above 30 GB should work.

    If you have less RAM, you can limit the number of files to load
    with this function with the parameter. First 8 files consumes 
    13 GB memory space.

    For more information on this issue, check out the stackoverflow
    answer: https://datascience.stackexchange.com/a/27794/61094.
    Another nice answer on this issue is the following:
    https://stackoverflow.com/a/60616527/5159551

    Parameters:
    num_of_files - How many files from the data folder you want to
                   load to. Range is (0, 22].
    """
    if num_of_files not in range(1, 23):
        raise Exception('Incorrect number of files.')

    # partial function
    par_func = functools.partial(
        pd.read_csv, 
        compression='bz2',
        encoding='ISO-8859-1',
        engine='c', 
        low_memory=True
    )

    # file path list
    file_list = list(glob.glob('data/*.csv.bz2'))

    # run partial function for all file paths and concat the dataframe
    df = pd.concat(map(par_func, file_list[:num_of_files]))

    return df


def read_as_dataframe_chunks(num_of_files=8, chunksize=500000):
    """
    Reads the data as dataframe chunks. Pandas returns object type
    of pandas.io.parsers.TextFileReader.

    Parameters:
    num_of_files - How many files from the data folder you want to
                   load to. Range is (0, 22].
    chunksize    - The size of each dataframe.

    Returns:
    A list of dataframe chunks for each file.

    Usage:
    # get the chunks list
    df_chunks_list = read_as_dataframe_chunks()

    # accessing to each dataframe in chunks
    for df_chunk in df_chunks_list:
        for df in df_chunk:
            print(df.shape)
    """
    if num_of_files not in range(1, 23):
        raise Exception('Incorrect number of files.')
        
    # another option for pd.read_csv is to use dtypes.
    # by passing dtype to pandas, we will define the data type for the column.
    # this is helpful, eliminates future data type confusions.
    dtype= {
        'CRSElapsedTime': 'float64',
        'CancellationCode': 'object',
        'TailNum': 'object',
        'Distance': 'float64'
    }

    # partial function
    par_func = functools.partial(
        pd.read_csv, 
        compression='bz2', 
        encoding='ISO-8859-1',
        engine='c',
        low_memory=False,
        chunksize=chunksize
    )

    # file path list
    file_list = list(glob.glob('data/*.csv.bz2'))

    # run partial function for all file paths and concat the dataframe
    df_chunks_list = list(map(par_func, file_list[:num_of_files]))

    return df_chunks_list


def count_num_of_fligts_per_carrier(df, verbose=False):
    """
    Given a dataframe of airlines dataset, it counts and 
    returns the number of airlines as a dictionary.

    Parameters:
    df - Airlines dataset

    Returns:
    Airline 'carrier_code' and # of flights as key, value pair.
    """
    # all carriers in this dataset
    carriers = df.UniqueCarrier.unique()
    
    # inital value dictionary
    carrier_counts = {}

    # update the global carrier_count
    for key in carriers:
        if key not in carrier_counts:
            carrier_counts.update({key: 0})

    # loop through each row in dataframe 
    for carrier in df.UniqueCarrier:
        carrier_counts[carrier] += 1

    if verbose:
        # Show the results
        print('Carrier counts:')
        #pprint.PrettyPrinter(carrier_counts, indent=2, compact=True,sort_dicts=True)
        pprint.pprint(object, stream=None, indent=2, width=80, depth=None, *, compact=False)
    
    return carrier_counts
   
