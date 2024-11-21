all: data figures

data: data/intermediates/random_planets.csv data/intermediates/transits.csv data/intermediates/radial_velocities.csv

figures: make_figures.py data/intermediates/transits.csv data/intermediates/radial_velocities.csv data/intermediates/sample_with_inclination.csv
	python make_figures.py

data/intermediates/transits.csv: gen_transits.py data/intermediates/sample_with_inclination.csv data/intermediates/random_planets.csv
	python gen_transits.py data/intermediates/sample_with_inclination.csv data/intermediates/random_planets.csv data/intermediates/transits.csv

data/intermediates/radial_velocities.csv: gen_radial_velocity.py data/intermediates/sample_with_inclination.csv data/intermediates/random_planets.csv
	python gen_radial_velocity.py data/intermediates/sample_with_inclination.csv data/intermediates/random_planets.csv data/intermediates/radial_velocities.csv

# data/intermediates/generated_signals.csv: calculate_signals.py data/intermediates/sample_with_inclination.csv data/intermediates/random_planets.csv
# 	python calculate_signals.py data/intermediates/sample_with_inclination.csv data/intermediates/random_planets.csv data/intermediates/generated_signals.csv

data/intermediates/random_planets.csv: generate_random_exoplanets.py
	python generate_random_exoplanets.py data/intermediates/random_planets.csv

data/intermediates/sample_with_inclination.csv: run_lofti.py data/intermediates/isoclassify_output.csv data/intermediates/sample_with_exoplanets.csv
	python run_lofti.py data/intermediates/isoclassify_output.csv data/intermediates/sample_with_exoplanets.csv data/intermediates/lofti data/intermediates/sample_with_inclination.csv

data/intermediates/isoclassify_output.csv: run_isoclassify.sh data/intermediates/sample_with_exoplanets.csv
	bash run_isoclassify.sh data/intermediates/sample_with_exoplanets.csv data/intermediates/isoclassify_input.csv data/intermediates/isoclassify_output.csv

data/intermediates/sample_with_exoplanets.csv: find_exoplanets.py data/intermediates/sample.csv data/intermediates/nea_exoplanets.csv data/intermediates/nea_tois.csv
	python find_exoplanets.py data/intermediates/sample.csv data/intermediates/nea_exoplanets.csv data/intermediates/nea_tois.csv data/intermediates/sample_with_exoplanets.csv

data/intermediates/nea_exoplanets.csv: filter_csv.sh data/NEA.csv
	sh filter_csv.sh data/NEA.csv data/intermediates/nea_exoplanets.csv

data/intermediates/nea_tois.csv: filter_csv.sh data/TOIS.csv
	sh filter_csv.sh data/TOIS.csv data/intermediates/nea_tois.csv

data/intermediates/sample.csv: select_sample.py data/intermediates/catalog_with_gammas.csv
	python select_sample.py data/intermediates/catalog_with_gammas.csv data/intermediates/sample.csv

data/intermediates/catalog_with_gammas.csv: calculate_gammas.py binary_gamma_errs.py data/all_columns_catalog.fits.gz
	python calculate_gammas.py data/all_columns_catalog.fits.gz data/intermediates/catalog_with_gammas.csv
