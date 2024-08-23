from astropy.io import fits

import pandas as pd
import numpy as np
import binary_gamma_errs as bge
import sys
import tqdm

print("Reading input...")

fits_data = fits.open(sys.argv[1])
data = pd.DataFrame.from_records(fits_data[1].data)

print("Calculating gammas...")

gamma_mean = []
gamma_uncertainty = []

for system in tqdm.tqdm(data.iloc, total=len(data)):
    system_gamma, system_gamma_uncertainty = bge.get_gamma(system, 100)
    gamma_mean.append(system_gamma)
    gamma_uncertainty.append(system_gamma_uncertainty)

data["gamma"] = gamma_mean
data["gamma_err"] = gamma_uncertainty

print("Writing file")

data.to_csv(sys.argv[2])
