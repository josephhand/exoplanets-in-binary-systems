import numpy as np
import sys
from astropy.io import fits

def calculate_gamma(
    ra,
    ra_companion,
    dec,
    dec_companion,
    proper_motion_ra,
    proper_motion_ra_companion,
    proper_motion_dec,
    proper_motion_dec_companion,
):

    delta_ra = ra - ra_companion
    delta_dec = dec - dec_companion

    delta_proper_motion_ra = proper_motion_ra - proper_motion_ra_companion
    delta_proper_motion_dec = proper_motion_dec - proper_motion_dec_companion

    position_proper_motion_dot_product = (
        delta_ra * delta_proper_motion_ra + delta_dec * delta_proper_motion_dec
    ) / np.sqrt(
        (delta_ra**2 + delta_dec**2)
        * (delta_proper_motion_ra**2 + delta_proper_motion_dec**2)
    )

    return np.arccos(position_proper_motion_dot_product) * 180 / np.pi


def draw_position_and_proper_motion(system, star_suffix):

    ra_mean = system["ra%s" % (star_suffix)]
    dec_mean = system["dec%s" % (star_suffix)]
    proper_motion_ra_mean = system["pmra%s" % (star_suffix)]
    proper_motion_dec_mean = system["pmdec%s" % (star_suffix)]

    mean = np.array([ra_mean, dec_mean, proper_motion_ra_mean, proper_motion_dec_mean])

    ra_error = system["ra_error%s" % (star_suffix)] / (3.6e6)
    dec_error = system["dec_error%s" % (star_suffix)] / (3.6e6)
    proper_motion_ra_error = system["pmra_error%s" % (star_suffix)]
    proper_motion_dec_error = system["pmdec_error%s" % (star_suffix)]

    ra_covariance = ra_error * ra_error
    dec_covariance = dec_error * dec_error
    proper_motion_ra_cov = proper_motion_ra_error * proper_motion_ra_error
    proper_motion_dec_cov = proper_motion_dec_error * proper_motion_dec_error

    ra_draw = np.random.normal()
    dec_draw = np.random.normal()
    proper_motion_ra_draw = np.random.normal()
    proper_motion_dec_draw = np.random.normal()

    Z = np.array([ra_draw, dec_draw, proper_motion_ra_draw, proper_motion_dec_draw])

    ra_dec_correlation = system["ra_dec_corr%s" % (star_suffix)]
    ra_pmra_correlation = system["ra_pmra_corr%s" % (star_suffix)]
    ra_pmdec_correlation = system["ra_pmdec_corr%s" % (star_suffix)]
    dec_pmra_correlation = system["dec_pmra_corr%s" % (star_suffix)]
    dec_pmdec_correlation = system["dec_pmdec_corr%s" % (star_suffix)]
    pmra_pmdec_correlation = system["pmra_pmdec_corr%s" % (star_suffix)]

    ra_dec_covariance = ra_dec_correlation * ra_error * dec_error
    ra_pmra_covariance = ra_pmra_correlation * ra_error * proper_motion_ra_error
    ra_pmdec_covariance = ra_pmdec_correlation * ra_error * proper_motion_dec_error
    dec_pmra_covariance = dec_pmra_correlation * dec_error * proper_motion_ra_error
    dec_pmdec_covariance = dec_pmdec_correlation * dec_error * proper_motion_dec_error
    pmra_pmdec_covariance = (
        pmra_pmdec_correlation * proper_motion_ra_error * proper_motion_dec_error
    )

    # ra, dec, pmra, pmdec
    covariance_matrix = np.array(
        [
            [ra_covariance, ra_dec_covariance, ra_pmra_covariance, ra_pmdec_covariance],
            [
                ra_dec_covariance,
                dec_covariance,
                dec_pmra_covariance,
                dec_pmdec_covariance,
            ],
            [
                ra_pmra_covariance,
                dec_pmra_covariance,
                proper_motion_ra_cov,
                pmra_pmdec_covariance,
            ],
            [
                ra_pmdec_covariance,
                dec_pmdec_covariance,
                pmra_pmdec_covariance,
                proper_motion_dec_cov,
            ],
        ]
    )
    covariance_matrix = np.reshape(covariance_matrix, (4, 4))

    cholesky_matrix = np.linalg.cholesky(covariance_matrix)

    sample = mean + np.dot(cholesky_matrix, Z)

    return sample


def get_gamma(system, draw_count):

    gamma_draws = [0] * draw_count

    for n in range(0, draw_count):

        ra_primary, dec_primary, proper_motion_ra_primary, proper_motion_dec_primary = (
            draw_position_and_proper_motion(system, star_suffix="1")
        )

        (
            ra_companion,
            dec_companion,
            proper_motion_ra_comianion,
            proper_motion_dec_companion,
        ) = draw_position_and_proper_motion(system, star_suffix="2")

        gamma_draws[n] = calculate_gamma(
            ra_primary,
            ra_companion,
            dec_primary,
            dec_companion,
            proper_motion_ra_primary,
            proper_motion_ra_comianion,
            proper_motion_dec_primary,
            proper_motion_dec_companion,
        )

    gamma_mean = np.mean(gamma_draws)
    gamma_uncertainty = np.std(gamma_draws)
    return gamma_mean, gamma_uncertainty
