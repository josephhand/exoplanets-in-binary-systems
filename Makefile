ddir = data
idir = $(ddir)/intermediates

all: $(idir)/random_planets.csv $(idir)/transits.csv $(idir)/radial_velocities.csv
	make -C figures

$(idir)/transits.csv: gen_transits $(idir)/sample_with_inclination.csv $(idir)/random_planets.csv
	./gen_transits $(idir)/sample_with_inclination.csv $(idir)/random_planets.csv $(idir)/transits.csv

$(idir)/radial_velocities.csv: gen_radial_velocity $(idir)/sample_with_inclination.csv $(idir)/random_planets.csv
	./gen_radial_velocity $(idir)/sample_with_inclination.csv $(idir)/random_planets.csv $(idir)/radial_velocities.csv

$(idir)/random_planets.csv: generate_random_exoplanets
	./generate_random_exoplanets $(idir)/random_planets.csv

$(idir)/sample_with_inclination.csv: refine_sample $(idir)/sample_with_masses.csv $(idir)/lofti.lock
	./refine_sample $(idir)/sample_with_masses.csv $(idir)/lofti $(idir)/sample_with_inclination.csv

$(idir)/lofti.lock: run_lofti run_lofti $(idir)/sample_with_masses.csv
	./run_lofti $(idir)/sample_with_masses.csv $(idir)/lofti $(idir)/lofti.lock

$(idir)/sample_with_masses.csv: add_isoclassify_output $(idir)/sample_with_exoplanets.csv $(idir)/isoclassify_output.csv
	./add_isoclassify_output $(idir)/sample_with_exoplanets.csv $(idir)/isoclassify_output.csv $(idir)/sample_with_masses.csv

$(idir)/isoclassify_output.csv: run_isoclassify $(idir)/sample_with_exoplanets.csv
	./run_isoclassify $(idir)/sample_with_exoplanets.csv $(idir)/isoclassify_input.csv $(idir)/isoclassify_output.csv

$(idir)/sample_with_exoplanets.csv: find_exoplanets $(idir)/sample.csv $(idir)/nea_exoplanets.csv $(idir)/nea_tois.csv
	./find_exoplanets $(idir)/sample.csv $(idir)/nea_exoplanets.csv $(idir)/nea_tois.csv $(idir)/sample_with_exoplanets.csv

$(idir)/nea_exoplanets.csv: filter_csv data/NEA.csv
	./filter_csv $(ddir)/NEA.csv $(idir)/nea_exoplanets.csv

$(idir)/nea_tois.csv: filter_csv data/TOIS.csv
	./filter_csv $(ddir)/TOIS.csv $(idir)/nea_tois.csv

$(idir)/sample.csv: select_sample $(idir)/catalog_with_gammas.csv
	./select_sample $(idir)/catalog_with_gammas.csv $(idir)/sample.csv

$(idir)/catalog_with_gammas.csv: calculate_gammas binary_gamma_errs data/all_columns_catalog.fits.gz
	./calculate_gammas $(ddir)/all_columns_catalog.fits.gz $(idir)/catalog_with_gammas.csv
