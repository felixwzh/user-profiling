#!/usr/bin/python
import re




# data structure
# RCA_FLAG:0	CONS_ID:1	LABEL:2	CONS_SORT_CODE:3	TYPE_CODE:4	APPR_OPINION:5
# METER_ID:6	CONS_NO:7	TS_FLAG:8	STATUS:9	STATUS_CODE:10	CONT_TYPE:11
# MEAS_BOX:12	TRADE_CODE:13	ELEC_ADDR:14	HEC_INDUSTRY_CODE:15	CONS_STATUS:16
# ORG_NO:17	ELEC_TYPE_CODE:18	LODE_ATTR_CODE:19	URBAN_RURAL_FLAG:20	SORT_CODE:21	CONTRACT_CAP:22
user=[None]*23
cons_id_dict={}
cons_no_dict={}
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
input=open('./data/train/04_c_cons.tsv',"r")
flag = 0
for line in input:
    if flag != 0:
        line=line.strip('\n')
        li = re.split('\t', line)
        user=[None]*23
        cons_id=int(li[0])
        cons_no=int(li[1])
        if len(li[0])>0: user[1]=cons_id
        if len(li[1])>0: user[7]=cons_no
        # if len(li[2])>0: user[]=(li[2]) ADDR
        #?????
        # if len(li[3])>0: user[13]=int(li[3])
        if len(li[3])>0: user[13]=li[3]
        if len(li[4])>0: user[18]=int(li[4])
        # if len(li[5])>0: user[22]=int(li[5])
        if len(li[5])>0: user[22]=li[5]
        if len(li[6])>0: user[19]=int(li[6])
        if len(li[7])>0: user[15]=int(li[7])
        if len(li[8])>0: user[10]=int(li[8])
        if len(li[9])>0: user[17]=int(li[9])
        if len(li[10])>0: user[3]=int(li[10])
        if len(li[11])>0: user[20]=int(li[11])

        cons_id_dict[cons_id]=[cons_no,user]
        cons_no_dict[cons_no]=[cons_id,user]
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
input=open('./data/train/05_c_cons_prc.tsv',"r")
flag = 0
for line in input:
    if flag != 0:
        line=line.strip('\n')
        li = re.split('\t', line)
        cons_id=int(li[0])
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
input=open('./data/train/06_cont_info.tsv',"r")
flag = 0
for line in input:
    if flag != 0:
        line=line.strip('\n')
        li = re.split('\t', line)
        cons_no=int(li[0])
        if cons_no in cons_no_dict:
            # if len(li[1])>0: cons_no_dict[cons_no][1][5]=(li[1])
            if len(li[2])>0: cons_no_dict[cons_no][1][11]=int(li[2])
            if len(li[3])>0: cons_no_dict[cons_no][1][9]=int(li[3])
        else:
            user=[None]*23
            user[1]=cons_no
            # if len(li[1])>0: user[5]=(li[1])
            if len(li[2])>0: user[11]=int(li[2])
            if len(li[3])>0: user[9]=int(li[3])
            cons_no_dict[cons_no]=[None,user]
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
input=open('./data/train/07_c_rca_cons.tsv',"r")
flag = 0
for line in input:
    if flag != 0:
        line=line.strip('\n')
        li = re.split('\t', line)
        cons_no=int(li[0])
        if cons_no in cons_no_dict:
            if len(li[1])>0: cons_no_dict[cons_no][1][17]=int(li[1])
            if len(li[2])>0: cons_no_dict[cons_no][1][0]=int(li[2])
            if len(li[3])>0: cons_no_dict[cons_no][1][16]=int(li[3])
        else:
            user=[None]*23
            user[1]=cons_no
            if len(li[1])>0: user[17]=int(li[1])
            if len(li[2])>0: user[0]=int(li[2])
            if len(li)==4: user[16]=int(li[2])# the li[3] may not exist
            #add this to other load part?
            cons_no_dict[cons_no]=[None,user]
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
input=open('./data/train/11_c_meter.tsv',"r")
flag = 0
for line in input:
    if flag != 0:
        line=line.strip('\n')
        li = re.split('\t', line)
        if len(li[5])>0: cons_id=int(li[5])
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

#  load label
#get label_list
print "start get label_list "
input_label = open("./data/train/train_label.csv","r")
user_list_label = {}
while 1:
    lines = input_label.readlines()
    if not lines:
        break
    for line in lines:
        line=int(line.strip('\n'))
        user_list_label[line]=1
input_label.close()
print "label_list done"


print "start add label"
#add label to user
# data structure
# RCA_FLAG:0	CONS_ID:1	LABEL:2	CONS_SORT_CODE:3	TYPE_CODE:4	APPR_OPINION:5 'NL'
# METER_ID:6	CONS_NO:7	TS_FLAG:8	STATUS:9	STATUS_CODE:10	CONT_TYPE:11
# MEAS_BOX:12	TRADE_CODE:13	ELEC_ADDR:14 'NL'	HEC_INDUSTRY_CODE:15	CONS_STATUS:16
# ORG_NO:17	ELEC_TYPE_CODE:18	LODE_ATTR_CODE:19	URBAN_RURAL_FLAG:20	SORT_CODE:21	CONTRACT_CAP:22
for cons_no in cons_no_dict:
    if cons_no in user_list_label:
        cons_no_dict[cons_no][1][2]=1
    else:
        cons_no_dict[cons_no][1][2]=0
print "add label done"


#start encode
# data structure
# RCA_FLAG:0	CONS_ID:1	LABEL:2	CONS_SORT_CODE:3	TYPE_CODE:4	APPR_OPINION:5 'NL'
# METER_ID:6	CONS_NO:7	TS_FLAG:8	STATUS:9	STATUS_CODE:10	CONT_TYPE:11
# MEAS_BOX:12	TRADE_CODE:13	ELEC_ADDR:14 'NL'	HEC_INDUSTRY_CODE:15	CONS_STATUS:16
# ORG_NO:17	ELEC_TYPE_CODE:18	LODE_ATTR_CODE:19	URBAN_RURAL_FLAG:20	SORT_CODE:21	CONTRACT_CAP:22
def encode(*index):
    print "encode begin "
    encode_item_list_list=[None]*23
    global cons_no_dict


    #add fake user
    fake_user=['other']*23
    cons_no_dict[110]=[None,fake_user]
    #add None user
    None_user=[None]*23
    cons_no_dict[911]=[None,None_user]

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

        user.append(user_item_index)#
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
        user.append(user_onehot_index) # user[3]

    print "new user list end"

    # output the uservec without None value
    output_onehot = open("./data/train/train_user_onehot_index.txt","w")
    for user in cons_no_dict.values():
        #output label
        if user[1][2]>0:
            output_onehot.write("1")
            output_onehot.write("\t")
        else:
            output_onehot.write("0")
            output_onehot.write("\t")
        #output index of one
        for i in index:
            if user[2][i]!=1:
                output_onehot.write(str(user[3][i]))
                output_onehot.write("\t")
        output_onehot.write('\n')
    output_onehot.close()
    # end
    print "output end"



    output_index=open("./data/train/item_onehot_index_dict.txt","w")


    counter=0
    for i in index:
        for values in encode_item_list_list[i]:
            output_index.write(str(i))
            output_index.write('\t')
            output_index.write(str(values))
            output_index.write('\t')
            output_index.write(str(encode_item_list_list[i][values]+1+counter))
            output_index.write('\n')
        counter=item_size_list[i]+counter
    output_index.close()




encode(0,3,4,8,9,10,11,12,13,15,16,17,18,19,20,21,22)








