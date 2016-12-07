#!/usr/bin/python
import re


cons_no_dict={}
#APP_NO:0	ID:1	BUSI_TYPE_CODE:2	URBAN_RURAL_FLAG:3	ORG_NO:4	HANDLE_TIME:5	ACCEPT_CONTENT:6	HANDLE_OPINION:7	CALLING_NO:8	ELEC_TYPE:9	CUST_NO:10	PROV_ORG_NO:11	CITY_ORG_NO:12
input=open('../data/test/01_arc_s_95598_wkst_test.tsv',"r")
flag = 0
for line in input:
    if flag != 0:
        line=line.strip('\n')
        li = re.split('\t', line)
        if len(li)==13:
            if len(li[8])>0:
                if int(li[10]) in cons_no_dict:
                    if int(li[8]) not in cons_no_dict[int(li[10])]:
                        cons_no_dict[int(li[10])].append(int(li[8]))
                else:
                    cons_no_dict[int(li[10])]=[]
                    cons_no_dict[int(li[10])].append(int(li[8]))
    flag+=1
input.close()


input=open('../data/test/test_to_predict.csv',"r")
output=open('../data/test/predict_user_calling_no.txt',"w")
flag = 0
counter_user_has_no_calling_no=0
counter_user_has_one_calling_no=0
counter_user_has_many_calling_no=0

for line in input:
    line=line.strip('\n')
    if int(line) in cons_no_dict:
        for no in cons_no_dict[int(line)]:
            output.write(str(no))
            output.write('\n')
        if len(cons_no_dict[int(line)])==1:counter_user_has_one_calling_no+=1
        else :counter_user_has_many_calling_no+=1
    else: counter_user_has_no_calling_no+=1



print 'counter_user_has_no_calling_no='+str(counter_user_has_no_calling_no)
print 'counter_user_has_one_calling_no='+str(counter_user_has_one_calling_no)
print 'counter_user_has_many_calling_no='+str(counter_user_has_many_calling_no)
input.close()
output.close()




