
from pathlib import Path
import numpy as np
import copy
from numpy.lib import recfunctions

def load_DSMC(dsmc_dir):
    data_dir = dsmc_dir
    dsmc_files = data_dir.glob('*.dat')
    dsmc_data = {}
    dsmc_dim = {}
    dsmc_nd = {}
    col_names = ['id', 'x', 'y_ND', 'T','Press', 'Mrho', 'u', 'v', 'tau_xx', \
                'tau_yy', 'tau_zz', 'tau_xy', 'tau_xz', 'tau_yz', 'qx', 'qy', 'qz']

    for f in dsmc_files:
        print(f"Found DSMC data file: {f.name}")
        a = f.stem.split('.')
        mach = float(f"{a[1]}.{a[2]}")
        kn = float(f"{a[3]}.{a[4]}")
        ts = int(a[5])
        dsmc_dim[(mach,kn)] = np.genfromtxt(f, skip_header=9, names = col_names)
        pixx = dsmc_dim[(mach,kn)]['tau_xx']-dsmc_dim[(mach,kn)]['Press']
        piyy= dsmc_dim[(mach,kn)]['tau_yy']-dsmc_dim[(mach,kn)]['Press']
        pizz = dsmc_dim[(mach,kn)]['tau_zz']-dsmc_dim[(mach,kn)]['Press']
        pixy = dsmc_dim[(mach,kn)]['tau_xy']
        dsmc_dim[(mach,kn)] = np.lib.recfunctions.append_fields(
            dsmc_dim[(mach,kn)],
            ['Pixx','Piyy','Pizz','Pixy'],
            [pixx, piyy, pizz, pixy],
            usemask = False)

    # make new nondimensional variable directory
    # x, y are nd. T -> T0; Press -> P0; Mrho -> rho0; u, v -> Vwall;
    # tau_** -> tau_**/P0; q* -> P0*Vwall
    dsmc_nd = copy.deepcopy(dsmc_dim)
    for (mach,kn) in dsmc_nd.keys():
        Vwall = mach * 322.687  
        dsmc_nd[(mach,kn)]['y_ND'] /= 5e-8
        dsmc_dim[(mach,kn)]['y_ND'] /= 5e-8
        mask = (abs(dsmc_nd[(mach,kn)]['y_ND']) < 0.15)
        P0 = np.mean(dsmc_nd[(mach,kn)]['Press'][mask])  
        T0 = np.mean(dsmc_nd[(mach,kn)]['T'][mask]) 
        rho0 = np.mean(dsmc_nd[(mach,kn)]['Mrho'][mask]) 
        
        dsmc_nd[(mach,kn)]['T'] /= T0
        dsmc_nd[(mach,kn)]['Press'] /= P0
        dsmc_nd[(mach,kn)]['Mrho'] /= rho0
        dsmc_nd[(mach,kn)]['u'] /= Vwall
        dsmc_nd[(mach,kn)]['v'] /= Vwall
        dsmc_nd[(mach,kn)]['tau_xx'] /= P0
        dsmc_nd[(mach,kn)]['tau_yy'] /= P0
        dsmc_nd[(mach,kn)]['tau_zz'] /= P0
        dsmc_nd[(mach,kn)]['tau_xy'] /= P0
        dsmc_nd[(mach,kn)]['tau_xz'] /= P0
        dsmc_nd[(mach,kn)]['tau_yz'] /= P0
        dsmc_nd[(mach,kn)]['Pixx'] /= P0
        dsmc_nd[(mach,kn)]['Piyy'] /= P0
        dsmc_nd[(mach,kn)]['Pizz'] /= P0
        dsmc_nd[(mach,kn)]['Pixy'] /= P0
        dsmc_nd[(mach,kn)]['qx'] /= (P0 * Vwall)
        dsmc_nd[(mach,kn)]['qy'] /= (P0 * Vwall)
        dsmc_nd[(mach,kn)]['qz'] /= (P0 * Vwall)
        # combine dim/nd data into master dict
        dsmc_data[(mach,kn)] = {
            'dim': dsmc_dim[(mach,kn)], 
            'nd': dsmc_nd[(mach,kn)]}
        dudy = np.gradient(dsmc_nd[(mach,kn)]['u'], dsmc_nd[(mach,kn)]['y_ND'])
        delta = dudy*(dsmc_nd[(mach,kn)]['T'])**0.5
        # 0.5 for argon; see myong 1999 paper
        dsmc_data[(mach,kn)]['nd'] = np.lib.recfunctions.append_fields(
            dsmc_data[(mach,kn)]['nd'],
            'delta',
            delta,
            usemask = False)
    return dsmc_data

