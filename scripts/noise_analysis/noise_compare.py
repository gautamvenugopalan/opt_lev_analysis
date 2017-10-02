###Script to compare the x position ASD from different files and generate a plot
import numpy as np
import matplotlib.pyplot as plt
import bead_util as bu
import dill as pickle
import configuration
from matplotlib.mlab import psd

#define parameters global to the noise analysis
f0 = 220. #Hz
dat_column = 0
NFFT = 2**14
cal_file ='/calibrations/step_cals/step_cal_20170903.p' 

#Put filenames into dict with plot label as key
bead_files= {"MS":"/data/20170903/bead1/turbombar_xyzcool_discharged.h5", "No MS": "/data/20170918/noise_tests/no_bead.h5", "DAQ": "/data/20170918/noise_tests/x_y_terminated.h5", "Electronics": "/data/20170918/noise_tests/all_beams_blocked.h5"}

def cal_constant(f0, cal_file = cal_file):
    '''derives m/V calibration constant from a charge step calibratioon file and resonant frequency'''
    vpn = pickle.load(open(cal_file, 'rb'))[0][0]
    p_param = configuration.p_param
    m = (4./3.)*np.pi*p_param['bead_radius']**3*p_param['bead_rho']
    k = m*(2.*np.pi*f0)**2
    return vpn*k
    


def plt_df(df, cf, lab):
    '''plots the x position ASD for DataFile with '''
    psd_dat, freqs = psd(cf*df.pos_data[:, dat_column], Fs = df.fsamp, NFFT = NFFT)
    plt.loglog(freqs, np.sqrt(psd_dat), label = lab)

#get calibration constant.
cf = cal_constant(f0)
for k in bead_files.keys():
    df = bu.DataFile()
    df.load(bead_files[k])
    plt_df(df, cf, k)


plt.legend()
plt.xlabel("Frequency [Hz]")
plt.ylabel("Displacement spectral density [$m/\sqrt{Hz}$]") 
plt.show()
