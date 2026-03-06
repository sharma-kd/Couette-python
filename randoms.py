#%%
import pickle
import matplotlib.pyplot as plt

# 1. Load the plot
with open('../plots/vs_y/pickles/M0.1-3.0_Kn0.01-1.0_dim_Vx.pkl', 'rb') as f:
    fig = pickle.load(f)

# 2. Get the axes object to make changes
ax = fig.gca()

# 3. Apply manual adjustments
ax.set_ylim(-0.2, 0.6)        # Change Y limits
ax.set_title("Refined Velocity Profile") 
ax.grid(True, linestyle='--') # Add a grid if you forgot

# 4. Move the legend manually if needed
ax.legend(bbox_to_anchor=(1.1, 1.05), loc='upper left')

# 5. Show or Resave
plt.show()
# fig.savefig('refined_plot.png', bbox_inches='tight')


# %%
# flow mach (T0 based) and its plots
import matplotlib.ticker as ticker
md_keys = list(md_data.keys())
dsmc_keys = list(dsmc_data.keys())
plt.figure()
tick_md = 0
tick_dsmc = 0
for (m,kn) in md_keys:
    mask = abs(md_data[(m,kn)]['dim']['Ycoord'])<0.3
    Tavg = np.mean(md_data[(m,kn)]['dim']['Temp'][mask])
    a_loc = np.sqrt(1.667*208.13*Tavg)
    m_loc = m*322.687/a_loc
    leg_md = f'MD' if tick_md == 0 else None
    plt.plot(m_loc,np.mean(md_data[(m,kn)]['dim']['Pressure'][mask]),marker ='^',label=leg_md,ms=8)
    tick_md+=1
    # plt.plot(m,m_loc, marker='o',label=leg_md)

for (m,kn) in dsmc_keys:
    mask = abs(dsmc_data[(m,kn)]['dim']['y_ND'])<0.3
    Tavg = np.mean(dsmc_data[(m,kn)]['dim']['T'][mask])
    a_loc = np.sqrt(1.667*208.13*Tavg)
    m_loc = m*322.687/a_loc
    leg_dsmc = f'dsmc' if tick_dsmc == 0 else None
    plt.plot(m_loc,np.mean(dsmc_data[(m,kn)]['dim']['Press'][mask]),marker ='*',label=leg_dsmc,ms=8)
    tick_dsmc+=1
    # plt.plot(m,m_loc,marker ='x',label=leg_dsmc)
plt.minorticks_on()
plt.xlabel('flow mach (T0 based)')
plt.ylabel('Pressure (dimensional)')
plt.legend()
plt.yscale('log')
plt.gca().yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs='auto', numticks=8))
plt.grid(True, linestyle='--')
plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')

plt.title('Pressure vs Flow Mach (T0 based)')

#%%
#####Pi_ij vs Q_i/Q_j constraint plot #########
plt.figure()
targetm = 0.1
keym = [key for key in md_data.keys() if key[0]==targetm]
keydm = [key for key in dsmc_data.keys() if key[0]==targetm]
for key in keym:
    mask = ((md_data[(key)]['nd']['Ycoord']) < 0.4) & ((md_data[(key)]['nd']['Ycoord']) > 0.15)
    x = md_data[(key)]['nd']['Pressure'][mask] + (md_data[(key)]['nd']['Piyy'][mask]/md_data[(key)]['nd']['Sxy'][mask])
    y = md_data[(key)]['nd']['Qx'][mask]/md_data[(key)]['nd']['Qy'][mask]
    plt.plot(x,y,marker='^',ls='None', label=f'MD kn = {key[1]}')
for keyd in keydm:
    maskd = ((dsmc_data[(keyd)]['nd']['y_ND']) < 0.4) & ((dsmc_data[(keyd)]['nd']['y_ND']) > 0.15)
    xd = dsmc_data[(keyd)]['nd']['Press'][maskd] + (dsmc_data[(keyd)]['nd']['Piyy'][maskd]/dsmc_data[(keyd)]['nd']['Pixy'][maskd])
    yd = dsmc_data[(keyd)]['nd']['qx'][maskd]/dsmc_data[(keyd)]['nd']['qy'][maskd]
    plt.plot(xd,yd,marker='*',ls = 'None', label=f'DSMC kn = {keyd[1]}')
plt.legend()
# plt.xlim(-0.5, 0.5)
plt.ylim(-5, 5)
plt.xlabel(r'p* + $\widehat{\Pi_{yy}}/\widehat{\Pi_{xy}}$')
plt.ylabel(r'$\widehat{Q_{x}}/\widehat{Q_{y}}$')
plt.title(f'Mach = {targetm}')

# %%