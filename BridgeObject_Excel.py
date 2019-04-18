# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 17:42:31 2019

@author: 30MC
"""
import BridgeObject_Pandas as bo
import pandas as pd
import numpy as np
import xlsxwriter

class ExcelObject(object):
    """
    
    """
    def __init__(self, bridge_object):
        self.bridge_object = bridge_object
        self.girder_list = bridge_object.girder_list
        self.girder_PTs = bridge_object.girder_PTs
        
        self.workbook = xlsxwriter.Workbook('PLEASE.xlsx')
        self.girder_sheets = {}
        for girder_label in self.girder_list:
            
            girder = GirderSheet(self.girder_PTs[girder_label], girder_label, self.workbook)
            girder.table_parser()
            self.girder_sheets[girder_label] = girder
            
        self.workbook.close()
        
class GirderSheet(ExcelObject):
    """
    
    """
    def __init__(self, girder_dfs, girder_label, workbook):
        self.workbook = workbook
        self.girder_dfs = girder_dfs
        self.girder_label = girder_label
        self.worksheet = self.workbook.add_worksheet(self.girder_label)
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

            self.start_cell_references['table_header_start'][0] += row_shift
            self.start_cell_references['table_data_start'][0] += row_shift
            
        for force_label in self.force_labels:
            force_df = self.girder_dfs[force_label]
            table_length = len(force_df)
            table_width = len(force_df.columns)
            table_end_cell_update()
            
            self.excel_force_tables[force_label] = ExcelForceTable(force_label, force_df, table_length, table_width, self.start_cell_references.copy(), self.worksheet)
#            print(self.start_cell_references)
            update_cell_references()
            
            
class ExcelForceTable(object):
    def __init__(self, force_label, force_df, table_length, table_width, cell_references, worksheet):
        self.force_label = force_label
        self.worksheet = worksheet
        self.force_df = force_df
        self.table_length = table_length
        self.table_width = table_width
        self.cell_references = cell_references
        self.table_column_labels = list(force_df.columns.values)
        self.live_load_column_labels = [label for label in self.table_column_labels if (('Max' in label) or 'Min' in label)]
        
        def formulize_load_factor_cells():
            '''creates a list of cells that contain load factors for each column in excel format'''
            load_factor_start_row = self.cell_references['load_factor_start'][0]
            load_factor_start_col = self.cell_references['load_factor_start'][1]   
            load_factor_end_col = self.cell_references['load_factor_end'][1]
            self.load_factor_cells = {}
            self.table_column_numbers = {}
            load_factor_col = load_factor_start_col  + 2 #+2 accounts for the station and girderdist columns
            for column_label in self.table_column_labels:
                self.load_factor_cells[column_label] = xlsxwriter.utility.xl_rowcol_to_cell(load_factor_start_row, load_factor_col)
                self.table_column_numbers[column_label] = load_factor_col
                load_factor_col += 1
#            print(self.load_factor_cells)
        
        def formulize_table_values():
            '''creates all table values into an excel formula format'''
            for column_label in self.table_column_labels:
                load_factor = self.load_factor_cells[column_label]
                table_stations = self.force_df.index.tolist()
                for station in table_stations:
                    self.force_df.loc[station, column_label] = '=' + load_factor + '*' + str(self.force_df.loc[station, column_label])
                    
        def create_loadcase_columns():
            '''Seperate live loads'''
            
            self.load_combo_dic = {}
            self.load_combo_list = []
            self.load_combo_labels = []
            for live_load_label in self.live_load_column_labels:
                table_start_row = self.cell_references['table_data_start'][0]
                load_combo_label = live_load_label + " Combo"
                cell_row = table_start_row
                load_combo = []
                for stations in self.force_df.index.tolist():
                    load_combo_string = "="
                    for column_label in self.table_column_labels:
                        if column_label not in self.live_load_column_labels:
                            cell_col = self.table_column_numbers[column_label]
                            load_combo_string += str(xlsxwriter.utility.xl_rowcol_to_cell(cell_row, cell_col)) + "+"
                        elif column_label == live_load_label:
                            cell_col = self.table_column_numbers[column_label]
                            load_combo_string += str(xlsxwriter.utility.xl_rowcol_to_cell(cell_row, cell_col))
                    load_combo.append(load_combo_string)
                    cell_row += 1
                self.load_combo_dic[load_combo_label] = load_combo
                self.load_combo_list.append(load_combo)
                self.load_combo_labels.append(load_combo_label)
#                print(self.load_combo_dic)
                
    
            '''combine live loads'''
            
        def formulize_stations():
            index = self.force_df.index.tolist()
            self.station_list = ['='+ str(i[0]) for i in index]

#            print(self.station_list)
            self.girder_dist_list = ['=' + str(i[1]) for i in index]
            
        def create_data_range():
            start_row = self.cell_references['table_header_start'][0]
            end_row = self.cell_references['table_end'][0]
            self.column_data_range ={}
            for column_label in self.table_column_labels:
                col = self.table_column_numbers[column_label]
                coord = str(xlsxwriter.utility.xl_rowcol_to_cell(start_row, col)) + ":" + str(xlsxwriter.utility.xl_rowcol_to_cell(end_row, col))
                self.column_data_range[column_label] = coord
                
                
        def create_excel_table():
            header_list = ['Stations', 'GirderDist',] + self.table_column_labels + self.load_combo_labels
            print(len(header_list))
#            print(header_list)
            self.table_headers = [{'header':header} for header in header_list]
#            print(self.table_headers)
            raw_table_data  = [self.station_list, self.girder_dist_list] + [self.force_df[column_label].tolist() for column_label in self.table_column_labels] + self.load_combo_list
            self.table_data = np.array(raw_table_data).T.tolist()
            print(self.table_data)
            
            self.worksheet.add_table(self.cell_references['table_header_start'][0], self.cell_references['table_header_start'][1], self.cell_references['table_end'][0], (self.cell_references['table_end'][1] + len(self.load_combo_labels)+ 2),
                                   {'data': self.table_data,
                                    'columns': self.table_headers},)
        
        
#        print(self.table_column_labels)
        formulize_load_factor_cells()
        formulize_table_values()
        create_loadcase_columns()
        formulize_stations()
        create_data_range()
        create_excel_table()
#        print(self.force_df)
#        print(self.force_df.index)
          

            
        
            
        
        
            
            
raw_data_file = r"C:\Users\30mc\Documents\Master Sword\Tools\Python Programs\Quick Bridge Analysis\Quick-bridge-Post-Processor\Test CSV\3-span-test.csv"
bridge = bo.BridgeObject(raw_data_file, "Bridge 1")
excel_bridge = ExcelObject(bridge)
print(excel_bridge.girder_sheets['Right Exterior Girder'].start_cell_references)

        
    
        
        
        
            

        
    