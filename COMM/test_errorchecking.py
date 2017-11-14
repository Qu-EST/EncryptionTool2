'''test error checking'''
import ErrorChecking as e

print("imported errorchecking")
PATH = r'C:\Users\jee11\Desktop\aug24' # filepath
UPPER_LIMIT = 83                # limit to remove forced stop
LOWER_LIMIT = 60                # limit to remove the bad data
#file names
BUR = '08-24_16-26-38 CW 1mW bur.csv'
BAB = '08-24_17-26-36 CW-1mW bab.csv'

print("reading the files")
burdf = e.read_file_gps_coun(PATH, BUR)
babdf = e.read_file_gps_coun(PATH, BAB)
print("cleaning the file")
burdf = e.clean_file(burdf)
babdf = e.clean_file(babdf)
print("files cleaned, now filtering the df with only the index")
# filter the index with the other lab
bab_index = babdf.index.to_series()
burdf = burdf.join(bab_index, how='inner')
bur_index = burdf.index.to_series()
babdf = babdf.join(bur_index, how='inner')
# print(burdf)  

burdf = burdf.drop('index', axis=1)
babdf = babdf.drop('index', axis=1)

print("filter done")

########################################################################
################    unique list    #####################################
# print(babdf)
# print(burdf)

# in babbio get the unique values and split the into lists

# unique_dict = e.split_df(babdf)
# unique_list = list(unique_dict.values())


# # xor_dic = e.perform_XOR(unique_dict)

# # print(xor_dic)

# good_mt = e.filter_goodkeys(unique_list, burdf)
# print(good_mt)

###################################################################
##################################################################

xor_bur_2half = e.xor_df(e.split_2half(burdf), burdf)
xor_bur_oddeven = e.xor_df(e.split_oddeven(burdf), burdf)
print("bur xor 2half")
print(xor_bur_2half)
print("bab xor odd even")
print(xor_bur_oddeven)

xor_bab_2half = e.xor_df(e.split_2half(babdf), babdf)
xor_bab_oddeven = e.xor_df(e.split_oddeven(babdf), babdf)
print("xor_bab_2half")
print(xor_bab_2half)
print("xor_bab_oddeven")
print(xor_bab_oddeven)

key_2half = xor_bab_2half[xor_bab_2half['xor']==xor_bur_2half['xor']]
key_oddeven = xor_bab_oddeven[xor_bab_oddeven['xor']==xor_bur_oddeven['xor']]
print(key_2half)
print(key_oddeven)
keylist_2half = key_2half.index1.tolist()
tlist=key_2half.index2.tolist()
keylist_2half.extend(tlist)
# keylist_2half = keylist_2half.sort()

keylist_oddeven = key_oddeven.index1.tolist()
keylist_oddeven.extend(key_oddeven.index2.tolist())
# keylist_oddeven =keylist_oddeven.sort()

keydf_2half= e.df(index=keylist_2half)
keydf_oddeven = e.df(index=keylist_oddeven)
print(burdf)
print(babdf)
print(keydf_2half)
print(keydf_oddeven)

keydf= keydf_2half.join(keydf_oddeven, how='inner')

print(keydf)


                       
