# coding = utf-8

import numpy as np
import math
import random
from utils import bootstrap
import split_tree

def choose_type(dataset, start,end):

    type_dict = {}

    for i in range(start,end):
        try:
            type_dict[dataset[i][-1]] += 1
        except KeyError:
            type_dict[dataset[i][-1]] = 1

    type = None
    count = 0
    for key,value in type_dict.items():
        if value>count:
            type = key

    return type

def choose_feature(dataset,start,end,feature_set):
    min_geni = 0.0
    min_f = None
    min_sv = None

    if end - start ==1 or len(set(dataset[start:end,-1])) ==1:
        new_branch = split_tree.TreeNode(None,None,True)
        new_branch.set_type(dataset[end][-1])

        return new_branch

    elif len(feature_set) == 1:
        type = choose_type(dataset,start,end)
        new_branch = split_tree.TreeNode(None, None, True)
        new_branch.set_type(dataset[end][-1])

        return new_branch


    for f in feature_set:
        feature_value = sorted(list(set(dataset[start:end,f])))
        split_list = [(feature_value[i] + feature_value[i + 1]) / 2 for i in range(len(feature_value) - 1)]

        for split_value in split_list:
            new_geni= cal_geni(dataset,start,end,f,split_value)

            if new_geni <min_geni:
                min_geni = new_geni
                min_f=f
                min_sv=split_value

    new_branch = split_tree.TreeNode(min_sv,min_f)

    i = trans_dataset(start,end,min_f,min_sv)

    new_feature = feature_set.remove(f)

    left_tree= choose_feature(dataset,start,i,new_feature)
    right_tree = choose_feature(dataset,i,end,new_feature)

    new_branch.extend(left_tree,right_tree)

    return new_branch

def trans_dataset(dataset,start,end,feature_id,feature_value):

    i = start
    j = end

    while i<j:
        if dataset[i][feature_id] >feature_value:
            tmp = dataset[j]
            dataset[j] = dataset[i]
            dataset[i] =tmp
        else:
            i +=1

    return i

def cal_geni(dataset,start,end,feature_id,feature_value): #to be changed

    f_le_count = {}
    f_ge_count = {}

    for i in range(start,end):
        if dataset[i][feature_id]< feature_value:
            try:
                f_le_count[dataset[i][-1]] += 1
            except KeyError:
                f_le_count[dataset[i][-1]]  = 1
        else:
            try:
                f_ge_count[dataset[i][-1]] += 1
            except KeyError:
                f_ge_count[dataset[i][-1]]  = 1

    total = end- start +1.0
    geni = 0.0

    for key,value in f_le_count.items():
        geni -=  key/total * math.log(key/total)

    for key,value in f_ge_count.items():
        geni -=  key/total * math.log(key/total)

    return  geni

def random_forest_classifier(dataset,random_number = None,tree_number = 10):

    rf = split_tree.RandomForest()
    end,feature = dataset.shape

    feature = range(feature-1)

    if random_number ==None:
        dataset_number = end/2




    for i in range(tree_number):

        sample_set = bootstrap(dataset,dataset_number)

        sample_feature = random.sample(feature,len(feature)/2)

        tree = choose_feature(sample_set,0,end/2,sample_feature)

        rf.Add_Tree(tree)

    return rf




if __name__ == '__main__':
    a = np.arange(0,20 ,0.5).reshape((-1,4))

    b =np.arange(0,20,1.0)
    c = [(b[i]+b[i+1])/2 for i in range(len(b)-1)]

    print a.shape[0]