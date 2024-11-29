ddir = data
idir = $(ddir)/intermediates

all: data figures

figures: data make_figures.py
	python make_figures.py

data: $(idir)/random_planets.csv $(idir)/transits.csv $(idir)/radial_velocities.csv

$(idir)/transits.csv: gen_transits.py $(idir)/sample_with_inclination.csv $(idir)/random_planets.csv
	python gen_transits.py $(idir)/sample_with_inclination.csv $(idir)/random_planets.csv $(idir)/transits.csv

$(idir)/radial_velocities.csv: gen_radial_velocity.py $(idir)/sample_with_inclination.csv $(idir)/random_planets.csv
	python gen_radial_velocity.py $(idir)/sample_with_inclination.csv $(idir)/random_planets.csv $(idir)/radial_velocities.csv

$(idir)/random_planets.csv: generate_random_exoplanets.py
	python generate_random_exoplanets.py $(idir)/random_planets.csv

$(idir)/sample_with_inclination.csv: refine_sample.py $(idir)/sample_with_masses.csv $(idir)/lofti.lock
	python refine_sample.py $(idir)/sample_with_masses.csv $(idir)/lofti $(idir)/sample_with_inclination.csv

$(idir)/lofti.lock: run_lofti.sh run_lofti.py $(idir)/sample_with_masses.csv
	./run_lofti.sh $(idir)/sample_with_masses.csv $(idir)/lofti $(idir)/lofti.lock

$(idir)/sample_with_masses.csv: add_isoclassify_output.py $(idir)/sample_with_exoplanets.csv $(idir)/isoclassify_output.csv
	python add_isoclassify_output.py $(idir)/sample_with_exoplanets.csv $(idir)/isoclassify_output.csv $(idir)/sample_with_masses.csv

$(idir)/isoclassify_output.csv: run_isoclassify.sh $(idir)/sample_with_exoplanets.csv
	bash run_isoclassify.sh $(idir)/sample_with_exoplanets.csv $(idir)/isoclassify_input.csv $(idir)/isoclassify_output.csv

$(idir)/sample_with_exoplanets.csv: find_exoplanets.py $(idir)/sample.csv $(idir)/nea_exoplanets.csv $(idir)/nea_tois.csv
	python find_exoplanets.py $(idir)/sample.csv $(idir)/nea_exoplanets.csv $(idir)/nea_tois.csv $(idir)/sample_with_exoplanets.csv

$(idir)/nea_exoplanets.csv: filter_csv.sh data/NEA.csv
	sh filter_csv.sh $(ddir)/NEA.csv $(idir)/nea_exoplanets.csv

$(idir)/nea_tois.csv: filter_csv.sh data/TOIS.csv
	sh filter_csv.sh $(ddir)/TOIS.csv $(idir)/nea_tois.csv

$(idir)/sample.csv: select_sample.py $(idir)/catalog_with_gammas.csv
	python select_sample.py $(idir)/catalog_with_gammas.csv $(idir)/sample.csv

$(idir)/catalog_with_gammas.csv: calculate_gammas.py binary_gamma_errs.py data/all_columns_catalog.fits.gz
	python calculate_gammas.py $(ddir)/all_columns_catalog.fits.gz $(idir)/catalog_with_gammas.csv
