# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 17:31:26 2023

@author: Patrick
"""

import binascii
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#5
# import sklearn.metrics as metrics
# from sklearn.linear_model import LogisticRegression
# from sklearn.preprocessing import StandardScaler
# from sklearn.impute import SimpleImputer


class MotionEnvParse:
    def __init__(self, filepath, file_name, title, stat, walk, loc, t):
        self.filepath = filepath
        self.filename = filepath+file_name
        self.file_name = file_name
        self.title = title+" "+t
        self.count = 0
        self.aq=True
        self.aq_list = []
        self.motion_list = []
        self.env_list = []
        self.time_start_motion = 0
        self.prev = 0
        self.max_signed_val = 65536/2
        
        self.stationary = stat
        self.walking = walk
        self.location = loc
        self.start_time = t
        self.acc_x_ = 0
        self.acc_x_2 = 0
        self.acc_y_ = 0
        self.acc_z_ = 0
        self.acc_x_diff1 = [0,0,0,0,0,0,0,0,0,0]
        self.acc_x_diff2 = [0,0,0,0,0,0,0,0,0,0]
        self.acc_y_diff1 = [0,0,0,0,0,0,0,0,0,0]
        self.acc_z_diff1 = [0,0,0,0,0,0,0,0,0,0]
        
        self.gyr_x_ = 0
        self.gyr_y_ = 0
        self.gyr_z_ = 0
        self.gyr_x_diff1 = [0,0,0,0,0,0,0,0,0,0]
        self.gyr_y_diff1 = [0,0,0,0,0,0,0,0,0,0]
        self.gyr_z_diff1 = [0,0,0,0,0,0,0,0,0,0]  
        
        self.parse_to_lists()
        self.aqi_flag = False
        self.aqi_list = []
        self.aqi_ma_list = []
        self.time_aqi = []
             
    def parse_to_lists(self):
        counter = 0
        rows = []
        features = []
        headers = ['time','acc_x','acc_y','acc_z','acc_x_d1','acc_x_d2','acc_x_d3','acc_x_d4','acc_x_d5','acc_x_d6','acc_x_d7',
                   'acc_x_d8','acc_z_d9','acc_y_d1','acc_y_d2','acc_y_d3','acc_y_d4','acc_y_d5','acc_y_d6','acc_y_d7',
                   'acc_y_d8','acc_y_d9','acc_z_d1','acc_z_d2','acc_z_d3','acc_z_d4','acc_z_d5','acc_z_d6','acc_z_d7',
                   'acc_z_d8','acc_z_d9','gyr_x','gyr_y','gyr_z','gyr_x_d1','gyr_x_d2','gyr_x_d3','gyr_x_d4','gyr_x_d5','gyr_x_d6','gyr_x_d7',
                   'gyr_x_d8','gyr_x_d9','gyr_y_d1','gyr_y_d2','gyr_y_d3','gyr_y_d4','gyr_y_d5','gyr_y_d6','gyr_y_d7',
                   'gyr_y_d8','gyr_y_d9','gyr_z_d1','gyr_z_d2','gyr_z_d3','gyr_z_d4','gyr_z_d5','gyr_z_d6','gyr_z_d7',
                   'gyr_z_d8','gyr_z_d9','mag_x','mag_y','mag_z','temp', 'pressure','pm10','pm4','pm2.5','pm1', 'stationary', 
                   'walking', 'location', 'start_time']
        with open(self.filename, 'r') as fr:
            for row in fr:
                if counter < 1:
                    counter = 3
                    continue
                # print(row)
                handle = row[24:28]
                handle = handle.replace(" ", "")
                
                time_start = row[36:42]
                time_start = time_start.replace(" ", "")
                if time_start == 'ffff' and self.aq:
                    # print("Air Quality")
                    self.aq = False
                    self.time_start = counter
                    self.parse_aq_data(row)
                elif time_start == 'aaaa':
                    # print("Environment")
                    self.aq = True
                    self.time_start = counter
                    self.parse_env_data(row)
                elif time_start == 'eeee':                    
                    features.append([self.motion_list[-1][0],self.motion_list[-1][1],self.motion_list[-1][2],self.motion_list[-1][3]
                                    ,self.motion_list[-1][4],self.motion_list[-1][5],self.motion_list[-1][6],self.motion_list[-1][7]
                                    ,self.motion_list[-1][8],self.motion_list[-1][9],self.motion_list[-1][10],self.motion_list[-1][11],self.motion_list[-1][12]
                                    ,self.motion_list[-1][13],self.motion_list[-1][14],self.motion_list[-1][15],self.motion_list[-1][16]
                                    ,self.motion_list[-1][17],self.motion_list[-1][18],self.motion_list[-1][19],self.motion_list[-1][20],self.motion_list[-1][21],self.motion_list[-1][22]
                                    ,self.motion_list[-1][23],self.motion_list[-1][24],self.motion_list[-1][25],self.motion_list[-1][26]
                                    ,self.motion_list[-1][27],self.motion_list[-1][28],self.motion_list[-1][29],self.motion_list[-1][30],self.motion_list[-1][31],self.motion_list[-1][32]
                                    ,self.motion_list[-1][33],self.motion_list[-1][34],self.motion_list[-1][35],self.motion_list[-1][36]
                                    ,self.motion_list[-1][37],self.motion_list[-1][38],self.motion_list[-1][39],self.motion_list[-1][40],self.motion_list[-1][41],self.motion_list[-1][42]
                                    ,self.motion_list[-1][43],self.motion_list[-1][44],self.motion_list[-1][45],self.motion_list[-1][46]
                                    ,self.motion_list[-1][47],self.motion_list[-1][48],self.motion_list[-1][49],self.motion_list[-1][50],self.motion_list[-1][51],self.motion_list[-1][52]
                                    ,self.motion_list[-1][53],self.motion_list[-1][54],self.motion_list[-1][55],self.motion_list[-1][56]
                                    ,self.motion_list[-1][57],self.motion_list[-1][58],self.motion_list[-1][59],self.motion_list[-1][60],self.motion_list[-1][61],self.motion_list[-1][62]
                                    ,self.motion_list[-1][63],self.env_list[-1][2],self.env_list[-1][1],
                                    self.aq_list[-1][4],self.aq_list[-1][3],self.aq_list[-1][2],self.aq_list[-1][1],
                                    self.stationary, self.walking, self.location, self.start_time])
                    
                    # MOX data
                else:
                    # Motion Data
                    counter = counter + 0.05
                    self.parse_motion_data(row, counter)
                    
                    features.append([self.motion_list[-1][0],self.motion_list[-1][1],self.motion_list[-1][2],self.motion_list[-1][3]
                                    ,self.motion_list[-1][4],self.motion_list[-1][5],self.motion_list[-1][6],self.motion_list[-1][7]
                                    ,self.motion_list[-1][8],self.motion_list[-1][9],self.motion_list[-1][10],self.motion_list[-1][11],self.motion_list[-1][12]
                                    ,self.motion_list[-1][13],self.motion_list[-1][14],self.motion_list[-1][15],self.motion_list[-1][16]
                                    ,self.motion_list[-1][17],self.motion_list[-1][18],self.motion_list[-1][19],self.motion_list[-1][20],self.motion_list[-1][21],self.motion_list[-1][22]
                                    ,self.motion_list[-1][23],self.motion_list[-1][24],self.motion_list[-1][25],self.motion_list[-1][26]
                                    ,self.motion_list[-1][27],self.motion_list[-1][28],self.motion_list[-1][29],self.motion_list[-1][30],self.motion_list[-1][31],self.motion_list[-1][32]
                                    ,self.motion_list[-1][33],self.motion_list[-1][34],self.motion_list[-1][35],self.motion_list[-1][36]
                                    ,self.motion_list[-1][37],self.motion_list[-1][38],self.motion_list[-1][39],self.motion_list[-1][40],self.motion_list[-1][41],self.motion_list[-1][42]
                                    ,self.motion_list[-1][43],self.motion_list[-1][44],self.motion_list[-1][45],self.motion_list[-1][46]
                                    ,self.motion_list[-1][47],self.motion_list[-1][48],self.motion_list[-1][49],self.motion_list[-1][50],self.motion_list[-1][51],self.motion_list[-1][52]
                                    ,self.motion_list[-1][53],self.motion_list[-1][54],self.motion_list[-1][55],self.motion_list[-1][56]
                                    ,self.motion_list[-1][57],self.motion_list[-1][58],self.motion_list[-1][59],self.motion_list[-1][60],self.motion_list[-1][61],self.motion_list[-1][62]
                                    ,self.motion_list[-1][63],np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
                                    ,self.stationary, self.walking, self.location, self.start_time])
        # print(self.env_list[-1][1],self.env_list[-1][2])
        # Creating Data Frame, parsing into csv file
        self.features_df = pd.DataFrame(features, columns=headers)
        self.features_df.to_csv(self.filepath+"Features\\"+self.file_name.replace(".txt", "_features__.csv"))
    
    '''
        Debugging function to print all contents of lists available
    '''
    def print_lists(self):
        for row in self.motion_list:
            print(row)
        for row in self.aq_list:
            print(row)
        for row in self.env_list:
            print(row)
        print(len(self.motion_list))
        print(len(self.aq_list))
    
    '''
        Plot the Acc data alone against time
    '''
    def plot_acc(self):
        plt.figure(1)
        plt.plot(self.motion_df['Time'], self.motion_df['Acc X'], label="X-Axis Acceleration")
        plt.plot(self.motion_df['Time'], self.motion_df['Acc Y'], label="Y-Axis Acceleration")
        plt.plot(self.motion_df['Time'], self.motion_df['Acc Z'], label="Z-Axis Acceleration")
        plt.xlabel('Time')
        plt.ylabel('Acceleration (mg)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        plt.legend()
        # plt.show()
        
    '''
        Plot the AQ data alone against time
    '''
    def plot_aq(self):
        plt.figure(2)
        plt.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM1.0'], label="MC PM1.0")
        plt.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM2.5'], label="MC PM2.5")
        plt.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM10'], label="MC PM10")
        plt.xlabel('Time (s)')
        plt.ylabel('Mass (ug/m^3)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        plt.legend()
        
        plt.figure(3)
        plt.plot(self.aq_df['Time'], self.aq_df['Number Concentration PM0.5'], label="NC PM0.5")
        plt.plot(self.aq_df['Time'], self.aq_df['Number Concentration PM1'], label="NC PM1.0")
        plt.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM2.5'], label="NC PM2.5")
        plt.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM4'], label="NC PM4")
        plt.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM10'], label="NC PM10")
        plt.xlabel('Time (s)')
        plt.ylabel('Mass (#/cm^3)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        plt.legend()
        plt.show()
    
    def plot_aq_moving_av(self):
        fig, ax = plt.subplots()
        ax.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM1.0 Moving Average'], label="MC PM1.0 Moving Average", color='purple')
        ax.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM2.5 Moving Average'], label="MC PM2.5 Moving Average", color='blue')
        ax.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM10 Moving Average'], label="MC PM10 Moving Average", color='yellow')
        ax.plot(self.time_av_plot, self.av_pm_1_mv, label="Average PM1.0", color="indigo", linestyle="dashed")
        ax.plot(self.time_av_plot, self.av_pm_25_mv, label="Average PM2.5", color="navy", linestyle="dashed")
        ax.plot(self.time_av_plot, self.av_pm_10_mv, label="Average PM10", color="gold", linestyle="dashed")
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Mass (ug/m^3)')
        ax.set_title('PM Data Moving Average with AQIH, '+self.title)
        ax2 = ax.twinx()
        ax2.plot(self.time_aqi, self.aqi_list, label="AQIH Raw Data", color='cyan')
        ax2.plot(self.time_aqi, self.aqi_ma_list, label="AQIH Moving Average Data", color='black', linestyle="dotted")
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('AQIH (1-10)')
        ax2.set_ylim([0,10])
        
        fig.legend(bbox_to_anchor=(1.15, 1), loc='upper left', borderaxespad=0.)
        fig.legend()
        
        plt.show() 
        titl = self.title.replace('/', '').replace(' ', '_').replace(',', '_')+"_"   
        fig.savefig(self.filepath+"Plots\\"+titl.replace(':', '')+"PM_Moving_Average_with_AQIH.png", format="png", bbox_inches="tight")
    
    '''
        Plotting the Acceleration data against time, along with the AQ (PM Data) on the same plot
        Also done for [Temp, Pressure], Magnetometer and Gyroscopic data
        
        save figures plotted
    '''
    def plot_aq_ug_acc(self):
        fig, ax1 = plt.subplots()
        ax1.plot(self.motion_df['Time'], self.motion_df['Acc X'], label="X-Axis Acceleration", color='green')
        ax1.plot(self.motion_df['Time'], self.motion_df['Acc Y'], label="Y-Axis Acceleration", color='orange')
        ax1.plot(self.motion_df['Time'], self.motion_df['Acc Z'], label="Z-Axis Acceleration", color='red')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Acceleration (g)')
        # ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        
        ax2 = ax1.twinx()
        # ax4 = ax1.twinx()
        
        ax2.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM1.0'], label="MC PM1.0", color='purple')
        ax2.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM2.5'], label="MC PM2.5", color='blue')
        # ax2.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM4'], label="MC PM4", color='cyan')
        ax2.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM10'], label="MC PM10", color='yellow')
        ax2.plot(self.time_av_plot, self.av_pm_1, label="Average PM1.0", color="indigo", linestyle="dashed")
        ax2.plot(self.time_av_plot, self.av_pm_25, label="Average PM2.5", color="navy", linestyle="dashed")
        ax2.plot(self.time_av_plot, self.av_pm_10, label="Average PM10", color="gold", linestyle="dashed")
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Mass (ug/m^3)')
        ax2.set_title('Acceleration Data, '+self.title)
        
        fig.legend(bbox_to_anchor=(1.2, 1), loc='upper left', borderaxespad=0.)
        fig.legend()
        titl = self.title.replace('/', '').replace(' ', '_').replace(',', '_')+"_"
        plt.show()
        fig.savefig(self.filepath+"Plots\\"+titl.replace(':', '')+"Acc.png", format="png", bbox_inches="tight")
        
        fig1, ax6 = plt.subplots()
        ax6.plot(self.motion_df['Time'], self.motion_df['Gyr X'], label="X-Axis Gyrsoscope", color='lightgreen')
        ax6.plot(self.motion_df['Time'], self.motion_df['Gyr Y'], label="Y-Axis Gyrsoscope", color='wheat')
        ax6.plot(self.motion_df['Time'], self.motion_df['Gyr Z'], label="Z-Axis Gyrsoscope", color='tomato')
        ax6.set_xlabel('Time (s)')
        ax6.set_ylabel('Gyroscope (dps)')
        # ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        
        ax7 = ax6.twinx()
        # ax4 = ax1.twinx()
        
        ax7.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM1.0'], label="MC PM1.0", color='purple')
        ax7.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM2.5'], label="MC PM2.5", color='blue')
        # ax7.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM4'], label="MC PM4", color='cyan')
        ax7.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM10'], label="MC PM10", color='yellow')
        ax7.plot(self.time_av_plot, self.av_pm_1, label="Average PM1.0", color="indigo", linestyle="dashed")
        ax7.plot(self.time_av_plot, self.av_pm_25, label="Average PM2.5", color="navy", linestyle="dashed")
        ax7.plot(self.time_av_plot, self.av_pm_10, label="Average PM10", color="gold", linestyle="dashed")
        ax7.set_xlabel('Time (s)')
        ax7.set_ylabel('Mass (ug/m^3)')
        ax7.set_title("Gyroscope Data, "+self.title)
        
        fig1.legend(bbox_to_anchor=(1.2, 1), loc='upper left', borderaxespad=0.)
        fig1.legend()
        plt.show()
        fig1.savefig(self.filepath+"Plots\\"+titl.replace(':', '')+"Gyr.png", format="png", bbox_inches="tight")
        
        fig3, ax8 = plt.subplots()
        ax8.plot(self.motion_df['Time'], self.motion_df['Mag X'], label="X-Axis Magnetometer", color='palegreen')
        ax8.plot(self.motion_df['Time'], self.motion_df['Mag Y'], label="Y-Axis Magnetometer", color='moccasin')
        ax8.plot(self.motion_df['Time'], self.motion_df['Mag Z'], label="Z-Axis Magnetometer", color='darksalmon')
        ax8.set_xlabel('Time (s)')
        ax8.set_ylabel('Magnetometer (Gauss)')
        # ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        
        ax9 = ax8.twinx()
        # ax4 = ax1.twinx()
        
        ax9.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM1.0'], label="MC PM1.0", color='purple')
        ax9.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM2.5'], label="MC PM2.5", color='blue')
        # ax9.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM4'], label="MC PM4", color='cyan')
        ax9.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM10'], label="MC PM10", color='yellow')
        ax9.plot(self.time_av_plot, self.av_pm_1, label="Average PM1.0", color="indigo", linestyle="dashed")
        ax9.plot(self.time_av_plot, self.av_pm_25, label="Average PM2.5", color="navy", linestyle="dashed")
        ax9.plot(self.time_av_plot, self.av_pm_10, label="Average PM10", color="gold", linestyle="dashed")
        ax9.set_xlabel('Time (s)')
        ax9.set_ylabel('Mass (ug/m^3)')
        ax9.set_title('Magnetometer Data, '+self.title)
        
        fig3.legend(bbox_to_anchor=(1.2, 1), loc='upper left', borderaxespad=0.)
        fig3.legend()
        plt.show()
        fig3.savefig(self.filepath+"Plots\\"+titl.replace(':', '')+"Mag.png", format="png", bbox_inches="tight")
        
        fig2, ax3 = plt.subplots()
        ax4 = ax3.twinx()
        ax5 = ax3.twinx()
       
        ax3.plot(self.env_df['Time'], self.env_df['Pressure'], label="Pressure", color='pink')
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Pressure (Bar)')
        
        ax4.plot(self.env_df['Time'], self.env_df['Temp'], label="Temperature", color='brown')
        ax4.set_xlabel('Time (s)')
        ax4.set_ylabel('Temperature (C)')
        ax4.spines['right'].set_position(('outward', 50))
        # ax4.spines.right.set_position(("axes", 1.2))
        
        ax5.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM1.0'], label="MC PM1.0", color='purple')
        ax5.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM2.5'], label="MC PM2.5", color='blue')
        # ax5.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM4'], label="MC PM4", color='cyan')
        ax5.plot(self.aq_df['Time'], self.aq_df['Mass Concentration PM10'], label="MC PM10", color='yellow')
        ax5.plot(self.time_av_plot, self.av_pm_1, label="Average PM1.0", color="indigo", linestyle="dashed")
        ax5.plot(self.time_av_plot, self.av_pm_25, label="Average PM2.5", color="navy", linestyle="dashed")
        ax5.plot(self.time_av_plot, self.av_pm_10, label="Average PM10", color="gold", linestyle="dashed")
        ax5.set_xlabel('Time (s)')
        ax5.set_ylabel('Mass (ug/m^3)') 
        
        fig2.legend(bbox_to_anchor=(1.2, 1), loc='upper left', borderaxespad=0.)
        fig2.legend()
        ax4.set_title('Temp and Pressure Data, '+self.title)
        plt.show()
        fig2.savefig(self.filepath+"Plots\\"+titl.replace(':', '')+"Temp-Press.png", format="png", bbox_inches="tight")
        
    '''
        Converting the lists of converted data imported through the txt file into
        a DataFrame, for ease of use
    '''
    def convert_lists_to_df(self):
        self.aq_df = pd.DataFrame(self.aq_list, columns=['Time', 'Mass Concentration PM1.0', 
                            'Mass Concentration PM2.5',  'Mass Concentration PM4', 'Mass Concentration PM10',
                             'Number Concentration PM0.5', 'Number Concentration PM1', 'Number Concentration PM2.5',
                             'Number Concentration PM4', 'Number Concentration PM10'])
        # Adding the moving average (Using 5 points to clalculate the moving average) column to df
        self.aq_df['Mass Concentration PM1.0 Moving Average'] = self.aq_df['Mass Concentration PM1.0'].rolling(window=5, min_periods=1).mean()
        self.aq_df['Mass Concentration PM2.5 Moving Average'] = self.aq_df['Mass Concentration PM2.5'].rolling(window=5, min_periods=1).mean()
        self.aq_df['Mass Concentration PM10 Moving Average'] = self.aq_df['Mass Concentration PM10'].rolling(window=5, min_periods=1).mean()
        self.motion_df = pd.DataFrame(self.motion_list, columns=['Time', 'Acc X', 'Acc Y', 'Acc Z','Acc X-1','Acc X-2','Acc X-3','Acc X-4','Acc X-5','Acc X-6','Acc X-7','Acc X-8','Acc X-9',
                                                                 'Acc Y-1','Acc Y-2','Acc Y-3','Acc Y-4','Acc Y-5','Acc Y-6','Acc Y-7','Acc Y-8','Acc Y-9',
                                                                 'Acc Z-1','Acc Z-2','Acc Z-3','Acc Z-4','Acc Z-5','Acc Z-6','Acc Z-7','Acc Z-8','Acc Z-9',
                                                                 'Gyr X','Gyr Y','Gyr Z', 'Gyr X-1','Gyr X-2','Gyr X-3','Gyr X-4','Gyr X-5','Gyr X-6','Gyr X-7','Gyr X-8','Gyr X-9',
                                                                  'Gyr Y-1','Gyr Y-2','Gyr Y-3','Gyr Y-4','Gyr Y-5','Gyr Y-6','Gyr Y-7','Gyr Y-8','Gyr Y-9',
                                                                  'Gyr Z-1','Gyr Z-2','Gyr Z-3','Gyr Z-4','Gyr Z-5','Gyr Z-6','Gyr Z-7','Gyr Z-8','Gyr Z-9',
                                                                 'Mag X', 'Mag Y', 'Mag Z'])
        self.env_df = pd.DataFrame(self.env_list, columns=['Time', 'Pressure', 'Temp'])
        
        # Min and max points of time for the AQ data gathered
        self.time_max = self.aq_df['Time'].max()
        self.time_min = self.aq_df['Time'].min()
        self.time_av_plot = [self.time_min, self.time_max]
        
        # Calculating average mass concentrations over the period from the raw data and the moving average data
        av_pm1 = self.aq_df['Mass Concentration PM1.0'].mean()
        av_pm1_mv = self.aq_df['Mass Concentration PM1.0 Moving Average'].mean()
        self.av_pm_1 = [av_pm1, av_pm1]
        self.av_pm_1_mv = [av_pm1_mv, av_pm1_mv]
        
        av_pm25 = self.aq_df['Mass Concentration PM2.5'].mean()
        av_pm25_mv = self.aq_df['Mass Concentration PM2.5 Moving Average'].mean()
        self.av_pm_25 = [av_pm25, av_pm25]
        self.av_pm_25_mv = [av_pm25_mv, av_pm25_mv]
        
        av_pm10 = self.aq_df['Mass Concentration PM10'].mean()
        av_pm10_mv = self.aq_df['Mass Concentration PM10 Moving Average'].mean()
        self.av_pm_10 = [av_pm10, av_pm10]
        self.av_pm_10_mv = [av_pm10_mv, av_pm10_mv]
        
        # print(self.title+":\t" +str(av_pm1)+",\t"+ str(av_pm25)+",\t"+ str(av_pm10))
        # print(self.title+":\t" +str(av_pm1_mv)+",\t"+ str(av_pm25_mv)+",\t"+ str(av_pm10_mv))
        
        pm10_list = self.aq_df['Mass Concentration PM10']
        pm25_list = self.aq_df['Mass Concentration PM2.5']
        pm10_ma_list = self.aq_df['Mass Concentration PM10 Moving Average']
        pm25_ma_list = self.aq_df['Mass Concentration PM2.5 Moving Average']
        loc_time = self.aq_df['Time']
        
        for i in range(len(pm10_list)):
            if i%12 == 0 and i!=0:
                pm25 = pm25_list[-12:].mean()
                pm10 = pm10_list[-12:].mean()
                pm25ma = pm25_ma_list[-12:].mean()
                pm10ma = pm10_ma_list[-12:].mean()
                self.aqi_list.append(self.calculate_aqih(pm25, pm10))
                self.aqi_ma_list.append(self.calculate_aqih(pm25ma, pm10ma))
                self.time_aqi.append(round(loc_time[i], 3))
    
    '''
        Parsing the raw AQ Data into a set of lists for each variable
    '''
    def parse_aq_data(self, row):
        
        p1 = row[42:48]
        p1 = p1.replace(" ", "")
        p1 = binascii.unhexlify(p1)
        p1 = int.from_bytes(p1, byteorder=sys.byteorder)
        p1 = p1/100
        if self.prev > 0:
            if abs(p1 - self.aq_list[-1][1]) > 100:
                p1 = self.aq_list[-1][1]
        
        p25 = row[48:54]
        p25 = p25.replace(" ", "")
        p25 = binascii.unhexlify(p25)
        p25 = int.from_bytes(p25, byteorder=sys.byteorder)
        p25 = p25/100
        if self.prev > 0:
            if abs(p25 - self.aq_list[-1][2]) > 100:
                p25 = self.aq_list[-1][2]
        
        p4 = row[54:60]
        p4 = p4.replace(" ", "")
        p4 = binascii.unhexlify(p4)
        p4 = int.from_bytes(p4, byteorder=sys.byteorder)
        p4= p4/100
        if self.prev > 0:
            if abs(p4 - self.aq_list[-1][3]) > 100:
                p4 = self.aq_list[-1][3]
        
        p10 = row[60:66]
        p10 = p10.replace(" ", "")
        p10 = binascii.unhexlify(p10)
        p10 = int.from_bytes(p10, byteorder=sys.byteorder)
        p10 = self.twos_complement(p10)
        p10 = p10/100
        if self.prev > 0:
            if abs(p10 - self.aq_list[-1][4]) > 100:
                p10 = self.aq_list[-1][4]
        
        n05 = row[66:72]
        n05 = n05.replace(" ", "")
        n05 = binascii.unhexlify(n05)
        n05 = int.from_bytes(n05, byteorder=sys.byteorder)
        n05 = self.twos_complement(n05)
        n05 = n05/100
        
        n1 = row[72:78]
        n1 = n1.replace(" ", "")
        n1 = binascii.unhexlify(n1)
        n1 = int.from_bytes(n1, byteorder=sys.byteorder)
        n1 = n1/100
        
        n25 = row[78:84]
        n25 = n25.replace(" ", "")
        n25 = binascii.unhexlify(n25)
        n25 = int.from_bytes(n25, byteorder=sys.byteorder)
        n25 = n25/100
        
        n4 = row[84:90]
        n4 = n4.replace(" ", "")
        n4 = binascii.unhexlify(n4)
        n4 = int.from_bytes(n4, byteorder=sys.byteorder)
        n4 = n4/100
        
        n10 = row[90:96]
        n10 = n10.replace(" ", "")
        n10 = binascii.unhexlify(n10)
        n10 = int.from_bytes(n10, byteorder=sys.byteorder)     
        n10 = n10/100
        new_row = [self.time_start_motion, p1, p25, p4, p10, n05, n1, n25, n4, n10]
        if round(self.time_start_motion, 3) % 60 ==0 and round(self.time_start_motion, 3) != 0:
            self.aqi_flag = True
        # print(new_row)
        self.aq_list.append(new_row) 
        self.prev+=1
                    
    '''
         Parsing the raw Environmental Data into a set of lists for each variable
    '''
    def parse_env_data(self, row):
        pressure = row[42:54]
        pressure = pressure.replace(" ", "")
        pressure = binascii.unhexlify(pressure)
        pressure = int.from_bytes(pressure, byteorder=sys.byteorder)
        pressure = pressure/100000
        
        temp = row[54:60]
        temp = temp.replace(" ", "")
        temp = binascii.unhexlify(temp)
        temp = int.from_bytes(temp, byteorder=sys.byteorder)
        temp = temp/10
        
        new_row = [self.time_start_motion, pressure, temp]
        # print(new_row)
        self.env_list.append(new_row)    
      
    '''
         Parsing the raw Motion Data into a set of lists for each variable
         Motion data is in hexadecimal little endian format 
    '''              
    def parse_motion_data(self, row, time_start):
        self.time_start_motion = row[36:42]
        self.time_start_motion = self.time_start_motion.replace(" ", "")
        self.time_start_motion = binascii.unhexlify(self.time_start_motion)
        self.time_start_motion = int.from_bytes(self.time_start_motion, byteorder=sys.byteorder)
        self.time_start_motion = time_start
        
        acc_x = row[42:48]
        acc_x = acc_x.replace(" ", "")
        acc_x = binascii.unhexlify(acc_x)
        acc_x = int.from_bytes(acc_x, byteorder=sys.byteorder)
        acc_x = self.twos_complement(acc_x)/1000
            
        acc_y = row[48:54]
        acc_y = acc_y.replace(" ", "")
        acc_y = binascii.unhexlify(acc_y)
        acc_y = int.from_bytes(acc_y, byteorder=sys.byteorder)
        acc_y = self.twos_complement(acc_y)/1000
        
        acc_z = row[54:60]
        acc_z = acc_z.replace(" ", "")
        acc_z = binascii.unhexlify(acc_z)
        acc_z = int.from_bytes(acc_z, byteorder=sys.byteorder)
        acc_z = self.twos_complement(acc_z)/1000
        
        gyr_x = row[60:66]
        gyr_x = gyr_x.replace(" ", "")
        gyr_x = binascii.unhexlify(gyr_x)
        gyr_x = int.from_bytes(gyr_x, byteorder=sys.byteorder)
        gyr_x = self.twos_complement(gyr_x)/1000
        
        gyr_y = row[66:72]
        gyr_y = gyr_y.replace(" ", "")
        gyr_y = binascii.unhexlify(gyr_y)
        gyr_y = int.from_bytes(gyr_y, byteorder=sys.byteorder)
        gyr_y = self.twos_complement(gyr_y)/1000
        
        gyr_z = row[72:78]
        gyr_z = gyr_z.replace(" ", "")
        gyr_z = binascii.unhexlify(gyr_z)
        gyr_z = int.from_bytes(gyr_z, byteorder=sys.byteorder)
        gyr_z = self.twos_complement(gyr_z)/1000
        
        mag_x = row[78:84]
        mag_x = mag_x.replace(" ", "")
        mag_x = binascii.unhexlify(mag_x)
        mag_x = int.from_bytes(mag_x, byteorder=sys.byteorder)
        mag_x = self.twos_complement(mag_x)/1000
        
        mag_y = row[84:90]
        mag_y = mag_y.replace(" ", "")
        mag_y = binascii.unhexlify(mag_y)
        mag_y = int.from_bytes(mag_y, byteorder=sys.byteorder)
        mag_y = self.twos_complement(mag_y)/1000
        
        mag_z = row[90:96]
        mag_z = mag_z.replace(" ", "")
        mag_z = binascii.unhexlify(mag_z)
        mag_z = int.from_bytes(mag_z, byteorder=sys.byteorder)
        mag_z = self.twos_complement(mag_z)/1000 
        
        self.acc_x_diff1[0] = acc_x - self.acc_x_
        self.acc_x_diff2[0] = acc_x - self.acc_x_2
        self.acc_y_diff1[0] = acc_y - self.acc_y_
        self.acc_z_diff1[0] = acc_z - self.acc_z_
        self.gyr_x_diff1[0] = gyr_x - self.gyr_x_
        self.gyr_y_diff1[0] = gyr_y - self.gyr_y_
        self.gyr_z_diff1[0] = gyr_z - self.gyr_z_
        
        new_row = [round(self.time_start_motion, 3), acc_x, acc_y, acc_z, self.acc_x_diff1[0], self.acc_x_diff1[1], self.acc_x_diff1[2], 
                   self.acc_x_diff1[3], self.acc_x_diff1[4], self.acc_x_diff1[5], self.acc_x_diff1[6], self.acc_x_diff1[7], self.acc_x_diff1[8], 
                   self.acc_y_diff1[0], self.acc_y_diff1[1], self.acc_y_diff1[2], self.acc_y_diff1[3], self.acc_y_diff1[4], self.acc_y_diff1[5], 
                   self.acc_y_diff1[6], self.acc_y_diff1[7], self.acc_y_diff1[8], self.acc_z_diff1[0], self.acc_z_diff1[1], self.acc_z_diff1[2], 
                   self.acc_z_diff1[3], self.acc_z_diff1[4], self.acc_z_diff1[5], self.acc_z_diff1[6], self.acc_z_diff1[7], self.acc_z_diff1[8],
                   gyr_x, gyr_y, gyr_z, self.gyr_x_diff1[0], self.gyr_x_diff1[1], self.gyr_x_diff1[2], 
                   self.gyr_x_diff1[3], self.gyr_x_diff1[4], self.gyr_x_diff1[5], self.gyr_x_diff1[6], self.gyr_x_diff1[7], self.gyr_x_diff1[8], 
                   self.gyr_y_diff1[0], self.gyr_y_diff1[1], self.gyr_y_diff1[2], self.gyr_y_diff1[3], self.gyr_y_diff1[4], self.gyr_y_diff1[5], 
                   self.gyr_y_diff1[6], self.gyr_y_diff1[7], self.gyr_y_diff1[8], self.gyr_z_diff1[0], self.gyr_z_diff1[1], self.gyr_z_diff1[2], 
                   self.gyr_z_diff1[3], self.gyr_z_diff1[4], self.gyr_z_diff1[5], self.gyr_z_diff1[6], self.gyr_z_diff1[7], self.gyr_z_diff1[8], 
                   mag_x, mag_y, mag_z]
        
        for i in range(8, 0, -1):
            self.acc_x_diff1[i]=self.acc_x_diff1[i-1]
            self.acc_x_diff2[i]=self.acc_x_diff2[i-1]
            self.acc_y_diff1[i]=self.acc_y_diff1[i-1]
            self.acc_z_diff1[i]=self.acc_z_diff1[i-1]
            
            self.gyr_x_diff1[i]=self.gyr_x_diff1[i-1]
            self.gyr_y_diff1[i]=self.gyr_y_diff1[i-1]
            self.gyr_z_diff1[i]=self.gyr_z_diff1[i-1]
        
        self.acc_x_2 = self.acc_x_
        self.acc_x_ = acc_x
        self.acc_y_ = acc_y
        self.acc_z_ = acc_z
        self.gyr_x_ = gyr_x
        self.gyr_y_ = gyr_y
        self.gyr_z_ = gyr_z
        # print(new_row)
        self.motion_list.append(new_row)
        
    def twos_complement(self, var):
        if var > self.max_signed_val:
            var = (65536-var)*-1
    
        return var
    
    def large_twos_complement(self, var):
        if var > 2147483648:
            var = (4294967296-var)*-1
    
        return var

    def calculate_aqih(self, pm25, pm10):
        aqi_25 = 0
        
        if pm25 > 0 and pm25 < 12:
            aqi_25 = 1
        elif pm25 < 24:
            aqi_25 = 2
        elif pm25 < 36:
            aqi_25 = 3
        elif pm25 < 42:
            aqi_25 = 4
        elif pm25 < 48:
            aqi_25 = 5
        elif pm25 < 54:
            aqi_25 = 6
        elif pm25 < 59:
            aqi_25 = 7
        elif pm25 < 65:
            aqi_25 = 8
        elif pm25 < 71:
            aqi_25 = 9
        else:
            aqi_25 = 10
            
        aqi_10 = 0
        
        if pm10 > 0 and pm10 < 17:
            aqi_10 = 1
        elif pm10 < 34:
            aqi_10 = 2
        elif pm10 < 51:
            aqi_10 = 3
        elif pm10 < 59:
            aqi_10 = 4
        elif pm10 < 67:
            aqi_10 = 5
        elif pm10 < 76:
            aqi_10 = 6
        elif pm10 < 84:
            aqi_10 = 7
        elif pm10 < 92:
            aqi_10 = 8
        elif pm10 < 101:
            aqi_10 = 9
        else:
            aqi_10 = 10
        
        aqi = round((aqi_25+aqi_10)/2)
        return aqi
    
def main(filepath, filename, title, stat, walk, loc, t):
    parse = MotionEnvParse(filepath, filename, title, stat, walk, loc, t)
    # parse.print_lists()
    parse.convert_lists_to_df()
    #parse.plot_aq_ug_acc()
    # parse.plot_aq()
    parse.plot_aq_moving_av()

if __name__ == "__main__":
    
#    filepath = "C:\\Users\\PByrne\\Documents\\GitHub\\masters_project\\Data_Collection\\"
    
    filepath = "C:\\Users\\Patrick\\Documents\\DCU\\Masters Project\\masters_project\\Data_Collection\\Birr\\"
    filename1 = "data_collection_stationary_birr2329071821.txt"
    filename2 = "data_collection_stationary_birr_2329071938.txt"
    filename3 = "data_collection_stationary_in_car_birr_2329071845.txt"
    title1 = "Stationary Data Collection Birr, 29/07/23"
    title2 = "Stationary Data Collection Birr, 29/07/23"
    title3 = "Stationary Data Collection Birr, 29/07/23"
    
    filename4 = "data_collection_walking_birr_2329071903.txt"
    title4 = "Walking Data Collection Birr, 29/07/23"
    
    main(filepath, filename1, title1,1,0,'Birr', '18:21')
    # main(filepath, filename2, title2,1,0,'Birr')
    main(filepath, filename3, title3,1,0,'Birr','18:45') 
    main(filepath, filename4, title4,0,1,'Birr','19:03')
    
    filepath = "C:\\Users\\Patrick\\Documents\\DCU\\Masters Project\\masters_project\\Data_Collection\\Heuston\\"
    filename='data_collection_stationary_heuston_2306081308.txt'
    title1 = "Stationary Data Collection Birr, 06/08/23"
    main(filepath, filename, title1, 1, 0, 'Heuston', '13:08')
    
    '''filename1 = "data_collection_stat_heuston_2308101030.txt"
    title1 = "Stationary Data Collection Heuston, 10/08/23 10:30"
    main(filepath, filename1, title1, 1, 0, 'Heuston', '10:30')
    
    filename1 = "data_collection_motion_heuston_2310081120.txt"
    title1 = "Walking Data Collection Heuston, 10/08/23 11:20"
    main(filepath, filename1, title1, 1, 0, 'Heuston', '11:20')
    
    filename1 = "data_heuston_stat_2310081000.txt"
    title1 = "Stationary Data Collection Heuston, 10/08/23 10:00"
    main(filepath, filename1, title1, 1, 0, 'Heuston', '10:00')
    
    filename1 = "data_heuston_stat_1008230942.txt"
    title1 = "Stationary Data Collection Heuston, 10/08/23 9:42"
    main(filepath, filename1, title1, 1, 0, 'Heuston', '9:42')
    
    filename1 = "data_collection_motion_heuston_2308101059.txt"
    title1 = "Walking Data Collection Heuston, 10/08/23 10:59"
    main(filepath, filename1, title1, 1, 0, 'Heuston', '10:59')
 
    filepath = "C:\\Users\\Patrick\\Documents\\DCU\\Masters Project\\masters_project\\Data_Collection\\Heuston\\"
    filename1 = "heuston_stat_2310081612.txt"
    title1 = "Stationary Data Collection Heuston, 10/08/23 16:12"
    main(filepath, filename1, title1, 1, 0, 'Heuston', '16:12')
    
    filename1 = "heuston_stat_2310081633.txt"
    title1 = "Stationary Data Collection Heuston, 10/08/23 16:33"
    main(filepath, filename1, title1, 1, 0, 'Heuston', '16:33')
    filepath = "C:\\Users\\Patrick\\Documents\\DCU\\Masters Project\\masters_project\\Data_Collection\\Heuston\\"
    filename1 = "testing_sample_1on_4off.txt"
    title1 = "Stationary Data Collection Heuston, 10/08/23 16:12"
    main(filepath, filename1, title1, 1, 0, 'Heuston', '16:12')
    '''
    filepath = "C:\\Users\\Patrick\\Documents\\DCU\\Masters Project\\masters_project\\Data_Collection\\Heuston\\_231708\\"
    file_details =[("heuston_stationary_2317081557_1on_4off.txt", "Stationary Data Collection Heuston, 17/08/23", 1, 0, '15:57'),
                   ("heuston_stationary_2317081625_1on_4off.txt", "Stationary Data Collection Heuston, 17/08/23", 1, 0, '16:25'),
                   ("heuston_stationary_2317081640_1on_4off.txt", "Stationary Data Collection Heuston, 17/08/23", 1, 0, '16:40'),
                   ("heuston_stationary_2317081648_1on_4off.txt", "Stationary Data Collection Heuston, 17/08/23", 1, 0, '16:48'),
                   ("heuston_stationary_2317081700_1on_4off.txt", "Stationary Data Collection Heuston, 17/08/23", 1, 0, '17:00'),
                   ("heuston_stationary_2317081728_1on_4off.txt", "Stationary Data Collection Heuston, 17/08/23", 1, 0, '17:28'),
                   ("heuston_stationary_2317081744_1on_4off.txt", "Stationary Data Collection Heuston, 17/08/23", 1, 0, '17:44'),
                   ("heuston_stationary_23170817501on_4off.txt", "Stationary Data Collection Heuston, 17/08/23", 1, 0, '17:50'),
                   ("heuston_walking_2317081802_1on_4off.txt", "Walking Data Collection Heuston, 17/08/23", 0, 1, '18:02'),
                   ("heuston_walking_2317081812_1on_4off.txt", "Walking Data Collection Heuston, 17/08/23", 0, 1, '18:12')]
    for (file_name, title, stat, walk, time_l) in file_details:
        main(filepath, file_name, title, stat, walk, 'Heuston', time_l)
    