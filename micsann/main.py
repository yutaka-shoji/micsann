# -*- coding: utf-8 -*-

#import os
import pkg_resources
import numpy as np
import torch
import warnings
import time

# define ANN architecture
class Net(torch.nn.Module):
    def __init__(self, NUM_LAYER, NUM_UNIT):
        super(Net, self).__init__()
        self.input_layer = torch.nn.Sequential(
            torch.nn.Linear(4, NUM_UNIT),
            torch.nn.ReLU(inplace=True)
        )
        middle = []
        for _ in range(NUM_LAYER):
            middle.append(torch.nn.Linear(NUM_UNIT, NUM_UNIT))
            middle.append(torch.nn.ReLU(inplace=True))
        self.middle_layers = torch.nn.Sequential(*middle)
        self.output_layer = torch.nn.Linear(NUM_UNIT, 1)

    def forward(self, x):
        x = self.input_layer(x)
        x = self.middle_layers(x)
        x = self.output_layer(x)
        return x

# calc dimensionless temperature Theta
def calc(df, quiet=False):
    if not quiet:
        print ("Calculating temperature response function of MICS...")
        start = time.time()

    #model_path = os.path.join(os.path.dirname(__file__), 'model/micsann_state.pth')
    model_path = pkg_resources.resource_stream('micsann', 'micsann_state.pth')
    model = Net(NUM_LAYER=5, NUM_UNIT=298)
    model = torch.nn.DataParallel(model)
    model.load_state_dict(torch.load(model_path))
    model.to('cpu')
    model.eval()

    with torch.no_grad():
        data = normalize(df)
        data = data.to('cpu')
        predicted_tensor = model(data)
        Theta_MICS_ANN = predicted_tensor.to('cpu').detach().numpy().ravel().copy()

    if not quiet:
        eltime = time.time() - start
        print ("Elapsed time: {:.2f}s\nFinished!".format(eltime))

    return Theta_MICS_ANN

# input normalization
def normalize(df):
    Fo_rc_min = 5e-4
    Fo_rc_max = 1e+4
    Pe_rc_min = 1e-3
    Pe_rc_max = 1e-3*1.1**(100-1)
    phi_min = 0
    phi_max = np.pi
    R_min = 0.999871
    R_max = 6.0

    # throw warning when input is out of validation range
    if np.min(df['Fo_rc']) < Fo_rc_min or Fo_rc_max < np.max(df['Fo_rc']):
        warnings.warn(
                'Fo_rc is out of validation range ({0:.2e} < Fo_rc < {1:.2e}).'
                .format(Fo_rc_min, Fo_rc_max),
                stacklevel=3
                )
    if np.min(df['Pe_rc']) < Pe_rc_min or Pe_rc_max < np.max(df['Pe_rc']):
        warnings.warn(
                'Pe_rc is out of validation range ({0:.2e} < Pe_rc < {1:.2e}).'
                .format(Pe_rc_min, Pe_rc_max),
                stacklevel=3
                )
    if np.min(df['phi']) < phi_min or phi_max < np.max(df['phi']):
        warnings.warn(
                'phi is out of validation range ({0:.2f} < phi < {1:.2f}).'
                .format(phi_min,phi_max),
                stacklevel=3
                )
    if np.min(df['R']) < R_min or R_max < np.max(df['R']):
        warnings.warn(
                'R is out of validation range ({0:.2f} < R < {1:.2f}).'
                .format(R_min,R_max),
                stacklevel=3
                )

    df_norm = df.rename(columns={'Fo_rc': 'log_Fo_rc', 'Pe_rc': 'log_Pe_rc'})
    df_norm['log_Fo_rc'] = (np.log(df['Fo_rc']) - np.log(Fo_rc_min))/(np.log(Fo_rc_max) - np.log(Fo_rc_min))
    df_norm['log_Pe_rc'] = (np.log(df['Pe_rc']) - np.log(Pe_rc_min))/(np.log(Pe_rc_max) - np.log(Pe_rc_min))
    df_norm['phi'] = (df['phi'] - phi_min)/(phi_max - phi_min)
    df_norm['R'] = (df['R'] - R_min)/(R_max - R_min)

    data = torch.tensor(df_norm[['log_Fo_rc','log_Pe_rc','phi','R']].values).float()

    return data

