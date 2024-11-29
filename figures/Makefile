idir=../data/intermediates


figures: cmd_plot.pdf exoplanet_signals_plot.pdf inclination_plot.pdf sample_plot.pdf sky_plot.pdf

cmd_plot.pdf: cmd_plot $(idir)/catalog_with_gammas.csv $(idir)/sample_with_inclination.csv
	./cmd_plot

exoplanet_signals_plot.pdf: exoplanet_signals_plot $(idir)/radial_velocities.csv $(idir)/transits.csv
	./exoplanet_signals_plot

inclination_plot.pdf: inclination_plot $(idir)/sample_with_inclination.csv
	./inclination_plot

sample_plot.pdf: sample_plot $(idir)/sample_with_inclination.csv
	./sample_plot

sky_plot.pdf: sky_plot $(idir)/sample_with_inclination.csv
	./sky_plot
