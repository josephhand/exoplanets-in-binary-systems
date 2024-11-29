import pandas as pd
import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib
import colour

from pathlib import Path

Path("figures").mkdir(exist_ok=True)

SMALL_SIZE = 6
MEDIUM_SIZE = 8
BIGGER_SIZE = 10

plt.rcParams.update({
    'text.usetex': True
})

plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

doc_line_width = 3.35289  # in
doc_text_width = 7.01014

# Sample Separation plot

binary_star_sample = pd.read_csv("data/intermediates/sample_with_inclination.csv")
distance_pc = 1000 / binary_star_sample["parallax1"]
sky_projected_separation_au = binary_star_sample["sep_AU"]
angular_separation_mas = sky_projected_separation_au / distance_pc

separation_plot = plt.figure(figsize=(doc_text_width, 3))
ax = separation_plot.gca()

points = ax.scatter(
    distance_pc,
    sky_projected_separation_au,
    c=angular_separation_mas,
    norm=matplotlib.colors.LogNorm(
        vmin=angular_separation_mas.min(), vmax=angular_separation_mas.max()
    ),
    s=(binary_star_sample["feh1"] * 400 + 25),
    alpha=0.7,
    edgecolor="none",
)

xlims = ax.get_xlim()
ylims = ax.get_ylim()

ax.plot([-100, 1000], [-100, 1000], color='black', alpha=0.2)
ax.text(750, 700, '1"')

ax.plot([-100, 1000], [200, 200], color='black', alpha=0.2)
ax.text(600, 210, '$200$au')

ax.set_xlim(xlims)
ax.set_ylim(ylims)

handles, labels = points.legend_elements(prop='sizes', color = points.cmap(0.2), alpha=0.7, num=4, func=lambda x: (x-25)/400)
legend = ax.legend(handles, labels, loc='lower right', title='Metallicity')

ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(100))
ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(50))

ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(100))
ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(25))

ax.tick_params(which='both', direction='in', top=True, right=True)

ax.set_xlabel("Distance (pc)")
ax.set_ylabel("Sky-Projected Separation (AU)")

colorbar = separation_plot.colorbar(points, ax=ax, ticks=[1, 3, 10])
colorbar.ax.set_yticklabels(['1', '3', '10'])

colorbar.set_label("Angular Separation ('')")

separation_plot.tight_layout()

separation_plot.savefig("figures/separation_plot.pdf")

# Radial Velocity Plot

rad_vel_data = pd.read_csv('data/intermediates/radial_velocities.csv')

exo_signal_plot = plt.figure(figsize=(doc_text_width, 2), constrained_layout=True)

gs = mpl.gridspec.GridSpec(1, 3, exo_signal_plot, width_ratios=[1,0.05,1.05])

ax = exo_signal_plot.add_subplot(gs[0])

cb = exo_signal_plot.add_subplot(gs[1])

xbins = np.linspace(0.5, 2, 100)
ybins = np.logspace(-2, 1, 100)

counts_random, _, _ = np.histogram2d(rad_vel_data['star_mass']/2e30, rad_vel_data['rv_K_random'], bins=[xbins,ybins])

counts_random = scipy.ndimage.gaussian_filter(counts_random, 3)

counts_aligned, _, _ = np.histogram2d(rad_vel_data['star_mass']/2e30, rad_vel_data['rv_K_perfect'], bins=[xbins,ybins])

counts_aligned = scipy.ndimage.gaussian_filter(counts_aligned, 3)

norm = mpl.colors.Normalize(vmin=np.min([counts_random, counts_aligned]), vmax=np.max([counts_random, counts_aligned]))

levels = np.linspace(norm.vmin, norm.vmax, 8)

contours_rand = ax.contour(xbins[1:], ybins[1:], counts_random.transpose(), extent=[xbins.min(), xbins.max(), ybins.min(), ybins.max()], cmap='Reds', norm=norm, alpha=0.5, label='Random inclinations', levels=levels)

contours_aligned = ax.contour(xbins[1:], ybins[1:], counts_aligned.transpose(), extent=[xbins.min(), xbins.max(), ybins.min(), ybins.max()], cmap='Blues', norm=norm, alpha=0.5, label='Aligned with host stars', levels=levels)

perfect_mean, _, _ = scipy.stats.binned_statistic(rad_vel_data['star_mass']/2e30, rad_vel_data['rv_K_perfect'], bins=xbins)

realistic_mean, _, _ = scipy.stats.binned_statistic(rad_vel_data['star_mass']/2e30, rad_vel_data['rv_K_aligned'], bins=xbins)

random_mean, _, _ = scipy.stats.binned_statistic(rad_vel_data['star_mass']/2e30, rad_vel_data['rv_K_random'], bins=xbins)

ax.plot(xbins[1:], perfect_mean, c=mpl.colormaps['Blues'](0.75), label='Aligned')
ax.plot(xbins[1:], realistic_mean, c=mpl.colormaps['Greys'](0.75), label=r'$\pm20^\circ$ Dispersion')
ax.plot(xbins[1:], random_mean, c=mpl.colormaps['Reds'](0.75), label='Isotropic')

idxs = np.linspace(0, 1, 256)
colors = np.array((mpl.colormaps['Blues'](idxs), mpl.colormaps['Reds'](idxs)))
cb.imshow(np.swapaxes(colors, 0, 1), origin='lower', aspect='auto', interpolation='none', extent=[0, 1, norm.vmin, norm.vmax], alpha=0.5)
cb.yaxis.set_label_position('right')
cb.set_ylabel('Model population density')

ax.set_xlim(0.5, 2)
ax.set_ylim(0.01, 10)
ax.set_yscale('log')

ax.set_xlabel(r'Star Mass ($M_\odot$)')
ax.set_ylabel(r'Expected RV (m/s)')

ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(0.5))
ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(0.1))

ax.tick_params(which='both', direction='in', top=True, right=True)

ax.legend(loc='lower left')

cb.tick_params(which='both', direction='out', left=False, bottom=False, right=True, labelleft=False, labelright=True, labelbottom=False)

# Transit plot

transit_signals = pd.read_csv("data/intermediates/transits.csv")

ax = exo_signal_plot.add_subplot(gs[2])

ax.hist(transit_signals['transit_depth_perfect'], weights=[100/len(transit_signals)]*len(transit_signals), bins=np.logspace(-6, -2, 50), color=mpl.colormaps['Blues'](0.75), alpha=0.5, label='Aligned')
ax.hist(transit_signals['transit_depth_aligned'], weights=[100/len(transit_signals)]*len(transit_signals), bins=np.logspace(-6, -2, 50), color=mpl.colormaps['Greys'](0.75), alpha=0.5, label=r'$20^\circ$ dispersion')
ax.hist(transit_signals['transit_depth_random'], weights=[100/len(transit_signals)]*len(transit_signals), bins=np.logspace(-6, -2, 50), color=mpl.colormaps['Reds'](0.75), alpha=0.5, label='Isotropic')

ax.set_ylabel(r'\% Transiting')
ax.set_xlabel('Transit Depth')
ax.set_xscale('log')

ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(0.05))

ax.tick_params(which='both', direction='in', top=True, right=True)

ax.legend()

exo_signal_plot.savefig("figures/exoplanet_signals.pdf", bbox_inches="tight")

# Inclination plot

inc_plot = plt.figure(figsize=(doc_line_width, 8))

ax = inc_plot.gca()

ax.errorbar(binary_star_sample['inclination'], range(len(binary_star_sample)), xerr=binary_star_sample['inclination_err'])

inc_plot.tight_layout()

inc_plot.savefig("figures/inclination_plot.pdf")

# Mollweide Plot

mollweide_plot = plt.figure(figsize=(doc_line_width, 1.7))

ax = mollweide_plot.add_subplot(111, projection='mollweide')

ras = binary_star_sample['ra1']
ras[ras > 180] = ras[ras > 180] - 360

ax.grid(linewidth = 0.25, zorder=-5)

distance_pc = 1000/binary_star_sample["parallax1"]

points = ax.scatter(np.deg2rad(ras), np.deg2rad(binary_star_sample['dec1']), s=4, c=distance_pc, cmap='plasma', edgecolor="none", alpha=0.7)

cb = mollweide_plot.colorbar(points)
cb.set_label("Distance (pc)")

ax.set_ylabel('Declination')
ax.set_xlabel('Right Ascension')

ax.set_xticks(np.deg2rad([-120, -60, 0, 60, 120]))
ax.set_yticks(np.deg2rad([-75, -60, -30, 0, 30, 60, 75]))
ax.set_yticklabels(["", r"-60\textdegree", r"-30\textdegree", r"0\textdegree", r"30\textdegree", r"60\textdegree", ""])

ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(np.deg2rad(10)))
ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(np.deg2rad(20)))

ax.tick_params(labeltop=False)

for label in ax.get_xticklabels():
    label.set_bbox(dict(pad=1, facecolor='white', edgecolor='none', alpha=0.5))

mollweide_plot.tight_layout()

mollweide_plot.savefig("figures/mollweide_plot.pdf")

# CMD plot

catalog = pd.read_csv("data/intermediates/catalog_with_gammas.csv")

gamag = np.concatenate(
    (catalog["phot_g_mean_mag1"], catalog["phot_g_mean_mag2"])
)
bpmag = np.concatenate(
    (catalog["phot_bp_mean_mag1"], catalog["phot_bp_mean_mag2"])
)
rpmag = np.concatenate(
    (catalog["phot_rp_mean_mag1"], catalog["phot_rp_mean_mag2"])
)
parallax = np.concatenate(
    (catalog["parallax1"], catalog["parallax2"])
)

filter = (bpmag < 100) & (rpmag < 100)

bp_rp = bpmag - rpmag
abs_gamag = gamag - 5*np.log10(100/parallax)

cmd_plot = plt.figure(figsize=(doc_line_width, 2.5))

ax = cmd_plot.gca()

data, xbins, ybins = np.histogram2d(bp_rp[filter], abs_gamag[filter], bins=(np.linspace(-1, 5, 500), np.linspace(-5, 18, 500)))

img = ax.imshow(data.T, interpolation='none', norm='log', aspect='auto', extent=(np.min(xbins), np.max(xbins), np.max(ybins), np.min(ybins)))

cb = cmd_plot.colorbar(img)
cb.set_label("System Count")

gamag = np.concatenate(
    (binary_star_sample["phot_g_mean_mag1"], binary_star_sample["phot_g_mean_mag2"])
)
bpmag = np.concatenate(
    (binary_star_sample["phot_bp_mean_mag1"], binary_star_sample["phot_bp_mean_mag2"])
)
rpmag = np.concatenate(
    (binary_star_sample["phot_rp_mean_mag1"], binary_star_sample["phot_rp_mean_mag2"])
)
parallax = np.concatenate(
    (binary_star_sample["parallax1"], binary_star_sample["parallax2"])
)

filter = (bpmag < 100) & (rpmag < 100)

bp_rp = bpmag - rpmag
abs_gamag = gamag - 5*np.log10(100/parallax)

ax.scatter(bp_rp[filter][:1000], abs_gamag[filter][:1000], edgecolors=mpl.colormaps['Oranges'](0.75), linewidths=0.5, s=2, alpha=0.7, c='none', label='Vetted Sample')
ax.legend(loc='upper right')


ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(5))
ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))

ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(2))
ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(0.5))

ax.tick_params(which='both', direction='in', top=True, right=True)

ax.set_xlabel("BP-RP (mag)")
ax.set_ylabel("Abs. G Mag")

cmd_plot.tight_layout()

cmd_plot.savefig('figures/cmd_plot.pdf')
