import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

import rga_util as ru

plt.rcParams.update({'font.size': 14})


#rga_data_file1 = '/daq2/20190514/bead1/rga_scans/background2000001.txt'
#rga_data_file1 = '/daq2/20190514/bead1/rga_scans/background_nextday000001.txt'

#rga_data_file1 = '/daq2/20190514/bead1/rga_scans/preleak000001.txt'
#rga_data_file1 = '/daq2/20190514/bead1/rga_scans/leak000001.txt'
#rga_data_file2 = '/daq2/20190514/bead1/rga_scans/postleak000001.txt'

#rga_data_file1 = '/daq2/20190514/bead1/rga_scans/pre_Ar-leak_3_000001.txt'
rga_data_file1 = '/daq2/20190514/bead1/rga_scans/Ar-leak_2_000001.txt'
rga_data_file2 = '/daq2/20190514/bead1/rga_scans/post_Ar-leak_4_000001.txt'

base = '/daq2/20190514/bead1/spinning/pramp3/He/rga_scans/'
rga_data_file1 = base + 'He_20190607_measurement_1/meas1_pre-He-leak_2_000001.txt'
rga_data_file2 = base + 'He_20190607_measurement_1/meas1_He-leak_1_000001.txt'

#rga_data_file1 = base + 'He_20190607_measurement_2/meas2_He-leak_2_000001.txt'
#rga_data_file2 = base + 'He_20190607_measurement_2/meas2_He-leak_3_000001.txt'


base1 = '/daq2/20190514/bead1/spinning/pramp3/He/rga_scans/'
rga_data_file1 = base1 + 'He_20190607_measurement_1/meas1_pre-He-leak_2_000001.txt'

base2 = '/daq2/20190625/rga_scans/'
rga_data_file2 = base2 + 'reseat_with-grease_000002.txt'


plot_scan = False
plot_all_scans = True
plot_together = True

title = 'RGA Scan Evolution: Reseating Window'

filename = '/home/charles/plots/20190626/rga_scans/rga-diff_window-reseat.png'
save = False

gases_to_label = {'He': 3.9, \
                  'H$_2$O': 18, \
                  'N$_2$': 28, \
                  'O$_2$': 32, \
                  'Ar': 40, \
                  #'Kr': 84, \
                  #'Xe': 131, \
                  #'SF$_6$': 146, \
                  }


#arrow_len = 0.02
#arrow_len = 0.2
arrow_len = 0.2


######################################################

dat1 = ru.get_rga_data(rga_data_file1, all_scans=True, scan_ind=0, \
                       plot=plot_scan, plot_many=plot_all_scans)
dat2 = ru.get_rga_data(rga_data_file2, all_scans=False, scan_ind=-1, \
                       plot=plot_scan, plot_many=plot_all_scans)

m1 = dat1['mass_vec']
m2 = dat2['mass_vec']

pp1 = dat1['partial_pressures']
pp2 = dat2['partial_pressures']

p1 = dat1['pressure']
p2 = dat2['pressure']

e1 = dat1['errs']
e2 = dat2['errs']

diff = pp2 - pp1
diff_err = np.sqrt(e1**2 + e2**2)

pp_mean = 0.5 * (pp1 + pp2)
p_mean = 0.5 * (dat1['pressure'] + dat2['pressure'])

#p_tot = p_mean
p_tot = dat1['pressure']



if plot_together:

    fun = lambda x: '{:0.3g}'.format(x)
    title_str = 'Scan Comparison'

    fig, ax = plt.subplots(1,1,dpi=150,figsize=(10,3))
    ax.errorbar(m1, pp1, yerr=e1, color='C0')
    ax.fill_between(m2, pp1, np.ones_like(pp1)*1e-10,\
                    alpha=0.5, color='C0', label=('Before: ' + fun(p1) + ' torr'))
    ax.errorbar(m2, pp2, yerr=e2, color='C1')
    ax.fill_between(m2, pp2, np.ones_like(pp2)*1e-10,\
                    alpha=0.5, color='C1', label=('After: ' + fun(p2) + ' torr'))
    ax.set_ylim(1e-9, 2*np.max([np.max(pp1), np.max(pp2)]) )
    ax.set_xlim(0,int(np.max([np.max(m1), np.max(m2)])))
    ax.set_yscale('log')
    ax.set_xlabel('Mass [amu]')
    ax.set_ylabel('Partial Pressure [torr]')
    fig.suptitle(title_str)
    plt.tight_layout()
    plt.legend()
    plt.subplots_adjust(top=0.87)
    plt.show()






fig, ax = plt.subplots(1,1,dpi=150,figsize=(10,4))

ax.errorbar(m1, diff/p_tot, yerr=diff_err/p_tot)
#ax.errorbar(m1, diff/pp1, yerr=diff_err/p_tot)

gas_keys = gases_to_label.keys()
labels = []
neg = False
negmax = 0
pos = False
posmax = 0
for gas in gas_keys:
    mass = gases_to_label[gas]
    mass_ind = np.argmin( np.abs(m1 - mass) )

    val_init = diff[mass_ind]
    if val_init > 0:
        pos = True
        val = np.max((diff/p_tot)[mass_ind-5:mass_ind+5]) + \
                np.max((diff_err/p_tot)[mass_ind-5:mass_ind+5])
        if val > posmax:
            posmax = val
    if val_init < 0:
        neg = True
        val = np.min((diff/p_tot)[mass_ind-5:mass_ind+5]) - \
                np.max((diff_err/p_tot)[mass_ind-5:mass_ind+5])
        if val < negmax:
            negmax = val

    labels.append(ax.annotate(gas, (mass, val), \
                              xytext=(mass, val + np.sign(val)*arrow_len), \
                              ha='center', va='center', \
                              arrowprops={'width': 2, 'headwidth': 3, \
                                          'headlength': 5, 'shrink': 0.0}))

ax.set_xlabel('Mass [amu]')
ax.set_ylabel('$(\Delta P \, / \, P_{\mathrm{init}})$ [abs]')
ax.set_xlim(0,150)

y1, y2 = ax.get_ylim()
if pos:
    y2 = posmax + 2.0*arrow_len
if neg:
    y1 = negmax - 2.0*arrow_len
ax.set_ylim(y1, y2)

fig.suptitle(title)

plt.tight_layout()
plt.subplots_adjust(top=0.89)

if save:
    fig.savefig(filename)

plt.show()