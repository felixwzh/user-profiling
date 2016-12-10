#!/usr/bin/python
from __future__ import division
import re

def ints(x):
    try:
        y=int(x)
        return y
    except ValueError:
        return None




# data structure
# RCA_FLAG:0	CONS_ID:1	LABEL:2	CONS_SORT_CODE:3	TYPE_CODE:4	APPR_OPINION:5
# METER_ID:6	CONS_NO:7	TS_FLAG:8	STATUS:9	STATUS_CODE:10	CONT_TYPE:11
# MEAS_BOX:12	TRADE_CODE:13	ELEC_ADDR:14	HEC_INDUSTRY_CODE:15	CONS_STATUS:16
# ORG_NO:17	ELEC_TYPE_CODE:18	LODE_ATTR_CODE:19	URBAN_RURAL_FLAG:20	SORT_CODE:21	CONTRACT_CAP:22
user=[None]*23
cons_id_dict={}
cons_no_dict={}
# user_info_list=[[]]*11# something wrong if write in this way , so changed it in an ugly way
user_info_list=[[],[],[],[],[],[],[],[],[],[],[]]

# user_info_list[0]:CONS_ID
# user_info_list[1]:23 items value in x axis
# user_info_list[2]:23 items index
# user_info_list[3]:23 items onehot index
# user_info_list[4]:event_list_01
# user_info_list[5]:event_list_02
# user_info_list[6]:event_list_03
# user_info_list[7]:event_list_08
# user_info_list[8]:event_list_09
# user_info_list[9]:event_list_10
# user_info_list[10]:event_list_12


# load user_to_predict from user_to_predict.csv
print "start get user_to_predict "
input = open("../data/test/test_to_predict.csv","r")
while 1:
    lines = input.readlines()
    if not lines:
        break
    for line in lines:
        line=ints(line.strip('\n'))
        if line!=None:
            user_info_list=[[],[],[],[],[],[],[],[],[],[],[]]
            cons_no_dict[line]=user_info_list
            cons_no_dict[line][1]=[None]*23
            cons_no_dict[line][2]=[None]*23
            cons_no_dict[line][3]=[None]*23
input.close()
print "get user_to_predict  done"






#load from 04
# in 04
# CONS_ID:0	    CONS_NO:1 	        ELEC_ADDR:2	    TRADE_CODE:3  	ELEC_TYPE_CODE:4
# CONTRACT_CAP:5	LODE_ATTR_CODE:6	    HEC_INDUSTRY_CODE:7	    STATUS_CODE:8
# ORG_NO:9	    CONS_SORT_CODE:10	    URBAN_RURAL_FLAG:11

# data structure
# RCA_FLAG:0	CONS_ID:1	LABEL:2	CONS_SORT_CODE:3	TYPE_CODE:4	APPR_OPINION:5 'NL'
# METER_ID:6	CONS_NO:7	TS_FLAG:8	STATUS:9	STATUS_CODE:10	CONT_TYPE:11
# MEAS_BOX:12	TRADE_CODE:13	ELEC_ADDR:14 'NL'	HEC_INDUSTRY_CODE:15	CONS_STATUS:16
# ORG_NO:17	ELEC_TYPE_CODE:18	LODE_ATTR_CODE:19	URBAN_RURAL_FLAG:20	SORT_CODE:21	CONTRACT_CAP:22
input=open('../data/test/04_c_cons_test.tsv',"r")
flag = 0
for line in input:
    if flag != 0:
        line=line.strip('\n')
        li = re.split('\t', line)
        if len(li)==12:
            if ints(li[1]) in cons_no_dict:
                # user=[None]*23
                # user_info_list=[[]]*11
                cons_id=ints(li[0])
                cons_no=ints(li[1])
                if len(li[0])>0: cons_no_dict[cons_no][1][1]=cons_id
                if len(li[1])>0: cons_no_dict[cons_no][1][7]=cons_no
                # if len(li[2])>0: cons_no_dict[cons_no][]=(li[2]) ADDR
                #?????
                # if len(li[3])>0: cons_no_dict[cons_no][13]=int(li[3])
                if len(li[3])>0: cons_no_dict[cons_no][1][13]=li[3]
                # if len(li[4])>0: cons_no_dict[cons_no][18]=int(li[4])
                if len(li[4])>0: cons_no_dict[cons_no][1][18]=li[4]
                # if len(li[5])>0: cons_no_dict[cons_no][22]=int(li[5])
                if len(li[5])>0: cons_no_dict[cons_no][1][22]=li[5]
                if len(li[6])>0: cons_no_dict[cons_no][1][19]=int(li[6])
                if len(li[7])>0: cons_no_dict[cons_no][1][15]=int(li[7])
                if len(li[8])>0: cons_no_dict[cons_no][1][10]=int(li[8])
                if len(li[9])>0: cons_no_dict[cons_no][1][17]=int(li[9])
                # if len(li[10])>0: cons_no_dict[cons_no][3]=int(li[10])
                if len(li[10])>0: cons_no_dict[cons_no][1][3]=li[10]
                if len(li[11])>0: cons_no_dict[cons_no][1][20]=int(li[11])

                cons_no_dict[cons_no][0]=[cons_id]
                # user_info_list[0].append(cons_id)
                # user_info_list[1]=user
                # cons_no_dict[cons_no]=user_info_list
                cons_id_dict[cons_id]=cons_no_dict[cons_no]
                # cons_id_dict[cons_id]=[cons_no,user]
                # cons_no_dict[cons_no]=[cons_id,user]
    flag+=1
input.close()
print "04 end"
# print cons_no_dict


# load from 05
# in 05 CONS_ID:0	TS_FLAG:1	ORG_NO:2

# data structure
# RCA_FLAG:0	CONS_ID:1	LABEL:2	CONS_SORT_CODE:3	TYPE_CODE:4	APPR_OPINION:5 'NL'
# METER_ID:6	CONS_NO:7	TS_FLAG:8	STATUS:9	STATUS_CODE:10	CONT_TYPE:11
# MEAS_BOX:12	TRADE_CODE:13	ELEC_ADDR:14 'NL'	HEC_INDUSTRY_CODE:15	CONS_STATUS:16
# ORG_NO:17	ELEC_TYPE_CODE:18	LODE_ATTR_CODE:19	URBAN_RURAL_FLAG:20	SORT_CODE:21	CONTRACT_CAP:22
input=open('../data/test/05_c_cons_prc_test.tsv',"r")
flag = 0
for line in input:
    if flag != 0:
        line=line.strip('\n')
        li = re.split('\t', line)
        if len(li)==3:
            cons_id=ints(li[0])
            if cons_id in cons_id_dict:
                if len(li[1])>0: cons_id_dict[cons_id][1][8]=int(li[1])
                if len(li[2])>0: cons_id_dict[cons_id][1][17]=int(li[2])
            # else:
            #     user=[None]*23
            #     user[1]=cons_id
            #     if len(li[1])>0: user[8]=int(li[1])
            #     if len(li[2])>0: user[17]=int(li[2])
            #     cons_id_dict[cons_id]=[None,user]
    flag+=1
input.close()
print "05 end"
# print cons_no_dict


# load from 06
#CONS_NO:0	APPR_OPINIO:"1	CONT_TYPE:2	STATUS:3
# data structure
# RCA_FLAG:0	CONS_ID:1	LABEL:2	CONS_SORT_CODE:3	TYPE_CODE:4	APPR_OPINION:5 'NL'
# METER_ID:6	CONS_NO:7	TS_FLAG:8	STATUS:9	STATUS_CODE:10	CONT_TYPE:11
# MEAS_BOX:12	TRADE_CODE:13	ELEC_ADDR:14 'NL'	HEC_INDUSTRY_CODE:15	CONS_STATUS:16
# ORG_NO:17	ELEC_TYPE_CODE:18	LODE_ATTR_CODE:19	URBAN_RURAL_FLAG:20	SORT_CODE:21	CONTRACT_CAP:22
input=open('../data/test/06_cont_info_test.tsv',"r")
flag = 0
for line in input:
    if flag != 0:
        line=line.strip('\n')
        li = re.split('\t', line)
        if len(li)==4:
            cons_no=ints(li[0])
            if cons_no in cons_no_dict:
                # if len(li[1])>0: cons_no_dict[cons_no][1][5]=(li[1])
                if len(li[2])>0: cons_no_dict[cons_no][1][11]=int(li[2])
                if len(li[3])>0: cons_no_dict[cons_no][1][9]=int(li[3])
            # else:
            #     user=[None]*23
            #     # user_info_list=[[]]*11
            #     user_info_list=[[],[],[],[],[],[],[],[],[],[],[]]
            #     user[1]=cons_no
            #     # if len(li[1])>0: user[5]=(li[1])
            #     if len(li[2])>0: user[11]=int(li[2])
            #     if len(li[3])>0: user[9]=int(li[3])
            #     user_info_list[1]=user
            #     cons_no_dict[cons_no]=user_info_list
            #     # cons_no_dict[cons_no]=[None,user]
    flag+=1
input.close()
print "06 end"


#load from 07
#CONS_NO:0	ORG_NO:1    RCA_FLAG:2	CONS_STATUS:3

# data structure
# RCA_FLAG:0	CONS_ID:1	LABEL:2	CONS_SORT_CODE:3	TYPE_CODE:4	APPR_OPINION:5 'NL'
# METER_ID:6	CONS_NO:7	TS_FLAG:8	STATUS:9	STATUS_CODE:10	CONT_TYPE:11
# MEAS_BOX:12	TRADE_CODE:13	ELEC_ADDR:14 'NL'	HEC_INDUSTRY_CODE:15	CONS_STATUS:16
# ORG_NO:17	ELEC_TYPE_CODE:18	LODE_ATTR_CODE:19	URBAN_RURAL_FLAG:20	SORT_CODE:21	CONTRACT_CAP:22
input=open('../data/test/07_c_rca_cons_test.tsv',"r")
flag = 0
for line in input:
    if flag != 0:
        line=line.strip('\n')
        li = re.split('\t', line)
        if len(li)==4:
            cons_no=ints(li[0])
            if cons_no in cons_no_dict:
                if len(li[1])>0: cons_no_dict[cons_no][1][17]=int(li[1])
                if len(li[2])>0: cons_no_dict[cons_no][1][0]=int(li[2])
                if len(li[3])>0: cons_no_dict[cons_no][1][16]=int(li[3])
            # else:
            #     user=[None]*23
            #     # user_info_list=[[]]*11
            #     user_info_list=[[],[],[],[],[],[],[],[],[],[],[]]
            #     user[1]=cons_no
            #     if len(li[1])>0: user[17]=int(li[1])
            #     if len(li[2])>0: user[0]=int(li[2])
            #     if len(li[3])>0: user[16]=int(li[3])
            #     #add this to other load part?
            #     user_info_list[1]=user
            #     cons_no_dict[cons_no]=user_info_list
            #     # cons_no_dict[cons_no]=[None,user]
    flag+=1
input.close()
print "07 end"

#load from 11
#METER_ID:0	ORG_NO:1	MEAS_BOX:2	SORT_CODE:3	TYPE_CODE:4	CONS_ID:5
# data structure
# RCA_FLAG:0	CONS_ID:1	LABEL:2	CONS_SORT_CODE:3	TYPE_CODE:4	APPR_OPINION:5 'NL'
# METER_ID:6	CONS_NO:7	TS_FLAG:8	STATUS:9	STATUS_CODE:10	CONT_TYPE:11
# MEAS_BOX:12	TRADE_CODE:13	ELEC_ADDR:14 'NL'	HEC_INDUSTRY_CODE:15	CONS_STATUS:16
# ORG_NO:17	ELEC_TYPE_CODE:18	LODE_ATTR_CODE:19	URBAN_RURAL_FLAG:20	SORT_CODE:21	CONTRACT_CAP:22
input=open('../data/test/11_c_meter_test.tsv',"r")
flag = 0
for line in input:
    if flag != 0:
        line=line.strip('\n')
        li = re.split('\t', line)
        if len(li)==6:
            if len(li[5])>0: cons_id=ints(li[5])
            if cons_id in cons_id_dict:
                if len(li[1])>0: cons_id_dict[cons_id][1][17]=int(li[1])
                if len(li[2])>0: cons_id_dict[cons_id][1][12]=li[2] # int(021937631X) invalid
                if len(li[3])>0: cons_id_dict[cons_id][1][21]=int(li[3])
                if len(li[4])>0: cons_id_dict[cons_id][1][4]=int(li[4])
        # else:
        #     user=[None]*23
        #     user[1]=cons_id
        #     if len(li[1])>0: user[17]=int(li[1])
        #     if len(li[2])>0: user[12]=li[2] # int(021937631X) invalid
        #     if len(li[3])>0: user[21]=int(li[3])
        #     if len(li[4])>0: user[4]=int(li[4])
        #     cons_id_dict[cons_id]=[None,user]
    flag+=1
input.close()
print "11 end"



print "start add label"
#add label to user
# data structure
# RCA_FLAG:0	CONS_ID:1	LABEL:2	CONS_SORT_CODE:3	TYPE_CODE:4	APPR_OPINION:5 'NL'
# METER_ID:6	CONS_NO:7	TS_FLAG:8	STATUS:9	STATUS_CODE:10	CONT_TYPE:11
# MEAS_BOX:12	TRADE_CODE:13	ELEC_ADDR:14 'NL'	HEC_INDUSTRY_CODE:15	CONS_STATUS:16
# ORG_NO:17	ELEC_TYPE_CODE:18	LODE_ATTR_CODE:19	URBAN_RURAL_FLAG:20	SORT_CODE:21	CONTRACT_CAP:22
# for cons_no in cons_no_dict:
#     if cons_no in user_list_label:
#         cons_no_dict[cons_no][1][2]=1
#     else:
#         cons_no_dict[cons_no][1][2]=0
# print "add label done"


#start encode
# data structure
# RCA_FLAG:0	CONS_ID:1	LABEL:2	CONS_SORT_CODE:3	TYPE_CODE:4	APPR_OPINION:5 'NL'
# METER_ID:6	CONS_NO:7	TS_FLAG:8	STATUS:9	STATUS_CODE:10	CONT_TYPE:11
# MEAS_BOX:12	TRADE_CODE:13	ELEC_ADDR:14 'NL'	HEC_INDUSTRY_CODE:15	CONS_STATUS:16
# ORG_NO:17	ELEC_TYPE_CODE:18	LODE_ATTR_CODE:19	URBAN_RURAL_FLAG:20	SORT_CODE:21	CONTRACT_CAP:22
# def encode(*index):
#     print "encode begin "
#     encode_item_list_list=[None]*23
#     global cons_no_dict
#
#
#     #add fake user
#     fake_user=['other']*23
#     # user_info_list=[[]]*11
#     user_info_list=[[],[],[],[],[],[],[],[],[],[],[]]
#     user_info_list[1]=fake_user
#     cons_no_dict[110]=user_info_list
#     #add None user
#     None_user=[None]*23
#     # user_info_list=[[]]*11
#     user_info_list=[[],[],[],[],[],[],[],[],[],[],[]]
#     user_info_list[1]=None_user
#     cons_no_dict[911]=user_info_list
#
#     for i in index:
#         encode_item_list_list[i]={}
#         encode_item_list_list[i][None]=len(encode_item_list_list[i])
#         #encode_item_list_list[i][None]=0
#
#         encode_item_list_list[i]['other']=len(encode_item_list_list[i])
#         #'other'  encode_item_list_list[i]['other']=1
#
#
#     print "encode index end"
#     # counter=1
#     for user in cons_no_dict.values():
#         # if counter%1000==0 :print counter
#         user_item_index=[None]*23
#         for i in index:
#             if user[1][i] not in encode_item_list_list[i]:
#                 encode_item_list_list[i][user[1][i]]=len(encode_item_list_list[i])
#             # if user[1][i] == None :
#             user_item_index[i]=encode_item_list_list[i][user[1][i]]+1#####  +1
#
#         user[2]=user_item_index#
#         # counter+=1
#     item_size_list=[None]*23
#     for i in index:
#         item_size_list[i]=len(encode_item_list_list[i])
#
#     for user in cons_no_dict.values():
#         user_onehot_index=[None]*23
#         counter=0
#         for i in index:
#             user_onehot_index[i]=user[2][i]+counter
#             counter+=item_size_list[i]
#         user[3]=user_onehot_index # user[3]
#
#     print "new user list end"
#
#     # output the uservec without None value
#     output_onehot = open("../data/train/train_user_onehot_index.txt","w")
#     for user in cons_no_dict.values():
#         #output label
#         if user[1][2]>0:
#             output_onehot.write("1")
#             output_onehot.write(" ")
#         else:
#             output_onehot.write("0")
#             output_onehot.write(" ")
#         #output index of one
#         for i in index:
#             if user[2][i]!=1:
#                 output_onehot.write(str(user[3][i]))
#                 output_onehot.write(":1 ")
#         output_onehot.write('\n')
#     output_onehot.close()
#     # end
#     print "output end"
#
#
#
#     output_index=open("../data/train/item_onehot_index_dict.txt","w")
#
#
#     counter=0
#     for i in index:
#         for values in encode_item_list_list[i]:
#             output_index.write(str(i))
#             output_index.write(' ')
#             output_index.write(str(values))
#             output_index.write(' ')
#             output_index.write(str(encode_item_list_list[i][values]+1+counter))
#             output_index.write('\n')
#         counter=item_size_list[i]+counter
#     output_index.close()
#
#
#
#
# encode(0,3,4,8,9,10,11,13,15,16,17,18,19,20,21,22)









index=[0,3,4,8,9,10,11,13,15,16,17,18,19,20,21,22]
print "encode begin "
encode_item_list_list=[None]*23


#add fake user
fake_user=['other']*23
# user_info_list=[[]]*11
user_info_list=[[],[],[],[],[],[],[],[],[],[],[]]
user_info_list[1]=fake_user
cons_no_dict[110]=user_info_list
#add None user
None_user=[None]*23
# user_info_list=[[]]*11
user_info_list=[[],[],[],[],[],[],[],[],[],[],[]]
user_info_list[1]=None_user
cons_no_dict[911]=user_info_list

for i in index:
    encode_item_list_list[i]={}
    encode_item_list_list[i][None]=len(encode_item_list_list[i])
    #encode_item_list_list[i][None]=0

    encode_item_list_list[i]['other']=len(encode_item_list_list[i])
    #'other'  encode_item_list_list[i]['other']=1


print "encode index end"
# counter=1
for user in cons_no_dict.values():
    # if counter%1000==0 :print counter
    user_item_index=[None]*23
    for i in index:
        if user[1][i] not in encode_item_list_list[i]:
            encode_item_list_list[i][user[1][i]]=len(encode_item_list_list[i])
        # if user[1][i] == None :
        user_item_index[i]=encode_item_list_list[i][user[1][i]]+1#####  +1

    user[2]=user_item_index#
    # counter+=1
item_size_list=[None]*23
for i in index:
    item_size_list[i]=len(encode_item_list_list[i])

for user in cons_no_dict.values():
    user_onehot_index=[None]*23
    counter=0
    for i in index:
        user_onehot_index[i]=user[2][i]+counter
        counter+=item_size_list[i]
    user[3]=user_onehot_index # user[3]

print "new user list end"






















#load event info
# creat a dict to link 01 and 02
# APP_NO:0	HANDLE_ID:1	COMM_NO:2	REQ_BEGIN_DATE:3
# REQ_FINISH_DATE:4	ORG_NO:5	BUSI_TYPE_CODE:6	WKST_BUSI_TYPE_CODE:7
comm_95598_dict={}
index_02=[0,1,2,3,4,5,6,7]
input=open('../data/test/02_s_comm_rec_test.tsv',"r")

flag = 0
for line in input:
    if flag != 0:
        line=line.strip('\n')
        li = re.split('\t', line)
        if len(li)==8:
            if len(li[0])>0:
                app_no=int(li[0])
                comm_95598_dict[app_no]=[None]*8
                for i in index_02:
                    if len(li[i])>0: comm_95598_dict[app_no][i]=li[i]
    flag+=1
input.close()
print "01 end"







# load from 01
# user_info_list[4]:event_list_01


# APP_NO:0	ID:1	BUSI_TYPE_CODE:2	URBAN_RURAL_FLAG:3  ORG_NO:4
# HANDLE_TIME:5      ACCEPT_CONTENT:6	HANDLE_OPINION:7	CALLING_NO:8
# ELEC_TYPE:9	CUST_NO:10	PROV_ORG_NO:11	CITY_ORG_NO:12
# index_01=[0,1,2,3,4,5,6,7,8,9,10,11,12]
index_01=[10]

input=open('../data/test/01_arc_s_95598_wkst_test.tsv',"r")
event_01=[None]*13
flag = 0
if len(index_01)>0:
    for line in input:
        if flag != 0:
            line=line.strip('\n')
            li = re.split('\t', line)
            if len(li)==13:
                if len(li[10])>0: cons_no=ints(li[10])
                event_01=[None]*13
                for i in index_01:
                    if len(li[i])>0: event_01[i]=li[i]
                if cons_no in cons_no_dict:
                    cons_no_dict[cons_no][4].append(event_01)
                # else:
                #     user_info_list=[[],[],[],[],[],[],[],[],[],[],[]]
                #     user_info_list[1]=cons_no_dict[911][1]
                #     user_info_list[2]=cons_no_dict[911][2]
                #     user_info_list[3]=cons_no_dict[911][3]
                #     user_info_list[1][7]=cons_no
                #     user_info_list[4].append(event_01)
                #     cons_no_dict[cons_no]=user_info_list
                if int(li[0]) in comm_95598_dict:
                    cons_no_dict[cons_no][5].append(comm_95598_dict[int(li[0])])
        flag+=1
    input.close()
print "01 end"


# load from 02
# user_info_list[5]:event_list_02










# load from 03
# user_info_list[6]:event_list_03
# APP_NO:0	OVERSEE_TIME:1	CUST_NO:2	CUST_NAME:3
# OVERSEE_RESON:4	OVERSEE_CONTENT:5	OVERSEE_APP_NO:6
# ORG_OR_DEPT:7	APP_BUSI_TYPE_CODE:8	ORG_NO:9
# index_03=[0,1,2,3,4,5,6,7,8,9]
index_03=[2]

input=open('../data/test/03_s_info_oversee_test.tsv',"r")
event_03=[None]*10
flag = 0
if len(index_03)>0:
    for line in input:
        if flag != 0:
            line=line.strip('\n')
            li = re.split('\t', line)
            if len(li)==10 and len(li[2])>0:
                cons_no=ints(li[2])
                event_03=[None]*10
                for i in index_03:
                    if len(li[i])>0: event_03[i]=li[i]
                if cons_no in cons_no_dict:
                    cons_no_dict[cons_no][6].append(event_03)
                # else:
                #     user_info_list=[[],[],[],[],[],[],[],[],[],[],[]]
                #     user_info_list[1]=cons_no_dict[911][1]
                #     user_info_list[2]=cons_no_dict[911][2]
                #     user_info_list[3]=cons_no_dict[911][3]
                #     user_info_list[1][7]=cons_no
                #     user_info_list[6].append(event_03)
                #     cons_no_dict[cons_no]=user_info_list
        flag+=1
    input.close()

print "03 end"




# load from 08
# user_info_list[7]:event_list_08
# 77777777777777777777777777777777777777777
# ORG_NO:0	CONS_NO:1	RCVED_YM:2	RCVED_DATE:3
# THIS_RCVED_AMT:4	THIS_PENALTY:5	OWE_AMT:6	RCVBL_YM:7	RCVBL_PENALTY:8
# index_08=[0,1,2,3,4,5,6,7,8]
index_08=[]
input=open('../data/test/08_a_rcved_flow_test.tsv',"r")
event_08=[None]*9
flag = 0
if len(index_08)>0:
    for line in input:
        if flag != 0:
            line=line.strip('\n')
            li = re.split('\t', line)
            if len(li)==9 and len(li[1])>0:
                cons_no=ints(li[1])
                event_08=[None]*9
                for i in index_08:
                    if len(li[i])>0: event_08[i]=li[i]
                if cons_no in cons_no_dict:
                    cons_no_dict[cons_no][7].append(event_08)
                # else:
                #     user_info_list=[[],[],[],[],[],[],[],[],[],[],[]]
                #     user_info_list[1]=cons_no_dict[911][1]
                #     user_info_list[2]=cons_no_dict[911][2]
                #     user_info_list[3]=cons_no_dict[911][3]
                #     user_info_list[1][7]=cons_no
                #     user_info_list[7].append(event_08)
                #     cons_no_dict[cons_no]=user_info_list
        flag=1
    input.close()

print "08 end"







# load from 09
# user_info_list[8]:event_list_09
# 88888888888888888888888888888888888888888888888888888888
# CONS_NO:0	RCVBL_YM:1	ORG_NO:2	PAY_MODE:3
# T_PQ:4	RCVBL_AMT:5	RCVED_AMT:6	STATUS_CODE:7
# RCVBL_PENALTY:8	RCVED_PENALTY:9	RISK_LEVEL_CODE:10	OWE_AMT:11
# CONS_SORT_CODE:12	ELEC_TYPE_CODE:13	CTL_MODE:14
# index_09=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
index_09=[0,5,8]

input=open('../data/test/09_arc_a_rcvbl_flow_test.tsv',"r")
event_09=[None]*15
flag = 0
if len(index_09)>0:
    for line in input:
        if flag != 0:
            line=line.strip('\n')
            li = re.split('\t', line)
            if len(li)==15 and len(li[0])>0:
                cons_no=ints(li[0])
                event_09=[None]*15
                for i in index_09:
                    if len(li[i])>0: event_09[i]=li[i]
                if cons_no in cons_no_dict:
                    cons_no_dict[cons_no][8].append(event_09)
                # else:
                #     user_info_list=[[],[],[],[],[],[],[],[],[],[],[]]
                #     user_info_list[1]=cons_no_dict[911][1]
                #     user_info_list[2]=cons_no_dict[911][2]
                #     user_info_list[3]=cons_no_dict[911][3]
                #     user_info_list[1][7]=cons_no
                #     user_info_list[8].append(event_09)
                #     cons_no_dict[cons_no]=user_info_list
        flag=1
    input.close()

print "09 end"







# load from 10
# user_info_list[9]:event_list_10
# not needed ..









# load from 12
# user_info_list[10]:event_list_12
# CONS_NO:0	ORG_NO:1	CHARGE_YM:2	CHARGE_DATE:3	PAY_MODE:4
# index_12=[0,1,2,3,4]

index_12=[]
input=open('../data/test/12_a_pay_flow_test.tsv',"r")
event_12=[None]*5
flag = 0
if len(index_12)>0:
    for line in input:
        if flag != 0:
            line=line.strip('\n')
            li = re.split('\t', line)
            if len(li)==5 and len(li[0])>0:
                cons_no=ints(li[0])
                event_12=[None]*5
                for i in index_12:
                    if len(li[i])>0: event_12[i]=li[i]
                if cons_no in cons_no_dict:
                    cons_no_dict[cons_no][10].append(event_12)
                # else:
                #     user_info_list=[[],[],[],[],[],[],[],[],[],[],[]]
                #     user_info_list[1]=cons_no_dict[911][1]
                #     user_info_list[2]=cons_no_dict[911][2]
                #     user_info_list[3]=cons_no_dict[911][3]
                #     user_info_list[1][7]=cons_no
                #     user_info_list[10].append(event_12)
                #     cons_no_dict[cons_no]=user_info_list
        flag=1
    input.close()

print "12 end"


# 95598 times for each user
# 95598_times saved in user_info_list[0][1]

# comm_times for each user
# comm_times saved in user_info_list[0][2]

# oversee_times for each user
# oversee_times saved in user_info_list[0][3]

# panalty_times for each user
# panalty_times saved in user_info_list[0][4]

# panalty_money_average for each user
# panalty_money_average saved in user_info_list[0][5]

# panalty_money_divide_money_average for each user
# panalty_money_divide_money_average saved in user_info_list[0][6]

# user_info_list[4]:event_list_01
# user_info_list[5]:event_list_02
# user_info_list[6]:event_list_03
# user_info_list[7]:event_list_08
# user_info_list[8]:event_list_09
# user_info_list[9]:event_list_10
# user_info_list[10]:event_list_12

for user in cons_no_dict.values():
    if len(user[0])<1:user[0].append(None)
    user[0].append(len(user[4]))
    user[0].append(len(user[5]))
    user[0].append(len(user[6]))

# load from 09
# user_info_list[8]:event_list_09
# 88888888888888888888888888888888888888888888888888888888
# CONS_NO:0	RCVBL_YM:1	ORG_NO:2	PAY_MODE:3
# T_PQ:4	RCVBL_AMT:5	RCVED_AMT:6	STATUS_CODE:7
# RCVBL_PENALTY:8	RCVED_PENALTY:9	RISK_LEVEL_CODE:10	OWE_AMT:11
# CONS_SORT_CODE:12	ELEC_TYPE_CODE:13	CTL_MODE:14
    panalty_times=0
    panalty_money_average=0.0
    panalty_money_divide_money_average=0.0
    if len(user[8])>0:
        for event in user[8]:
            if float(event[8])>0:
                panalty_times+=1
                panalty_money_average+=float(event[8])
                if float(event[5])>0: panalty_money_divide_money_average=float(event[8])/float(event[5])
        if panalty_times >0:
            panalty_money_average/=panalty_times
            panalty_money_divide_money_average/=panalty_times
    user[0].append(panalty_times)
    user[0].append(panalty_money_average)
    user[0].append(panalty_money_divide_money_average)




#######################################
index=[0,3,4,8,9,10,11,13,15,16,17,18,19,20,21,22]
input_index=open('../data/train/item_onehot_index_dict.txt',"r")
#   user[13] [22] [12] are int
#   other = -1
onehot_index_dict_list=[None]*23
for i in index:
    onehot_index_dict_list[i]={}

max_index=0
for line in input_index:
    line=line.strip('\n')
    li = re.split(' ', line)
    ind = int(li[0])
    if int(li[2])>max_index:max_index=int(li[2])
    if ind==13 or ind==22 or ind==12 or ind ==18 or ind ==3:
        if li[1]=='other':
            onehot_index_dict_list[ind]['other']=int(li[2])
        elif li[1]=='None':
            onehot_index_dict_list[ind][None]=int(li[2])
        else:
            onehot_index_dict_list[ind][li[1]]=int(li[2])
    else:
        if li[1]=='other':
            onehot_index_dict_list[ind]['other']=int(li[2])
        elif li[1]=='None':
            onehot_index_dict_list[ind][None]=int(li[2])
        else:
            onehot_index_dict_list[ind][int(li[1])]=int(li[2])

input_index.close()



output_index=open('../data/test/test_user_onehot_index.txt',"w")
for user in cons_no_dict.values():
    output_index.write('0 ')
    for i in index:

        if user[1][i] not in onehot_index_dict_list[i]:
            output_index.write(str(onehot_index_dict_list[i]['other']))
            output_index.write(':1 ')
        elif user[1][i]!=None:
            output_index.write(str(onehot_index_dict_list[i][user[1][i]]))
            output_index.write(':1 ')
    for j in range(1,7):
        if len(user[0])>j:
            if user[0][j]!=None:
                if user[0][j]>0:
                    output_index.write(str(max_index+j))
                    output_index.write(':')
                    output_index.write(str(user[0][j]))
                    output_index.write(' ')
    output_index.write('\n')
output_index.write('0 ')
output_index.write(str(max_index+6))
output_index.write(':0')
output_index.write('\n')
output_index.close()



