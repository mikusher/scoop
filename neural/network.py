"""
Use pandas to read in the data in database (euro_all) and create a neural network to predict
"""

# use pandas to read in the data in database (euro_all) and create a neural network to predict

import pandas as pd
from numpy import float64
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import weka

import controller.database as db


# read data in database table euro_all, and create a neural network to predict
def brain_machine():
    # read data
    df = get_dataframe('view_all_content')
    df = df.drop(['million', 'game_date'], axis=1)

    ss = StandardScaler()

    data = pd.DataFrame(index=range(0, len(df)),
                        columns=['num_one', 'num_two', 'num_tre', 'num_fou', 'num_fiv', 'str_one', 'str_two'],
                        dtype=float64)
    for i in range(0, len(data)):
        data["num_one"][i] = df["num_one"][i]
        data["num_two"][i] = df["num_two"][i]
        data["num_tre"][i] = df["num_tre"][i]
        data["num_fou"][i] = df["num_fou"][i]
        data["num_fiv"][i] = df["num_fiv"][i]
        data["str_one"][i] = df["str_one"][i]
        data["str_two"][i] = df["str_two"][i]
    data.head()

    final_data = data.values
    train_data = final_data[0:200, :]
    valid_data = final_data[200:, :]
    return train_data, valid_data


def get_dataframe(table_name: str):
    # check if table_name not None, empty or null
    df = None
    if table_name is not None or table_name != '' or table_name != ' ':
        df = pd.read_sql_table(table_name, db.engine)
        df["Date"] = pd.to_datetime(df.game_date, format="%m/%d/%Y")
        df.index = df['Date']
        df = df.sort_index(ascending=True, axis=0)
    return df


# use weka to predict
def weka_predict(train_data, valid_data):
    from weka.classifiers import Classifier
    # create a weka model
    c = Classifier(name='weka.classifiers.trees.J48', ckargs={'-K': 1})
    # train the model
    c.train(train_data)
    # predict the model
    predicted = c.predict(valid_data)
    return predicted


# use weka to predict
def neural():
    train_data, valid_data = brain_machine()
    predicted = weka_predict(train_data, valid_data)
    return predicted
