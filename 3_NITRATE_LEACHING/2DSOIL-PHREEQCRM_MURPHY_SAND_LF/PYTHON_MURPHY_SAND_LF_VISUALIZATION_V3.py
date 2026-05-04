# Import necessary libraries

import numpy as NP
import pandas as PD
import matplotlib.pyplot as PLT
import matplotlib.patches as mpatches
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import os

# CLEAR SCREEN
os.system('cls')

# LOAD THE MASS BALANCE FILES

NR_MASS_BALANCE = PD.read_csv('MASS_BALANCE_PHREEQC_NR.txt')
ZK_MASS_BALANCE = PD.read_csv('MASS_BALANCE_PHREEQC_ZK.txt')
FK_MASS_BALANCE = PD.read_csv('MASS_BALANCE_PHREEQC_FK.txt')
CK_MASS_BALANCE = PD.read_csv('MASS_BALANCE_PHREEQC_CK.txt')
FK_ND_MASS_BALANCE = PD.read_csv('MASS_BALANCE_PHREEQC_FK_ND.txt')
CK_ND_MASS_BALANCE = PD.read_csv('MASS_BALANCE_PHREEQC_CK_ND.txt')
ZK_ND_MASS_BALANCE = PD.read_csv('MASS_BALANCE_PHREEQC_ZK_ND.txt')

# SET INDEX

print('MASS_BALANCE Columns:')
print(NR_MASS_BALANCE.columns)
print(ZK_MASS_BALANCE.columns)
print(FK_MASS_BALANCE.columns)
print(CK_MASS_BALANCE.columns)
print(FK_ND_MASS_BALANCE.columns)
print(CK_ND_MASS_BALANCE.columns)
print(ZK_ND_MASS_BALANCE.columns)

NR_MASS_BALANCE['TIME_COMMON'] = NR_MASS_BALANCE['TIME_2DSOIL']-NR_MASS_BALANCE['TIME_2DSOIL'].iloc[0]
ZK_MASS_BALANCE['TIME_COMMON'] = ZK_MASS_BALANCE['TIME_2DSOIL']-ZK_MASS_BALANCE['TIME_2DSOIL'].iloc[0]
FK_MASS_BALANCE['TIME_COMMON'] = FK_MASS_BALANCE['TIME_2DSOIL']-FK_MASS_BALANCE['TIME_2DSOIL'].iloc[0]
CK_MASS_BALANCE['TIME_COMMON'] = CK_MASS_BALANCE['TIME_2DSOIL']-CK_MASS_BALANCE['TIME_2DSOIL'].iloc[0]
FK_ND_MASS_BALANCE['TIME_COMMON'] = FK_ND_MASS_BALANCE['TIME_2DSOIL']-FK_ND_MASS_BALANCE['TIME_2DSOIL'].iloc[0]
CK_ND_MASS_BALANCE['TIME_COMMON'] = CK_ND_MASS_BALANCE['TIME_2DSOIL']-CK_ND_MASS_BALANCE['TIME_2DSOIL'].iloc[0]
ZK_ND_MASS_BALANCE['TIME_COMMON'] = ZK_ND_MASS_BALANCE['TIME_2DSOIL']-ZK_ND_MASS_BALANCE['TIME_2DSOIL'].iloc[0]

NR_MASS_BALANCE = NR_MASS_BALANCE.set_index('TIME_COMMON')
ZK_MASS_BALANCE = ZK_MASS_BALANCE.set_index('TIME_COMMON')
FK_MASS_BALANCE = FK_MASS_BALANCE.set_index('TIME_COMMON')
CK_MASS_BALANCE = CK_MASS_BALANCE.set_index('TIME_COMMON')
FK_ND_MASS_BALANCE = FK_ND_MASS_BALANCE.set_index('TIME_COMMON')
CK_ND_MASS_BALANCE = CK_ND_MASS_BALANCE.set_index('TIME_COMMON')
ZK_ND_MASS_BALANCE = ZK_ND_MASS_BALANCE.set_index('TIME_COMMON')

NR_MASS_BALANCE['TOTAL_NITRIFIED_N'] = NR_MASS_BALANCE['DELTA_NITRIFIED_N'].cumsum()
ZK_MASS_BALANCE['TOTAL_NITRIFIED_N'] = ZK_MASS_BALANCE['DELTA_NITRIFIED_N'].cumsum()
FK_MASS_BALANCE['TOTAL_NITRIFIED_N'] = FK_MASS_BALANCE['DELTA_NITRIFIED_N'].cumsum()
CK_MASS_BALANCE['TOTAL_NITRIFIED_N'] = CK_MASS_BALANCE['DELTA_NITRIFIED_N'].cumsum()
FK_ND_MASS_BALANCE['TOTAL_NITRIFIED_N'] = FK_ND_MASS_BALANCE['DELTA_NITRIFIED_N'].cumsum()
CK_ND_MASS_BALANCE['TOTAL_NITRIFIED_N'] = CK_ND_MASS_BALANCE['DELTA_NITRIFIED_N'].cumsum()
ZK_ND_MASS_BALANCE['TOTAL_NITRIFIED_N'] = ZK_ND_MASS_BALANCE['DELTA_NITRIFIED_N'].cumsum()

NR_MASS_BALANCE['TOTAL_DENITRIFIED_N'] = NR_MASS_BALANCE['DELTA_DENITRIFIED_N'].cumsum()
ZK_MASS_BALANCE['TOTAL_DENITRIFIED_N'] = ZK_MASS_BALANCE['DELTA_DENITRIFIED_N'].cumsum()
FK_MASS_BALANCE['TOTAL_DENITRIFIED_N'] = FK_MASS_BALANCE['DELTA_DENITRIFIED_N'].cumsum()
CK_MASS_BALANCE['TOTAL_DENITRIFIED_N'] = CK_MASS_BALANCE['DELTA_DENITRIFIED_N'].cumsum()
FK_ND_MASS_BALANCE['TOTAL_DENITRIFIED_N'] = FK_ND_MASS_BALANCE['DELTA_DENITRIFIED_N'].cumsum()
CK_ND_MASS_BALANCE['TOTAL_DENITRIFIED_N'] = CK_ND_MASS_BALANCE['DELTA_DENITRIFIED_N'].cumsum()
ZK_ND_MASS_BALANCE['TOTAL_DENITRIFIED_N'] = ZK_ND_MASS_BALANCE['DELTA_DENITRIFIED_N'].cumsum()

NR_MINERAL_N = NR_MASS_BALANCE['MINERAL_N']
ZK_MINERAL_N = ZK_MASS_BALANCE['MINERAL_N']
FK_MINERAL_N = FK_MASS_BALANCE['MINERAL_N']
CK_MINERAL_N = CK_MASS_BALANCE['MINERAL_N']
FK_ND_MINERAL_N = FK_ND_MASS_BALANCE['MINERAL_N']
CK_ND_MINERAL_N = CK_ND_MASS_BALANCE['MINERAL_N']
ZK_ND_MINERAL_N = ZK_ND_MASS_BALANCE['MINERAL_N']

print('')
print('MASS_BALANCE Columns PART 2')
print(NR_MASS_BALANCE.columns)
print(ZK_MASS_BALANCE.columns)
print(FK_MASS_BALANCE.columns)
print(CK_MASS_BALANCE.columns)
print(FK_ND_MASS_BALANCE.columns)
print(CK_ND_MASS_BALANCE.columns)
print(ZK_ND_MASS_BALANCE.columns)


# LOAD THE G05 file

NR_G05 = PD.read_csv('NR/DELHI_MURPHY.G05')
ZK_G05 = PD.read_csv('ZK/DELHI_MURPHY.G05')
FK_G05 = PD.read_csv('FK/DELHI_MURPHY.G05')
CK_G05 = PD.read_csv('CK/DELHI_MURPHY.G05')
FK_ND_G05 = PD.read_csv('FK_ND/DELHI_MURPHY.G05')
CK_ND_G05 = PD.read_csv('CK_ND/DELHI_MURPHY.G05')
ZK_ND_G05 = PD.read_csv('ZK_ND/DELHI_MURPHY.G05')
OBSERVED_DATA = PD.read_excel('OBSERVED_DATA.xlsx', sheet_name='OBSERVED_N_LEACHED_DATA')

print('NR_G05 Columns:', NR_G05.columns)
print('OBSERVED_DATA Columns:', OBSERVED_DATA.columns)
print(OBSERVED_DATA.head(10))

NR_G05['TIME_COMMON'] = NR_G05['       Date_time']-NR_G05['       Date_time'].iloc[0]
ZK_G05['TIME_COMMON'] = ZK_G05['       Date_time']-ZK_G05['       Date_time'].iloc[0]
FK_G05['TIME_COMMON'] = FK_G05['       Date_time']-FK_G05['       Date_time'].iloc[0]
CK_G05['TIME_COMMON'] = CK_G05['       Date_time']-CK_G05['       Date_time'].iloc[0]
FK_ND_G05['TIME_COMMON'] = FK_ND_G05['       Date_time']-FK_ND_G05['       Date_time'].iloc[0]
CK_ND_G05['TIME_COMMON'] = CK_ND_G05['       Date_time']-CK_ND_G05['       Date_time'].iloc[0]
ZK_ND_G05['TIME_COMMON'] = ZK_ND_G05['       Date_time']-ZK_ND_G05['       Date_time'].iloc[0]

NR_G05 = NR_G05.set_index('TIME_COMMON')
ZK_G05 = ZK_G05.set_index('TIME_COMMON')    
FK_G05 = FK_G05.set_index('TIME_COMMON')
CK_G05 = CK_G05.set_index('TIME_COMMON')
FK_ND_G05 = FK_ND_G05.set_index('TIME_COMMON')
CK_ND_G05 = CK_ND_G05.set_index('TIME_COMMON')
ZK_ND_G05 = ZK_ND_G05.set_index('TIME_COMMON')

NR_G05['TOTAL_N_LEACHED'] = NR_G05['        N_Leach'].mul(-1).cumsum()
ZK_G05['TOTAL_N_LEACHED'] = ZK_G05['        N_Leach'].mul(-1).cumsum()
FK_G05['TOTAL_N_LEACHED'] = FK_G05['        N_Leach'].mul(-1).cumsum()
CK_G05['TOTAL_N_LEACHED'] = CK_G05['        N_Leach'].mul(-1).cumsum()
FK_ND_G05['TOTAL_N_LEACHED'] = FK_ND_G05['        N_Leach'].mul(-1).cumsum()
CK_ND_G05['TOTAL_N_LEACHED'] = CK_ND_G05['        N_Leach'].mul(-1).cumsum()
ZK_ND_G05['TOTAL_N_LEACHED'] = ZK_ND_G05['        N_Leach'].mul(-1).cumsum()

NR_MERGED_MASS_BALANCE_G05 = NR_G05.join(NR_MASS_BALANCE, how='inner')
ZK_MERGED_MASS_BALANCE_G05 = ZK_G05.join(ZK_MASS_BALANCE, how='inner')
FK_MERGED_MASS_BALANCE_G05 = FK_G05.join(FK_MASS_BALANCE, how='inner')
CK_MERGED_MASS_BALANCE_G05 = CK_G05.join(CK_MASS_BALANCE, how='inner')
FK_ND_MERGED_MASS_BALANCE_G05 = FK_ND_G05.join(FK_ND_MASS_BALANCE, how='inner')
CK_ND_MERGED_MASS_BALANCE_G05 = CK_ND_G05.join(CK_ND_MASS_BALANCE, how='inner')
ZK_ND_MERGED_MASS_BALANCE_G05 = ZK_ND_G05.join(ZK_ND_MASS_BALANCE, how='inner')

print('MERGED_MASS_BALANCE_G05 Columns:')
print(NR_MERGED_MASS_BALANCE_G05.columns)
print(ZK_MERGED_MASS_BALANCE_G05.columns)
print(FK_MERGED_MASS_BALANCE_G05.columns)
print(CK_MERGED_MASS_BALANCE_G05.columns)
print(FK_ND_MERGED_MASS_BALANCE_G05.columns)
print(CK_ND_MERGED_MASS_BALANCE_G05.columns)
print(ZK_ND_MERGED_MASS_BALANCE_G05.columns)

print('HEAD FOR FK_ND_MERGED_MASS_BALANCE_G05')
print(FK_ND_MERGED_MASS_BALANCE_G05.head(10))
print(FK_ND_MERGED_MASS_BALANCE_G05.tail(10))

FIGURE, AXES = PLT.subplots(nrows=2, ncols=1, figsize=(21, 11), sharex=True)

AXES[0].scatter(OBSERVED_DATA['TIME_DAYS'], OBSERVED_DATA['NITRATE_LEACHED'], label='Observed', marker='o', s=50, color='black')
AXES[0].plot(NR_MERGED_MASS_BALANCE_G05.index, NR_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'], label='NR', linewidth=4, linestyle='-', color='#0072B2')
AXES[0].plot(ZK_MERGED_MASS_BALANCE_G05.index, ZK_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'], label='ZK', linewidth=4, linestyle='-', color='#E69F00')
AXES[0].plot(ZK_ND_MERGED_MASS_BALANCE_G05.index, ZK_ND_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'], label='ZK-ND', linewidth=4, linestyle='--', color='#E69F00')
AXES[0].plot(FK_MERGED_MASS_BALANCE_G05.index, FK_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'], label='FK', linewidth=4, linestyle='-', color='#009E73')
AXES[0].plot(FK_ND_MERGED_MASS_BALANCE_G05.index, FK_ND_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'], label='FK-ND', linewidth=4, linestyle='--', color='#009E73')
AXES[0].plot(CK_MERGED_MASS_BALANCE_G05.index, CK_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'], label='CK', linewidth=4, linestyle='-', color='#800000')
AXES[0].plot(CK_ND_MERGED_MASS_BALANCE_G05.index, CK_ND_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'], label='CK-ND', linewidth=4, linestyle='--', color='#800000')


#AXES = PLT.gca()
AXES[0].set_xlim([0, OBSERVED_DATA['TIME_DAYS'].max()+0.001])
AXES[0].set_ylim([0, 60])
AXES[0].set_xticks(NP.arange(0, AXES[0].get_xlim()[1], 4))
AXES[0].set_xlabel('Time (in days)', fontsize=24, fontfamily='Times New Roman')
AXES[0].set_ylabel('Cumulative NO$_3$-N Leached \n (kg/ha)', fontsize=24, fontfamily='Times New Roman')
AXES[0].set_title('(a)', fontsize=36, fontfamily='Times New Roman', loc='left', pad=20)
AXES[0].tick_params(axis='x', labelsize=24, labelrotation=0, labelcolor='black', labelfontfamily = 'Times New Roman' 
                    ,labelleft=True, labelright=False, labeltop=False, labelbottom=True, direction='in', 
                    length=6, width=1, colors='black', grid_color='black', grid_alpha=0.5)
AXES[0].tick_params(axis='y', labelsize=24, labelfontfamily = 'Times New Roman')
AXES[0].legend(loc='upper left', prop={'family': 'Times New Roman', 'size': 16})
AXES[0].set_yticks(NP.arange(0, 65, 10))
AXES[0].grid(True)

dates = OBSERVED_DATA['TIME_DAYS']
manual_labels = [
    ('1', 'WA#1'),
    ('9', 'WA#2'),
    ('23', 'WA#3')
                ]

for label_date, label_text in manual_labels:
    label_date = PD.to_numeric(label_date)
    closest_idx = (dates - label_date).abs().idxmin()
    AXES[0].annotate(label_text,
                 xy=(dates.iloc[closest_idx], 55),
                 xytext=(0, 0),
                 textcoords='offset points',
                 fontsize=20,
                 bbox=dict(boxstyle='round,pad=0.1', edgecolor='#800000', facecolor='white', alpha=1),label='Water Application', ha = 'center')
    AXES[0].legend()

# ADD THE LEGEND WITH THE CUSTOM PATCH FOR GROWTH STAGES
manual_label_patch = mpatches.Patch(
    edgecolor='#800000',  # maroon
    facecolor='white',
    alpha=0.8,
    linewidth=2,
    label='Water Application'
)

AXES[0].legend(title = '$Legend$', title_fontsize=16,
               handles=AXES[0].get_legend_handles_labels()[0] + [manual_label_patch], 
               loc='lower right', ncol = 5, framealpha=1, 
               frameon=True, edgecolor='black', prop={'family': 'Times New Roman', 'size': 16})

print('Legend Labels')
print(AXES[0].get_legend_handles_labels())



#FIGURE = PLT.figure(figsize=(12, 6))
AXES[1].plot(NR_MERGED_MASS_BALANCE_G05.index, NR_MERGED_MASS_BALANCE_G05['MINERAL_N'], label='NR', linewidth=4, linestyle='-', color='#0072B2')
AXES[1].plot(ZK_MERGED_MASS_BALANCE_G05.index, ZK_MERGED_MASS_BALANCE_G05['MINERAL_N'], label='ZK', linewidth=4, linestyle='-', color='#E69F00')
AXES[1].plot(ZK_ND_MERGED_MASS_BALANCE_G05.index, ZK_ND_MERGED_MASS_BALANCE_G05['MINERAL_N'], label='ZK-ND', linewidth=4, linestyle='--', color='#E69F00')
AXES[1].plot(FK_MERGED_MASS_BALANCE_G05.index, FK_MERGED_MASS_BALANCE_G05['MINERAL_N'], label='FK', linewidth=4, linestyle='-', color='#009E73')
AXES[1].plot(FK_ND_MERGED_MASS_BALANCE_G05.index, FK_ND_MERGED_MASS_BALANCE_G05['MINERAL_N'], label='FK-ND', linewidth=4, linestyle='--', color='#009E73')
AXES[1].plot(CK_MERGED_MASS_BALANCE_G05.index, CK_MERGED_MASS_BALANCE_G05['MINERAL_N'], label='CK', linewidth=4, linestyle='-', color='#800000')
AXES[1].plot(CK_ND_MERGED_MASS_BALANCE_G05.index, CK_ND_MERGED_MASS_BALANCE_G05['MINERAL_N'], label='CK-ND', linewidth=4, linestyle='--', color='#800000')   

#AXES = PLT.gca()
AXES[1].set_ylim([0, 30])
AXES[1].set_xlabel('Time (in days)', fontsize=24, fontfamily='Times New Roman')
AXES[1].set_ylabel('Soil NO$_3$-N \n (kg/ha)', fontsize=24, fontfamily='Times New Roman')
AXES[1].set_title('(b)', fontsize=36, fontfamily='Times New Roman', loc='left', pad=20)
AXES[1].tick_params(labelsize=24, labelfontfamily='Times New Roman')
AXES[1].set_yticks(NP.arange(0, 35, 10))
#AXES[1].legend(loc='upper right', prop={'family': 'Times New Roman', 'size': 16})
AXES[1].grid(True)

print('Size of CK_MERGED_MASS_BALANCE_G05 MINERAL_N:')
print(len(CK_MERGED_MASS_BALANCE_G05['MINERAL_N']))
PLT.subplots_adjust(hspace=0.6)
PLT.tight_layout()
PLT.show()



FIGURE = PLT.figure(figsize=(12, 6))
PLT.plot(ZK_MERGED_MASS_BALANCE_G05.index, ZK_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'], label='ZK', linewidth=2, color='orange')
PLT.plot(FK_MERGED_MASS_BALANCE_G05.index, FK_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'], label='FK', linewidth=2, color='green')
PLT.plot(CK_MERGED_MASS_BALANCE_G05.index, CK_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'], label='CK', linewidth=2, color='red')
PLT.plot(FK_ND_MERGED_MASS_BALANCE_G05.index, FK_ND_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'], label='FK-ND', linewidth=2, color='purple')
PLT.plot(CK_ND_MERGED_MASS_BALANCE_G05.index, CK_ND_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'], label='CK-ND', linewidth=2, color='brown')
PLT.plot(ZK_ND_MERGED_MASS_BALANCE_G05.index, ZK_ND_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'], label='ZK-ND', linewidth=2, color='pink')
AXES = PLT.gca()
AXES.set_xlabel('Date', fontsize=20, fontfamily='Times New Roman')
AXES.set_ylabel('NO$_3$-N (kg/ha)', fontsize=20, fontfamily='Times New Roman')
#AXES.set_title('Case wise time series of denitrified NO$_3$-N (in Kg/Ha)', fontsize=20, fontfamily='Times New Roman')
AXES.tick_params(labelsize=16, labelfontfamily='Times New Roman')
AXES.legend(loc='upper left', prop={'family': 'Times New Roman', 'size': 16})

FIGURE = PLT.figure(figsize=(12, 6))
PLT.plot(ZK_MERGED_MASS_BALANCE_G05.index, ZK_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'], label='ZK', linewidth=2, linestyle = '-.', color='orange')
PLT.plot(FK_MERGED_MASS_BALANCE_G05.index, FK_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'], label='FK', linewidth=2, linestyle = '-.', color='green')
PLT.plot(CK_MERGED_MASS_BALANCE_G05.index, CK_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'], label='CK', linewidth=2, linestyle = '-.', color='red')
PLT.plot(FK_ND_MERGED_MASS_BALANCE_G05.index, FK_ND_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'], label='FK-ND', linewidth=2, linestyle = '-.', color='purple')
PLT.plot(CK_ND_MERGED_MASS_BALANCE_G05.index, CK_ND_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'], label='CK-ND', linewidth=2, linestyle = '-.', color='brown')
PLT.plot(ZK_ND_MERGED_MASS_BALANCE_G05.index, ZK_ND_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'], label='ZK-ND', linewidth=2, linestyle = '-.', color='pink')
AXES = PLT.gca()
AXES.set_xlabel('Date', fontsize=20, fontfamily='Times New Roman')
AXES.set_ylabel('NO$_3$-N (kg/ha)', fontsize=20, fontfamily='Times New Roman')
#AXES.set_title('Case wise time series of nitrified NO$_3$-N (in Kg/Ha)', fontsize=20, fontfamily='Times New Roman')
AXES.tick_params(labelsize=16, labelfontfamily='Times New Roman')
AXES.legend(loc='upper left', prop={'family': 'Times New Roman', 'size': 16})

print(len(NR_G05['        N_Leach']))
print(len(NR_MASS_BALANCE['TOTAL_DENITRIFIED_N']))

print('Leached N at the end:')
print(ZK_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'].iloc[-1], FK_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'].iloc[-1], CK_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'].iloc[-1])
print('Mineral N at the end:')
print(ZK_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[-1], FK_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[-1], CK_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[-1])
print('Denitrified N at the end:')
print(ZK_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'].iloc[-1], FK_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'].iloc[-1], CK_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'].iloc[-1])
print('Nitrified N at the end:')
print(ZK_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'].iloc[-1], FK_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'].iloc[-1], CK_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'].iloc[-1])
print('FK_ND N at the end:')
print(FK_ND_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'].iloc[-1], FK_ND_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[-1], FK_ND_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'].iloc[-1], FK_ND_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'].iloc[-1])
print('CK_ND N at the end:')
print(CK_ND_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'].iloc[-1], CK_ND_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[-1], CK_ND_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'].iloc[-1], CK_ND_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'].iloc[-1])
print('ZK_ND N at the end:')
print(ZK_ND_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'].iloc[-1], ZK_ND_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[-1], ZK_ND_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'].iloc[-1], ZK_ND_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'].iloc[-1])


########################################################################################
##########        FIGURE 2: BAR CHARTS FOR LEACHED AND RESIDUAL NITRATE       ##########
########################################################################################

FIGURE, AXES = PLT.subplots(nrows=2, ncols=1, figsize=(21, 11), sharex=True)
# Stacked bar chart for leached and residual values for each scenario

OBSERVED_DATA_RESIDUAL = 11.31

# Add CONDITIONAL_KINETICS_NO_DENITRIFICATION_LEACHED and RESIDUAL to the chart
scenario_labels = [
    'NR', 'ZK', 'ZK-ND', 'FK', 'FK-ND', 'CK', 'CK-ND', 'Observed'
                  ]
leached_values = [
    NR_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'].iloc[-1],
    ZK_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'].iloc[-1],
    ZK_ND_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'].iloc[-1],
    FK_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'].iloc[-1],
    FK_ND_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'].iloc[-1],
    CK_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'].iloc[-1],
    CK_ND_MERGED_MASS_BALANCE_G05['TOTAL_N_LEACHED'].iloc[-1],
    OBSERVED_DATA['NITRATE_LEACHED'].iloc[-1]
]

residual_values = [
    NR_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[-1],
    ZK_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[-1],
    ZK_ND_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[-1],
    FK_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[-1],
    FK_ND_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[-1],
    CK_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[-1],
    CK_ND_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[-1],
    OBSERVED_DATA_RESIDUAL
]

bar_width = 0.6
AXES[0].bar(scenario_labels, leached_values, bar_width, label='Leached NO$_3$-N', color='#F28C38')
AXES[0].bar(scenario_labels, residual_values, bar_width, bottom=leached_values, label='Soil NO$_3$-N', color='#4C78A8')
AXES[0].set_ylabel('NO$_3$-N (kg/ha)', fontsize=24, fontfamily='Times New Roman')
#AXES[0].set_xlabel('Type of kinetics', fontsize=24, fontfamily='Times New Roman')
AXES[0].set_title('(a)', fontsize=32, fontfamily='Times New Roman', loc = 'left')
AXES[0].set_ylim([0, 90])
AXES[0].set_xticks(range(len(scenario_labels)))
AXES[0].set_xticklabels(scenario_labels, ha='center', fontsize=18, fontfamily='Times New Roman')
AXES[0].tick_params(labelsize=24, labelfontfamily='Times New Roman')
AXES[0].tick_params(axis='x', labelsize=24, labelrotation=0, labelcolor='black', labelfontfamily = 'Times New Roman' 
                    ,labelleft=True, labelright=False, labeltop=False, labelbottom=True, direction='out', 
                    length=6, width=1, colors='black', grid_color='black', grid_alpha=0.5)
AXES[0].legend(loc='upper right', prop={'family': 'Times New Roman', 'size': 24})
#PLT.tight_layout()


#FIGURE = PLT.figure(figsize=(12, 6))
# Stacked bar chart for leached and residual values for each scenario

OBSERVED_DATA_MINERALIZED = 21.19
OBSERVED_DATA_DENITRIFIED = 0.71

# Add CONDITIONAL_KINETICS_NO_DENITRIFICATION_LEACHED and RESIDUAL to the chart
scenario_labels = [
    'NR', 'ZK', 'ZK-ND', 'FK', 'FK-ND', 'CK', 'CK-ND', 'Observed'
                  ]

leached_values = [
    NR_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'].iloc[-1],#-NR_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[0],
    ZK_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'].iloc[-1],#-ZK_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[0],
    ZK_ND_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'].iloc[-1],#-ZK_ND_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[0],
    FK_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'].iloc[-1],#-FK_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[0],
    FK_ND_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'].iloc[-1],#-FK_ND_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[0],
    CK_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'].iloc[-1],#-CK_MERGED_MASS_BALANCE_G05['MINERAL_N'].iloc[0],
    CK_ND_MERGED_MASS_BALANCE_G05['TOTAL_NITRIFIED_N'].iloc[-1],#-CK_ND_MERGED_MASS_BALANCE_G05
    OBSERVED_DATA_MINERALIZED 
]

residual_values = [
    NR_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'].iloc[-1],
    ZK_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'].iloc[-1],
    ZK_ND_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'].iloc[-1],
    FK_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'].iloc[-1],
    FK_ND_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'].iloc[-1],
    CK_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'].iloc[-1],
    CK_ND_MERGED_MASS_BALANCE_G05['TOTAL_DENITRIFIED_N'].iloc[-1],
    OBSERVED_DATA_DENITRIFIED

]

x = NP.arange(len(scenario_labels))
width = 0.35

bars1 = AXES[1].bar(x - width/2, leached_values, width, label='Total nitrification', color='#008080')
bars2 = AXES[1].bar(x + width/2, residual_values, width, label='Total denitrification', color='#E69F00')
AXES[1].set_ylabel('NO$_3$-N (kg/ha)', fontsize=24, fontfamily='Times New Roman')
#AXES[1].set_xlabel('Type of kinetics', fontsize=24, fontfamily='Times New Roman')
AXES[1].set_title('(b)',fontsize=32, fontfamily='Times New Roman', loc = 'left')
AXES[1].set_ylim([0, 60])
AXES[1].set_xticks(x)
AXES[1].set_xticklabels(scenario_labels, fontsize=14, fontfamily='Times New Roman')
AXES[1].tick_params(labelsize=24, labelfontfamily='Times New Roman')
AXES[1].tick_params(axis='x', labelsize=24, labelrotation=0, labelcolor='black', labelfontfamily = 'Times New Roman' 
                    ,labelleft=True, labelright=False, labeltop=False, labelbottom=True, direction='out', 
                    length=6, width=1, colors='black', grid_color='black', grid_alpha=0.5)
AXES[1].legend(loc='upper right', prop={'family': 'Times New Roman', 'size': 24})
PLT.tight_layout()

#PLT.show()



# PLOTTING RMSE FOR DIFFERENT CASES
RMSE_DATA = PD.read_excel('COMPARISON_OF_RESULTS.xlsx', sheet_name='RMSE')
print('RMSE_DATA Columns:', RMSE_DATA.columns)

NR_RMSE = RMSE_DATA['NR'].iloc[-1]
ZK_RMSE = RMSE_DATA['ZK'].iloc[-1]
ZK_ND_RMSE = RMSE_DATA['ZK_ND'].iloc[-1]
FK_RMSE = RMSE_DATA['FK'].iloc[-1]
FK_ND_RMSE = RMSE_DATA['FK_ND'].iloc[-1]
CK_RMSE = RMSE_DATA['CK'].iloc[-1]
CK_ND_RMSE = RMSE_DATA['CK_ND'].iloc[-1]

print('RMSE Values:')
print(f'NR_RMSE: {NR_RMSE}')
print(f'ZK_RMSE: {ZK_RMSE}')
print(f'ZK_ND_RMSE: {ZK_ND_RMSE}')
print(f'FK_RMSE: {FK_RMSE}')
print(f'FK_ND_RMSE: {FK_ND_RMSE}')
print(f'CK_RMSE: {CK_RMSE}')
print(f'CK_ND_RMSE: {CK_ND_RMSE}')

# CREATE HORIZONTAL BAR CHART FOR RMSE VALUES
rmse_scenario_labels = ['NR', 'ZK', 'ZK-ND', 'FK', 'FK-ND', 'CK', 'CK-ND']
rmse_values = [NR_RMSE, ZK_RMSE, ZK_ND_RMSE, FK_RMSE, FK_ND_RMSE, CK_RMSE, CK_ND_RMSE]

# Define colors - same as used in the line plots for consistency
rmse_colors = ['#0072B2', '#E69F00', '#009E73', '#800000', '#E69F00', '#009E73', '#800000']
rmse_alphas = [1.0, 1.0, 1.0, 1.0, 0.7, 0.7, 0.7]  # Make ND scenarios slightly transparent
FIGURE_RMSE_H = PLT.figure(figsize=(10, 8))

# Create horizontal bar chart by plotting each bar individually to handle different alphas
bars_h = []
for i, (label, value, color, alpha) in enumerate(zip(rmse_scenario_labels, rmse_values, rmse_colors, rmse_alphas)):
    bar = PLT.barh(i, value, 
                   color=color, 
                   alpha=alpha,
                   edgecolor='black',
                   linewidth=1.2,
                   height=0.6)
    bars_h.extend(bar)

# Set the y-axis labels
PLT.yticks(range(len(rmse_scenario_labels)), rmse_scenario_labels)

# Customize the horizontal plot
AXES_RMSE_H = PLT.gca()
AXES_RMSE_H.set_ylabel('Types of kinetics', fontsize=24, fontfamily='Times New Roman')
AXES_RMSE_H.set_xlabel('RMSE (NO3-N in kg/ha)', fontsize=24, fontfamily='Times New Roman')
#AXES_RMSE_H.set_title('RMSE Comparison Across Different Simulation Scenarios', fontsize=18, fontfamily='Times New Roman', pad=20)

# Customize ticks and labels
PLT.xticks(fontsize=16, fontfamily='Times New Roman')
PLT.yticks(fontsize=16, fontfamily='Times New Roman')

# Add value labels at the end of each bar
for i, (bar, value) in enumerate(zip(bars_h, rmse_values)):
    width = bar.get_width()
    PLT.text(width + max(rmse_values)*0.01, bar.get_y() + bar.get_height()/2.,
             f'{value:.2f}',
             ha='left', va='center', fontsize=14, fontfamily='Times New Roman', fontweight='bold')

# Add grid for better readability
PLT.grid(True, axis='x', alpha=0.3, linestyle='--')
AXES_RMSE_H.set_axisbelow(True)

# Set x-axis limits to provide some space after the longest bar
PLT.xlim(0, max(rmse_values) * 1.2)

PLT.tight_layout()

# RMSE RANKING TABLE
print('\n' + '='*60)
print('RMSE RANKING (Best to Worst Performance)')
print('='*60)

# Create a list of tuples (scenario, rmse) and sort by RMSE
rmse_ranking = list(zip(rmse_scenario_labels, rmse_values))
rmse_ranking.sort(key=lambda x: x[1])  # Sort by RMSE value (ascending)

print(f"{'Rank':<6} {'Scenario':<12} {'RMSE':<10} {'Performance':<15}")
print('-' * 50)

for rank, (scenario, rmse) in enumerate(rmse_ranking, 1):
    if rank == 1:
        performance = "Best"
    elif rank <= 3:
        performance = "Good"
    elif rank <= 5:
        performance = "Average"
    else:
        performance = "Poor"
    
    print(f"{rank:<6} {scenario:<12} {rmse:<10.2f} {performance:<15}")

print('\n' + '='*60)

# Show both plots
PLT.show()
OBSERVED_RMSE = 0.0


