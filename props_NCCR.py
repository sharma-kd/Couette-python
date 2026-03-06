from pathlib import Path
import numpy as np

def load_NSF_NCCR(nccr_dir):
    dir = nccr_dir
    nccr_files = dir.glob('NCCR_*')
    nsf_files = dir.glob('NSF_*')
    # vex,del2,tw2,t0w2,tsw2,slp02,slps2,uvs2,strs2,stny,-2.*stny,qys2,qxs2 : line 1
    # s*, y*, uy*, T*, Qy*, Qx*, Pixy*, Piyy*, Pixx* : rest of the lines
    nccr_col_names = ['s', 'y', 'u', 'T', 'Qy', 'Qx', 'Pixy', 'Piyy', 'Pixx']
    nsf_col_names = ['s', 'y', 'u', 'T', 'Qy', 'Qx', 'Pixy', 'Piyy', 'Pixx']
    nccr_nd = {}
    nsf_nd = {}

    for f in nccr_files:
        print(f"Found NCCR data file: {f.name}")
        # file name: NCCR_Mach_{mach}_Kn_{kn}
        a = f.stem.split('_')
        mach = float(a[2])
        kn = float(a[4])
        nccr_nd[(mach, kn)] = np.genfromtxt(f, skip_header=1, names=nccr_col_names)
    
    for f in nsf_files:
        print(f"Found NSF data file: {f.name}")
        # file name: NSF_Mach_{mach}_Kn_{kn}
        a = f.stem.split('_')
        mach = float(a[2])
        kn = float(a[4])
        nccr_nd[(mach, kn)] = np.genfromtxt(f, skip_header=1, names=nsf_col_names)

    for key in nccr_nd.keys():
        dudy = np.gradient(nccr_nd[key]['u'], nccr_nd[key]['y'])
        delta = dudy*(nccr_nd[key]['T']**0.5)
        nccr_nd[key] = np.lib.recfunctions.append_fields(nccr_nd[key], 'delta',delta, usemask=False)
    
    for key in nsf_nd.keys():
        dudy = np.gradient(nsf_nd[key]['u'], nsf_nd[key]['y'])
        delta = dudy*(nsf_nd[key]['T']**0.5)
        nsf_nd[key] = np.lib.recfunctions.append_fields(nsf_nd[key], 'delta',delta, usemask=False)
    
    return nccr_nd, nsf_nd
