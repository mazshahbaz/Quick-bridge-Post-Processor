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


class BridgeObject(object):
    '''
    The Bridge object proccesses the raw data from CSI bridge, into discrete objects 
    and organizes the data to easily interpert the analysis with charts and spread sheets
    
    raw_date = a csv file of the table outputs form CSI Bridge
    
    The Bridge Object will first extract the number of spans from the CSV file
    create "Span" objects, and those will create "Girder Objects" and so on.
    '''
    def __init__(self, raw_data, bridge_label):
        """ each line of the csv is broken read as a dictionary with the fields as the keys """
        # reading csv file
#        self.raw_date = raw_data
#        with open(raw_data, 'r') as csvfile: 
#            self.csv_reader = csv.DictReader(csvfile) 
        self.raw_data = raw_data
        self.bridge_label = bridge_label
        
        def CreateSpans(raw_data):
            spans = {}
            span_list = []
            """ Find all Unique Spans"""
            for row in raw_data:
                span_label = row[span_field]
                if span_label not in span_list:
                    span_list.append(span_label)
        
            """
            *** I think i actullay fixed this issue.....
            Create Unique Span objects
            **Note: Had to break into two loops, Spans would not continue
                    to create Span objects after span 1
            """  
            for span_label in span_list:
                spans[span_label] = Span(span_label, raw_data)
            return spans
        
        self.spans = CreateSpans(self.raw_data)
    
    def get_bridge_label(self):
        return self.bridge_label
    
    def get_span_labels(self):
        return [key for key in self.spans.keys()]
    
    def get_spans(self):
        return [value for value in self.spans.values()]
    
    def get_span(self, span_label):
        return self.spans[span_label]
        
    def n_spans(self):
        return len(self.spans)
        
class Span(BridgeObject):
    def __init__(self, span_label, raw_data):
        print("creating span object")
        self.span_label = span_label
        self.raw_data = raw_data
    
        def create_girders(raw_data):
            girders = {}
            girder_list = []
            """ Find all Unique Girders for this span"""
            for row in raw_data:
                girder_label = row[girder_field]
                if (row[span_field] == span_label) and girder_label not in girder_list:
                    girder_list.append(girder_label)
        
            """
            Create Unique Span objects
            **Note: Had to break into two loops, Spans would not continue
                    to create Span objects after span 1
            """  
            for girder_label in girder_list:
                girders[girder_label] = Girder(span_label, girder_label, raw_data)
            return girders         
    
        self.girders = create_girders(self.raw_data)
    
    def get_span_label(self):
        return self.span_label
    
    def get_girder_labels(self):
        return [key for key in self.girders.keys()]
    
    def get_girders(self):
        return [value for value in self.girders.values()]
    
    def get_girder(self, girder_label):
        return self.girders[girder_label]
    
    def n_girders(self):
        return len(self.girders)
    
    
class Girder(Span):
    """
    The Girder object contains all the properties of a bridge girder such as:
        cuts: Discrete section cuts along the girder
        Stations: local distance/length along the girder which correspons to a cut
        Global_Stations: The Global station of a girder cut in the entire bridge object
        load_Cases: A Dictionary of all the load cases present on a particular Girder  
    """
    print("creating girder object")
    def __init__(self,span_label, girder_label, raw_data):
#        Span.__init__(self, span_label)
        self.span_label = span_label
        self.girder_label = girder_label
        self.raw_data = raw_data
        
        def create_stations(raw_data):
            stations = {}
            """ Find all Unique Cuts per Girder"""
            for row in raw_data:
                cut_label = row[cut_field]
                station = row[station_field]
                global_station = row[globalx_field]
#                if (row[span_field] == span_label) and (row[girder_field] == girder_label) and ([station, global_station] not in stations.values()) and cut_label not in stations.keys():
                if (row[span_field] == span_label) and (row[girder_field] == girder_label) and cut_label not in stations.keys():
                    stations[cut_label] = [station,  global_station]
            return stations
            
        self.stations = create_stations(self.raw_data)
        
        def create_load_cases(stations, raw_data):
            load_case_labels = []
            load_cases = {}
            """ Find all Unique load_cases per Girder, as well as step types per load case (max, min, etc..)"""
            for row in raw_data:
                load_case_label = row[load_case_field]
                step_type = row[step_type_field]
                if (row[span_field] == span_label) and (row[girder_field] == girder_label) and ([load_case_label, step_type] not in load_case_labels):
                    load_case_labels.append([load_case_label, step_type])
        
            for load_case_label in load_case_labels:
                if load_case_label[1] == "Max" or load_case_label[1] == "Min":
                    print(load_case_label[1])
                    load_case_label[0] = str(load_case_label[0]) + "_" + str(load_case_label[1])
                load_cases[load_case_label[0]] = LoadCase(span_label, girder_label, stations, load_case_label[0], load_case_label[1], raw_data)
            return load_cases
        
        self.load_cases = create_load_cases(self.stations, self.raw_data)
        self.force_tables = ForceTables(self.span_label, self.girder_label, self.stations, self.load_cases)
        
        
    def get_girder_label(self):
        return self.girder_label
    
    def get_cuts(self):
        return [key for key in self.stations.keys()]
    
    def get_stations(self):
        return self.stations
    
    def get_station(self, cut):
        return self.stations[cut][0]
    
    def get_global_station(self, cut):
        return self.stations[cut][1]
    
    def n_cuts(self):
        return len(self.stations)
    
    def get_load_case_labels(self):
        return [key for key in self.load_cases.keys()]
    
    def get_load_cases(self):
        return [value for value in self.load_cases.values()]
    
    def get_load_case(self, load_case_label):
        return self.load_cases[load_case_label]
    
    def get_force_tables(self):
        return self.force_tables

    
class LoadCase(Girder):
    """
    A load Case contains all the force effects caused by that particular "Case" at each station along the girder.
    
    Some load cases (Moving Loads) will have two or more instances since they have a Minnimum and Maximum case.
    these cases are filtered using the "step_type" which indicates if it is a Min or Max case.
    """
    def __init__(self, span_label, girder_label, stations, load_case_label, step_type, raw_data):
        self.span_label = span_label
        self.girder_label = girder_label
        self.stations =  stations
        self.raw_data = raw_data
        if step_type == "Max" or step_type == "Min":
            self.load_case_label = load_case_label[:-4]
        else:
            self.load_case_label = load_case_label
        self.step_type = step_type
        
        """ initialize a dictioary to represent each load type, where the section cut is the key"""
        self.M3 = {cut: None for cut in self.stations.keys()}
        self.V2 = {cut: None for cut in self.stations.keys()}
        self.M2 = {cut: None for cut in self.stations.keys()}
        self.V3 = {cut: None for cut in self.stations.keys()}
        self.P = {cut: None for cut in self.stations.keys()}
        self.T = {cut: None for cut in self.stations.keys()}
        
        self.forces = {"M3": self.M3,
                       "V2": self.V2,
                       "M2": self.M2,
                       "V3": self.V3,
                       "P": self.P,
                       "T": self.T}
        
#        self.force_fields = [M3_field, V2_field, M2_field, V3_field, P_field, T_field]
        
        def add_forces(forces, span_label, girder_label, load_case_label, raw_data):
            for row in raw_data:
                if (row[span_field] == span_label) and (row[girder_field] == girder_label) and (row[load_case_field] == load_case_label) and (row[step_type_field] == step_type):
                    cut = row[cut_field]
                    forces["M3"][cut] = row[M3_field]
                    forces["V2"][cut] = row[V2_field]
                    forces["M2"][cut] = row[M2_field]
                    forces["V3"][cut] = row[V3_field]
                    forces["P"][cut] = row[P_field]
                    forces["T"][cut] = row[T_field]
            return forces
        
        self.forces = add_forces(self.forces, self.span_label, self.girder_label, self.load_case_label, self.raw_data)
        
    def get_load_case_label(self):
        return self.load_case_label
 
    """ Get the whole dictionary for a specific force type """
    def get_M3(self):
        return self.M3
    
    def get_V2(self):
        return self.V2
    
    def get_M2(self):
        return self.M2
    
    def get_V3(self):
        return self.V3
    
    def get_P(self):
        return self.P
    
    def get_T(self):
        return self.T
    
    """ Get indiividual values of a force at a cut location"""
    def get_M3_cut(self, cut):
        return self.M3[cut]
    
    def get_V2_cut(self, cut):
        return self.V2[cut]
    
    def get_M2_cut(self, cut):
        return self.M2[cut]
    
    def get_V3_cut(self, cut):
        return self.V3[cut]
    
    def get_P_cut(self, cut):
        return self.P[cut]
    
    def get_T_cut(self, cut):
        return self.T[cut]    
    
    
    def get_step_type(self):
        return self.step_type
    
    def get_forces(self):
        return self.forces
    
class ForceTables(Girder):
    def __init__(self, span_label, girder_label, stations, load_cases):
        self.span_label = span_label
        self.girder_label = girder_label
        self.stations =  stations
        self.load_cases = load_cases
        self.load_case_labels = [key for key in load_cases.keys()]
        self.table_headers = ["Station"] + self.load_case_labels + ["Global Station"]
        
        self.M3_table = [self.table_headers]
        self.V2_table = [self.table_headers]
        self.M2_table = [self.table_headers]
        self.V3_table = [self.table_headers]
        self.P_table = [self.table_headers]
        self.T_table = [self.table_headers]
        
        self.tables = [self.M3_table, self.V2_table, self.M2_table, self.V3_table, self.P_table, self.T_table]
        
        def create_tables(girder, tables):
            """
            This Function populates each of the force effect tables with:
                - Stations
                - Forces for each load case in a seperate column
                - The Global station
            """
#            M3_row, V2_row, M2_row, V3_row, P_row, T_row = [], [], [], [], [], []
            for cut in stations.keys():
                M3_row = []
                V2_row = []
                M2_row = []
                V3_row = []
                P_row = []
                T_row = []
                rows = [M3_row, V2_row, M2_row, V3_row, P_row, T_row]
                station = stations[cut][0]
                for row in rows:
                    row.append(station)
                for load_case in load_cases.values():
                    M3_row.append(load_case.get_M3_cut(cut))
#                    print(M3_row)
                    V2_row.append(load_case.get_V2_cut(cut))
                    M2_row.append(load_case.get_M2_cut(cut))
                    V3_row.append(load_case.get_V3_cut(cut))
                    P_row.append(load_case.get_P_cut(cut))
                    T_row.append(load_case.get_T_cut(cut))
                for row in rows:
                    global_station = stations[cut][1]
                    row.append(global_station)
                    
                    i = 0
#                tables[0].append(M3_row)
#                tables[1].append(V2_row)
                for table in tables:
                    table.append(rows[i])
                    i+=1
                
            return tables
        
        self.tables = create_tables(self.load_cases, self.tables)
        
    
    def get_M3_table(self):
        return self.M3_table
    
    def get_V2_table(self):
        return self.V2_table
    
    def get_M2_table(self):
        return self.M2_table
    
    def get_V3_table(self):
        return self.V3_table
    
    def get_P_table(self):
        return self.P_table
    
    def get_T_table(self):
        return self.T_table
    
    
#"""Main"""
#raw_data_file = r"C:\Users\30mc\Documents\Master Sword\Tools\Quick Bridge Analysis\Simple Data.csv"
#csv_reader = csv.DictReader(open(raw_data_file, 'r'))
#raw_data = [row for row in csv_reader]

"""Define CSV fields for object to reference """
fields = ["BridgeObj", "BridgeCut", "Station", "Span", "Girder", "GirderDist", "LocType", "OutputCase", "CaseType", "StepType", "P" ,"V2" ,"V3" ,"T", "M2", "M3", "GlobalX", "GlobalY", "GlobalZ"]
bridge_field = fields[0]
cut_field = fields[1]
station_field = fields[2]
span_field = fields[3]  
girder_field = fields[4]
load_case_field = fields[7]
step_type_field = fields[9]
M3_field = fields[15]
V2_field = fields[11]
M2_field = fields[14]
V3_field = fields[12]
P_field = fields[10]
T_field = fields[13]
globalx_field = fields[16]

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