from sys import argv as args

import pickle as pkl
import numpy as np
import pandas as pd

sample = pd.read_csv(args[1])

inclination = []
inclination_err = []
inclination_lower = []
inclination_upper = []

for system in sample.iloc:
    with open(f'{args[2]}/{system["source_id1"]}_results', 'rb') as f:
        results = pkl.load(f)

    inclination.append(np.mean(results.inc))
    inclination_err.append(np.std(results.inc))
    inclination_lower.append(np.percentile(results.inc, 16))
    inclination_upper.append(np.percentile(results.inc, 84))

sample['inclination'] = inclination
sample['inclination_err'] = inclination_err
sample['inclination_lower'] = inclination_lower
sample['inclination_upper'] = inclination_upper

well_aligned_systems = np.abs(sample['inclination'] - 90) < sample['inclination_err']

sample = sample[well_aligned_systems].copy()

sample.to_csv(args[3])
