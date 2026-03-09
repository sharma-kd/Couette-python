#%%
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os


def plot_y(md_data, dsmc_data, nccr_data, md_plot_key, dsmc_plot_key, var_vs_y, dimflag, ylabel, title):
    #plot all profiles vs y for md and dsmc
    plt.figure(figsize=(8, 6))
    md_var, dsmc_var, nccr_var, nsf_var = var_vs_y
    marks = ['.', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', 
    'p', 'P', '*', 'h', 'H', '+', 'x', 'X', 'D', 'd', '|', '_']
    tick_md = 0
    for (mach, kn) in md_plot_key:
        # MD data
        plt.plot(md_data[(mach, kn)][f'{dimflag}']['Ycoord'], 
                 md_data[(mach, kn)][f'{dimflag}'][f'{md_var}'],
                 ls = ':',marker = marks[tick_md], alpha=0.7,
                   label=f'MD M={mach} Kn = {kn}', ms=4)
        tick_md += 1
    tick_dsmc = 0
    for (mach, kn) in dsmc_plot_key:
        # DSMC data
        plt.plot(dsmc_data[(mach, kn)][f'{dimflag}']['y_ND'], 
                 dsmc_data[(mach, kn)][f'{dimflag}'][f'{dsmc_var}'],
                 ls = '-.', marker = marks[tick_dsmc],label=f'DSMC M={mach} Kn = {kn}', ms = 4)
        tick_dsmc += 1
    tick_nccr = 0
    for (mach, kn) in nccr_plot_key:
        # NCCR data
        plt.plot(nccr_data[(mach, kn)][f'{dimflag}']['y'], 
                 nccr_data[(mach, kn)][f'{dimflag}'][f'{nccr_var}'],
                 ls = '--', marker = marks[tick_nccr],label=f'NCCR M={mach} Kn = {kn}', ms = 4)
        tick_nccr += 1
    tick_nsf = 0
    for (mach, kn) in nsf_plot_key:
        # NSF data
        plt.plot(nsf_data[(mach, kn)][f'{dimflag}']['y'], 
                 nsf_data[(mach, kn)][f'{dimflag}'][f'{nsf_var}'],
                 ls = '-.', marker = marks[tick_nsf],label=f'NSF M={mach} Kn = {kn}', ms = 4)
        tick_nsf += 1
    plt.xlabel('y')
    plt.xlim(-0.48,0.48)
    plt.ylabel(f'{ylabel}')
    plt.title(f'{title}')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    
    # Save the Figure object
    file_path = f'../plots/vs_y/pickles/{title.replace(" ","_")}.pkl'
    with open(file_path, 'wb') as f:
        pickle.dump(plt.gcf(), f)
    plt.savefig(f'../plots/vs_y/{title.replace(" ","_")}.png', dpi=300,bbox_inches='tight')
    print(f"Plotting {md_var}-{dsmc_var}---vs---y---{dimflag} for M = {md_plot_key[0][0]}")
    plt.close()

def plot_Mkn(md_data, dsmc_data, nccr_data, var_vs_Mkn, dimflag, vflag, ylabel):
    #plot requested profiles vs Mach/Kn for md and dsmc
    md_v, dsmc_v =  var_vs_Mkn
    md_plot_key = md_data.keys()
    dsmc_plot_key = dsmc_data.keys()
    tick_md = 0
    plt.figure()
    titlef = 'mach' if vflag=='M' else 'knudsen'
    for (mach, kn) in md_plot_key:
        # MD data, no lines here as multiple M/Kn values exist for a single Kn/M value. 
        md_mask = abs(md_data[(mach, kn)]['nd']['Ycoord']) < 0.25
        md_label = f'MD' if tick_md == 0 else None
        x = mach if vflag=='M' else kn
        plt.plot(x, np.mean(md_data[(mach, kn)][f'{dimflag}'][f'{md_v}'][md_mask]),
                marker = 'o',c = 'blue', label=md_label, ms=6, ls = 'none')
        tick_md += 1
    tick_dsmc = 0
    for (mach, kn) in dsmc_plot_key:
        # DSMC data
        dsmc_mask = abs(dsmc_data[(mach, kn)]['nd']['y_ND']) < 0.25
        dsmc_label = f'DSMC' if tick_dsmc == 0 else None
        x = mach if vflag=='M' else kn
        plt.plot(x, np.mean(dsmc_data[(mach, kn)][f'{dimflag}'][f'{dsmc_v}'][dsmc_mask]),  
                marker = 'x', label=dsmc_label, ms = 6, c = 'red', ls = 'none')
        tick_dsmc += 1
    plt.xlabel(f'{titlef}')
    plt.ylabel(f'{ylabel}')
    plt.title(f'{ylabel} ({dimflag}) vs {titlef}')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.tight_layout()
    
    if vflag=='M':
        plt.savefig(f'../plots/M_var/{ylabel}_vs_{titlef}_{dimflag}.png', dpi=300)
        file_path = f'../plots/M_var/pickles/{ylabel}_vs_{titlef}_{dimflag}.pkl'
        with open(file_path, 'wb') as f:
            pickle.dump(plt.gcf(), f)
    else:
        plt.savefig(f'../plots/Kn_var/{ylabel}_vs_{titlef}_{dimflag}.png', dpi=300)
        file_path = f'../plots/Kn_var/pickles/{ylabel}_vs_{titlef}_{dimflag}.pkl'
        with open(file_path, 'wb') as f:
            pickle.dump(plt.gcf(), f)
    # print(f"Plotting {md_v}-{dsmc_v}--vs--{titlef}-{dimflag}")
    plt.close()

def plot_Mkn1(md_data, dsmc_data, nccr_data, var_vs_Mkn, dimflag, vflag, ylabel):
    #plot requested profiles vs Mach/Kn for md and dsmc: Near wall region
    md_v, dsmc_v =  var_vs_Mkn
    md_plot_key = md_data.keys()
    dsmc_plot_key = dsmc_data.keys()
    tick_md = 0
    plt.figure()
    titlef = 'mach' if vflag=='M' else 'knudsen'
    for (mach, kn) in md_plot_key:
        # MD data, no lines here as multiple M/Kn values exist for a single Kn/M value. 
        md_mask = (md_data[(mach, kn)]['nd']['Ycoord']) > 0.40
        md_label = f'MD' if tick_md == 0 else None
        x = mach if vflag=='M' else kn
        plt.plot(x, np.mean(md_data[(mach, kn)][f'{dimflag}'][f'{md_v}'][md_mask]),
                marker = 'o',c = 'blue', label=md_label, ms=6, ls = 'none')
        tick_md += 1
    tick_dsmc = 0
    for (mach, kn) in dsmc_plot_key:
        # DSMC data
        dsmc_mask = (dsmc_data[(mach, kn)]['nd']['y_ND']) > 0.40
        dsmc_label = f'DSMC' if tick_dsmc == 0 else None
        x = mach if vflag=='M' else kn
        plt.plot(x, np.mean(dsmc_data[(mach, kn)][f'{dimflag}'][f'{dsmc_v}'][dsmc_mask]),  
                marker = 'x', label=dsmc_label, ms = 6, c = 'red', ls = 'none')
        tick_dsmc += 1
    plt.xlabel(f'{titlef}')
    plt.ylabel(f'{ylabel}')
    plt.title(f'{ylabel} ({dimflag}) vs {titlef}')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.tight_layout()
    
    if vflag=='M':
        plt.savefig(f'../plots/M_var/{ylabel}_vs_{titlef}_{dimflag}.png', dpi=300)
        file_path = f'../plots/M_var/pickles/{ylabel}_vs_{titlef}_{dimflag}.pkl'
        with open(file_path, 'wb') as f:
            pickle.dump(plt.gcf(), f)
    else:
        plt.savefig(f'../plots/Kn_var/{ylabel}_vs_{titlef}_{dimflag}.png', dpi=300)
        file_path = f'../plots/Kn_var/pickles/{ylabel}_vs_{titlef}_{dimflag}.pkl'
        with open(file_path, 'wb') as f:
            pickle.dump(plt.gcf(), f)
    plt.close()

def str_cons_fig(md_data, dsmc_data, nccr_data):
    tick_md = 0
    tick_dsmc = 0
    plt.figure()
    for (mach, kn) in md_data.keys():
        # MD data
        md_label = f'MD' if tick_md == 0 else None
        md_mask = abs(md_data[(mach, kn)]['nd']['Ycoord']) < 0.25
        plt.plot(np.mean(md_data[(mach, kn)]['nd']['Sxy'][md_mask]), 
                 np.mean(md_data[(mach, kn)]['nd']['Piyy'][md_mask]),
                 c = 'blue', marker = 'o', label=md_label, ms=6, ls = 'none')
        tick_md += 1
    for (mach, kn) in dsmc_data.keys():
        # DSMC data
        dsmc_label = f'DSMC' if tick_dsmc == 0 else None
        dsmc_mask = abs(dsmc_data[(mach, kn)]['nd']['y_ND']) < 0.25
        plt.plot(np.mean(dsmc_data[(mach, kn)]['nd']['Pixy'][dsmc_mask]), 
                 np.mean(dsmc_data[(mach, kn)]['nd']['Piyy'][dsmc_mask]),
                 c = 'red', marker = 'x',label=dsmc_label, ms = 6, ls = 'none')
        tick_dsmc += 1
    plt.xlabel(r'$\widehat{\Pi_{xy}}$')
    plt.ylabel(r'$\widehat{\Pi_{yy}}$')
    m_min = min(key[0] for key in md_data.keys())
    m_max = max(key[0] for key in md_data.keys())
    kn_min = min(key[1] for key in md_data.keys())
    kn_max = max(key[1] for key in md_data.keys())
    tit = f'$\\widehat{{\\Pi_{{xy}}}}$ vs $\\widehat{{\\Pi_{{yy}}}}$ : Mach {m_min}-{m_max}, Kn {kn_min}-{kn_max}'

    plt.title(tit)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.tight_layout()
    file_path = f'../plots/Stress_constraints.pkl'
    with open(file_path, 'wb') as f:
        pickle.dump(plt.gcf(), f)
    plt.savefig(f'../plots/Stress_constraints.png', dpi = 300)
    plt.close()
    
# %%
