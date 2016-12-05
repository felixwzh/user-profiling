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
#

def get_user_list_04(source_file_name,item_list):
    # get user from file and add it to the user_list_all,which includes all the users from all the files
    input = open(source_file_name,'r')
    flag = 0
    for line in input:
        if flag != 0:
            line=line.strip('\n')
            s1 = re.split('\t', line)
            user={}.fromkeys(item_all,'None')
            for i in range(0,len(s1)):
                if s1[i] != '':
                    user[item_list[i]] = s1[i]

            user_list_all.append(user)
            CONS_ID_list[user['CONS_ID']]=1
            CONS_NO_list[user['CONS_NO']]=1
        flag=1
    input.close()


def get_user_list(source_file_name,item_list):
    #get user from file and add it to the user_list_all,which includes all the users from all the files
    if 'CONS_NO' in item_list:
        input = open(source_file_name,'r')
        flag = 0
        for line in input:
            if flag != 0:
                line=line.strip('\n')
                user={}.fromkeys(item_all,'None')
                s1 = re.split('\t', line)
                # #
                user_flag = 0
                if s1[item_list.index('CONS_NO')] in CONS_NO_list:
                    for pre_user in user_list_all:
                        if pre_user['CONS_NO'] == s1[item_list.index('CONS_NO')] and s1[item_list.index('CONS_NO')]!='None':
                            CONS_NO=pre_user['CONS_NO']
                            for i in range(0,len(s1)):
                                if s1[i] != '':
                                    pre_user[item_list[i]] = s1[i]
                            pre_user['CONS_NO']=CONS_NO
                            user_flag =1
                            break
                    if user_flag==1 : continue

                for i in range(0,len(s1)):
                    if s1[i] != '':
                        user[item_list[i]] = s1[i]
                # #
                user['CONS_ID']=user['CONS_NO']
                CONS_NO_list[user['CONS_NO']]=1
                user_list_all.append(user)
            else: flag=1
        input.close()
    elif 'CONS_ID' in item_list:
        counter=1
        input = open(source_file_name,'r')
        flag = 0

        for line in input:
            if counter%100==0:
                print counter
            if flag != 0:
                line=line.strip('\n')
                user={}.fromkeys(item_all,'None')
                s1 = re.split('\t', line)
                # #
                user_flag = 0
                if s1[item_list.index('CONS_ID')] in CONS_ID_list:
                    for pre_user in user_list_all:
                        if pre_user['CONS_ID'] == s1[item_list.index('CONS_ID')] and s1[item_list.index('CONS_ID')]!='None' :
                            CONS_ID=pre_user['CONS_ID']
                            for i in range(0,len(s1)):
                                if s1[i] != '':
                                    pre_user[item_list[i]] = s1[i]
                            pre_user['CONS_ID']=CONS_ID
                            user_flag = 1
                            counter+=1
                            break

                    if user_flag==1 : continue

                for i in range(0,len(s1)):
                    if s1[i] != '':
                        user[item_list[i]] = s1[i]
                # #
                user['CONS_NO']=user['CONS_ID']
                CONS_ID_list[user['CONS_ID']]=1
                counter+=1
                user_list_all.append(user)
            else: flag=1
        input.close()
#
# def get_user_list(source_file_name,item_list):
#     # get user from file and add it to the user_list_all,which includes all the users from all the files
#     input = open(source_file_name,'r')
#     flag = 0
#     for line in input:
#         if flag != 0:
#             line=line.strip('\n')
#             user={}.fromkeys(item_all,'None')
#             s1 = re.split('\t', line)
#             for i in range(0,len(s1)):
#                 if s1[i] != '':
#                     user[item_list[i]] = s1[i]
#
#             user_list_all.append(user)
#         flag=1
#     input.close()


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



    #onehot encode
    enc = OneHotEncoder()
    enc.fit(user_list_new)
    user_list_onehot = enc.transform(user_list_new).toarray()
    # user in user_list_onehot,user[1]==1 means this user has a label; user[0]==1,means this user dosen't have a label



    #build the dict of every categorical data
    item_onehot_index_dict_dict={}.fromkeys(encode_item)
    for i in range(0,len(encode_item)):
        item_onehot_index_dict={}
        for user in user_list:
            item_onehot_index_dict[user[encode_item[i]]]=\
                encode_item_dict_list[encode_item[i]].index(user[encode_item[i]])\
                +enc.feature_indices_[i+1]
        item_onehot_index_dict_dict[encode_item[i]]=item_onehot_index_dict

    #out put this dict to "item_onehot_index_dict.txt"
    output_index=open("item_onehot_index_dict.txt","w")
    for item in item_onehot_index_dict_dict:
        for value in item_onehot_index_dict_dict[item]:
            output_index.write(item+'\t'+value+'\t'+str(item_onehot_index_dict_dict[item][value])+'\n')
    output_index.close()



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
    #
    # output the uservec with None value
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
    # end

    return user_list_onehot
#end def encode()


# --------------------------------------------------------------------------
# get items from s{04.05.06.07.11}.txt,and merge them into a list :item_all
item_04=get_items("./data/train/04_c_cons.tsv")
item_05=get_items("./data/train/05_c_cons_prc.tsv")
item_06=get_items("./data/train/06_cont_info.tsv")
item_07=get_items("./data/train/07_c_rca_cons.tsv")
item_11=get_items("./data/train/11_c_meter.tsv")

item_all = list(set(item_04+item_05+item_06+item_07+item_11+['LABEL']))

user_list_all=[]
user = {}.fromkeys(item_all)


#get user from s{04.05.06.07.11}.txt and add them to user_list_all

CONS_NO_list={}
CONS_ID_list={}

print '04'
get_user_list_04("./data/train/04_c_cons.tsv",item_04)
print '05'
get_user_list("./data/train/05_c_cons_prc.tsv",item_05)
print '06'
get_user_list("./data/train/06_cont_info.tsv",item_06)
print '07'
get_user_list("./data/train/07_c_rca_cons.tsv",item_07)
print '11'
get_user_list("./data/train/11_c_meter.tsv",item_11)
print "end 11"



#get label_list
input_label = open("./data/train/train_label.csv","r")
user_list_lable = {}
while 1:
    lines = input_label.readlines()
    if not lines:
        break
    for line in lines:
        line=line.strip('\n')
        user_list_lable[line]=1
input_label.close()

print "add label"
#add label to user
for user in user_list_all:
    if user['CONS_NO'] in user_list_lable:
        user['LABEL'] = '1'
    else:
        user['LABEL'] = '0'
print "add label end"
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
# for i in user_list_all:
#     for it in item_all:
#         output_all.write(i[it])
#         output_all.write('\t')
#     output_all.write('\n')
# output_all.close()
#

#encode users
encode(item_all,user_list_all,0,3,4,8,9,10,11,12,13,15,16,17,18,19,20,21,22,)
# LABEL-2;APPR_OPINION-5 ;ELEC_ADDR-14; CONS_ID-1,CONS_NO-7,METER_ID-6  ignored

# RCA_FLAG:0	CONS_ID:1	LABEL:2	CONS_SORT_CODE:3	TYPE_CODE:4	APPR_OPINION:5
# METER_ID:6	CONS_NO:7	TS_FLAG:8	STATUS:9	STATUS_CODE:10	CONT_TYPE:11
# MEAS_BOX:12	TRADE_CODE:13	ELEC_ADDR:14	HEC_INDUSTRY_CODE:15	CONS_STATUS:16
# ORG_NO:17	ELEC_TYPE_CODE:18	LODE_ATTR_CODE:19	URBAN_RURAL_FLAG:20	SORT_CODE:21	CONTRACT_CAP:22
