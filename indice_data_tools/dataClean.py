# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 10:22:56 2020
此部分填补原数据缺失值、进行数据切片和价差绘图
@author: fyf
"""
import pandas as pd
import os
import matplotlib.pyplot as plt

#index name dic
dic = {'IC': '000905', 'IF':'000300',  'IH': '000016'}

#fill NA and calculate vwap -> write to 'output/' file
def souceDataFillNA(future, name, mul):
    future_filled = future.fillna(axis=0,method='ffill')
    future_filled['vwap'] = future_filled['amt']/future_filled['volume']/mul
    future_filled.fillna(0, inplace = True)
    if name != 0:
        future_filled.to_csv('output/' + name + '_filled.csv', index = False)
    
    return future_filled

def mkdir(path):
    path = path.strip()
    path = path.rstrip("/")
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path) 


#每个月开仓之后01-02,01-03的分钟closeprice价差 
def fig(df, date, feq, index_name, if_start_from_t):
    print('producing fig_'  + str(date))
    if if_start_from_t:
        version_name = 'v1'
    else:
        version_name = 'v2'
    output_path = 'output/fig_' + str(feq) + 'm/' + index_name + version_name + '/'   
    mkdir(output_path)
    fig = plt.figure()
    #此处可选画 01-02,01-03 或仅画 01-03
    name_list = df.columns.tolist()
    ax = df[name_list].plot(figsize = (45,25), use_index = True, fontsize=30, grid = True)
#    ax = df['01-03'].plot(figsize = (30,15), use_index = True, fontsize=30, grid = True)
#    ax.set_ylabel('01-03')
    fig=ax.get_figure()
    fig.savefig(output_path + str(date) + '.png')


def extractTodayData2(future, date):
    lim1 = 93000
    lim2 = 150000    
    
    future_today = future[(future['date'] == date) 
    & (future['clock'] <= lim2)
    & (future['clock'] >= lim1)]
    
    future_today.index = range(len(future_today))
    return future_today

def changeFuture1(future00, future01, future02, future03, date, k):
    if k >= 2:
        if str(date)[4:6] in ['01', '04', '07', '10']:
            f01 = future00
            f02 = future01
            f03 = future02
        else:
            f01 = future00
            f02 = future02
            f03 = future03
    else:
        f01 = future01
        f02 = future02
        f03 = future03
    return [f01, f02, f03]

def changeFuture2(future00, future01, future02, future03, date, k):
    if k >= 2:
        f01 = future00
        f02 = future02
        f03 = future03
    else:
        f01 = future01
        f02 = future02
        f03 = future03
    return [f01, f02, f03]


#原始价差是分钟数据，15m切片的高开低收就是每15分钟里面的原始价差的最高值、初始值、最低值、和期末值（高开低收）
#get max open min close
def getDesSpread(df, feq, dataType, mul):  
    clock_list = []
    if feq == 15:
        clock_list = [93000,94500,100000,101500,103000,104500,110000,111500,112900,
                      131500,133000,134500,140000,141500,143000,144500,150000]
    elif feq == 30:
        clock_list = [93000,100000,103000,110000,112900,133000,140000,143000,150000]
        
    elif feq == 60:
        clock_list = [93000,103000,112900,140000,150000]
        
    df_sparse = df[df['clock'].isin(clock_list)]

    res = pd.DataFrame()
    index_list = df_sparse.index.tolist()
    for i in range(0, len(index_list)-1):
        front = index_list[i] + 1
        if i == 0:
            front = index_list[i]
        
        tail = index_list[i+1]
        r = df.iloc[range(front, tail+1)]
        r['group'] = [i] * (tail - front +1)
        res = res.append(r)
    
    if dataType == 'spread':
        pds = []
        name_list = res.columns.tolist()[2:]
        for name in name_list:
            max_l = res.groupby('group')[name].max().tolist()
            min_l = res.groupby('group')[name].min().tolist()  
            first_l = res.groupby('group')[name].first().tolist()
            last_l = res.groupby('group')[name].last().tolist()
            clock_l = res.groupby('group')['clock'].last().tolist() 
            date_l = res.groupby('group')['date'].last().tolist() 
            volume_l= [0]*len(date_l)
            amt_l = [0]*len(date_l)
            vwap_l = [0]*len(date_l)
            pds.append(pd.DataFrame({'date':date_l, 'clock': clock_l, 'high': max_l, 'open': first_l,
                                     'low': min_l, 'close': last_l, 'volume' : volume_l, 'amt': amt_l,
                                     'vwap':vwap_l}))
        result =  pds
    
    else:
        max_l = res.groupby('group')['high'].max().tolist()
        min_l = res.groupby('group')['low'].min().tolist()  
        first_l = res.groupby('group')['open'].first().tolist()
        last_l = res.groupby('group')['close'].last().tolist()
        volume_l = res.groupby('group')['volume'].sum().tolist()
        amt_l = res.groupby('group')['amt'].sum().tolist()
        clock_l = res.groupby('group')['clock'].last().tolist() 
        date_l = res.groupby('group')['date'].last().tolist()
        vwap_l = []
        for i in range(len(amt_l)):
            if volume_l[i] == 0:
                vwap_l.append(0)
            else:
                vwap_l.append(amt_l[i]/volume_l[i]/mul)
    
        result = pd.DataFrame({'date':date_l, 'clock': clock_l, 'high': max_l, 'open': first_l,
                                     'low': min_l, 'close': last_l, 'volume' : volume_l, 'amt': amt_l,
                                     'vwap': vwap_l})
               
    return result




    

def spreadRecord(deliveryDate, future00, future01, future02, future03, index, mul,
                 freq_list,data_type_list,index_name,if_start_from_t, if_0203_swift,if_fig):
   # 3 different versions
    if if_start_from_t and if_0203_swift:
        version_name = 'v1'
    elif not if_start_from_t and not if_0203_swift:
        version_name = 'v2'
    elif if_start_from_t and not if_0203_swift:
        version_name = 'v3'
    
    for i in range(0, len(deliveryDate) - 1):
        #get the first and the last date of the month
        date = int(deliveryDate.iloc[i])
        date_next = int(deliveryDate.iloc[i+1])
        #get the work-day date within the month
        f_date = pd.DataFrame(future01.groupby('date')['date'].last())
        f_date_m = f_date[f_date['date'] <= date_next]
        f_date_m_list = f_date_m[f_date_m['date'] >= date]['date'].tolist()
        #calculate the res for 3 frequency [1,15,30,60]:       
        for feq in freq_list:
            for data_type in data_type_list:           
                if data_type == 'spread':
                    output_path = 'output/' + index_name + version_name + '/' + str(feq) +'m/' + index_name 
                    if if_0203_swift:
                        mkdir(output_path + '01-' + index_name + '02/')
                        mkdir(output_path + '01-' + index_name + '03/')
                    else:
                        mkdir(output_path + '00-' + index_name + '01/')
                        mkdir(output_path + '00-' + index_name + '02/')
                        mkdir(output_path + '00-' + index_name + '03/')
                    
                    if feq == 1:                                      
                        dd, clock, r1, r2, r3 = [], [], [], [], []           
                        if if_start_from_t:
                            f_date_m_list_junior = f_date_m_list
                        else:
                            f_date_m_list_junior = f_date_m_list[1:]
                        k = 0   
                        for d in f_date_m_list_junior:
                            k += 1
                            #get the correct contracts
                            if if_0203_swift:
                                f_list = changeFuture1(future00, future01, future02, future03, date, k)
                            elif if_start_from_t:
                                f_list = changeFuture2(future00, future01, future02, future03, date, k)
                            else:
                                f_list = [future00, future01, future02, future03]
                           
                            #extract the date today                   
                            f_t = [f[f['date'] == d] for f in f_list]
                            dd += [d] * f_t[0].shape[0]
                            clock += f_t[0]['clock'].tolist()
                            r1 += (f_t[0]['close'] - f_t[1]['close']).tolist()
                            r2 += (f_t[0]['close'] - f_t[2]['close']).tolist()
                            if not if_start_from_t:
                                r3 += (f_t[0]['close'] - f_t[3]['close']).tolist()
                        
                        Des0102 = pd.DataFrame({'date':dd, 'clock': clock, 'high': r1, 'open': r1,
                                 'low': r1, 'close': r1, 'volume' : [0]*len(r1), 'amt': [0]*len(r1), 'vwap':[0]*len(r1)})
                        Des0103 = pd.DataFrame({'date':dd, 'clock': clock, 'high': r2, 'open': r2,
                                 'low': r2, 'close': r2, 'volume' : [0]*len(r2), 'amt': [0]*len(r2), 'vwap':[0]*len(r2)})
                        if not if_start_from_t:
                            Des0104 = pd.DataFrame({'date':dd, 'clock': clock, 'high': r3, 'open': r3,
                                 'low': r3, 'close': r3, 'volume' : [0]*len(r2), 'amt': [0]*len(r3), 'vwap':[0]*len(r3)})
    
                        print('producing' + output_path + str(date))
                        if if_start_from_t:
                            Des0102.to_csv(output_path + '01-' + index_name + '02/' + str(date) + '.csv', index = False)
                            Des0103.to_csv(output_path + '01-' + index_name + '03/' + str(date) + '.csv', index = False)    
                        else:
                            Des0102.to_csv(output_path + '00-' + index_name + '01/' + str(date) + '.csv', index = False)
                            Des0103.to_csv(output_path + '00-' + index_name + '02/' + str(date) + '.csv', index = False)    
                            Des0104.to_csv(output_path + '00-' + index_name + '03/' + str(date) + '.csv', index = False)
                      
                        if if_fig:
                            date_clock = [str(dd[i])[4:8] +'/'+ str(clock[i])[0:-2] for i in range(0, len(clock))] 
           
                    else:
                        Des0102 = pd.DataFrame()
                        Des0103 = pd.DataFrame()
                        Des0104 = pd.DataFrame()
                        if if_start_from_t:
                            f_date_m_list_junior = f_date_m_list
                        else:
                            f_date_m_list_junior = f_date_m_list[1:]
                        k = 0   
                        for d in f_date_m_list_junior:
                            k += 1
                            #get the correct contracts
                            if if_0203_swift:
                                f_list = changeFuture1(future00, future01, future02, future03, date, k)
                            elif if_start_from_t:
                                f_list = changeFuture2(future00, future01, future02, future03, date, k)
                            else:
                                f_list = [future00, future01, future02, future03]
                            #extract the date today                   
                            f_t = [extractTodayData2(f,d) for f in f_list]
    
                            dd = f_t[0]['date'].tolist()
                            clock = f_t[0]['clock'].tolist()
                            if if_start_from_t:
                                r1 = (f_t[0]['close'] - f_t[1]['close']).tolist()
                                r2 = (f_t[0]['close'] - f_t[2]['close']).tolist()
                                df = pd.DataFrame({'date': dd, 'clock' : clock, '01-02': r1, '01-03': r2})
                                Des = getDesSpread(df, feq, 'spread', mul)
                                Des0102 = Des0102.append(Des[0], sort = False)
                                Des0103 = Des0103.append(Des[1], sort = False)
                            else:
                                r1 = (f_t[0]['close'] - f_t[1]['close']).tolist()
                                r2 = (f_t[0]['close'] - f_t[2]['close']).tolist()
                                r3 = (f_t[0]['close'] - f_t[3]['close']).tolist()
                                df = pd.DataFrame({'date': dd, 'clock' : clock, '00-01': r1, '00-02': r2, '00-03': r3})
                                Des = getDesSpread(df, feq, 'spread', mul)
                                Des0102 = Des0102.append(Des[0], sort = False)
                                Des0103 = Des0103.append(Des[1], sort = False)
                                Des0104 = Des0104.append(Des[2], sort = False)
                        
                        if if_start_from_t:
                            Des0102.to_csv(output_path + '01-' + index_name + '02/' + str(date) + '.csv', index = False)
                            Des0103.to_csv(output_path + '01-' + index_name + '03/' + str(date) + '.csv', index = False)    
                        else:
                            Des0102.to_csv(output_path + '00-' + index_name + '01/' + str(date) + '.csv', index = False)
                            Des0103.to_csv(output_path + '00-' + index_name + '02/' + str(date) + '.csv', index = False)    
                            Des0104.to_csv(output_path + '00-' + index_name + '03/' + str(date) + '.csv', index = False)
                        
                        if if_fig:
                            r1 = Des0102['close'].tolist()
                            r2 = Des0103['close'].tolist()
                            if not if_start_from_t:
                                r3 = Des0104['close'].tolist()
                            date_l = Des0102['date'].tolist()
                            clock_l = Des0102['clock'].tolist()
                            date_clock = [str(date_l[i])[4:8] +'/'+ str(clock_l[i])[0:-2] for i in range(0, len(clock_l))]
                
                elif data_type == 'contracts': 
                    output_path = 'output/' + index_name + version_name + '/' + str(feq) +'m/' + index_name +'0'
                    
                    if if_start_from_t:
                        f_date_m_list_junior = f_date_m_list
                        Des_contracts = [pd.DataFrame(),pd.DataFrame(),pd.DataFrame()]
                    else:
                        f_date_m_list_junior = f_date_m_list[1:]
                        Des_contracts = [pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()]
                    
                    k = 0
                    for d in f_date_m_list_junior:
                        k += 1
                        #get the correct contracts
                        if if_0203_swift:
                            f_list = changeFuture1(future00, future01, future02, future03, date, k)
                        elif if_start_from_t:
                            f_list = changeFuture2(future00, future01, future02, future03, date, k)
                        else:
                            f_list = [future00, future01, future02, future03]
                  
                        #extract the date today                   
                        f_t = [extractTodayData2(f,d) for f in f_list]
                        if feq == 1:
                            des_list = f_t
                        else:
                            des_list = [getDesSpread(f, feq, data_type, mul) for f in f_t]
                        for j in range(len(Des_contracts)):
                            Des_contracts[j] = Des_contracts[j].append(des_list[j], sort = False)
                    
                    if len(Des_contracts) == 3:
                        c = 0 #control the name of the contracts
                    else:
                        c = -1
                    for des in Des_contracts:
                        c += 1
                        output_path_new = output_path + str(c) + '/'
                        mkdir(output_path_new)
                        print('producing ' + output_path_new + str(date))
                        des.to_csv(output_path_new + str(date) + '.csv', index = False)
                else:
                    output_path = 'output/' + index_name + version_name + '/' + str(feq) +'m/' + dic.get(index_name) + '/'
                    mkdir(output_path)
                    index_des = pd.DataFrame()
                    if if_start_from_t:
                        f_date_m_list_junior = f_date_m_list
                    else:
                        f_date_m_list_junior = f_date_m_list[1:]
                    
                    k = 0
                    for d in f_date_m_list_junior:
                        k += 1
                        index_today = extractTodayData2(index,d)
                        if feq == 1:
                            index_des = index_des.append(index_today)
                        else:
                            index_des = index_des.append(getDesSpread(index_today, feq, data_type, 1), sort=False)
                    print('producing' + output_path + str(date))
                    
                    index_des.to_csv(output_path + str(date) + '.csv', index = False)
   
            if if_fig:
                if if_start_from_t:
                    res = pd.DataFrame({'time':date_clock, '01-02': r1, '01-03': r2})
                else:
                    res = pd.DataFrame({'time':date_clock, '00-01': r1, '00-02': r2, '00-03': r3})
                res.index = res['time']
                fig(res, date, feq, index_name, if_start_from_t)

    
    