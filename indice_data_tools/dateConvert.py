# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 11:16:12 2020
此部分对数据的日期格式进行个性化的转换
@author: fyfse
"""
import datetime
import pandas as pd

#convert 期货合约到期日日期数据yyyy/mm/dd to yyyymmdd(int)
def convertDateStrToInt(deliveryDate):
    deliveryDateSeries = deliveryDate['delivery date'].str.split('/')
    
#    deliveryDateSeries = pd.Series(deliveryDate).str.split('-')
    for i in range(0, len(deliveryDateSeries)):
        month = deliveryDateSeries[i][1]
        day = deliveryDateSeries[i][2]
        if len(month) == 1:
            month = '0' + month
        if len(day) == 1:
            day = '0' + day
        deliveryDateSeries[i] = int(deliveryDateSeries[i][0] + month + deliveryDateSeries[i][2])
    return deliveryDateSeries

#def convertDateStrToInt2(input_list):
##    deliveryDateSeries = deliveryDate['合约到期日'].str.split('/')
#    two_D_list = input_list.split('/')
#    for i in range(0, len(deliveryDateSeries)):
#        month = deliveryDateSeries[i][1]
#        if len(month) == 1:
#            month = '0' + month
#        deliveryDateSeries[i] = int(deliveryDateSeries[i][0] + month + deliveryDateSeries[i][2])
#    return deliveryDateSeries

#对日期进行自然日的加减以求得前后某天的日期，返回yyyymmdd(int)
def calculateLimitDate(d, t):
    s = str(d)[0:4] + '-' + str(d)[4:6] + '-' + str(d)[6:8]
    date = datetime.datetime.strptime(s,'%Y-%m-%d').date()
    limit = date + datetime.timedelta(days=-t)
    str_p = datetime.datetime.strftime(limit,'%Y/%m/%d')
    sl = str_p.split('/')
    m = ''
    for i in range(0, len(sl)):
        m += sl[i]
    return int(m)

#deliveryDateIC = pd.read_csv('futuredeliveryIC.csv')
#deliveryDateSeries = dc.convertDateStrToInt(deliveryDateIC).loc[12:56]
#deliveryDateSeries.to_csv('delivery_date_series.csv', index = False, header = False)
