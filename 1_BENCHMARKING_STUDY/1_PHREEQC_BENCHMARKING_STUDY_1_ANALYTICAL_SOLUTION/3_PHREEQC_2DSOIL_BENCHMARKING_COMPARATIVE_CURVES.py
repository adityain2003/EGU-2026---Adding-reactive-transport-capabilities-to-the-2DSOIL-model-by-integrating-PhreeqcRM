import numpy as NP
import pandas as pd
import matplotlib.pyplot as PLT
from matplotlib.ticker import MultipleLocator

# Set Times New Roman font for all text
PLT.rcParams['font.family'] = 'Times New Roman'

DATAFRAME_CASE_1 = pd.read_excel('RESULTS_BENCHMARKING_ANALYTICAL_SOLUTION_750CM.xlsx', sheet_name='CASE_1')
DATAFRAME_CASE_2 = pd.read_excel('RESULTS_BENCHMARKING_ANALYTICAL_SOLUTION_750CM.xlsx', sheet_name='CASE_2')
DATAFRAME_CASE_3 = pd.read_excel('RESULTS_BENCHMARKING_ANALYTICAL_SOLUTION_750CM.xlsx', sheet_name='CASE_3')


# Select rows where DAY == 1

# Figure aspect ratio options:
# Current: (10, 10) = 1:1 square ratio
# Landscape: (15, 10) = 3:2 landscape ratio  
# Wide: (18, 6) = 3:1 wide ratio
# Portrait: (8, 12) = 2:3 portrait ratio

FIGURE,AXES = PLT.subplots(nrows=1, ncols=3, figsize=(19.2, 10.8))  # 15:8 landscape for 3 subplots
#PLT.subplots_adjust(top=0.90, bottom=0.125)
AX_1 = AXES[0]
AX_2 = AXES[1]
AX_3 = AXES[2]


###############################################################
#############            CASE-1          ######################
###############################################################
DATAFRAME_CASE_1_DAY_0 = DATAFRAME_CASE_1[DATAFRAME_CASE_1['DAY'] == 0]
DATAFRAME_CASE_1_DAY_1 = DATAFRAME_CASE_1[DATAFRAME_CASE_1['DAY'] == 1]
DATAFRAME_CASE_1_DAY_2 = DATAFRAME_CASE_1[DATAFRAME_CASE_1['DAY'] == 2]
DATAFRAME_CASE_1_DAY_3 = DATAFRAME_CASE_1[DATAFRAME_CASE_1['DAY'] == 3]

# Plot Y vs CONC_RATIO_SIMULATED with a solid line
AX_1.plot(DATAFRAME_CASE_1_DAY_0['CONC_RATIO_SIMULATED'], DATAFRAME_CASE_1_DAY_0['Y'],zorder=1, linestyle='--', color='red', label='Simulated (t = 0 Day)')
AX_1.plot(DATAFRAME_CASE_1_DAY_1['CONC_RATIO_SIMULATED'], DATAFRAME_CASE_1_DAY_1['Y'],zorder=1, linestyle='--', color='blue', label='Simulated (t = 1 Day)')
AX_1.plot(DATAFRAME_CASE_1_DAY_2['CONC_RATIO_SIMULATED'], DATAFRAME_CASE_1_DAY_2['Y'],zorder=1, linestyle='--', color='green', label='Simulated (t = 2 Day)')
AX_1.plot(DATAFRAME_CASE_1_DAY_3['CONC_RATIO_SIMULATED'], DATAFRAME_CASE_1_DAY_3['Y'],zorder=1, linestyle='--', color='orange', label='Simulated (t = 3 Day)')
# Add analytical data as scatter
AX_1.scatter(DATAFRAME_CASE_1['CONC_RATIO_ANALYTICAL_DAY_0'], DATAFRAME_CASE_1['Y_ANALYTICAL_DAY_0'],zorder=2, color='red',edgecolor='black', s=20, label='Analytical (t = 0 Day)')
AX_1.scatter(DATAFRAME_CASE_1['CONC_RATIO_ANALYTICAL_DAY_1'], DATAFRAME_CASE_1['Y_ANALYTICAL_DAY_1'],zorder=2, color='blue',edgecolor='black', s=20, label='Analytical (t = 1 Day)')
AX_1.scatter(DATAFRAME_CASE_1['CONC_RATIO_ANALYTICAL_DAY_2'], DATAFRAME_CASE_1['Y_ANALYTICAL_DAY_2'],zorder=2, color='green',edgecolor='black', s=20, label='Analytical (t = 2 Day)')
AX_1.scatter(DATAFRAME_CASE_1['CONC_RATIO_ANALYTICAL_DAY_3'], DATAFRAME_CASE_1['Y_ANALYTICAL_DAY_3'],zorder=2, color='orange',edgecolor='black', s=20, label='Analytical (t = 3 Day)')
AX_1.set_xlabel('Concentration (mols/l)',fontsize=20, labelpad=10)
AX_1.set_xlim(-0.001, 1.0)
AX_1.set_ylabel('Height above the column base (cm)',fontsize=20)
AX_1.set_ylim(bottom=0, top=750)
AX_1.set_yticks([0, 100, 200, 300, 400, 500, 600, 700, 750])
AX_1.set_clip_on(True)
AX_1.tick_params(axis='both', labelsize=20, pad=10)
AX_1.set_title('(a)',fontsize=24)
AX_1.grid(True)
AX_1.legend(fontsize = 18, borderaxespad=0.02, frameon=True, framealpha=1.0, markerscale=2.0)

###############################################################
#############            CASE-2          ######################
###############################################################
DATAFRAME_CASE_2_DAY_0 = DATAFRAME_CASE_2[DATAFRAME_CASE_2['DAY'] == 0]
DATAFRAME_CASE_2_DAY_1 = DATAFRAME_CASE_2[DATAFRAME_CASE_2['DAY'] == 1]
DATAFRAME_CASE_2_DAY_2 = DATAFRAME_CASE_2[DATAFRAME_CASE_2['DAY'] == 2]
DATAFRAME_CASE_2_DAY_3 = DATAFRAME_CASE_2[DATAFRAME_CASE_2['DAY'] == 3]

AX_2.plot(DATAFRAME_CASE_2_DAY_0['CONC_RATIO_SIMULATED'], DATAFRAME_CASE_2_DAY_0['Y'],zorder=1, linestyle='--', color='red', label='Simulated (t = 0 Day)')
AX_2.plot(DATAFRAME_CASE_2_DAY_1['CONC_RATIO_SIMULATED'], DATAFRAME_CASE_2_DAY_1['Y'],zorder=1, linestyle='--', color='blue', label='Simulated (t = 1 Day)')
AX_2.plot(DATAFRAME_CASE_2_DAY_2['CONC_RATIO_SIMULATED'], DATAFRAME_CASE_2_DAY_2['Y'],zorder=1, linestyle='--', color='green', label='Simulated (t = 2 Day)')
AX_2.plot(DATAFRAME_CASE_2_DAY_3['CONC_RATIO_SIMULATED'], DATAFRAME_CASE_2_DAY_3['Y'],zorder=1, linestyle='--', color='orange', label='Simulated (t = 3 Day)')
# Add analytical data as scatter
AX_2.scatter(DATAFRAME_CASE_2['CONC_RATIO_ANALYTICAL_DAY_0'], DATAFRAME_CASE_2['Y_ANALYTICAL_DAY_0'],zorder=2, color='red',edgecolor='black', s=20, label='Analytical (t = 0 Day)')
AX_2.scatter(DATAFRAME_CASE_2['CONC_RATIO_ANALYTICAL_DAY_1'], DATAFRAME_CASE_2['Y_ANALYTICAL_DAY_1'],zorder=2, color='blue',edgecolor='black', s=20, label='Analytical (t = 1 Day)')
AX_2.scatter(DATAFRAME_CASE_2['CONC_RATIO_ANALYTICAL_DAY_2'], DATAFRAME_CASE_2['Y_ANALYTICAL_DAY_2'],zorder=2, color='green',edgecolor='black', s=20, label='Analytical (t = 2 Day)')
AX_2.scatter(DATAFRAME_CASE_2['CONC_RATIO_ANALYTICAL_DAY_3'], DATAFRAME_CASE_2['Y_ANALYTICAL_DAY_3'],zorder=2, color='orange',edgecolor='black', s=20, label='Analytical (t = 3 Day)')
AX_2.set_xlabel('Concentration (mols/l)',fontsize=20, labelpad=10)
AX_2.set_xlim(-0.001, 1.0)
AX_2.set_ylim(bottom=0, top=750)
#AX_2.set_yticks([0, 100, 200, 300, 400, 500, 600, 700, 750])
AX_2.set_clip_on(True)
AX_2.tick_params(axis='x', labelsize=20, pad=10)
# Remove y-axis tick labels, keep only x-axis labels
AX_2.tick_params(axis='y', labelleft=False, direction='in')
AX_2.set_title('(b)',fontsize=24)
AX_2.grid(True)
#AX_2.legend(fontsize = 16)

###############################################################
#############            CASE-3          ######################
###############################################################
DATAFRAME_CASE_3_DAY_0 = DATAFRAME_CASE_3[DATAFRAME_CASE_3['DAY'] == 0]
DATAFRAME_CASE_3_DAY_1 = DATAFRAME_CASE_3[DATAFRAME_CASE_3['DAY'] == 1]
DATAFRAME_CASE_3_DAY_2 = DATAFRAME_CASE_3[DATAFRAME_CASE_3['DAY'] == 2]
DATAFRAME_CASE_3_DAY_3 = DATAFRAME_CASE_3[DATAFRAME_CASE_3['DAY'] == 3]

AX_3.plot(DATAFRAME_CASE_3_DAY_0['CONC_RATIO_SIMULATED'], DATAFRAME_CASE_3_DAY_0['Y'],zorder=1, linestyle='--', color='red', label='Simulated (t = 0 Day)')
AX_3.plot(DATAFRAME_CASE_3_DAY_1['CONC_RATIO_SIMULATED'], DATAFRAME_CASE_3_DAY_1['Y'],zorder=1, linestyle='--', color='blue', label='Simulated (t = 1 Day)')
AX_3.plot(DATAFRAME_CASE_3_DAY_2['CONC_RATIO_SIMULATED'], DATAFRAME_CASE_3_DAY_2['Y'],zorder=1, linestyle='--', color='green', label='Simulated (t = 2 Day)')
AX_3.plot(DATAFRAME_CASE_3_DAY_3['CONC_RATIO_SIMULATED'], DATAFRAME_CASE_3_DAY_3['Y'],zorder=1, linestyle='--', color='orange', label='Simulated (t = 3 Day)')
# Add analytical data as scatter
AX_3.scatter(DATAFRAME_CASE_3['CONC_RATIO_ANALYTICAL_DAY_0'], DATAFRAME_CASE_3['Y_ANALYTICAL_DAY_0'],zorder=2, color='red',edgecolor='black', s=20, label='Analytical (t = 0 Day)')
AX_3.scatter(DATAFRAME_CASE_3['CONC_RATIO_ANALYTICAL_DAY_1'], DATAFRAME_CASE_3['Y_ANALYTICAL_DAY_1'],zorder=2, color='blue',edgecolor='black', s=20, label='Analytical (t = 1 Day)')
AX_3.scatter(DATAFRAME_CASE_3['CONC_RATIO_ANALYTICAL_DAY_2'], DATAFRAME_CASE_3['Y_ANALYTICAL_DAY_2'],zorder=2, color='green',edgecolor='black', s=20, label='Analytical (t = 2 Day)')
AX_3.scatter(DATAFRAME_CASE_3['CONC_RATIO_ANALYTICAL_DAY_3'], DATAFRAME_CASE_3['Y_ANALYTICAL_DAY_3'],zorder=2, color='orange',edgecolor='black', s=20, label='Analytical (t = 3 Day)')
AX_3.set_xlabel('Concentration (mols/l)',fontsize=20, labelpad=10)
AX_3.set_xlim(-0.001, 1.0)
AX_3.set_ylim(bottom=0, top=750)
AX_3.set_yticks([0, 100, 200, 300, 400, 500, 600, 700, 750])
AX_3.set_clip_on(True)
AX_3.tick_params(axis='x', labelsize=20, pad=10)
AX_3.tick_params(axis='y', direction='in', labelleft=False, labelright=True, labelsize=20, pad=10)
AX_3.tick_params(right=True, direction='out')
AX_3.set_title('(c)',fontsize=24)
AX_3.grid(True)
#AX_3.legend(fontsize = 16)



# Export high-DPI images in multiple formats
# Method 1: High DPI PNG (300 DPI - publication quality)
PLT.savefig('PHREEQC_Benchmarking_Curves_300DPI.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none', format='png')

# Method 2: Very high DPI PNG (600 DPI - excellent quality)
PLT.savefig('PHREEQC_Benchmarking_Curves_600DPI.png', dpi=600, format='png')

# Method 3: Vector format (PDF - scalable, perfect for publications)
PLT.savefig('PHREEQC_Benchmarking_Curves_Vector.pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none', format='pdf')

# Method 4: Vector format (SVG - scalable, good for web)
PLT.savefig('PHREEQC_Benchmarking_Curves_Vector.svg', bbox_inches='tight',
            facecolor='white', edgecolor='none', format='svg')

# Method 5: EPS format (Encapsulated PostScript - good for LaTeX)
PLT.savefig('PHREEQC_Benchmarking_Curves_Vector.eps', bbox_inches='tight',
            facecolor='white', edgecolor='none', format='eps')


PLT.show()
