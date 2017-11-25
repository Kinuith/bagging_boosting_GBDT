# coding = utf-8

import numpy as np
import  random

def bootstrap(dataset, n ,fetch= True): #dataset must be numpy.array

    length = dataset.shape[0]-1


    if fetch:

        j = random.randint(0, length)
        outputdata = np.array([dataset[j]], dtype=np.float32)

        for i in range(n-1):
            j = random.randint(0,length)

            outputdata=np.concatenate((outputdata,[dataset[j]]),axis=0)
    else:
        back_list = random.sample([i for i in range(length)])
        outputdata = np.array([dataset[back_list[0]]],dtype=np.float32)

        for i in range(n-1):
            outputdata = np.concatenate((outputdata,[dataset[i+1]]),axis=0)

    return outputdata





