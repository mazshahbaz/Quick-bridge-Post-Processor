# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 17:42:31 2019

@author: 30MC
"""
import BridgeObject_Pandas as bo
import pandas as pd
import xlsxwriter

class ExcelObject(object):
    """
    
    """
    def __init__(self, bridge_object):
        self.bridge_object = bridge_object
        self.girder_list = bridge_object.girder_list
        self.girder_PTs = bridge_object.girder_PTs
        
        self.girder_sheets = {}
        for girder_label in self.girder_list:
            girder = GirderSheet(self.girder_PTs[girder_label], girder_label)
            girder.table_parser()
            self.girder_sheets[girder]= GirderSheet(self.girder_PTs[girder])
            
        
        

class GirderSheet(ExcelObject):
    """
    
    """
    def __init__(self, girder_dfs, girder_label):
        
        self.girder_dfs = girder_dfs
        self.girder_label
        self.force_labels = ["M3", "V2", "M2", "V3", "P", "T"]
        
        self.table_spacing = 8
        self.title_cell = [2,2]
        self.start_cell_references = {"force_label": [6,2],
                                 "load_factor": [8,2],
                                 "table_header_start": [9,2],
                                 "table_data_start":[10,2],
                                 "table_end":[]}
        
    def cell_row(cell):
        return cell[0]
        
    def cell_col(cell):
        return cell[1]
    
    def table_parser(self, girder_force_df):
        for force_label in self.force_labels:
            force_df = self.girder_dfs[force_label]
            table_length = len(force_df)
            table_width = len(force_df.columns)
            
    def formulize_data(girder_force_df):
        
            
            
raw_data_file = r"C:\Users\30mc\Documents\Master Sword\Tools\Python Programs\Quick Bridge Analysis\Quick-bridge-Post-Processor\Test CSV\3-span-test.csv"
bridge = BridgeObject(raw_data_file, "Bridge 1")
        
    
        
        
        
            

        
    