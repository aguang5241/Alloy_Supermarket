import sqlite3
import pandas as pd

db_file = 'AlloySupermarket/res/AsDB.db'
csv_file = 'AlloySupermarket/res/AsDB.csv'

data_list = []

def get_data():
    data = pd.read_csv(csv_file)
    # print(data)
    Al = data['EL_Al']
    Si = data['EL_Si']
    Mg = data['EL_Mg']
    Sc = data['EL_Sc']
    UTS = data['UTS']
    YS = data['YS']
    EL = data['EL']
    for i in range(len(Al)):
        # print(i)
        data_list.append((Al[i], Si[i], Mg[i], Sc[i], UTS[i], YS[i], EL[i]))
    # print(len(data_list))
    insert_mult_data(data_list)


def insert_mult_data(data):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    sql = 'insert into Al_Si_Mg_Sc(Al, Si, Mg, Sc, UTS, YS, El) values (?, ?, ?, ?, ?, ?, ?)'
    # 插入多条数据
    cur.executemany(sql, data)
    conn.commit()
    cur.close()
    conn.close()
    print(cur.rowcount)

# get_data()