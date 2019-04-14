# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 13:22:21 2019

@author: 30MC
"""
import BridgeObject
import csv
import xlsxwriter

"""
Excel Workbook (Global Girders)
    Excel Sheet (Global Summary Table)
    Excel Sheet (Global Girder)
        Summary Table
        Table for each Force Type (M3, V2, M2, V3, P, T)
        Chart for each Force Type (M3, V2, M2, V3, P, T)
        
Excel Workbook (Span)
    Excel Sheet per (Girder)
        Table for each Force Type (M3, V2, M2, V3, P, T)
        Chart for each Force Type (M3, V2, M2, V3, P, T)
"""

class GlobalBridge(object):
    """
    This Class creates a workbook that represents girders along th entire bridge length, not just span.
    **Currently only works for bridges that have the same number of girders at each span
    """
    def __init__(self, Bridge):
        self.Bridge = Bridge
        self.bridge_label = self.Bridge.get_bridge_label()
        self.spans = Bridge.get_spans()
        self.global_girder_labels = self.spans[0].get_girder_labels()
        
        self.global_girders = {}
        for global_girder_label in self.global_girder_labels:
            global_girder = [span.get_girder(global_girder_label) for span in self.spans ]
            self.global_girders[global_girder_label] = GlobalGirder(global_girder, global_girder_label)
                
            
            
class GlobalGirder(GlobalBridge):
    def __init__(self, global_girder, global_girder_label):
        self.global_girder = global_girder
        self.global_girder_label = global_girder_label
        print("creating global firder for: ", self.global_girder_label)
        
        
        M3_tables = [girder.get_force_tables().get_M3_table() for girder in self.global_girder]
        V2_tables = [girder.get_force_tables().get_V2_table() for girder in self.global_girder]
        M2_tables = [girder.get_force_tables().get_M2_table() for girder in self.global_girder]
        V3_tables = [girder.get_force_tables().get_V3_table() for girder in self.global_girder]
        P_tables = [girder.get_force_tables().get_P_table() for girder in self.global_girder]
        T_tables = [girder.get_force_tables().get_T_table() for girder in self.global_girder]
        
        print(len(M3_tables))
        
        force_tables = [M3_tables, V2_tables, M2_tables, V3_tables, P_tables, T_tables]
        local_table_labels = M3_tables[1][0]
#        print(local_table_labels)
        global_table_labels = local_table_labels[:-1]
#        print(global_table_labels)
        
        self.global_tables = []
        for tables in force_tables:
            global_table = []
            for table in tables:
                print("appending table")
                table = table[1:]
                for row in table:
                    row[0] = row.pop()
                global_table.append(table)
            self.global_tables.append(global_table_labels + global_table)
        
        self.global_M3_table = self.global_tables[0]
        self.global_V2_table = self.global_tables[1]
        self.global_M2_table = self.global_tables[2]
        self.global_V3_table = self.global_tables[3]
        self.global_P_table = self.global_tables[4]
        self.global_T_table = self.global_tables[5]
        
        self.global_tables = {"M3_table": self.global_M3_table, "V2_table": self.global_V2_table, "M2_table": self.global_M2_table, "V3_table": self.global_V3_table, "P _Table": self.global_P_table, "T_table": self.global_T_table}
        
        print(self.global_M3_table)
        










"""Main"""
raw_data_file = r"C:\Users\30mc\Documents\Master Sword\Tools\Quick Bridge Analysis\Simple Data 2.csv"
csv_reader = csv.DictReader(open(raw_data_file, 'r'))
raw_data = [row for row in csv_reader]

bridge1 = BridgeObject.BridgeObject(raw_data, "BOBJ1")
global_bridge = GlobalBridge(bridge1)





#""" Create the Bridge object """
#bridge1 = BridgeObject.BridgeObject(raw_data, "BOBJ1")
#span1 = bridge1.get_span("Span1")
#girder1 = span1.get_girder("Right Exterior Girder")
#force_tables = girder1.get_force_tables()
#M3_table = force_tables.get_M3_table()
#
#print(M3_table)
#
#span2 = bridge1.get_span("Span2")
#girder2 = span2.get_girder("Right Exterior Girder")
#force_tables2 = girder2.get_force_tables()
#M3_table2 = force_tables2.get_M3_table()
#
#print(M3_table2)
#print(force_tables.get_girder_label())
#
#M3_data = M3_table[1:]
#M3_headers = M3_table[0]
#head = [{'header':header} for header in M3_headers]
#
#
#print(M3_data)
#print(M3_headers)
#print(head)
#workbook = xlsxwriter.Workbook('tables.xlsx')
#worksheet1 = workbook.add_worksheet()
##worksheet2 = workbook.add_worksheet()
##worksheet3 = workbook.add_worksheet()
##worksheet4 = workbook.add_worksheet()
##worksheet5 = workbook.add_worksheet()
##worksheet6 = workbook.add_worksheet()
##worksheet7 = workbook.add_worksheet()
##worksheet8 = workbook.add_worksheet()
#
#table_width = len(head)
#table_height = len(M3_table)
#
#
#
#worksheet1.add_table(1,1,table_height,table_width, 
#                    {'data': M3_data,
#                    'columns': head})
#
#workbook.close()
