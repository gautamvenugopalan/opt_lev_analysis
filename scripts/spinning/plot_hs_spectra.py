import os, fnmatch, sys

import dill as pickle

import scipy.interpolate as interp
import scipy.optimize as opti
import scipy.signal as signal

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

import bead_util as bu
import configuration as config

plt.rcParams.update({'font.size': 16})

# dirname = '/data/old_trap/20190905/bead1/spinning/ringup/100kHz_1'
# dirname = '/data/old_trap/20190905/bead1/spinning/ringup/test3'
# dirname = '/data/old_trap/20190905/bead1/spinning/residual_field_tests/nominal_config'
# dirname = '/data/old_trap/20190905/bead1/spinning/residual_field_tests/monitors_unplugged'
# dirname = '/data/old_trap/20190905/bead1/spinning/residual_field_tests/monitors_unplugged_term'
# dirname = '/data/old_trap/20190905/bead1/spinning/residual_field_tests/tabor_off'
# dirname = '/data/old_trap/20190905/bead1/spinning/residual_field_tests/tabor_off_proper_conn'
# dirname = '/data/old_trap/20190905/bead1/spinning/residual_field_tests/tabor_unplugged'
# dirname = '/data/old_trap/20190905/bead1/spinning/residual_field_tests/rot_diode_unplugged'
# dirname = '/data/old_trap/20190905/bead1/spinning/residual_field_tests/different_srs_output'
# dirname = '/data/old_trap/20190905/bead1/spinning/residual_field_tests/drive_at_9k'
# dirname = '/data/old_trap/20190905/bead1/spinning/residual_field_tests/drive_at_9k_better_term'
# dirname = '/data/old_trap/20190905/bead1/spinning/residual_field_tests/drive_at_9k_much_later'

# dirname = '/data/old_trap/20190905/bead1/spinning/ringdown_manual/50kHz_start_4'
# dirname = '/data/old_trap/20190905/bead1/spinning/ringdown_manual/100kHz_start_2'
# dirname = '/data/old_trap/20190905/bead1/spinning/ringdown_manual/terminal_velocity_test'
# dirname = '/data/old_trap/20190905/bead1/spinning/ringdown_manual/terminal_velocity_test_later'

# dirname = '/data/old_trap/20190905/bead1/spinning/high_speed_tests/210kHz'

# dirname = '/data/old_trap/20190905/bead1/spinning/ringdown/210kHz_start_1'


# dirname = '/data/old_trap/20191017/bead1/spinning/ringdown/term_velocity_check_7'

# dirname = '/data/old_trap/20191017/bead1/spinning/junk/shit_test_99'
# dirname = '/data/old_trap/20191017/bead1/spinning/ringdown/110kHz_start_test'

# dirname = '/data/old_trap/20200322/gbead1/spinning/ringdown/110kHz_1'
# dirname = '/data/old_trap/20200322/gbead1/spinning/wobble/wobble_init/wobble_0000'
# dirname = '/data/old_trap/20200322/gbead1/spinning/ringdown/terminal_velocity_check_2'

# dirname = '/data/old_trap/20200727/bead1/spinning/hf_spin_up'
# dirname = '/data/old_trap/20200727/bead1/spinning/junk/test3'
# dirname = '/data/old_trap/20200727/bead1/spinning/amplitude_change_much-later'
# dirname = '/data/old_trap/20200727/bead1/spinning/wobble_slow/wobble_0/'

# dirname = '/data/old_trap/20200727/bead1/spinning/lowp_arb_spinup/'
# dirname = '/data/old_trap/20200727/bead1/spinning/lowp_arb_spinup_2/'

# dirname = '/data/old_trap/20200727/bead1/spinning/junk/old_drive_test_4/'
# dirname = '/data/old_trap/20200727/bead1/spinning/phase_fb_tests/100Hz_mod_2/'

# dirname = '/data/old_trap/20200924/bead1/spinning/initial_test'
# dirname = '/data/old_trap/20200924/bead1/spinning/dipole_meas/initial/trial_0000'
# dirname = '/data/old_trap/20200924/bead1/spinning/crosstalk_check'
# dirname = '/data/old_trap/20200924/bead1/spinning/dds_phase_modulation_8Vpp_test'
# dirname = '/data/old_trap/20200924/bead1/spinning/dds_phase_impulse_3Vpp_high_dg_2/trial_0000'
# dirname = '/data/old_trap/20200924/bead1/spinning/junk/55kHz_check'
# dirname = '/data/old_trap/20200924/bead1/spinning/ringdown/55kHz_start_2'
# dirname = '/data/old_trap/20200924/bead1/spinning/junk/110kHz_start_2'

# dirname  = '/data/old_trap/20201113/bead1/spinning/dipole_meas/initial'
# dirname  = '/data/old_trap/20230306/bead4/spinning/spinup2'
# dirname  = '/data/old_trap/20230306/bead4/spinning/25kHz_steady_state'

# dirname  = '/data/old_trap/20230327/bead1/spinning/dipole_meas/initial_zadj'
# dirname  = '/data/old_trap/20230327/bead1/spinning/dipole_meas/initial_zadj_28k'
# dirname  = '/data/old_trap/20230327/bead1/spinning/phase_mod_test_sweep_0_05scale_hf'
# dirname = '/data/old_trap/20230327/bead1/spinning/spindown_100kHz'


# base = '/data/old_trap/20230410/bead1/spinning/'

# # meas = 'change_direction_xy_to_xz'
# # meas = 'dipole_meas/initial_zadj'
# # meas = 'phase_modulate_0_01scale'
# # meas = 'phase_modulate_0_05scale'
# # meas = 'dds_phase_impulse_test'
# meas = 'phase_modulation_sweeps/10Hz_to_700Hz_0007'
# # meas = 'phase_modulation_sweeps/700Hz_to_10Hz_0007'



base = '/data/old_trap/20230531/bead1/spinning/'
# meas = 'spinup'
# meas = 'test_25kHz'
meas = 'phase_modulation_sweeps/10Hz_to_700Hz_8Vpp_5sec_settle'

dirname = os.path.join(base, meas)




use_dir = True
#use_dir = False

# bases = ['/data/old_trap/20190905/bead1/spinning/residual_field_tests/nominal_config', \
#          '/data/old_trap/20190905/bead1/spinning/residual_field_tests/monitors_unplugged_term', \
#          '/data/old_trap/20190905/bead1/spinning/residual_field_tests/rot_diode_unplugged', \
#          '/data/old_trap/20190905/bead1/spinning/residual_field_tests/drive_at_9k_better_term', \
#         ]
# labels = ['Initial: Tabor off, optically driven rotation', \
#           'Tabor monitor -> Terminator', \
#           'Rot. diode -> Terminator', \
#           'Tabor on, but chamber elec. terminated', \
#          ]


savefig = False
fig_savename = ''
#fig_savename = '/home/cblakemore/plots/20190905/residual_field_tests.svg'


data_axes = [0,1]
axes_labels = ['Cross-polarized light', 'Tabor Monitor']
# data_axes = [0]
# axes_labels = ['Cross-polarized light']

use_filename_labels = False
labels = []

#file_inds = (-10,-1)
file_inds = (0, 100)
file_step = 1

userNFFT = 2**20
fullNFFT = True

plot_freqs = (48500.0, 51500.0)
# plot_freqs = (0.1, 250000.0)

waterfall = False
waterfall_fac = 100

invert_zorder = False
invert_colors = True

#window = mlab.window_hanning
window = mlab.window_none

# ylim = (1e-21, 1e-14)
#ylim = (1e-7, 1e-1)
# ylim = (1e-6, 8e-4)
ylim = ()


# xlim = (190000.0, 200600.0)
xlim = (48500.0, 51500.0)
# xlim = (10.0, 250000.0)
# xlim = ()

# xticks = [190000.0, 192500.0, 195000.0, 197500.0, 200000.0]
xticks = None

track_feature = False
tracking_band = 500.0
tracking_axis = 0
tracking_savefile = ''
# tracking_savefile = '/data/old_trap_processed/spinning/ringdown/20200322/term_velocity_check_2.npy'

# approx_feature_loc = 10000.0
# approx_feature_loc = 4216.0
approx_feature_loc = 0.0

###########################################################

cmap = 'plasma'
#cmap = 'jet'


def lorentzian(x, A, mu, gamma, c):
    return A * (gamma**2 / ((x-mu)**2 + gamma**2)) + c



def plot_many_spectra(files, data_axes=[0,1,2], colormap='plasma', \
                      invert_colors=False, invert_zorder=False, \
                      sort='time', \
                      plot_freqs=(0.0,1000000.0), labels=[]):
    '''Loops over a list of file names, loads each file,
       then plots the amplitude spectral density of any number 
       of data channels

       INPUTS: files, list of files names to extract data
               data_axes, list of pos_data axes to plot

       OUTPUTS: none, plots stuff
    '''



    dfig, daxarr = plt.subplots(len(data_axes),sharex=True,sharey=False, \
                                figsize=(8,4*len(data_axes)))
    if len(data_axes) == 1:
        daxarr = [daxarr]

    colors = bu.get_colormap(len(files), cmap=colormap)
    if invert_colors:
        colors = colors[::-1]

    zorders = np.arange(len(files)) + 5
    if invert_zorder:
        zorders = zorders[::-1]

    if track_feature:
        times = []
        feature_locs = []

    old_per = 0
    print(f"Processing {len(files)} files...")
    for fil_ind, fil in enumerate(files):

        color = colors[fil_ind]
        zorder = zorders[fil_ind]
        
        # Display percent completion
        bu.progress_bar(fil_ind, len(files))

        # Load data
        obj = bu.hsDat(fil, load=True)

        # plt.figure()
        # plt.plot(obj.dat[:,1])
        # plt.show()
        # input()

        fsamp = obj.attribs['fsamp']
        nsamp = obj.attribs['nsamp']
        t = obj.attribs['time']

        freqs = np.fft.rfftfreq(nsamp, d=1.0/fsamp)

        if waterfall:
            fac = waterfall_fac**fil_ind
        else:
            fac = 1.0

        if not fullNFFT:
            NFFT = userNFFT
        else:
            NFFT = nsamp


        for axind, ax in enumerate(data_axes):
            # if fullNFFT:
            #     NFFT = len(df.pos_data[ax])
            # else:
            #     NFFT = userNFFT
        
            # asd = np.abs(np.fft.rfft(obj.dat[:,axind]))

            psd, freqs = mlab.psd(obj.dat[:,axind], Fs=obj.attribs['fsamp'], \
                                    NFFT=NFFT, window=window)
            asd = np.sqrt(psd)

            plot_inds = (freqs > plot_freqs[0]) * (freqs < plot_freqs[1])


            if len(labels):
                daxarr[axind].loglog(freqs[plot_inds], asd[plot_inds]*fac, \
                                     label=labels[fil_ind], color=colors[fil_ind], \
                                     zorder=zorder)
            else:
                daxarr[axind].loglog(freqs[plot_inds], asd[plot_inds]*fac, \
                                     color=colors[fil_ind], \
                                     zorder=zorder)

            daxarr[axind].set_ylabel('$\\sqrt{\\mathrm{PSD}}$')
            if ax == data_axes[-1]:
                daxarr[axind].set_xlabel('Frequency [Hz]')

    if len(axes_labels):
        for labelind, label in enumerate(axes_labels):
            daxarr[labelind].set_title(label)

    if len(labels):
        daxarr[0].legend(fontsize=10)
    if len(xlim):
        daxarr[0].set_xlim(xlim[0], xlim[1])
    if len(ylim):
        daxarr[0].set_ylim(ylim[0], ylim[1])

    if xticks is not None:
        daxarr[1].set_xticks(xticks)
        daxarr[1].set_xticks([], minor=True)

    plt.tight_layout()

    if savefig and fig_savename:
        dfig.savefig(fig_savename)


    plt.show()

    # if not savefigs:
    #     plt.show()


if use_dir:
    allfiles, lengths = bu.find_all_fnames(dirname, sort_time=True)
    allfiles = allfiles[file_inds[0]:file_inds[1]:file_step]

if use_filename_labels:
    labels = np.copy(allfiles)

plot_many_spectra(allfiles, data_axes=data_axes, colormap=cmap, \
                  plot_freqs=plot_freqs, labels=labels, \
                  invert_colors=invert_colors, \
                  invert_zorder=invert_zorder)