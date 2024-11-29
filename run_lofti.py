from sys import argv as args
import sys
import pandas as pd
import numpy as np

import tqdm
from lofti_gaia import Fitter, FitOrbit

sample = pd.read_csv(args[1])

inclination_mean = []
inclination_err = []

inclination_lower = []
inclination_upper = []

semimajor_axis_mean = []
semimajor_axis_uncertainty = []

if int(args[3]) >= len(sample):
    sys.exit(0)

# for system in tqdm.tqdm(sample.iloc, total=len(sample)):

system = sample.iloc[int(args[3])]

primary_star_gaia_id = system["source_id1"]
secondary_star_gaia_id = system["source_id2"]

primary_star_mass = (system["mass1"], system["mass_err1"])
secondary_star_mass = (system["mass2"], system["mass_err2"])

# Filter out stars with undetermined mass
is_mass_valid = (primary_star_mass[0] > 0.01) and (secondary_star_mass[0] > 0.01)

if is_mass_valid:

    lofti_fitter = Fitter(
        primary_star_gaia_id,
        secondary_star_gaia_id,
        primary_star_mass,
        secondary_star_mass,
        Norbits=200,
    )

    lofti_fitter.results_filename = f"{args[2]}/{primary_star_gaia_id}_results"
    lofti_fitter.stats_filename = f"{args[2]}/{primary_star_gaia_id}_stats"

    orbits = FitOrbit(lofti_fitter)
