# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 17:33:02 2019

@author: 30MC
"""

"""
The Bridge Class will take the following structure:
    
Bridge Object:
    ''' Bridge Span
        ''' Bridge Girder
            '''Bridge Cut
            '''Girder Station
            '''Load Case (each load case has 6 dictionaries {key=station: value = force effect}
                '''M3 (Major Moment 33/xx)
                '''V2 (Major Shear 22)
                '''M2 (Minor Moment 22)
                '''V3 (Minor Shear 33/yy)
                '''P (Axial)
                '''T (Torsion)
            '''Force Tables
                
                
The Raw data will come in the form of a CSV file with the following Headings:
BridgeObj, BridgeCut, Station, Span, Girder, GirderDist, LocType, OutputCase, CaseType, StepType, P ,V2 ,V3 ,T, M2, M3, GlobalX, GlobalY, GlobalZ
"""

import csv
import numpy as np
import pandas as pd


class BaseBridgeObject(object):
    """
    
    """
    def __init__(self, raw_data, bridge_label):
        self.raw_df = pd.read_csv(raw_data)
        self.bridge_label = bridge_label
        self.force_labels= ["M3", "V2", "M2", "V3", "P", "T"]


class BridgeObject(BaseBridgeObject):
    '''
    The Bridge object proccesses the raw data from CSI bridge, into discrete objects 
    and organizes the data to easily interpert the analysis with charts and spread sheets
    
    raw_data = a csv file of the table outputs form CSI Bridge
    df = dataframe
    raw_pivot_tables = list of pivot tables for each force label, which includes all bridge girders and all spans
    
    '''
    def __init__(self, raw_data, bridge_label):
        BaseBridgeObject.__init__(self, raw_data, bridge_label)
        print("Create Bridge Object")
        print(" ")
#        self.raw_pivot_tables = create_global_PT()
    
        def create_global_PT(): 
            """ function to initalize all the global Pivot tables for each force label """
            self.global_pivot_tables = {force_label: GlobalPivotTable(self.raw_df, force_label) for force_label in self.force_labels}
            print("\t  - Bridge Pivot Tables initalized")
            
        def create_span_list():
            self.span_list = self.global_pivot_tables["M3"].global_pivot_table.index.unique(level='Span').tolist()
            print("/t - Bridge Spans: ", self.span_list)
            
        def create_girder_list():
            """ uses the first global pivot table ("M3") to obtain a list of girders from the index """
            girder_labels = self.global_pivot_tables["M3"].global_pivot_table.index.unique(level='Girder').tolist()
            self.girder_list = [girder_label for girder_label in girder_labels]
            # rearrange list so Right Exterior Girder is first in the list if present
            if "Right Exterior Girder" in self.girder_list:
                self.girder_list.remove("Right Exterior Girder")
                self.girder_list =  ["Right Exterior Girder"] + self.girder_list
            print("\t - Bridge Girders: ", self.girder_list)
        
        def create_girder_PTs():
            """ extracts a pivot table for each girder for each forcelabel from the global pivot tables """
            self.girder_PTs = {}
            for girder_label in self.girder_list:
                print("\t", "- Create Pivot Tables for Girder: ", girder_label)
                PT_dic = {}
                for force_label in self.force_labels:
                    print("\t", "  Combining: ", force_label)
                    girder_table_segments = []
                    for span in self.span_list:
                        print("\t" * 2, span)
                        girder_table_segments.append(self.global_pivot_tables[force_label].global_pivot_table.loc[girder_label, span])
                    PT_dic[force_label] = pd.concat(girder_table_segments)
                self.girder_PTs[girder_label] = PT_dic
                
                

        create_global_PT()
        create_span_list()
        create_girder_list()
        create_girder_PTs()
        
    def get_girder_force_df(self, girder_label, force_label):
        return self.girder_PTs[girder_label][force_label]
    
    def get_girder_load_cases():
        pass
    
    def get_girder_stations():
        pass
    
    def get_girder_global_stations():
        pass
        
        
class GlobalPivotTable(BridgeObject):
    """
    creates global bridge pivot tables based on the input raw_dataframe
    """
    def __init__(self, raw_df, force_label):
        self.raw_df = raw_df
        self.force_label = force_label
        self.table_label = "full_bridge_" + force_label + "_table"
        
        """Create Live Load Cases Pivot Table"""
        self.live_pivot_table = pd.pivot_table(self.raw_df, values=self.force_label, index=['Girder', 'Span', 'Station', 'GirderDist'], columns=['StepType', 'OutputCase'])
        self.live_pivot_table.columns = self.live_pivot_table.columns.to_series().str.join('_')
        live_load_cases = self.live_pivot_table.columns.tolist()
        live_load_cases = [ele[4:] for ele in live_load_cases]
        self.unique_live_load_cases = []
        for ele in live_load_cases:
            if ele not in self.unique_live_load_cases:
               self.unique_live_load_cases.append(ele)

        """Create Pivot Table for all cases except live load cases"""
        self.global_pivot_table = pd.pivot_table(self.raw_df, values=self.force_label, index=['Girder', 'Span', 'Station', 'GirderDist'], columns=['OutputCase'])
        self.global_pivot_table = self.global_pivot_table.drop(columns=self.unique_live_load_cases)
        
        """Combine pivot tables"""
        self.global_pivot_table = pd.concat([self.global_pivot_table, self.live_pivot_table], axis=1) #Axis=1 means its concactinating along the columns
        print(self.global_pivot_table)
        
    def get_girder_force_span_PT(self, girder_label, span):
        return self.global_pivot_table.loc[girder_label, span]
        
class GirderTables(BridgeObject):
    """
    
    """
    def __init__(self, force_labels, raw_pivot_tables, girder_label):
        self.BaseBridge

   
    
"""Main"""
#raw_data_file = r"C:\Users\30mc\Documents\Master Sword\Tools\Python Programs\Quick Bridge Analysis\Quick-bridge-Post-Processor\Test CSV\3-span-test.csv"
#bridge = BridgeObject(raw_data_file, "Bridge 1")
##bridge.create_global_PT()
##print(bridge.raw_pivot_tables[0].force_label)
#print(bridge.span_list)
#print(bridge.get_girder_force_df('Right Exterior Girder','M3'))
#


#print(bridge_tables[0].raw_pivot_table)
#x = bridge_tables[0].raw_pivot_table.loc['Right Exterior Girder', 'Span 1']
#y = bridge_tables[0].raw_pivot_table.loc['Right Exterior Girder', 'Span 2']
#print(pd.concat([x,y]))
##index = bridge_tables[0].raw_pivot_table["Right Interior Girder", "Span 1", "Stations"]
##print(index)
##df = pd.DataFrame(np.random.randn(8, 3), index=index,
##                                         columns=['A', 'B', 'C'])
#
#
#writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
#df.to_excel(writer, sheet_name='Sheet1')























#"""Define CSV fields for object to reference """
#fields = ["BridgeObj", "BridgeCut", "Station", "Span", "Girder", "GirderDist", "LocType", "OutputCase", "CaseType", "StepType", "P" ,"V2" ,"V3" ,"T", "M2", "M3", "GlobalX", "GlobalY", "GlobalZ"]
#bridge_field = fields[0]
#cut_field = fields[1]
#station_field = fields[2]
#span_field = fields[3]  
#girder_field = fields[4]
#load_case_field = fields[7]
#step_type_field = fields[9]
#M3_field = fields[15]
#V2_field = fields[11]
#M2_field = fields[14]
#V3_field = fields[12]
#P_field = fields[10]
#T_field = fields[13]
#globalx_field = fields[16]

#""" Create the Bridge object """
#bridge1 = BridgeObject(raw_data, "BOBJ1")
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

#for span in bridge1.get_spans():
#    span_label = span.get_span_label()
#    girders = span.get_girders()
#    for girder in girders:
#        girder_label = girder.get_girder_label()
#        M3_table = [span_label, girder_label]
#        for cut in girder.get_cuts():
#            row = []
#            row.append(girder.get_station(cut))
#            for load_case in girder.get_load_cases():
#                row.append(load_case.get_M3()[cut])
#            M3_table.append(row)
#        print(M3_table)







#
#
#
#
#"""Span Object Tests"""
#print("-Begin Span Object Tests")
#print("\t", "Number of spans: ", bridge1.n_spans())
#print("\t", "Span List: ", bridge1.get_span_labels())
#span_1 = bridge1.get_span("Span1")
#print("\t"*2, span_1.get_span_label(), "has", span_1.n_girders(), "girders in it")
#print("\t"*3, "Girder List: ", span_1.get_girder_labels())
#span_2 = bridge1.get_span("Span2")
#print("\t"*2, span_2.get_span_label(), "has", span_2.n_girders(), "girders in it")
#print("\t"*3, "Girder List: ", span_2.get_girder_labels())
#
#"""Girder Object Tests"""
#girder1 = span_1.get_girder("Right Exterior Girder")
#girder2 = span_1.get_girder("Interior Girder")
#
#g1_dead = girder1.get_load_case("DEAD")
#print("-Begin Girder Object Tests")
#print("Span 1")
#print("\t", "Girder 1 label test: ", girder1.get_girder_label())
#print("\t"*2, "Girder 1 cuts: ", girder1.get_cuts())
#print("\t"*2, "Girder 1 stations: ", girder1.get_stations())
#print("\t"*2, "Number of stations: ", girder1.n_cuts()) 
#print("\t"*3, "Girder 1 Dead load: ", g1_dead.get_M3())
#print("\t"*3, "Girder 1 Dead load step_type: ", g1_dead.get_step_type())
#
#print("\t", "Girder 2 label test: ", girder2.get_girder_label())
#print("\t"*2, "Girder 2 cuts: ", girder2.get_cuts())
#print("\t"*2, "Girder 2 stations: ", girder2.get_stations())  
#print("\t"*2, "Number of stations: ", girder2.n_cuts())
#
#
#girder12 = span_2.get_girder("Right Exterior Girder")
#girder22 = span_2.get_girder("Left Exterior Girder")
#
#g1_dead = girder12.get_load_case("DEAD_Max")
#g1_dead_min = girder12.get_load_case("DEAD_Min")
#print("Span 2")
#print("\t", "Girder 1 label test: ", girder12.get_girder_label())
#print("\t"*2, "Girder 1 cuts: ", girder12.get_cuts())
#print("\t"*2, "Girder 1 stations: ", girder12.get_stations())
#print("\t"*2, "Number of stations: ", girder12.n_cuts()) 
#print("\t"*2, "Girder 1 load Cases: ", girder12.get_load_case_labels())
#print("\t"*3, "Girder 1 Dead load: ", g1_dead.get_load_case_label())
#print("\t"*3, "Girder 1 Dead load: ", g1_dead.get_step_type())
#print("\t"*4, "Girder 1 Dead load Max: ", g1_dead.get_M3())
#print("\t"*3, "Girder 1 Dead load: ", g1_dead_min.get_load_case_label())
#print("\t"*3, "Girder 1 Dead load: ", g1_dead_min.get_step_type())
#print("\t"*4, "Girder 1 Dead load Min: ", g1_dead_min.get_M3())
#
#
#print("\t", "Girder 2 label test: ", girder22.get_girder_label())
#print("\t"*2, "Girder 2 cuts: ", girder22.get_cuts())
#print("\t"*2, "Girder 2 stations: ", girder22.get_stations())  
#print("\t"*2, "Number of stations: ", girder22.n_cuts())    