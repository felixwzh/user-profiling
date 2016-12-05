#!/usr/bin/python
import re
from sklearn.preprocessing import OneHotEncoder



def get_items(source_file_name):
    # get item name list from file
    input = open(source_file_name,'r')
    for line in input:
        line=line.strip('\n')
        items = re.split('\t', line)
        break
    input.close()
    return items



def get_user_list(source_file_name,item_list):
    # get user from file and add it to the user_list_all,which includes all the users from all the files
    input = open(source_file_name,'r')
    flag = 0
    for line in input:
        if flag != 0:
            line=line.strip('\n')
            user={}.fromkeys(item_all,'None')
            s1 = re.split('\t', line)
            for i in range(0,len(s1)):
                if s1[i] != '':
                    user[item_list[i]] = s1[i]

            user_list_all.append(user)
        flag=1
    input.close()




def encode(item_list,user_list,*index):
    #encode to one hot code and out put the data in one hot in "data_onehot.txt"
    user_list_new=[]
    encode_item=[]
    encode_item_dict_list={}

    #end
    #add fake user
    fake_user={}
    for item in item_list:
        fake_user[item]='None'
    fake_user["LABEL"]='0'
    user_list.insert(0,fake_user)
    #add other user
    other_user={}
    for item in item_list:
        other_user[item]='other'
    other_user["LABEL"]='0'
    user_list.insert(0,other_user)
    #end

    for i in index:
        encode_item.append(item_list[i])
        encode_item_dict_list[item_list[i]]=[]
        encode_item_dict_list[item_list[i]].append('None')
        for user in user_list:
            if user[item_list[i]] not in encode_item_dict_list[item_list[i]]:
                encode_item_dict_list[item_list[i]].append(user[item_list[i]])
    for user in user_list:
        new_user=[]
        for i in range(0,len(encode_item)):
            new_user.append(int(encode_item_dict_list[encode_item[i]].index(user[encode_item[i]])))
        if user['LABEL']=='0': new_user.insert(0,0)
        elif user['LABEL']=='1': new_user.insert(0,1)
        user_list_new.append(new_user)


    print "start OneHotEncoder"
    #onehot encode
    enc = OneHotEncoder()
    enc.fit(user_list_new)
    user_list_onehot = enc.transform(user_list_new).toarray()
    # user in user_list_onehot,user[1]==1 means this user has a label; user[0]==1,means this user dosen't have a label
    print "OneHotEncoder end"


    #build the dict of every categorical data
    item_onehot_index_dict_dict={}.fromkeys(encode_item)
    for i in range(0,len(encode_item)):
        item_onehot_index_dict={}
        for user in user_list:
            item_onehot_index_dict[user[encode_item[i]]]=\
                encode_item_dict_list[encode_item[i]].index(user[encode_item[i]])\
                +enc.feature_indices_[i+1]
        item_onehot_index_dict_dict[encode_item[i]]=item_onehot_index_dict


    print "start write item_onehot_index_dict.txt"
    #out put this dict to "item_onehot_index_dict.txt"
    output_index=open("item_onehot_index_dict.txt","w")
    for item in item_onehot_index_dict_dict:
        for value in item_onehot_index_dict_dict[item]:
            output_index.write(item+'\t'+value+'\t'+str(item_onehot_index_dict_dict[item][value])+'\n')
    output_index.close()
    print "end write item_onehot_index_dict.txt"



    # # output the uservec ignore the None value
    # output_onehot=open("data_onehot.txt","w")
    # for user in user_list_onehot:
    #     # output label
    #     output_onehot.write(str(int(user[1]))+'\t')
    #     # output index of one
    #     for i in range(2,len(user)):
    #         if user[i]!=0.0:
    #             if i not in enc.feature_indices_:
    #                 output_onehot.write(str(i)+'\t')
    #     output_onehot.write('\n')
    # output_onehot.close()
    # # end

    # output the uservec with None value
    print "start write data_onehot.txt"
    output_onehot = open("data_onehot.txt","w")
    for user in user_list_onehot:
        #output label
        output_onehot.write(str(int(user[1]))+'\t')
        #output index of one
        for i in range(2,len(user)):
            if user[i]!=0.0:
                output_onehot.write(str(i)+'\t')
        output_onehot.write('\n')
    output_onehot.close()
    print "end write data_onehot.txt"
    # end

    return user_list_onehot
#end def encode()


# --------------------------------------------------------------------------
# get items from s{04.05.06.07.11}.txt,and merge them into a list :item_all
item_04=get_items("../../04_c_cons_test.tsv")
item_05=get_items("../../05_c_cons_prc_test.tsv")
item_06=get_items("../06_cont_info_test.tsv")
item_07=get_items("../07_c_rca_cons_test.tsv")
item_11=get_items("../11_c_meter_test.tsv")

print "item_list done!\n\n"
item_all = list(set(item_04+item_05+item_06+item_07+item_11+['LABEL']))

user_list_all=[]
user = {}.fromkeys(item_all)


#get user from s{04.05.06.07.11}.txt and add them to user_list_all
print "start get user_list in 04"
get_user_list("../04_c_cons_test.tsv",item_04)

print "start get user_list in 05"
get_user_list("../05_c_cons_prc_test.tsv",item_05)

print "start get user_list in 06"
get_user_list("../06_cont_info_test.tsv",item_06)

print "start get user_list in 07"
get_user_list("../07_c_rca_cons_test.tsv",item_07)

print "start get user_list in 11"
get_user_list("../11_c_meter_test.tsv",item_11)

print "user_list done"

# solve the problem that some user only has 'CONS_NO' or 'CONS_ID'
for user in user_list_all:
    if user['CONS_ID']=='None':
        user['CONS_ID']=user['CONS_NO']
    if user['CONS_NO']=='None':
        user['CONS_NO']=user['CONS_ID']



#merge
# merge users that have the same CONS_ID
print "start merge by CONS_ID"
user_CONS_ID_dict={}
for user in user_list_all:
    if user['CONS_ID'] not in user_CONS_ID_dict:
        user_CONS_ID_dict[user['CONS_ID']]=user
    else:
        for item in item_all:
            if user_CONS_ID_dict[user['CONS_ID']][item]=='None':
                user_CONS_ID_dict[user['CONS_ID']][item]=user[item]

#merge users that have the same CONS_NO
print "start merge by CONS_NO"
user_CONS_NO_dict={}
for user in user_CONS_ID_dict.values():
    if user['CONS_NO'] not in user_CONS_NO_dict:
        user_CONS_NO_dict[user['CONS_NO']]=user
    else:
        for item in item_all:
            if user_CONS_NO_dict[user['CONS_NO']][item]=='None':
                user_CONS_NO_dict[user['CONS_NO']][item]=user[item]
print "merge done"

#get the final user_list
user_list=[]
for CONS_NO in user_CONS_NO_dict:
    user_list.append(user_CONS_NO_dict[CONS_NO])



#get label_list
print "start get label_list "
input_label = open("../train_label.csv","r")
user_list_lable = []
while 1:
    lines = input_label.readlines()
    if not lines:
        break
    for line in lines:
        line=line.strip('\n')
        user_list_lable.append(line)
input_label.close()
print "label_list done"


print "start add label"
#add label to user
for user in user_list:
    if user['CONS_NO'] in user_list_lable:
        user['LABEL'] = '1'
    else:
        user['LABEL'] = '0'
print "add label done"

# #all out for check
# #users before merge
# output_all = open("data_all.txt","w")
# for it in item_all:
#     output_all.write(it)
#     output_all.write('\t')
# output_all.write('\n')
# for i in user_list_all:
#     for it in item_all:
#         output_all.write(str(i[it]))
#         output_all.write('\t')
#     output_all.write('\n')
# output_all.close()
#
# #users after merge
# output_all = open("data.txt","w")
# for it in item_all:
#     output_all.write(it)
#     output_all.write('\t')
# output_all.write('\n')
# for i in user_list:
#     for it in item_all:
#         output_all.write(i[it])
#         output_all.write('\t')
#     output_all.write('\n')
# output_all.close()
#

#encode users
print "start encode"
encode(item_all,user_list,0,3,4,8,9,10,11,12,13,15,16,17,18,19,20,21,22,)
print "all done"
# LABEL-2;APPR_OPINION-5 ;ELEC_ADDR-14; CONS_ID-1,CONS_NO-7,METER_ID-6  ignored

# RCA_FLAG:0	CONS_ID:1	LABEL:2	CONS_SORT_CODE:3	TYPE_CODE:4	APPR_OPINION:5
# METER_ID:6	CONS_NO:7	TS_FLAG:8	STATUS:9	STATUS_CODE:10	CONT_TYPE:11
# MEAS_BOX:12	TRADE_CODE:13	ELEC_ADDR:14	HEC_INDUSTRY_CODE:15	CONS_STATUS:16
# ORG_NO:17	ELEC_TYPE_CODE:18	LODE_ATTR_CODE:19	URBAN_RURAL_FLAG:20	SORT_CODE:21	CONTRACT_CAP:22
