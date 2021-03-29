# _*_coding : 
# 开发团队 ：
# 开发人员 ：GuoTao
# 开发时间 ：2021/3/29  18:20
# 文件名称 ：lesson6.py
# 开发工具 ：PyCharm

import pandas as pd
from fbprophet import Prophet
#数据加载
train = pd.read_csv('./train.csv')
# print(train)

#数据转化，以每天为单位采样
train['Datetime']=pd.to_datetime(train['Datetime'])

train.index= train['Datetime']
train.drop(['ID','Datetime'],axis=1,inplace=True)

daily_train= train.resample('D').sum()#'D'表示以天为单位


#采用预留字符
daily_train['ds']= daily_train.index
daily_train['y']=daily_train['Count']

daily_train.drop(['Count'],axis=1,inplace=True)
# print(daily_train)

#创建模型
m = Prophet(yearly_seasonality=True, seasonality_prior_scale=0.1)
# 预测未来7个月，213天
m.fit(daily_train)
future = m.make_future_dataframe(periods=213)
print(future)
forecast = m.predict(future)
print(forecast)
m.plot(forcast)