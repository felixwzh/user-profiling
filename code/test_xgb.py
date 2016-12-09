import os
import random
import numpy as np
import xgboost as xgb
import tools


def count_positive(li, thr):
    count = 0
    for i in li:
        if i > thr - 1E-10:
            count = count + 1
    return count

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
        lo = del_element(li, (1, 3)) # remove [1] market price and [2] bias items.
        out_line = ' '.join(lo)
        fo.write(out_line+'\n')
    fi.close()
    fo.close()
    print "Transformed " + in_path

def shuffle_data(in_path, out_path):
    if not os.path.isfile(in_path):
        print "ERROR: file not exist. " + in_path
        exit(-1)
    fi = open(in_path, 'r')
    lines = []
    for in_line in fi:
        lines.append(in_line)
    fi.close()

    random.seed(233)
    random.shuffle(lines)

    fo = open(out_path, 'w')
    for out_line in lines:
        fo.write(out_line)
    fo.close()

    print "Shuffled " + in_path


def read_data_list_split(in_path):
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


def read_data_list(in_path):
    if not os.path.isfile(in_path):
        print "ERROR: file not exist. " + in_path
        exit(-1)
    data_list = []
    fi = open(in_path, 'r')
    for line in fi:
        data_list.append(line)
    fi.close()
    return data_list


def save_data_list(dataset, out_path):
    if os.path.isfile(out_path):
        print "WARNING: may override the existed data."
    fo = open(out_path, 'w')
    for line in dataset:
        fo.write(line + '\n')
    fo.close()
    print "Saved " + out_path

def read_data_np(in_path):
    """
    Read in data source and return Numpy array of data.
    :param in_path:
    :return: array of dataset
    """
    data_list = read_data_list(in_path)
    data_array = np.array(data_list)
    return data_array


def list_split_eval(dataset=[], ratio=0.2, r_seed=233, seq_flag=False):
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
        shuffle_data(dataset, r_seed)
    s_line = int((1-ratio) * len(dataset))
    train_set = dataset[:s_line]
    eval_set = dataset[s_line:]
    return train_set, eval_set

def dmatrix_gen_eval(dm_full, ratio=0.2, r_seed=233):
    idx_list = range(dm_full.num_row())
    idx_set = set(idx_list)
    random.seed(r_seed)
    sam_set = set(random.sample(idx_set, int(len(idx_set) * ratio))) # eval
    diff_idx_set = idx_set - sam_set # train
    dm_train = dm_full.slice(list(diff_idx_set))
    dm_eval = dm_full.slice(list(sam_set))
    return dm_train, dm_eval


def shuffle_list(dataset=[], r_seed=666):
    dtype_name = type(data).__name__.lower()
    if dtype_name != 'list':
        print "Shuffle only support list type of data!"
        exit(-1)
    random.seed(r_seed)
    random.shuffle(dataset)
    return dataset

def list_pos_ratio(dataset=[]):
    dtype_name = type(dataset).__name__.lower()
    if dtype_name != 'list':
        print "Only support list type of data!"
        exit(-1)
    n_arr = np.array(dataset)
    return array_pos_ratio(n_arr)


def array_pos_ratio(dataset=np.array([])):
    dtype_name = type(dataset).__name__.lower()
    if dtype_name != 'ndarray':
        print "Only support ndarray type of data!"
        exit(-1)
    ratio = 1.0 * np.count_nonzero(dataset) / len(dataset)
    return ratio

# folder = "../data/"
folder = "../ipinyou/1458/"

if not os.path.exists(folder + 'train.data'):
    transform_data(folder + 'train.yzx.txt', folder + 'train.data')
    shuffle_data(folder + 'train.data', folder + 'train.data')
else:
    print "Found " + folder + 'train.data'
if not os.path.exists(folder + 'test.data'):
    transform_data(folder + 'test.yzx.txt', folder + 'test.data')
else:
    print "Found " + folder + 'test.data'

# train_data = read_data_list(folder + 'train.data')
# # process training data
# train_set, eval_set = list_split_eval(train_data); del train_data
# save_data_list(train_set, folder + 'training.data')
# save_data_list(eval_set, folder + 'eval.data')
# # TODO: negative downsampling
# done


while True:
    # read in data
    dtrain_full = xgb.DMatrix(folder + 'train.data')
    dtest = xgb.DMatrix(folder + 'test.data')
    # deval = xgb.DMatrix(folder + 'eval.data')

    if dtrain_full.num_col() != dtest.num_col():
        print "Please unify the col num of train and test: " + `dtrain_full.num_col() - 1`
        del dtrain_full; del dtest
        raw_input()
    else:
        break

print dtrain_full.num_row()
print dtrain_full.num_col()

print dtest.num_row()
print dtest.num_col()

# shuffle & split evaluation data
dtrain, deval = dmatrix_gen_eval(dtrain_full)

# specify parameters via map
base_score = array_pos_ratio(dtrain.get_label()) # calculated from full train or sub train?
param = {   
            'early_stopping_rounds': 2,
            'base_score': base_score,
            'subsample': 0.6,
            'eta': 0.01, 
            'gamma': 0.5,
            'min_child_weight': 1,
            'max_depth': 20,
            'silent': 0, 
            'scale_pos_weight': 0.7,
            'objective': 'binary:logistic',
            'eval_metric': 'auc',
            # 'eval_metric': 'error',
            # 'objective':'multi:softmax', 'num_class':2,
            'nthread':4
        }
num_round = 10
evallist  = [(dtrain, 'train'), (deval, 'eval')]
bst = xgb.train(param, dtrain, num_round, evallist)

# make prediction
preds = bst.predict(dtest, ntree_limit=bst.best_iteration)
print "max " + `preds.max()`
print "meam " + `preds.mean()`
print "len " + `len(preds)`
print "pos: " + `1.0 * count_positive(preds, base_score) / len(preds)`

# TEST part
# thr = 0.170
# count = 0
# for val in preds:
#     if val > 0.45:
#         count = count + 1
# print `count` + ' in ' + `len(preds)` + ' is positive.'


# xgb <- xgboost(data = data.matrix(X[,-1]), 
#  label = y, 
#  eta = 0.1,
#  max_depth = 15, 
#  nround=25, 
#  subsample = 0.5,
#  colsample_bytree = 0.5,
#  seed = 1,
#  eval_metric = "merror",
#  objective = "multi:softprob",
#  num_class = 12,
#  nthread = 3
# )