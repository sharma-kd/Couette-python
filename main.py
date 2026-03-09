#%% main.py
import os
import importlib
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import props_MD, props_DSMC, plots
from props_DSMC import load_DSMC
from props_MD import load_MD
from props_NCCR import load_NSF_NCCR
from plots import plot_y, plot_Mkn, plot_Mkn1, str_cons_fig

# Reload modules to reflect any changes
importlib.reload(props_MD)
importlib.reload(props_DSMC)
importlib.reload(plots)

# from rename import rename_files
# rename_files(r'E:\Works\Couette\16_09_2025_paper_try_2\MD_DSMC_comparision\py_post_processing\data\MD')
# from plots_vs_y import plot_mkn
# from plots_vs_y import plot_single

#%% 
# work/plot directories
md_dir = Path(__file__).parent.parent / "data"/ "MD-01-03-2026"
dsmc_dir = Path(__file__).parent.parent / "data"/ "DSMC"
nccr_dir = Path(__file__).parent.parent / "data"/ "NCCR"
os.makedirs('plots', exist_ok=True)
os.makedirs('plots/vs_y', exist_ok=True)
os.makedirs('plots/M_var', exist_ok=True)
os.makedirs('plots/Kn_var', exist_ok=True)
os.makedirs('plots/vs_y/pickles', exist_ok=True)
os.makedirs('plots/M_var/pickles', exist_ok=True)
os.makedirs('plots/Kn_var/pickles', exist_ok=True)

#%% load data
MD_channel_width = 500E-10               # channel width in m
MD_bin_area = 74.48*27.44*1E-20         # bin area in m^2
MD_dia = 3.1E-10                        # argon diameter in m
md_data = load_MD(MD_channel_width, MD_bin_area, MD_dia,md_dir)
print("MD data loaded successfully.")
dsmc_data = load_DSMC(dsmc_dir)
print("DSMC data loaded successfully.")
nccr_data, nsf_data = load_NSF_NCCR(nccr_dir)
print("NSF and NCCR data loaded successfully.")

# print(dsmc_data.keys())
# print(md_data.keys())

#%%
# change MD keys from (mach, num_atoms) to (mach, kn)
md_data_kn = {}
for (mach, num_atoms) in md_data.keys():
    kn = md_data[(mach, num_atoms)]['kn']
    md_data_kn[(mach, kn)] = md_data[(mach, num_atoms)]
md_data = md_data_kn
print("MD data keys changed to include Knudsen number.")
# print(md_data.keys())

# %%
# common mapping keys for MD and DSMC
v_map = {
    'vx': ('Vx', 'u'),
    'vy': ('Vy', 'v'),
    'pi_xx': ('Pixx', 'Pixx'),
    'pi_yy': ('Piyy', 'Piyy'),
    'pi_xy': ('Sxy', 'Pixy'),
    'p' : ('Pressure', 'Press'),
    'T' : ('Temp', 'T'),
    'qx' : ('Qx', 'qx'),
    'qy' : ('Qy', 'qy'),
    'pi_zz': ('Pizz', 'Pizz'),
    'qz' : ('Qz', 'qz'),
    'delta' : ('delta', 'delta')}

#%% plots vs M/Kn
# plot_Mkn(md_data, dsmc_data, var_vs_Mkn, dimflag, vflag, ylabel)
mkn_vars = list(v_map.keys())[2:9]
# print(mkn_vars)
for var in mkn_vars:
    for dimflag in ['dim', 'nd']:
        
        for vflag in ['M','Kn']:
            plot_Mkn(md_data, dsmc_data, nccr_data, v_map[var], dimflag, vflag, f'{var}')

#%%
# # plots vs y
# # plot_y(md_data, dsmc_data, var_vs_y, dimflag, ylabel, title):
# print(v_map.keys())

md_keys = list(md_data.keys())
dsmc_keys = list(dsmc_data.keys())
for i in range(0,len(md_keys),3):
    md_plot_keys = md_keys [i:i+3]                  # 1 mach 3 kn each time
    target_machs = {key[0] for key in md_plot_keys}
    dsmc_plot_keys = [key for key in dsmc_data.keys() if key[0] in target_machs]
    min_mach = min([key[0] for key in md_plot_keys])
    min_kn = min([key[1] for key in md_plot_keys])
    max_kn = max([key[1] for key in md_plot_keys])
    for var in v_map.keys():
        if 'delta' not in var:
            plot_y(md_data, dsmc_data, md_plot_keys, dsmc_plot_keys, v_map[var], 'dim', 
                f'{var}', f'M{min_mach}_Kn{min_kn}-{max_kn}_dim_{var}')
        plot_y(md_data, dsmc_data, md_plot_keys, dsmc_plot_keys, v_map[var], 'nd', 
               f'{var}', f'M{min_mach}_Kn{min_kn}-{max_kn}_ND_{var}')

#%%
# # # 2. stress constraints' plots for all mach numbers and knudsen numbers
str_cons_fig(md_data, dsmc_data)    


#%%
# GAMMA for Argon: 1.667
# R/M for Argon: 208.13
# # # 1. plots for the special variables (delta) vs Mach/Kn
# # # 3. plots for individual variables for all mach numbers and knudsen numbers (desired axes and so on)
# # -------MD dim vars-------
# # ('Ycoord', 'numberdensity', 'Vx', 'Vy', 'Vz', 'Temp', 'Sxx', 'Syy', 'Szz', 'Sxy', 'Sxz', 'Syz', \
# # 'Pixx', 'Piyy', 'Pizz', 'Pressure', 'Qx', 'Qy', 'Qz')
# # -------MD nd vars-------
# # ('Ycoord', 'numberdensity', 'Vx', 'Vy', 'Vz', 'Temp', 'Sxx', 'Syy', 'Szz', 'Sxy', 'Sxz', 'Syz', \
# # 'Pixx', 'Piyy', 'Pizz', 'Pressure', 'Qx', 'Qy', 'Qz', 'TT0')
# # ********************************************************************************************************************
# # ********************************************************************************************************************
# # -------DSMC dim vars-------
# # ('id', 'x', 'y_ND', 'T', 'Press', 'Mrho', 'u', 'v', 'tau_xx', 'tau_yy', 'tau_zz', 'tau_xy', \
# # 'tau_xz', 'tau_yz', 'qx', 'qy', 'qz')
# # -------DSMC nd vars-------
# # ('id', 'x', 'y_ND', 'T', 'Press', 'Mrho', 'u', 'v', 'tau_xx', 'tau_yy', 'tau_zz', 'tau_xy', \
# # 'tau_xz', 'tau_yz', 'qx', 'qy', 'qz')


# %%
