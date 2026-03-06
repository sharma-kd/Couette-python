#%% load MD data
from pathlib import Path
import numpy as np

def load_MD(channel_width, bin_area, dia,dir):

    # channel_width = 50E-10 # 50 angstrom in meters
    # bin_area = 74.48*74.48*1E-20  # bin area in m^2
    # dia = 3.1E-10  # argon diameter in meters

    md_dir = dir
    md_prop_dat = {}
    md_dim = {}
    md_nd = {}
    md_data = {}
    md_prop_files = md_dir.glob('Props_all.*.txt')
    prop_names = ['Chunk ID','y_prop','Ncount','num_rho','vx','vy',\
                'vz','fx','fy','fz']


    for f in md_prop_files:
        print(f"Found MD props file: {f.name}")
        a = f.stem.split('.')
        mach = float(f"{a[1]}.{a[2]}")
        num_atoms = int(a[3])
        data = np.genfromtxt(f, skip_header=4, names = prop_names)
        mask = abs(data['y_prop']) < max((channel_width*0.5),20)                                   # near centerline flag
        num0 = np.mean(data['Ncount'][mask])
        bin_vol = bin_area * (data['y_prop'][1] - data['y_prop'][0])*1e-10   # bin volume in m^3
        kn_loc = 1/(np.sqrt(2)*np.pi*(num0/bin_vol)*channel_width*dia*dia)
        kn_md = round(kn_loc,1)
        # print(f"Computed Knudsen number for M={mach}, N={num_atoms} is {kn_md}: saving data to md_prop_dat.")
        md_prop_dat[(mach,kn_md,num_atoms)] = data
        
    #%% load MD dim/nd vars
    md_dim_files = md_dir.glob('dimVars-*.txt')
    for f in md_dim_files:
        print(f"Found MD dim vars file: {f.name}")
        a = f.stem.split('-')
        mach = float(a[1])
        num_atoms = int(a[2])
        # print(f"Computed Knudsen number for M={mach}, N={num_atoms} is {kn_md}: saving data to md_dim.")
        md_dim[(mach,num_atoms)] = np.genfromtxt(f,  names = True)
    md_nd_files = md_dir.glob('ndVars-*.txt')
    for f in md_nd_files:
        print(f"Found MD nd vars file: {f.name}")
        a = f.stem.split('-')
        mach = float(a[1])
        num_atoms = int(a[2])
        # print(f"Computed Knudsen number for M={mach}, N={num_atoms} is {kn_md}: saving data to md_nd")
        md_nd[(mach,num_atoms)] = np.genfromtxt(f,  names = True)
        # Ycoord normalization; correction for dim/nd and props y dim
        # md_nd[(mach,num_atoms)]['Ycoord'] = md_nd[(mach,num_atoms)]['Ycoord']*50/68
        md_dim[(mach,num_atoms)]['Ycoord'] = md_nd[(mach,num_atoms)]['Ycoord']
        md_nd[(mach,num_atoms)]['Temp'] = md_nd[(mach,num_atoms)]['TT0']

    #%% combine md data into master dict
    for (mach, kn_md, num_atoms) in md_prop_dat.keys():
        key1 = (mach,num_atoms)
        md_data[(mach,num_atoms)] = {
            'kn': kn_md,
            'props': md_prop_dat[(mach, kn_md, num_atoms)],
            'dim': md_dim[key1],
            'nd': md_nd[key1]}
        dudy_nd = np.gradient(md_nd[key1]['Vx'], md_nd[key1]['Ycoord'])
        delta = dudy_nd*(md_nd[key1]['Temp'])**0.5 
        # 0.5 for argon; see myong 1999 paper
        md_data[(mach,num_atoms)]['nd'] = np.lib.recfunctions.append_fields(
            md_data[(mach,num_atoms)]['nd'],
            'delta',
            delta,
            usemask = False)
    return md_data

    # # Accessing Kn directly from the master dict
    # current_kn = md_data[(0.5, 2000)]['kn']

    # # Accessing the property array
    # current_array = md_data[(0.5, 2000)]['props']
