
'''error checking'''
import pandas, os
from pandas.core.frame import DataFrame as df
import numpy as np
from matplotlib import pyplot as plt

def read_file_gps_coun(path, filename):
    ''' get the data from the file with gps used as the sync mechanism'''
    os.chdir(path)
    print("Reading the file from {}".format(os.getcwd()))
    names = ['index', 'hour', 'minute', 'sec', 'mmm', 'pcounter', 'mt']
    key_df = pandas.read_csv(filename, index_col=0, header=None, names=names)
    return key_df

def clean_file(key_df, lower_limit=60, upper_limit=83):
    '''clean the given df, remove the initial zeros,
    remove the leading zeros and return the df'''
    one_indexes = (np.where(key_df.index == 1)[0])
    key_df = key_df[one_indexes[0]:]
    zero_indexes = (np.where(key_df.index == 0)[0])
    key_df = key_df[:zero_indexes[0]]
    key_df = key_df[key_df.mt < upper_limit]
    key_df = key_df[key_df.mt > lower_limit]
    return key_df

def filter_goodkeys(master_list, df1):
    '''Input: list of lists that is received from the babbio over network, the each list has same values in it. 
    output: Df of goot mt and index'''
    dfs_dict = {}
    mdf = df1['mt']
    for elements in enumerate(master_list):
        dfs_dict[elements[0]] = elements[1]
        dfs_dict[elements[0]] = df(index=dfs_dict[elements[0]])
        dfs_dict[elements[0]] = dfs_dict[elements[0]].join(mdf, how='inner')
        mode_elements = dfs_dict[elements[0]].mode().loc[0, 'mt']
        dfs_dict[elements[0]] = dfs_dict[elements[0]][dfs_dict[elements[0]].mt == mode_elements]
    good_mt = df(columns=['mt'])
    for keys  in dfs_dict:
        good_mt = pandas.concat([good_mt,dfs_dict[keys]]) 
    return good_mt

def split_df(df1):
    '''Find all the unique values in the given df, 
    split into unique list of dfs and return the list'''
#get the unique values in the mother df,
#create a dictionary, with n elements, where n is the number of unique values
#the elements in the dic will be a list 
#each ones will hold one unique values indexes
#return the dic.
    df_lists = {}
    unique_mts = df1.mt.unique()
    for mts in unique_mts:
        df_lists[mts] = []

    for indexes in df1.index:
        df_lists[df1.mt[indexes]].append(indexes)
        
    return df_lists

def get_shift(df1,df2):
    '''give a sample of the two df
    and get the shift btw the values'''
    difference = df1['mt']-df2['mt']
    diff_values = difference.value_counts()
    shift_by = diff_values.idxmax()
    return shift_by


def perform_XOR_unique(unique_dict):
    '''get the dict of the unique_values 
    return the XOR dict'''
    item1 = None
    item2 = None
    XOR_dic = {}
    while len(unique_dict) >= 2:
        item1 = unique_dict.popitem()
        item2 = unique_dict.popitem()
        xor = item1[0] ^ item2[0]
        listvalue = [item1[1], item2[1]]
        XOR_dic[xor] = listvalue
        
    if len(unique_dict) is 1:
        item1 = unique_dict.popitem()
        xor = item1[0] ^ item2[0]
        listvalue = [item1[1], item2[1]]
        XOR_dic[xor] = listvalue

    return XOR_dic
    
def split_2half(kdf):
    '''get the df and split it into 2 halves by dividing in to half'''
    kdf = kdf.reset_index()
    if len(kdf)%2 == 1:
        kdf.loc[int(len(kdf))]= kdf.loc[int(len(kdf)-1)]
    df1 =  df(columns = ['index1', 'index2'])
    df1['index1'] = kdf['index'][:int(len(kdf)/2)]
    kdf = kdf[int(len(kdf)/2):]
    kdf= kdf.reset_index()
    df1['index2']=kdf['index']
    return df1

def split_oddeven(kdf):
    ''' get the keydf and split into 2 df of odd and even'''
    kdf = kdf.reset_index()
    if(len(kdf)%2 == 1):
        kdf.loc[int(len(kdf))]= kdf.loc[int(len(kdf)-1)]
    df1 =  df(columns = ['index1', 'index2'])
    df1['index1'] = kdf['index'][kdf.index%2 == 0]
    df1 = df1.reset_index()
    df1 = df1.drop('index', axis=1)
    tempdf2 =  kdf['index'][kdf.index%2 == 1]
    tempdf2 = tempdf2.reset_index()
    df1['index2'] = tempdf2['index']
    return df1

def xor_df(indexdf, kdf):
    '''get the keydf with 2 columns of index
    return the keydf with xor key of the indexes in the 2 columns'''
    tempdf1 = kdf.loc[indexdf['index1']]['mt']
    tempdf2 = kdf.loc[indexdf['index2']]['mt']
    tempdf1 = tempdf1.reset_index()
    tempdf2 = tempdf2.reset_index()
    xor = tempdf1^tempdf2
    xor = xor.drop('index', axis=1)
    indexdf['xor'] = xor
    return indexdf
