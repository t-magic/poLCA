#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import pandas as pd
import re
import csv
from collections import OrderedDict
import xlsxwriter

def m3_to_xlsx(M3_file, polout_file, original_df_columns, xlsx_file):
    print(original_df_columns)
    param_dict = OrderedDict()

    with codecs.open(M3_file, 'r') as f:
        txt_list = f.read().split('\n')
    #txt_list

    with codecs.open(polout_file, 'r') as f:
        polout_list = f.read().split('\n')

    class_count = 0
    next_flag_for_ECPS = False
    ECPS_list = []
    for line in txt_list:
        if next_flag_for_ECPS:
            line = [float(x.strip()) for x in line.strip().split(' ')]
            ECPS_list.append(line)


            next_flag_for_ECPS = False
        else:
            items0 = re.match('Conditional item', line)
            if items0 != None:
                class_count += 1
                param_dict[class_count] = OrderedDict()
                index  = 0
            else:
                items = re.match('\$', line)
                if items != None:
                    #print(line)
                    #key = line
                    key = original_df_columns[index]
                    index += 1
                    param_dict[class_count][key] = []
                else:
                    items2 = re.match('class (\d+):  (.+) (.+)', line)
                    if items2 != None:
                        param_dict[class_count][key].append(['class ' + items2.group(1), float(items2.group(3))])
                    else:
                        items3 = re.match('Estimated class population shares', line)
                        if items3 != None:
                            next_flag_for_ECPS = True
    #param_dict
    #print('ECPS_list = {}'.format(ECPS_list))
    # xlsxファイルを用意する
    xbook = xlsxwriter.Workbook(xlsx_file)

    # polデータを書き出す。
    xsheet = xbook.add_worksheet('polout')
    for row_count, line_list in enumerate(polout_list):
        line_list = line_list.replace('"', '').split(" ")
        if row_count == 0:
            line_list = [""] + line_list
        for colno in range(len(line_list)):
            if row_count > 0 and colno > 0:
                line_list[colno] = float(line_list[colno])
        xsheet.write_row(row_count, 0, line_list)

    # classデータを書き出す
    title_row = ['']
    for class_count, dict_item in param_dict.items():
        title_row.append('class {}'.format(class_count))
        xsheet = xbook.add_worksheet('class {}'.format(class_count))
        all_list = [title_row, ['Predicted class memberships'] + ECPS_list[class_count - 1]]
        #print('class_count = {}'.format(class_count))
        #print('ECPS_list[{0}] = {1}'.format(class_count, ECPS_list[class_count - 1]))
        #all_list.append()
        for key, listx in param_dict[class_count].items():
            each = [key]
            for item in listx:
                each.append(item[1])
            all_list.append(each)
        all_list
        for row_count, line_list in enumerate(all_list):
            line_list = [str(x) for x in line_list]
            #print('++ line_list = {}'.format(line_list))

            for colno in range(len(line_list)):
                if row_count > 0 and colno > 0:
                    line_list[colno] = float(line_list[colno])

            xsheet.write_row(row_count, 0, line_list)
    xbook.close()
