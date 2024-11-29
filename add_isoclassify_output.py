from sys import argv as args
import pandas as pd
import numpy as np

sample = pd.read_csv(args[1])
isoclassify_results = pd.read_csv(args[2])

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

sample.to_csv(args[3])
