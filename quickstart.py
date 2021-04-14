#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import micsann
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # input parameters condition
    period = 1                                                  # year
    t = np.logspace(np.log10(60), np.log10(3600*8760*period))   # s (from 1 min to 1 year in log space)
    alpha = 6.0e-7                                              # m^2 s^-1
    r_c = 0.06                                                  # m
    r = 0.1                                                     # m
    U = 50/(8760*3600)                                          # m s^-1
    Fo_rc = alpha*t/(r_c**2)
    Pe_rc = U*r_c/alpha
    phi = np.pi
    R = r/r_c
    # make input dataframe
    df = pd.DataFrame({
        'Fo_rc': Fo_rc,
        'Pe_rc': np.full_like(Fo_rc, Pe_rc),
        'phi': np.full_like(Fo_rc, phi),
        'R': np.full_like(Fo_rc, R)
        })
    # calc dimensionless temperature of MICS-ANN model
    Theta = micsann.calc(df)
    # plot
    plot_Theta_Fo(Fo_rc, Pe_rc, phi, R, Theta)

# visualize
def plot_Theta_Fo(Fo_rc, Pe_rc, phi, R, Theta):
    plt.rcParams['font.size'] = 12
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'Times New Roman'
    plt.rcParams["mathtext.fontset"] = "stix"

    fig = plt.figure(figsize=(5,4), tight_layout=True)
    ax = fig.add_subplot(1, 1, 1)
    linewidth = 0.5

    sct = ax.scatter(
        Fo_rc, Theta,
        facecolor='white',
        edgecolor='black',
        s=20,
        linewidth=linewidth
    )

    ax.set_xlabel(r'$Fo_{r_\mathrm{c}}$')
    ax.set_ylabel(r'$\Theta_{MICS-ANN}$')
    ax.set_title(
            r'$Pe_{r_\mathrm{c}} = %.2e$, $\varphi = %.2f$, $R = %.2f$' % (Pe_rc, phi, R),
            fontsize=10
            )
    ax.set_ylim([-0.2, 5.2])
    ax.set_xscale('log')

    plt.show()

if __name__ == '__main__':
    main()

