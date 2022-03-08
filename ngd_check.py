# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 09:02:34 2022

@author: A2433
"""


import os
import pandas as pd
import numpy as np

device_path = os.path.join('.','device_list.csv')
if not os.path.exists(device_path):
    default_data = [['V3',r'\\192.168.0.3\Ngdata-A'],['V4',r'\\192.168.0.5\ngdata'],['V5',r'\\192.168.0.7\ngdata']]
    device_df = pd.DataFrame(default_data,columns = ['device','dir'])
    device_df.to_csv(device_path,index = False)

def checking():
    check_vispers = device_df.dir.tolist()
    loss_list =[]
    for v in check_vispers:
        date_list = os.listdir(v)
        date_list = [i for i in date_list if (len(i)==8)]
        for d in date_list:
            date_dir = os.path.join(v,d)
            part_list = os.listdir(date_dir)
            part_list = [i for i in part_list if (i.split('-')[0]=='V3') | (i.split('-')[0]=='V4') | (i.split('-')[0]=='V5')]
            for p in part_list:
                part_dir = os.path.join(date_dir,p)
                lot_list = os.listdir(part_dir)
                lot_list = [i for i in lot_list if (i.split('-')[0]=='V3') | (i.split('-')[0]=='V4') | (i.split('-')[0]=='V5')]
                for l in lot_list:
                    lot_dir = os.path.join(part_dir,l)
                    side_list = os.listdir(lot_dir)
                    side_list = [i for i in side_list if (i.split('-')[0]=='V3') | (i.split('-')[0]=='V4') | (i.split('-')[0]=='V5')]
                    side_list = [i for i in side_list if (i.split('_')[-1]=='1')]
                    A_side = 0
                    B_side = 0
                    if len(side_list)>1:
                        for s in side_list:
                            try:
                                side_dir = os.path.join(lot_dir,s)
                                if side_dir.split('_')[-2] == 'A':
                                    A_side = len(os.listdir(os.path.join(side_dir,'ngpointdata')))
                                if side_dir.split('_')[-2] == 'B':
                                    B_side = len(os.listdir(os.path.join(side_dir,'ngpointdata')))
                            except:
                                pass
                        loss_list.append([lot_dir,d,p,l,s,A_side,B_side])
    result = pd.DataFrame(np.array(loss_list),columns = ['path','date','part_no','lot','side','A','B'])
    result.to_csv(os.path.join('.','raw_data.csv'))
    result = result[result.A != result.B]
    result.to_csv(os.path.join('.','result.csv'))

if __name__ == '__main__':
    checking()