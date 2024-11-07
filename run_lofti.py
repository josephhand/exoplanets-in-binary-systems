from sys import argv as args
import pandas as pd
import numpy as np

import tqdm
from lofti_gaia import Fitter, FitOrbit

isoclassify_results = pd.read_csv(args[1])

mass = np.array(isoclassify_results["iso_mass"])
mass_upper_uncertainty = isoclassify_results["iso_mass_err1"]
mass_lower_uncertainty = isoclassify_results["iso_mass_err2"]

mass_symmetric_uncertainty = np.max(
    np.abs([mass_upper_uncertainty, mass_lower_uncertainty]), axis=0
)

rad = np.array(isoclassify_results["iso_rad"])
rad_upper_uncertainty = isoclassify_results["iso_rad_err1"]
rad_lower_uncertainty = isoclassify_results["iso_rad_err2"]

rad_symmetric_uncertainty = np.max(
    np.abs([rad_upper_uncertainty, rad_lower_uncertainty]), axis=0
)

teff = np.array(isoclassify_results["iso_teff"])
teff_upper_uncertainty = isoclassify_results["iso_teff_err1"]
teff_lower_uncertainty = isoclassify_results["iso_teff_err2"]

teff_symmetric_uncertainty = np.max(
    np.abs([teff_upper_uncertainty, teff_lower_uncertainty]), axis=0
)

feh = np.array(isoclassify_results["iso_feh"])
feh_upper_uncertainty = isoclassify_results["iso_feh_err1"]
feh_lower_uncertainty = isoclassify_results["iso_feh_err2"]

feh_symmetric_uncertainty = np.max(
    np.abs([feh_upper_uncertainty, feh_lower_uncertainty]), axis=0
)

sample = pd.read_csv(args[2])

sample["mass1"] = mass[: len(sample)]
sample["mass2"] = mass[len(sample) :]

sample["mass_err1"] = mass_symmetric_uncertainty[: len(sample)]
sample["mass_err2"] = mass_symmetric_uncertainty[len(sample) :]

sample["rad1"] = rad[: len(sample)]
sample["rad2"] = rad[len(sample) :]

sample["rad_err1"] = rad_symmetric_uncertainty[: len(sample)]
sample["rad_err2"] = rad_symmetric_uncertainty[len(sample) :]

sample["teff1"] = teff[: len(sample)]
sample["teff2"] = teff[len(sample) :]

sample["teff_err1"] = teff_symmetric_uncertainty[: len(sample)]
sample["teff_err2"] = teff_symmetric_uncertainty[len(sample) :]

sample["feh1"] = feh[: len(sample)]
sample["feh2"] = feh[len(sample) :]

sample["feh_err1"] = feh_symmetric_uncertainty[: len(sample)]
sample["feh_err2"] = feh_symmetric_uncertainty[len(sample) :]

inclination_mean = []
inclination_uncertainty = []

semimajor_axis_mean = []
semimajor_axis_uncertainty = []

for system in tqdm.tqdm(sample.iloc, total=len(sample)):

    primary_star_gaia_id = system["source_id1"]
    secondary_star_gaia_id = system["source_id2"]

    primary_star_mass = (system["mass1"], system["mass_err1"])
    secondary_star_mass = (system["mass2"], system["mass_err2"])

    is_mass_valid = primary_star_mass[0] < 0.01 or secondary_star_mass[0] < 0.01

    if is_mass_valid:
        inclination_mean.append(None)
        inclination_uncertainty.append(None)
        continue

    lofti_fitter = Fitter(
        primary_star_gaia_id,
        secondary_star_gaia_id,
        primary_star_mass,
        secondary_star_mass,
        Norbits=1000,
    )

    lofti_fitter.results_filename = f"{args[3]}/{primary_star_gaia_id}_results"
    lofti_fitter.stats_filename = f"{args[3]}/{primary_star_gaia_id}_stats"

    orbits = FitOrbit(lofti_fitter)

    system_inclination_mean = np.mean(orbits.results.inc)
    system_inclination_uncertainty = np.std(orbits.results.inc)

    inclination_mean.append(system_inclination_mean)
    inclination_uncertainty.append(system_inclination_uncertainty)

    samples_semimajor_axis = orbits.results.sma * orbits.results.distance
    system_semimajor_axis_mean = np.mean(samples_semimajor_axis)
    system_semimajor_axis_uncertainty = np.std(samples_semimajor_axis)

    semimajor_axis_mean.append(system_semimajor_axis_mean)
    semimajor_axis_uncertainty.append(system_semimajor_axis_uncertainty)

sample["inclination"] = inclination_mean
sample["inclination_err"] = inclination_uncertainty

sample["semimajor_axis"] = semimajor_axis_mean
sample["semimajor_axis_err"] = semimajor_axis_uncertainty

well_aligned_systems = (sample["inclination"] - 90) < sample["inclination_err"]


sample = sample[well_aligned_systems].copy()

sample.to_csv(args[4])
