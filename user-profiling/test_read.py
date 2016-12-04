import re



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


# --------------------------------------------------------------------------
# get items from s{04.05.06.07.11}.txt,and merge them into a list :item_all
item_04=get_items("/nas/Workspaces/zhwang/data/train/04_c_cons.tsv")
item_05=get_items("/nas/Workspaces/zhwang/data/train/05_c_cons_prc.tsv")
item_06=get_items("/nas/Workspaces/zhwang/data/train/06_cont_info.tsv")
item_07=get_items("/nas/Workspaces/zhwang/data/train/07_c_rca_cons.tsv")
item_11=get_items("/nas/Workspaces/zhwang/data/train/11_c_meter.tsv")

item_all = list(set(item_04+item_05+item_06+item_07+item_11+['LABEL']))

user_list_all=[]
user = {}.fromkeys(item_all)


#get user from s{04.05.06.07.11}.txt and add them to user_list_all
get_user_list("/nas/Workspaces/zhwang/data/train/04_c_cons.tsv",item_04)
get_user_list("/nas/Workspaces/zhwang/data/train/05_c_cons_prc.tsv",item_05)
get_user_list("/nas/Workspaces/zhwang/data/train/06_cont_info.tsv",item_06)
get_user_list("/nas/Workspaces/zhwang/data/train/07_c_rca_cons.tsv",item_07)
get_user_list("/nas/Workspaces/zhwang/data/train/11_c_meter.tsv",item_11)


# solve the problem that some user only has 'CONS_NO' or 'CONS_ID'
for user in user_list_all:
    if user['CONS_ID']=='None':
        user['CONS_ID']=user['CONS_NO']
    if user['CONS_NO']=='None':
        user['CONS_NO']=user['CONS_ID']


#merge
# merge users that have the same CONS_ID
user_CONS_ID_dict={}
for user in user_list_all:
    if user['CONS_ID'] not in user_CONS_ID_dict:
        user_CONS_ID_dict[user['CONS_ID']]=user
    else:
        for item in item_all:
            if user_CONS_ID_dict[user['CONS_ID']][item]=='None':
                user_CONS_ID_dict[user['CONS_ID']][item]=user[item]

#merge users that have the same CONS_NO
user_CONS_NO_dict={}
for user in user_CONS_ID_dict.values():
    if user['CONS_NO'] not in user_CONS_NO_dict:
        user_CONS_NO_dict[user['CONS_NO']]=user
    else:
        for item in item_all:
            if user_CONS_NO_dict[user['CONS_NO']][item]=='None':
                user_CONS_NO_dict[user['CONS_NO']][item]=user[item]


#get the final user_list
user_list=[]
for CONS_NO in user_CONS_NO_dict:
    user_list.append(user_CONS_NO_dict[CONS_NO])



#add label to user
for user in user_list:
    user['LABEL'] = 'None'



# get the encode_item list
encode_item=[]
input_index=open("item_onehot_index_dict.txt",'r')
while 1:
    lines = input_index.readlines()
    if not lines:
        break
    for line in lines:
        line=line.strip('\n')
        s1 = re.split('\t', line)
        if s1[0] not in encode_item:
            encode_item.append(s1[0])
input_index.close()

# get onehot_index_dict
onehot_index_dict={}.fromkeys(encode_item)

for item in encode_item:
    onehot_index_dict[item]={}
input_index=open("item_onehot_index_dict.txt",'r')
while 1:
    lines = input_index.readlines()
    if not lines:
        break
    for line in lines:
        line=line.strip('\n')
        s1 = re.split('\t', line)
        onehot_index_dict[s1[0]][s1[1]]=s1[2]


output_index= open("test_user_onehot_index.txt",'w')


for user in user_list:
    output_index.write('unlabeled'+'\t')
    index=[]
    for item in encode_item:
        if user[item] in onehot_index_dict[item].keys():
            index.append(int(onehot_index_dict[item][user[item]]))
        else:
            index.append(int(onehot_index_dict[item]['other']))
    index.sort()
    for i in index:
        output_index.write(str(i)+'\t')
    output_index.write('\n')

for item in encode_item:

    print onehot_index_dict[item].keys()
output_index.close()

# LABEL-2;APPR_OPINION-5 ;ELEC_ADDR-14; CONS_ID-1,CONS_NO-7,METER_ID-6  ignored

# RCA_FLAG:0	CONS_ID:1	LABEL:2	CONS_SORT_CODE:3	TYPE_CODE:4	APPR_OPINION:5
# METER_ID:6	CONS_NO:7	TS_FLAG:8	STATUS:9	STATUS_CODE:10	CONT_TYPE:11
# MEAS_BOX:12	TRADE_CODE:13	ELEC_ADDR:14	HEC_INDUSTRY_CODE:15	CONS_STATUS:16
# ORG_NO:17	ELEC_TYPE_CODE:18	LODE_ATTR_CODE:19	URBAN_RURAL_FLAG:20	SORT_CODE:21	CONTRACT_CAP:22
