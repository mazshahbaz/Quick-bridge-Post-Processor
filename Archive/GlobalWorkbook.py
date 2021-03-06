# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 15:29:59 2019

@author: 30MC
"""

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

import BridgeObject
import GlobalBridge
import csv
import xlsxwriter


class GlobalWorkbook(object):
    def __init__(self, global_bridge):
        self.global_bridge = global_bridge
        self.bridge_label = global_bridge.bridge_label
        self.workbook = xlsxwriter.Workbook('PLEASE.xlsx')
        self.summarysheet = self.workbook.add_worksheet()
        
        self.global_girder_labels = self.global_bridge.global_girder_labels
        self.global_girders = self.global_bridge.global_girders
        
        self.girder_sheets = []
        print(self.global_girder_labels)
        for label in self.global_girder_labels:
            self.girder_sheets.append(GirderSheet(self.workbook, self.global_girders[label], label))
        
        self.workbook.close()
        
class GirderSheet(GlobalWorkbook):
    def __init__(self, workbook, global_girder, label):
        self.workbook = workbook
        self.global_girder = global_girder
        self.girder_label = label
        self.global_tables = self.global_girder.global_tables
        self.global_table_keys = self.global_girder.global_table_keys
        
        title_cell = [2,2]
        force_title_cell = [4,2]
        load_factor_cell_start =  [6,3]
        table_start_cell = [7,2]
        table_end_cell = [0,0]
        table_spacing = 6
        
        girder_sheet = self.workbook.add_worksheet(self.girder_label)
        
        
        for force_label in self.global_table_keys:
            table = ExcelTableCreator(self.workbook, self.global_girder, self.girder_label, force_label, self.global_tables[force_label], load_factor_cell_start)
            force_table = table.force_table
            force_table_data = table.force_table_data
            table_headers = table.table_headers
            
            print(force_table_data)
            print(table_headers)
            
            table_length = len(force_table_data)
            table_width= len(table_headers) - 1
            print(table_width)
            table_end_cell[0]= table_start_cell[0] + table_length
            table_end_cell[1]= table_start_cell[1] + table_width
            table_coord = table_start_cell + table_end_cell
            
            print(table_start_cell[0], table_start_cell[1], table_end_cell[0], table_end_cell[1])
            excel_table = girder_sheet.add_table(table_start_cell[0], table_start_cell[1], table_end_cell[0], table_end_cell[1],
                                   {'data': force_table_data,
                                    'columns': table_headers},)
            
            table_end_cell[1] = 2 
            vertical_shift = table_end_cell[0] - table_start_cell[0] + table_spacing
                    
            force_title_cell[0] += vertical_shift
            load_factor_cell_start[0] += vertical_shift
            table_start_cell[0] += vertical_shift
            
#        self.xtbl = ExcelTableCreator(self.workbook,self.global_girder, self.girder_label, "M3", self.global_tables["M3"], load_factor_cell_start)
        
        
    
#        for force_label in self.global_table_keys:
#            force_table = self.global_tables[force_label]
#            force_table_data = force_table[1:]
#            table_headers = [{'header':header} for header in force_table[0]]
#            print(force_table)
#            print(table_headers)
#            print(force_table_data)
#            
#            girder_sheet.write(force_title_cell[0], force_title_cell[1], force_label)
#            
#            table_length = len(force_table) - 1
#            table_width= len(force_table[0]) - 1
#            table_end_cell[0]= table_start_cell[0] + table_length
#            table_end_cell[1]= table_start_cell[1] + table_width
#            table_coord = table_start_cell + table_end_cell
#            
#            print(table_start_cell[0], table_start_cell[1], table_end_cell[0], table_end_cell[1])
#            excel_table = girder_sheet.add_table(table_start_cell[0], table_start_cell[1], table_end_cell[0], table_end_cell[1],
#                                   {'data': force_table_data,
#                                    'columns': table_headers},)
#            
#            table_end_cell[1] = 2 
#            vertical_shift = table_end_cell[0] - table_start_cell[0] + table_spacing
#                    
#            force_title_cell[0] += vertical_shift
#            load_factor_cell_start[0] += vertical_shift
#            table_start_cell[0] += vertical_shift
         
        girder_sheet.write(0,0, '2')
        girder_sheet.write(1, 0, '=A1*7')

class ExcelTableCreator(GirderSheet):
    """
    The table creator takes the tables from the Global Bridge Object and modifies them to include:
        - Sum columns for different load cases (Max/Min)
        - Converts data into equations that are multiplied by the load Factors
    """
    def __init__(self, workbook, global_girder, girder_label, force_label, force_table, load_factor_cell_start):
        self.workbook = workbook
        self.global_girder = global_girder
        self.girder_label = girder_label
        self.force_label = force_label
        self.force_table = force_table
        self.load_factor_cell_start = load_factor_cell_start
        
        self.force_table_data = force_table[1:]
        load_case_labels = force_table[0][1:]
        
        """ Determine the number of live load cases """
        self.live_load_case_labels = [load_case_label for load_case_label in load_case_labels if (("_Max" in load_case_label) or ("_Min" in load_case_label))]
        
        """ Create Table Headers """
        if len(self.live_load_case_labels) > 0:
            self.table_header_list = force_table[0] + [live_load_case_label + "_Combo" for live_load_case_label in self.live_load_case_labels]
        else:
            self.table_header_list = force_table[0] + ["Combo"]
        self.table_headers = [{'header':header} for header in self.table_header_list]
            
        """ Assign each header to an excel column number """
        table_column_dictionary = {}
        column = 2
        for header in self.table_header_list:
            table_column_dictionary[header] = column
            column += 1
        
        """Modify force table data to be in equation format"""
        for row in self.force_table_data:
            load_factor_cell = self.load_factor_cell_start
            print("hello")
            i_col = 0
            load_factor_cell[1] = 3
            for cell in row:
                """convert from RC notation to cell notation"""
                if i_col > 0:
                    load_factor_cell_excel = xlsxwriter.utility.xl_rowcol_to_cell(load_factor_cell[0], load_factor_cell[1], row_abs=True, col_abs=True)
#                    cell = int(cell)
                    cell = "=" + cell + "*" + load_factor_cell_excel
                    row[i_col] = cell
                    load_factor_cell[1] +=1
                i_col +=1
        
        self.force_table = self.table_headers + self.force_table_data
                
            
            
            
class SummarySheet(GlobalWorkbook):
    def __init__():
        return



"""Main"""
raw_data_file = r"C:\Users\30mc\Documents\Master Sword\Tools\Quick Bridge Analysis\3-span-test.csv"
#raw_data_file = r"C:\Users\30mc\Documents\Master Sword\Tools\Quick Bridge Analysis\s.csv"
csv_reader = csv.DictReader(open(raw_data_file, 'r'))
raw_data = [row for row in csv_reader]

bridge1 = BridgeObject.BridgeObject(raw_data, "BOBJ1")
global_bridge = GlobalBridge.GlobalBridge(bridge1)
x = GlobalWorkbook(global_bridge)

#xtbl = x.girder_sheets[0]
#print(xtbl.xtbl.table_headers)
#print(xtbl.xtbl.force_table)