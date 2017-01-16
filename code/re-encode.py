#!/usr/bin/python

#-*- coding: utf-8 -*-

from __future__ import division
import re

def ints(x):
    try:
        y = int(x)
        return y
    except ValueError:
        return None

def init_user_info_list(len=20):
    # do get a user_info_list
    b = []
    # user_info_list = [[], [], [], [], [], [], [], [], [], [], []]
    for i in range(0, len):
        b.append([])
    return b

def init_categorical_dict_list(len):
    b=[]
    for i in range(0,len):
        b.append({})
    return b

# data structure:
# for each user :user_info_list=[[], [], [], [], [], [], [], [], [], [], []]
# user_info_list[1]-[12] for file info
# user_info_list[13] for merged categorical data
# user_info_list[14] for merged continous data
# user_info_list[15] for categorical index
# for all users :user_info_dict={CONS_NO:user_info_list}


def load_file(cons_no_dict,cons_id_dict,file_no,file_path):
    input = open(file_path, "r")
    flag = 0
    for line in input:
        if flag == 0:
            line = line.strip('\n')
            li = re.split('\t', line)
            items_no = len(li)

            cons_no_index = -1
            if "CONS_NO" in li:
                cons_no_index = li.index("CONS_NO")

            cons_id_index = -1
            if "CONS_ID" in li:
                cons_id_index = li.index("CONS_ID")

            if cons_no_index == -1 and cons_id_index == -1:
               break

    if flag != 0:
        line = line.strip('\n')
        li = re.split('\t', line)
        if len(li) == items_no:
            user = [None] * items_no

            for i in range(0, items_no):
                if len(li[i]) > 0: user[i] = li[i]

            if cons_id_index != -1:
                cons_id = ints(li[cons_id_index])
                if cons_id in cons_id_dict:
                  cons_id_dict[cons_id][file_no] = user

            if cons_no_index != -1:
                cons_no = ints(li[cons_no_index])
                if cons_no in cons_no_dict:
                    cons_no_dict[cons_no][file_no] = user
    flag += 1
    input.close()
    print str(file_no)+" end"


def load_event_file(cons_no_dict,cons_id_dict,file_no,file_path):
        # file 12/9/8/3/1/00/
    input = open(file_path, "r")
    flag = 0
    for line in input:
        if flag == 0:
            line = line.strip('\n')
            li = re.split('\t', line)
            items_no = len(li)

            cons_no_index = -1
            cons_id_index = -1
            cust_no_index = -1
            if "CONS_NO" in li:
                cons_no_index = li.index("CONS_NO")

            elif "CONS_ID" in li:
                cons_id_index = li.index("CONS_ID")

            elif "CUST_NO" in li:
                cust_no_index = li.index("CUST_NO")

            else:
                break

        if flag != 0:
            line = line.strip('\n')
            li = re.split('\t', line)
            if len(li) == items_no:
                event = [None] * items_no

                for i in range(0, items_no):
                    if len(li[i]) > 0: event[i] = li[i]


                if cons_id_index != -1:
                    cons_id = ints(li[cons_id_index])
                    if cons_id in cons_id_dict:
                        cons_id_dict[cons_id][file_no].append(event)

                elif cons_no_index != -1:
                    cons_no = ints(li[cons_no_index])
                    if cons_no in cons_no_dict:
                        cons_no_dict[cons_no][file_no].append(event)

                elif cust_no_index != -1:
                    cons_no = ints(li[cons_no_index])
                    if cons_no in cons_no_dict:
                        cons_no_dict[cons_no][file_no].append(event)

        flag += 1
    input.close()
    print str(file_no)+" end"


def load_file_from_04(cons_no_dict,cons_id_dict,file_no,file_path='../data/train/04_c_cons.tsv'):
    input = open(file_path, "r")
    flag = 0
    for line in input:
        if flag == 0:
            line = line.strip('\n')
            li = re.split('\t', line)
            items_no = len(li)
            if "CONS_NO" in li:
                cons_no_index= li.index("CONS_NO")
            if "CONS_ID" in li:
                cons_id_index = li.index("CONS_ID")

        if flag != 0:
            line = line.strip('\n')
            li = re.split('\t', line)

            if len(li) == items_no:
                user = [None] * items_no
                user_info_list = init_user_info_list()
                cons_no = ints(li[cons_no_index])
                cons_id = ints(li[cons_id_index])

                for i in range(0,items_no):
                    if len(li[i]) > 0: user[i] = li[i]

                user_info_list[4] = user
                cons_id_dict[cons_id] = user_info_list
                cons_no_dict[cons_no] = user_info_list


        flag += 1
    input.close()
    print "4 end"



def init_items_in_file(items_in_file_list,file_no,file_path):
    input = open(file_path, "r")
    flag = 0
    for line in input:
        if flag == 0:
            line = line.strip('\n')
            li = re.split('\t', line)
            items_no = len(li)
            for i in range(0,items_no):
                items_in_file_list[file_no][li[i]]= i
        else:
            break

        flag = 1
    input.close()

# categorical_item_index_dict={}
# def add_categorical_item_to_dict(item,categorical_item_index_dict=categorical_item_index_dict):
#     categorical_item_index_dict[item]=len(categorical_item_index_dict)



categorical_item_list=[
    "RCA_FLAG", "CONS_ID", "CONS_SORT_CODE", "TYPE_CODE",
    "APPR_OPINION",  "METER_ID", "CONS_NO", "TS_FLAG", "STATUS", "STATUS_CODE",
    "CONT_TYPE", "MEAS_BOX", "TRADE_CODE","HEC_INDUSTRY_CODE",
    "CONS_STATUS", "ORG_NO", "ELEC_TYPE_CODE", "LODE_ATTR_CODE", "URBAN_RURAL_FLAG",
    "SORT_CODE", "CONTRACT_CAP" ]
# remove , "ELEC_ADDR"

def merge_categorical_data_for_user(cons_no_dict,categorical_item_list):
    """

    :param cons_no_dict:
    :param categorical_item_list:
    :return:
    """
    # in user_info_list[0] also cons_no_dict[CONS_NO][0]
    for user in cons_no_dict.values():
        user[13]=init_user_info_list(len(categorical_item_list))
        for item in categorical_item_list:
            index=categorical_item_list.index(item)
            # if user has this data
            for file_no in range(1,13):
                if item in items_in_file_list[file_no]:
                    if len(user[file_no])>items_in_file_list[file_no][item]:
                        data=user[file_no][items_in_file_list[file_no][item]]
                        user[13][index].append(data)
                    break

def cal_categorical_index(cons_no_dict, categorical_item_list, ignore_rate):
    """
    calculate the categorical data index and save it in user_info_list[15]

    :param cons_no_dict:
    :param categorical_item_list:
    :param ignore_rate: long tail data
    :return: no return
    """
    for user in cons_no_dict.values():
        user[15] = [None] * len(categorical_item_list)

    for item in categorical_item_list:

        total_num=0
        item_value_dict = {}
        index_in_list=categorical_item_list.index(item)
        for user in cons_no_dict.values():
            categorical_data_list=user[13]
            if len(categorical_data_list[index_in_list])==0:
                continue
            cur_data = categorical_data_list[index_in_list][0]
            if cur_data == None:
                continue
            elif cur_data not in item_value_dict:
                item_value_dict[cur_data]=1
                total_num+=1
            else:
                item_value_dict[cur_data] += 1
                total_num += 1

        no=0
        tmp_dict={}
        for data in item_value_dict:
            if data not in tmp_dict:
                if item_value_dict[data]/total_num<ignore_rate:
                    tmp_dict[data]=0
                    # print item
                    # print data
                    # print str(item_value_dict[data]/total_num)
                else:
                    no+=1
                    tmp_dict[data]=no

        for user in cons_no_dict.values():
            categorical_data_list = user[13]
            if len(categorical_data_list[index_in_list]) == 0:
                user[15][index_in_list]=0
                continue
            cur_data = categorical_data_list[index_in_list][0]
            if cur_data == None:
                user[15][index_in_list] = 0
            else:
                user[15][index_in_list]=tmp_dict[cur_data]

    max=0
    cur_max=0
    for i in range(0,len(categorical_item_list)):
        for user in cons_no_dict.values():
            user[15][i]+=(max+1)
            if user[15][i]>cur_max:
                cur_max = user[15][i]
        max=cur_max




def output_categorical_index(cons_no_dict,output_file_path):
    """

    :param cons_no_dict:
    :param output_file_path: "../data/train/train_user_onehot_index.txt"
    :return:
    """
    output_onehot = open(output_file_path, "w")

    for user in cons_no_dict.values():
        output_onehot.write(str(user[0]))
        output_onehot.write(" ")
        for index in user[15]:
            output_onehot.write(str(index))
            output_onehot.write(":1 ")
        output_onehot.write('\n')
    output_onehot.close()




def get_and_add_label(file_path,cons_no_dict):
    """

    :param file_path:
    :param cons_no_dict:
    :return:
    """
    input_label = open(file_path, "r")
    user_list_label = {}
    while 1:
        lines = input_label.readlines()
        if not lines:
            break
        for line in lines:
            line = ints(line.strip('\n'))
            user_list_label[line] = 1
    input_label.close()

    for cons_no in cons_no_dict:
        if cons_no in user_list_label:
            cons_no_dict[cons_no][0] = 1
        else:
            cons_no_dict[cons_no][0] = 0



# data structure
# RCA_FLAG:0	CONS_ID:1	LABEL:2	CONS_SORT_CODE:3	TYPE_CODE:4	APPR_OPINION:5
# METER_ID:6	CONS_NO:7	TS_FLAG:8	STATUS:9	STATUS_CODE:10	CONT_TYPE:11
# MEAS_BOX:12	TRADE_CODE:13	ELEC_ADDR:14	HEC_INDUSTRY_CODE:15	CONS_STATUS:16
# ORG_NO:17	ELEC_TYPE_CODE:18	LODE_ATTR_CODE:19	URBAN_RURAL_FLAG:20	SORT_CODE:21	CONTRACT_CAP:22

items_in_file_list=[]
for i in range(0,13):
    items_in_file_list.append({})

cons_id_dict = {}
cons_no_dict = {}


load_file_from_04(cons_no_dict,cons_id_dict,'../data/train/04_c_cons.tsv')
load_file(cons_no_dict,cons_id_dict,5,'../data/train/05_c_cons_prc.tsv')
load_file(cons_no_dict,cons_id_dict,6,'../data/train/06_cont_info.tsv')
load_file(cons_no_dict,cons_id_dict,7,'../data/train/07_c_rca_cons.tsv')
load_file(cons_no_dict,cons_id_dict, 11, '../data/train/11_c_meter.tsv')
load_event_file(cons_no_dict,cons_id_dict, 1, '../data/train/01_arc_s_95598_wkst_train.tsv')
load_event_file(cons_no_dict,cons_id_dict, 2, '../data/train/02_s_comm_rec.tsv')
load_event_file(cons_no_dict,cons_id_dict, 3, '../data/train/03_s_info_oversee.tsv')
load_event_file(cons_no_dict,cons_id_dict, 8, '../data/train/08_a_rcved_flow.tsv')
load_event_file(cons_no_dict,cons_id_dict, 9, '../data/train/09_arc_a_rcvbl_flow.tsv')
load_event_file(cons_no_dict,cons_id_dict, 12, '../data/train/12_a_pay_flow.tsv')

# print cons_no_dict

init_items_in_file(items_in_file_list, 1, '../data/train/01_arc_s_95598_wkst_train.tsv')
init_items_in_file(items_in_file_list, 2, '../data/train/02_s_comm_rec.tsv')
init_items_in_file(items_in_file_list, 3, '../data/train/03_s_info_oversee.tsv')
init_items_in_file(items_in_file_list, 4, '../data/train/04_c_cons.tsv')
init_items_in_file(items_in_file_list, 5, '../data/train/05_c_cons_prc.tsv')
init_items_in_file(items_in_file_list, 6, '../data/train/06_cont_info.tsv')
init_items_in_file(items_in_file_list, 7, '../data/train/07_c_rca_cons.tsv')
init_items_in_file(items_in_file_list, 8, '../data/train/08_a_rcved_flow.tsv')
init_items_in_file(items_in_file_list, 9, '../data/train/09_arc_a_rcvbl_flow.tsv')
init_items_in_file(items_in_file_list, 11, '../data/train/11_c_meter.tsv')
init_items_in_file(items_in_file_list, 12, '../data/train/12_a_pay_flow.tsv')


# for item in categorical_item_list:
#     add_categorical_item_to_dict(item)
# print categorical_item_index_dict
#
merge_categorical_data_for_user(cons_no_dict,categorical_item_list)

cal_categorical_index(cons_no_dict, categorical_item_list,0.0005)

get_and_add_label("../data/train/train_label.csv",cons_no_dict)

for user in cons_no_dict.values():
    print user[15]

output_categorical_index(cons_no_dict,"../data/train/train_user_onehot_index.txt")