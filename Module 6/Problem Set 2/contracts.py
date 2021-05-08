import numpy as np
import random as py_random
import numpy.random as np_random
import time
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import re

contractors = pd.ExcelFile('Top_100_Contractors_Report_Fiscal_Year_2015.xls')

names = contractors.sheet_names

departments = [re.search(".*00\)*",name) for name in names]

departments = list(filter(None,departments))

vendor_code = {}
vendor_code_df = pd.DataFrame()
dataset = pd.DataFrame()
vendor_id = 1
for item in departments:
    data_tmp = contractors.parse(item.string)
    #department= re.search("[A-Z]+[a-z]*",item.string).string
    for vendor_name in data_tmp['Global Vendor Name']:
        if vendor_name not in vendor_code:
            vendor_code[vendor_name] = vendor_id
            vendor_id = vendor_id+1
    data_tmp['vendor_code'] = data_tmp['Global Vendor Name'].map(vendor_code)
    #code = re.search("[0-9]+",item.string).string
    data_tmp['department'] = item.string
    dataset=dataset.append(data_tmp, ignore_index = True)
vendor_code_df = pd.DataFrame.from_dict(vendor_code,orient='index')
vendor_code_df.reset_index(level=0, inplace=True)
vendor_code_df.columns = ['global_vendor_name','id']
dataset['id'] = dataset.index
dataset.drop(['Global Vendor Name','%Total Actions','%Total Dollars'],axis = 1, inplace = True)

conn = sqlite3.connect('contracts.db')

conn.execute('''DROP TABLE IF EXISTS contractors''')
conn.execute('''DROP TABLE IF EXISTS actions''')
dataset.to_sql(name='actions',con=conn)
vendor_code_df.to_sql(name='contractors',con=conn)