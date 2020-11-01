from data_preprocessing import decompress_pickle, compressed_pickle
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
import ipywidgets

import time
from functools import wraps

def logging(func):
    """function for logging the time

    Parameters
    ----------
    func: function
        the to measure function
    """
    @wraps(func)
    def logger(*args, **kwargs):
        """actual timer"""
        start = time.time()
        func(*args, **kwargs)
        print(f"Calling {func.__name__}: Needed {time.time() - start:.5f} seconds!")

    return logger

@logging

def catboost_regressor():
# load data
    df = decompress_pickle("./data/preprocessed/BikeRental_complete.pbz2")

    X = df.drop('cnt', axis = 1)
    X = X.drop('yr', axis=1) 
    X = X.drop('dteday', axis = 1)
    X = X.drop('atemp', axis = 1)
    X = X.drop('casual', axis = 1)
    X = X.drop('registered', axis = 1)
    Y = df['cnt']

    from sklearn.model_selection import train_test_split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=0)

    Y_train_mean = Y_train.mean()
    Y_train_meandev = sum((Y_train-Y_train_mean)**2)
    Y_test_meandev = sum((Y_test-Y_train_mean)**2)

    model = CatBoostRegressor(loss_function='RMSE', depth=10, learning_rate=0.05, iterations=1000, od_type='Iter', od_wait=10) 

    model.fit(
        X_train, Y_train, 
        use_best_model=True, 
        eval_set=(X_test, Y_test),
        verbose=True,  
        plot=True
        
    )

    Y_train_pred = model.predict(X_train)
    Y_train_dev = sum((Y_train-Y_train_pred)**2) 
    r2 = 1 - Y_train_dev/Y_train_meandev 
    print("R2 =", r2)

    Y_test_pred = model.predict(X_test)
    Y_test_dev = sum((Y_test-Y_test_pred)**2)
    pseudor2 = 1 - Y_test_dev/Y_test_meandev
    print("Pseudo-R2 =", pseudor2)

catboost_regressor()