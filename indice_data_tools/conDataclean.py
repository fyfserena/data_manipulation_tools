# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 10:05:41 2020

@author: fyf
"""
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

import dateConvert as dc
import dataClean
import datetime


#规定各合约乘数
MUL_IH = 300
MUL_IF = 300
MUL_IC = 200

while(True):
    YEAR = datetime.datetime.now().year
    MONTH = datetime.datetime.now().month
    DAY = datetime.datetime.now().day
    #run the file at 4am everyday
    START_TIME =  datetime.datetime(YEAR,MONTH,DAY,5,0,0,0)
    END_TIME =  datetime.timedelta(microseconds = 500000) + START_TIME
    if datetime.datetime.now() >= START_TIME and datetime.datetime.now() < END_TIME:
        # Option 1 读取原始行情数据并清理保持
        index016 = pd.read_csv('input/index016.csv') # 指数数据
        future01600 = pd.read_csv('input/IH00.csv') #00合约
        future01601 = pd.read_csv('input/IH01.csv') #01合约
        future01602 = pd.read_csv('input/IH02.csv') #02合约
        future01603 = pd.read_csv('input/IH03.csv') #03合约
        
        index300 = pd.read_csv('input/index300.csv')
        future30000 = pd.read_csv('input/IF00.csv')
        future30001 = pd.read_csv('input/IF01.csv')
        future30002 = pd.read_csv('input/IF02.csv')
        future30003 = pd.read_csv('input/IF03.csv')
        
        index905 = pd.read_csv('input/index905.csv')
        future90500 = pd.read_csv('input/IC00.csv')
        future90501 = pd.read_csv('input/IC01.csv')
        future90502 = pd.read_csv('input/IC02.csv')
        future90503 = pd.read_csv('input/IC03.csv')
        
        
          # 清理数据（1.缺失值使用前值填充，2.计算vwap, 3.在output文件输出形如'index016_filled.csv'的数据文档）
        index_IH = dataClean.souceDataFillNA(index016, 'index016', 1)   
        future00_IH = dataClean.souceDataFillNA(future01600, 'future01600', MUL_IH)
        future01_IH = dataClean.souceDataFillNA(future01601, 'future01601', MUL_IH)
        future02_IH = dataClean.souceDataFillNA(future01602, 'future01602', MUL_IH)
        future03_IH = dataClean.souceDataFillNA(future01603, 'future01603', MUL_IH)
        
        index_IF = dataClean.souceDataFillNA(index300, 'index300', 1)   
        future00_IF = dataClean.souceDataFillNA(future30000, 'future30000', MUL_IF)
        future01_IF = dataClean.souceDataFillNA(future30001, 'future30001', MUL_IF)
        future02_IF = dataClean.souceDataFillNA(future30002, 'future30002', MUL_IF)
        future03_IF = dataClean.souceDataFillNA(future30003, 'future30003', MUL_IF)
        
        index_IC = dataClean.souceDataFillNA(index905, 'index905', 1)   
        future00_IC = dataClean.souceDataFillNA(future90500, 'future90500', MUL_IC)
        future01_IC = dataClean.souceDataFillNA(future90501, 'future90501', MUL_IC)
        future02_IC = dataClean.souceDataFillNA(future90502, 'future90502', MUL_IC)
        future03_IC = dataClean.souceDataFillNA(future90503, 'future90503', MUL_IC)
    
        #Option 2： 若有已清理好的数据，则直接读取(运行以下被注释的语句） 
        #(注意把在output输出的filled文件放入input文件中同文件夹下)
        #index_IH = pd.read_csv('input/index016_filled.csv', index_col = [0])   
        #future00_IH = pd.read_csv('input/future01600_filled.csv', index_col = [0])
        #future01_IH = pd.read_csv('input/future01601_filled.csv', index_col = [0])
        #future02_IH = pd.read_csv('input/future01602_filled.csv', index_col = [0])
        #future03_IH = pd.read_csv('input/future01603_filled.csv', index_col = [0])
        #
        #index_IF = pd.read_csv('input/index300_filled.csv', index_col = [0])   
        #future00_IF = pd.read_csv('input/future30000_filled.csv', index_col = [0])
        #future01_IF = pd.read_csv('input/future30001_filled.csv', index_col = [0])
        #future02_IF = pd.read_csv('input/future30002_filled.csv', index_col = [0])
        #future03_IF = pd.read_csv('input/future30003_filled.csv', index_col = [0])
        #
        #index_IC = pd.read_csv('input/index905_filled.csv', index_col = [0])   
        #future00_IC = pd.read_csv('input/future90500_filled.csv', index_col = [0])
        #future01_IC = pd.read_csv('input/future90501_filled.csv', index_col = [0])
        #future02_IC = pd.read_csv('input/future90502_filled.csv', index_col = [0])
        #future03_IC = pd.read_csv('input/future90503_filled.csv', index_col = [0])
        
        
        
        '''
        校验合约到期日，合约到期日应小于等于期货数据最后一天
        input: deliveryDateSeries, future00 (默认四个期货合约数据日期一样)
        output：校验后的合约到期日
        '''
        def check_date_valid(deliveryDateSeries, future):
            last_date = future.date.unique()[-1]
            return deliveryDateSeries[deliveryDateSeries <= last_date]
            
        
        #读取合约到期日数据 （注意 ：合约到期日的日期范围 应 被包含于 指数/合约数据的日期范围）
        deliveryDateIH = pd.read_csv('input/futuredeliveryIH.csv', encoding = 'utf-8-sig') # 合约到期日数据
        deliveryDateSeries_IH = check_date_valid(dc.convertDateStrToInt(deliveryDateIH), future00_IH) # 调整原日期格式为所需格式并返回
        
        deliveryDateIF = pd.read_csv('input/futuredeliveryIF.csv', encoding = 'utf-8-sig')
        deliveryDateSeries_IF = check_date_valid(dc.convertDateStrToInt(deliveryDateIF), future00_IF)
        
        deliveryDateIC = pd.read_csv('input/futuredeliveryIC.csv', encoding = 'utf-8-sig')
        deliveryDateSeries_IC = check_date_valid(dc.convertDateStrToInt(deliveryDateIC), future00_IC)
        
        
            
#        def test_cdv():
#            deliveryDateIC = pd.read_csv('delivery_date_series.csv', encoding = 'utf-8-sig')
#            deliveryDateSeries_IC = dc.convertDateStrToInt(deliveryDateIC)
#            future00_IC = pd.read_csv('IC00.csv')
#            return check_date_valid(deliveryDateSeries_IC, futureIC00)
#            
            
        
        '''
        行情切片函数使用说明
        spreadRecord(deliveryDate, future00, future01, future02, future03, index, mul,
                         freq_list, data_type_list, index_name, if_start_from_t, if_0203_swift, if_fig)
        
            input(变量名 含义 数据格式): 
                   deliveryDate      合约的到期日  series/df
                   future00/01/02/03 合约行情数据  df
                   index             指数行情数据  df
                   mul               合约乘数      int(eg.300,200)
                   freq_list         需求切片的频率 list (默认[1,15,30,60] 单位：分钟)
                   data_type_list    需要切的数据对象  list (['spread', 'contracts', 'index'] （价差，合约行情，指数行情）)
                   index_name        指数名称       string (eg. IH IF IC)
                   if_start_from_t   True:切片从t日开始 False:从t+1开始  Bool
                   if_0203_swift     True:02/03合约在14710月向前平移  Flase：仅有01合约平移  Bool
                   if_fig            True:画价差图 False:不画图  Bool
        
        
        
        '''
        #使用举例
        #输出三个指数1m, 15m, 30m, 60m 的 价差，合约行情，指数行情切片数据 使用t+0 02，03合约平移的切片方法，不画图
        dataClean.spreadRecord(deliveryDateSeries_IH, future00_IH, future01_IH, future02_IH, future03_IH, index_IH, MUL_IH,
                               [1,30], ['spread', 'contracts', 'index'], 'IH', True, True, False)
        dataClean.spreadRecord(deliveryDateSeries_IF,future00_IF, future01_IF, future02_IF, future03_IF, index_IF, MUL_IF,
                               [1,30], ['spread', 'contracts', 'index'], 'IF', True, True, False)
        dataClean.spreadRecord(deliveryDateSeries_IC, future00_IC, future01_IC, future02_IC, future03_IC, index_IC, MUL_IC,
                               [1,30], ['spread', 'contracts', 'index'], 'IC', True, True, False)                  
      n  dataClean.spreadRecord(deliveryDateSeries_IH, future00_IH, future01_IH, future02_IH, future03_IH, index_IH, MUL_IH,
                               [1,30], ['spread', 'contracts', 'index'], 'IH', False, False, False)
        dataClean.spreadRecord(deliveryDateSeries_IF,future00_IF, future01_IF, future02_IF, future03_IF, index_IF, MUL_IF,
                               [1,30], ['spread', 'contracts', 'index'], 'IF', False, False, False)
        dataClean.spreadRecord(deliveryDateSeries_IC, future00_IC, future01_IC, future02_IC, future03_IC, index_IC, MUL_IC,
                               [1,30], ['spread', 'contracts', 'index'], 'IC', False, False, False)                  
        
        #输出三个指数30m的 价差切片数据 使用t+0 02,03合约平移的切片方法，并画价差图
        #dataClean.spreadRecord(deliveryDateSeries_IH, future00_IH, future01_IH, future02_IH, future03_IH, index_IH, MUL_IH,
        #                       [30], ['spread'], 'IH', True, True, True)      
        #dataClean.spreadRecord(deliveryDateSeries_IF, future00_IF, future01_IF, future02_IF, future03_IF, index_IF, MUL_IF,
        #                       [30], ['spread'], 'IF', True, True, True)      
        #dataClean.spreadRecord(deliveryDateSeries_IC, future00_IC, future01_IC, future02_IC, future03_IC, index_IC, MUL_IC,
        #                       [30], ['spread'], 'IC', True, True, True)      