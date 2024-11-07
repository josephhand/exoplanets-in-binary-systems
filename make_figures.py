import pandas as pd
import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib
import colour

from pathlib import Path

Path("figures").mkdir(exist_ok=True)

SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
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
    s=(binary_star_sample["feh1"] * 400 + 12),
    alpha=0.7,
    edgecolor="none",
)

handles, labels = points.legend_elements(prop='sizes', color = points.cmap(0.2), alpha=0.7, num=3, func=lambda x: (x-12)/400)
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

# Transit plot

transit_signals = pd.read_csv("data/intermediates/transits.csv")

transit_plot = plt.figure(figsize=(doc_line_width, 3))
ax = transit_plot.gca()

ax.hist(transit_signals['transit_depth_perfect'], weights=[100/len(transit_signals)]*len(transit_signals), bins=np.logspace(-6, -1, 50), color=mpl.colormaps['Blues'](0.75), alpha=0.5, label='Aligned')
ax.hist(transit_signals['transit_depth_aligned'], weights=[100/len(transit_signals)]*len(transit_signals), bins=np.logspace(-6, -1, 50), color=mpl.colormaps['Reds'](0.75), alpha=0.5, label=r'$20^\circ$ dispersion')
ax.hist(transit_signals['transit_depth_random'], weights=[100/len(transit_signals)]*len(transit_signals), bins=np.logspace(-6, -1, 50), color=mpl.colormaps['Greys'](0.75), alpha=0.5, label='Isotropic')

ax.set_ylabel('Fraction of All Exoplanets (%)')
ax.set_xlabel('Transit Depth')
ax.set_xscale('log')

ax.tick_params(which='both', direction='in', top=True, right=True)

ax.legend()

transit_plot.tight_layout()

transit_plot.savefig("figures/transit_plot.pdf")

# Gamma Inclination Plot

inclination_plot = plt.figure(figsize=(doc_line_width, 3))

ax = inclination_plot.gca()

ax.errorbar(binary_star_sample['gamma'], binary_star_sample['inclination'], xerr=binary_star_sample['gamma_err'], yerr=binary_star_sample['inclination_err'], fmt='.', color='red', ms=2, elinewidth=0.5, alpha=0.2)

ax.set_xlabel(r'Gamma ($^\circ$)')
ax.set_ylabel(r'Inclination ($^\circ$)')

ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(60))
ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(10))

ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(30))
ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(10))

ax.tick_params(which='both', direction='in', top=True, right=True)

inclination_plot.tight_layout()

inclination_plot.savefig('figures/inclination_plot.pdf')

# Radial Velocity Plot

rad_vel_data = pd.read_csv('data/intermediates/radial_velocities.csv')

rad_vel_plot = plt.figure(figsize=(doc_line_width, 3), constrained_layout=True)

gs = mpl.gridspec.GridSpec(1, 2, rad_vel_plot, width_ratios=[1,0.05])

ax = rad_vel_plot.add_subplot(gs[0])

cb = rad_vel_plot.add_subplot(gs[1])

xbins = np.linspace(0, 1.5, 100)
ybins = np.logspace(-2, 2, 100)

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

ax.set_xlim(0, 1.5)
ax.set_ylim(0.01, 100)
ax.set_yscale('log')

ax.set_xlabel(r'Star Mass ($M_\odot$)')
ax.set_ylabel(r'Expected RV (m/s)')

ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(0.5))
ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(0.1))

ax.tick_params(which='both', direction='in', top=True, right=True)

ax.legend()

cb.tick_params(which='both', direction='out', left=False, bottom=False, right=True, labelleft=False, labelright=True, labelbottom=False)

rad_vel_plot.savefig('figures/rv_plot.pdf')
