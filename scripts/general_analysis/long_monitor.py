import os, fnmatch, sys

import dill as pickle

import scipy.interpolate as interp

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

import bead_util as bu
import configuration as config

plt.rcParams.update({'font.size': 14})



dir1 = '/data/old_trap/20230322/bead1/zoffset_sweep_5mbar_up_2'
maxfiles = 500

new_trap = False

tfdate = '20190619'  # Bangs bead
tfdate = '20200327'  # gbead
tfdate = ''
tf_plot = False

### Things to monitor and eventually plot
monitor_keys = [ \
                'power', \
                'mean_position', \
                'qpd_amp', \
                'backreflection',
               ]

### Option to plot the monitored variables as a function 
### of a parameter, rather than time
plot_parametrically = True
parameter = 'mean_feedback_z'
# parameter = 'backreflection_amp'


###########################################################
###########################################################
###########################################################

# cmap = 'inferno'
cmap = 'plasma'
#cmap = 'jet'


allfiles, lengths = bu.find_all_fnames(dir1, sort_time=True)
allfiles = allfiles[:maxfiles]



def long_monitor(files, monitor_keys, \
                 parameter='', plot_parametrically=False):
    '''Loops over a list of file names, loads each file, diagonalizes,
       then plots the amplitude spectral density of any number of data
       or cantilever/electrode drive signals

       INPUTS: 

            files, list of files names to extract data
               
            monitor_keys, an iterable object with strings specifying
                what we should monitor
    '''

    nfiles = len(files)

    if plot_parametrically:
        param_arr = np.zeros((2, nfiles))

    single_panel_figsize = (8, 4)
    double_panel_figsize = (8, 6.5)
    triple_panel_figsize = (8, 9)

    if 'power' in monitor_keys:
        power_fig, power_ax = plt.subplots(1, 1, figsize=single_panel_figsize)
        power_arr = np.zeros((2, nfiles))

    if 'mean_position' in monitor_keys:
        pos_fig, pos_axarr = plt.subplots(3, 1, sharex=True, \
                                          figsize=triple_panel_figsize)
        pos_arr = np.zeros((6, nfiles))

    if 'qpd_amp' in monitor_keys:
        qpd_fig, qpd_axarr = plt.subplots(2, 2, sharex=True, sharey=True,
                                          figsize=(10, 6.5))
        qpd_arr = np.zeros((8, nfiles))

    if 'backreflection' in monitor_keys:
        refl_fig, refl_axarr = plt.subplots(2, 1, sharex=True,\
                                            figsize=double_panel_figsize)
        refl_arr = np.zeros((4, nfiles))

    times = np.zeros(nfiles)

    print(f"Processing {nfiles} files...")
    for fil_ind, fil in enumerate(files):
        
        # Display percent completion
        bu.progress_bar(fil_ind, nfiles)

        # Load data
        df = bu.DataFile()
        if new_trap:
            df.load_new(fil)
        else:
            df.load(fil)

        if fil_ind == 0:
            t0 = df.time*1e-9
        times[fil_ind] = df.time*1e-9 - t0

        # if len(other_axes):
        #     df.load_other_data()

        df.calibrate_stage_position()

        if 'power' in monitor_keys:
            power_arr[0, fil_ind] = np.abs(np.mean(df.power))
            power_arr[1, fil_ind] = np.std(df.power)
        if 'power' in parameter and plot_parametrically:
            param_arr[0, fil_ind] = np.abs(np.mean(df.power))
            param_arr[1, fil_ind] = np.std(df.power)

        if 'mean_position' in monitor_keys:
            pos_arr[0, fil_ind] = np.mean(df.pos_data[0])
            pos_arr[3, fil_ind] = np.std(df.pos_data[0])
            pos_arr[1, fil_ind] = np.mean(df.pos_data[1])
            pos_arr[4, fil_ind] = np.std(df.pos_data[1])
            pos_arr[2, fil_ind] = np.mean(df.pos_data[2])
            pos_arr[5, fil_ind] = np.std(df.pos_data[2])
        if 'mean_position' in parameter and plot_parametrically:
            if '_x' in parameter:
                pos_ind = 0
            elif '_y' in parameter:
                pos_ind = 1
            elif '_z' in parameter:
                pos_ind = 2
            param_arr[0, fil_ind] = np.mean(df.pos_data[pos_ind])
            param_arr[1, fil_ind] = np.std(df.pos_data[pos_ind])

        if 'qpd_amp' in monitor_keys:
            qpd_arr[0, fil_ind] = np.mean(df.amp[0])
            qpd_arr[4, fil_ind] = np.std(df.amp[0])
            qpd_arr[1, fil_ind] = np.mean(df.amp[1])
            qpd_arr[5, fil_ind] = np.std(df.amp[1])
            qpd_arr[2, fil_ind] = np.mean(df.amp[2])
            qpd_arr[6, fil_ind] = np.std(df.amp[2])
            qpd_arr[3, fil_ind] = np.mean(df.amp[3])
            qpd_arr[7, fil_ind] = np.std(df.amp[3])
        if 'qpd_amp' in parameter and plot_parametrically:
            qpd_ind = int(parameter.split('_')[-1])
            param_arr[0, fil_ind] = np.mean(df.amp[qpd_ind])
            param_arr[1, fil_ind] = np.std(df.amp[qpd_ind])

        if 'backreflection' in monitor_keys:
            refl_arr[0, fil_ind] = np.mean(df.amp[4])
            refl_arr[2, fil_ind] = np.std(df.amp[4])
            refl_arr[1, fil_ind] = np.mean(df.phase[4])
            refl_arr[3, fil_ind] = np.std(df.phase[4])
        if 'backreflection' in parameter and plot_parametrically:
            if 'amp' in parameter:
                param_arr[0, fil_ind] = np.mean(df.amp[4])
                param_arr[1, fil_ind] = np.std(df.amp[4])
            elif 'phase' in parameter:
                param_arr[0, fil_ind] = np.mean(df.phase[4])
                param_arr[1, fil_ind] = np.std(df.phase[4])

        if 'mean_feedback' in parameter and plot_parametrically:
            if '_x' in parameter:
                fb_ind = 0
            elif '_y' in parameter:
                fb_ind = 1
            elif '_z' in parameter:
                fb_ind = 2
            param_arr[0, fil_ind] = np.mean(df.pos_fb[fb_ind])
            param_arr[1, fil_ind] = np.std(df.pos_fb[fb_ind])

    if plot_parametrically:
        plot_x = param_arr[0]
    else:
        plot_x = times

    if 'power' in monitor_keys:
        power_ax.errorbar(plot_x, power_arr[0], yerr=power_arr[1])
        power_ax.set_ylabel('Power [arb.]')
        if plot_parametrically:
            power_ax.set_xlabel(f'{parameter}')
        else:
            power_ax.set_xlabel('Time [s]')
        power_fig.tight_layout()

    if 'mean_position' in monitor_keys:
        pos_axarr[0].errorbar(plot_x, pos_arr[0], yerr=pos_arr[0+3])
        pos_axarr[1].errorbar(plot_x, pos_arr[1], yerr=pos_arr[1+3])
        pos_axarr[2].errorbar(plot_x, pos_arr[2], yerr=pos_arr[2+3])

        pos_axarr[0].set_ylabel('X-position [arb.]')
        pos_axarr[1].set_ylabel('Y-position [arb.]')
        pos_axarr[2].set_ylabel('Z-position [arb.]')
        if plot_parametrically:
            pos_axarr[2].set_xlabel(f'{parameter}')
        else:
            pos_axarr[2].set_xlabel('Time [s]')

        pos_fig.tight_layout()

    if 'qpd_amp' in monitor_keys:
        qpd_axarr[0,0].errorbar(plot_x, qpd_arr[2], yerr=qpd_arr[2+4])
        qpd_axarr[0,1].errorbar(plot_x, qpd_arr[0], yerr=qpd_arr[0+4])
        qpd_axarr[1,0].errorbar(plot_x, qpd_arr[3], yerr=qpd_arr[3+4])
        qpd_axarr[1,1].errorbar(plot_x, qpd_arr[1], yerr=qpd_arr[1+4])

        qpd_axarr[0,0].set_ylabel('QPD Amp. [arb.]')
        qpd_axarr[1,0].set_ylabel('QPD Amp. [arb.]')
        if plot_parametrically:
            for i in [0,1]:
                qpd_axarr[1,i].set_xlabel(f'{parameter}')
        else:
            for i in [0,1]:
                qpd_axarr[1,i].set_xlabel('Time [s]')

        ylim = qpd_axarr[0,0].get_ylim()
        qpd_axarr[0,0].set_ylim(0, ylim[1])

        qpd_fig.tight_layout()

    if 'backreflection' in monitor_keys:
        refl_axarr[0].errorbar(plot_x, refl_arr[0], yerr=refl_arr[0+2])
        refl_axarr[1].errorbar(plot_x, refl_arr[1], yerr=refl_arr[1+2])

        refl_axarr[0].set_ylabel('Refl. Amp. [arb.]')
        refl_axarr[1].set_ylabel('Refl. Phase [$\\pi$-rad]')
        if plot_parametrically:
            refl_axarr[1].set_xlabel(f'{parameter}')
        else:
            refl_axarr[1].set_xlabel('Time [s]')

        refl_fig.tight_layout()


    plt.show()






long_monitor(allfiles, monitor_keys, \
             parameter=parameter, \
             plot_parametrically=plot_parametrically)