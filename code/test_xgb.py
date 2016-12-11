import os
import sys
import random
import numpy as np
import xgboost as xgb
import tools


def count_positive(li, thr):
    count = 0
    for i in li:
        if i > thr - 1E-11:
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
        fo.write(out_line+'\n') # since trans from list, so '\n' is needed.
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
        fo.write(line)
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


def f1_score_by_abs_score(labels, preds, thr):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i in range(len(preds)):
        label = labels[i]
        prob = preds[i]
        if label > 0.5: # true
            if prob > thr - 1E-11: # positive
                tp = tp + 1
            else: # negative
                fn = fn + 1
        else: # false
            if prob > thr - 1E-11: # positive
                fp = fp + 1
            else: # negative
                tn = tn + 1
    precision = 1.0 * tp / (tp + fp)
    recall = 1.0 * tp / (tp + fn)
    f1_score = 2.0 * precision * recall / (precision + recall) if precision > 0 or recall > 0 else 0.0
    return f1_score, precision, recall, tp, tn, fp, fn


def f1_score_by_sort(labels, preds, thr):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    # results = zip(range(len(preds)), preds)
    # sort by value
    # s_keys = [k for (k,v) in sorted(results.items(), key=operator.itemgetter(1), reverse=True)]
    sorted_index = np.argsort(-preds)
    cut_line = int(len(preds)*thr)
    print "cut_line: " + `cut_line`
    prefer_index = sorted_index[:cut_line]
    # print prefer_index
    hate_index = sorted_index[cut_line:]
    # raw_input()
    # count
    for idx in prefer_index:
        # print `preds[idx]` + '\t' + `labels[idx]`
        if idx < cut_line: # positive
            # print labels[idx]
            if labels[idx] > 0.5: # true    
                tp = tp + 1
            else: # false
                fp = fp + 1
        else: # negative
            if labels[idx] > 0.5: # true
                fn = fn + 1
            else: # false
                tn = tn + 1
    precision = 1.0 * tp / (tp + fp)
    recall = 1.0 * tp / (tp + fn)
    f1_score = 2.0 * precision * recall / (precision + recall) if precision > 0 or recall > 0 else 0.0
    return f1_score, precision, recall, tp, tn, fp, fn


def get_pos_index(preds, thr):
    sorted_index = np.argsort(-preds)
    cut_line = int(len(preds)*thr)
    prefer_index = sorted_index[:cut_line]
    return prefer_index





# 0. INITIALIZATION
if len(sys.argv) < 2:
    print "python test_xgb.py debug(1/0) refresh_model(1/0) thr_search_flag(1/0) thr_or_cut(1/0)"
    exit(-1)
debug = True if int(sys.argv[1]) > 0 else False
refresh_flag = False
thr_search_flag = False
pred_file = 'test_to_predict.csv'
thr_or_cut = True
if len(sys.argv) > 2:
    refresh_flag = True if int(sys.argv[2]) > 0 else False
if len(sys.argv) > 3:
    thr_search_flag = True if int(sys.argv[3]) > 0 else False
if len(sys.argv) > 4:
    thr_or_cut = True if int(sys.argv[4]) > 0 else False




# 1. LOAD part
folder = "../ipinyou/1458/" if debug else "../data/"

# iPinYou
if debug:
    if not os.path.exists(folder + 'train.data'):
        transform_data(folder + 'train.yzx.txt', folder + 'train.data')
        shuffle_data(folder + 'train.data', folder + 'train.data')
    else:
        print "Found " + folder + 'train.data'
    if not os.path.exists(folder + 'test.data'):
        transform_data(folder + 'test.yzx.txt', folder + 'test.data')
    else:
        print "Found " + folder + 'test.data'

# Power sensitive
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
if debug:
    dtrain, deval = dmatrix_gen_eval(dtrain_full)
else:
    dtrain, deval = dmatrix_gen_eval(dtrain_full, ratio=0.4) # 0.6 + 0.4
    dpredict = dtest.slice(range(dtest.num_row()-1))
    deval, dtest = dmatrix_gen_eval(deval, ratio=0.5) # 0.2 + 0.2





# 2. TRAIN part
base_score = array_pos_ratio(dtrain_full.get_label()) # calculated from full train or sub train?
print "base_score: " + `base_score`
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
            'eval_metric': 'auc',
            # 'eval_metric': 'error',
            'objective': 'binary:logistic',
            # 'objective':'multi:softmax', 'num_class':2,
            'nthread':4
        }
num_round = 10
evallist  = [(dtrain, 'train'), (deval, 'eval')]
model_file = folder + 'xgb.model'
if not refresh_flag and os.path.exists(model_file) and os.path.isfile(model_file):
    bst = xgb.Booster({'nthread':4}) #init model
    bst.load_model(model_file) # load data
else:
    bst = xgb.train(param, dtrain, num_round, evallist)
    bst.save_model(folder + 'xgb.model')

# make prediction
preds = bst.predict(dtest)#, ntree_limit=bst.best_iteration)
max_prob = preds.max()
mean_prob = preds.mean()
print "max " + `preds.max()`
print "meam " + `preds.mean()`
print "len " + `len(preds)`
print "pos ratio: " + `1.0 * count_positive(preds, base_score) / len(preds)`





# 3. TEST part
best_thr = base_score + 1E-11
# best_thr = mean_prob
if not thr_search_flag:
    if thr_or_cut:
        f1_score, precision, recall, tp, tn, fp, fn = f1_score_by_abs_score(dtest.get_label(), preds, best_thr)
    else:
        f1_score, precision, recall, tp, tn, fp, fn = f1_score_by_sort(dtest.get_label(), preds, best_thr)
    print "f1_score\t" + `f1_score`
    print "precision\t" + `precision`
    print "recall\t" + `recall`
else: # thr searching method.
    print "Searching best thr ..."
    # random.seed(100)
    # value_set = random.sample(set(preds), 20)
    ran = [(0.8 + v * 0.02) for v in range(10)] + [(1.0 + v * 0.02) for v in range(10)]
    value_set = [best_thr * v for v in ran]
    best_f1 = -1.0
    best_thr = -1.0
    print "scale\tthr_v\tf1\tprec\trec"
    for (r,v) in zip(ran, value_set):
        if thr_or_cut:
            f1_score, precision, recall, tp, tn, fp, fn = f1_score_by_abs_score(dtest.get_label(), preds, v)
        else:
            f1_score, precision, recall, tp, tn, fp, fn = f1_score_by_sort(dtest.get_label(), preds, v)
        print "%.2f\t%.2f\t%.2f\t%.2f\t%.2f" % (r, v, f1_score, precision, recall)
        # `r` + '\t' + `v` + '\t' + `f1_score` + '\t' + `precision` + '\t' + `recall`
        if f1_score > best_f1:
            best_thr = v
            best_f1 = f1_score
    print "best thr: " + `best_thr`
    print "best f1: " + `best_f1`





# 4. PREDICT part
if not debug:
    pred_users = read_data_list(folder + pred_file)
    preds = bst.predict(dpredict)#, ntree_limit=bst.best_iteration)
    prefer_users = []
    # by threshold
    if thr_or_cut:
        for idx in range(len(preds)):
            if preds[idx] > best_thr - 1E-11:
                prefer_users.append(pred_users[idx])
    else:
        sorted_index = np.argsort(-preds)
        cut_line = int(len(preds)*best_thr)
        print "final cut_line: " + `cut_line`
        prefer_index = sorted_index[:cut_line]
        prefer_users = [pred_users[idx] for idx in prefer_index]
    save_data_list(prefer_users, folder + 'sens_user.txt')

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