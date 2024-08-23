import pandas as pd
import numpy as np
import binary_gamma_errs as bge
import sys

print("Reading input...")

catalog = pd.read_csv(sys.argv[1])

print("Selecting sample...")

angle_from_aligned = np.min((catalog["gamma"], 180 - catalog["gamma"]), axis=0)

alignment_filter = angle_from_aligned < catalog["gamma_err"]
apparent_magnitude_filter = catalog["phot_g_mean_mag1"] < 15
sky_projected_separation_filter = catalog["sep_AU"] < 800

combined_filter = (
    alignment_filter & apparent_magnitude_filter & sky_projected_separation_filter
)
sample = catalog.loc[combined_filter].copy()

print("Writing output...")

sample.to_csv(sys.argv[2])
