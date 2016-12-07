import os
import random
import numpy as np
import xgboost as xgb
import tools


def del_element(li, index):
    """
    To remove something from the list.
    :param li: list
    :param index: the index of the elements to be removed. m or (m, n)
    :return: new list
    """
    if tools.check_type(index, 'tuple'):
        return li[:index[0]] + li[index[1]:]
    elif tools.check_type(index, 'int'):
        return li[:index] + li[index+1:]
    else:
        print 'Index error!'
        return li


def transform_data(in_path, out_path):
    """
    Transform the YZX data to YX data.
    :param in_path: data path
    :param out_path: output data path
    :return:
    """
    if not os.path.isfile(in_path):
        print "ERROR: file not exist. " + in_path
        exit(-1)
    fi = open(in_path, 'r')
    fo = open(out_path, 'w')
    for in_line in fi:
        li = in_line.split()
        lo = del_element(li, (1, 3))
        out_line = ' '.join(lo)
        fo.write(out_line+'\n')
    fi.close()
    fo.close()


def read_data_list(in_path):
    """
    Read in data source and return list of data.
    :param in_path:
    :return: list of dataset
    """
    if not os.path.isfile(in_path):
        print "ERROR: file not exist. " + in_path
        exit(-1)
    data_list = []
    fi = open(in_path, 'r')
    for line in fi:
        li = line.split()
        data_list.append(li)
    fi.close()
    return data_list


def read_data_np(in_path):
    """
    Read in data source and return Numpy array of data.
    :param in_path:
    :return: array of dataset
    """
    data_list = read_data_list(in_path)
    data_array = np.array(data_list)
    return data_array


@tools.deprecated
def split_eval(dataset=[], ratio=0.2, r_seed=233, seq_flag=False):
    """
    Split the dataset into train set and evaluation set.
    :param dataset:
    :param ratio: evaluation set ratio of the original dataset
    :param r_seed: random seed
    :param seq_flag: True if sequentially split,
        otherwise shuffle the dataset then split
    :return:
    """
    if not seq_flag:
        random.seed(r_seed)
        random.shuffle(dataset)
    s_line = (1-ratio) * len(dataset)
    train_set = dataset[:s_line]
    eval_set = dataset[s_line:]
    return train_set, eval_set

folder = "../data/"

# transform_data(folder + 'train.yzx.txt', folder + 'train.data')
# transform_data(folder + 'test.yzx.txt', folder + 'test.data')

# read in data
# dtrain = xgb.DMatrix(folder + 'train.data')
# dtest = xgb.DMatrix(folder + 'test.data')

dtrain = xgb.DMatrix(folder + 'train/train_user_onehot_index.txt')
dtest = xgb.DMatrix(folder + 'test/test_user_onehot_index.txt')

print dtrain.num_col()
print dtrain.num_row()

print dtest.num_col()
print dtest.num_row()

# dtrain = xgb.DMatrix('./data/train.data')
# dtest = xgb.DMatrix('./data/test.data')

# specify parameters via map
param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'binary:logistic'}
watchlist = [(dtrain, 'train'), (dtest, 'eval')]
evallist  = [(dtrain, 'eval'), (dtrain, 'train')]
num_round = 2
bst = xgb.train(param, dtrain, num_round, evallist)

# make prediction
preds = bst.predict(dtest)