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
            self.girder_sheets[girder_label] = girder
            
        
class GirderSheet(ExcelObject):
    """
    
    """
    def __init__(self, girder_dfs, girder_label):
        
        self.girder_dfs = girder_dfs
        self.girder_label = girder_label
        self.force_labels = ["M3", "V2", "M2", "V3", "P", "T"]
        
        self.excel_force_tables = {"M3":[], "V2":[], "M2":[], "V3":[], "P":[], "T":[]}
        self.table_spacing = 8
        self.title_cell = [2,2]
        self.start_cell_references = {"force_label": [6,2],
                                 "load_factor_start": [8,2],
                                 "load_factor_end": [],
                                 "table_header_start": [9,2],
                                 "table_data_start":[10,2],
                                 "table_end":[]}
        
    
    def table_parser(self):
    
        def cell_row(cell):
            return cell[0]
        
        def cell_col(cell):
            return cell[1]
    
        def table_end_cell_update():
            end_row = cell_row(self.start_cell_references['table_header_start']) + table_length - 1
            end_col = cell_col(self.start_cell_references['table_header_start']) + table_width - 1
            self.start_cell_references['table_end'] = [end_row, end_col]
            self.start_cell_references['load_factor_end'] = [self.start_cell_references['load_factor_start'][0], self.start_cell_references['load_factor_start'][1] + table_width-1]
            
        def update_cell_references():
            row_shift = table_length + self.table_spacing - 1
            column_shift = table_width - 1 
            self.start_cell_references['force_label'][0] += row_shift
            
            self.start_cell_references['load_factor_start'][0] += row_shift
            self.start_cell_references['load_factor_end'] = [self.start_cell_references['load_factor_start'][0], self.start_cell_references['load_factor_start'][1] + column_shift]
            
            self.start_cell_references['table_header_start'][0] += row_shift
            self.start_cell_references['table_data_start'][0] += row_shift
            
        for force_label in self.force_labels:
            force_df = self.girder_dfs[force_label]
            table_length = len(force_df)
            table_width = len(force_df.columns)
            table_end_cell_update()
            
            self.excel_force_tables[force_label] = ExcelForceTable(force_label, force_df, table_length, table_width, self.start_cell_references.copy())
            print(self.start_cell_references)
            update_cell_references()
            
            
class ExcelForceTable(GirderSheet):
    def __init__(self, force_label, force_df, table_length, table_width, cell_references):
        self.force_label = force_label
        self.force_df = force_df
        self.table_length = table_length
        self.table_width = table_width
        self.cell_references = cell_references
        
        load_factor_cells = [self.cell_references[load_factor_start]]
    
    
            

            
        
            
        
        
            
            
raw_data_file = r"C:\Users\30mc\Documents\Master Sword\Tools\Python Programs\Quick Bridge Analysis\Quick-bridge-Post-Processor\Test CSV\3-span-test.csv"
bridge = bo.BridgeObject(raw_data_file, "Bridge 1")
excel_bridge = ExcelObject(bridge)
print(excel_bridge.girder_sheets['Right Exterior Girder'].start_cell_references)

        
    
        
        
        
            

        
    