from tensorflow.keras.models import load_model
import pymysql
import numpy as np
from sklearn.preprocessing import StandardScaler
import pandas as pd


def pre_value(code):
    load_model_path = "static/getdata/2.79_35_mem_5_lstm_1_dense_1_units_32.h5"
    data_path = "static/getdata/data/static_data/sortdata.csv"
    db = pymysql.connect(host="120.77.58.237", port=3306, user="Wzh", password="Wzh1192548088.", db="WebSite")
    cursor = db.cursor()
    # sql查寻5天数据
    sql = '''select Close,Highest,Lowest,Open,Volume from ''' + "WebSite.`" + code + "`"
    # print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()[1:]

    arr = np.array(data)
    arr = np.array(data)
    # 数据处理
    ori_data = pd.read_csv(data_path)
    ori_data = ori_data[["Close", "Highest", "Lowest", "Open", "Volume"]]
    scaler = StandardScaler()
    scaler.fit(ori_data)
    arr = scaler.transform(arr)
    data = arr[np.newaxis, :, :]
    model = load_model(load_model_path)
    pre_data = model.predict(data)
    print(pre_data.ravel())
    return pre_data.ravel()
